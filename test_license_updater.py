import unittest
from unittest.mock import patch, mock_open, MagicMock
import pandas as pd
import subprocess
import sys
import io
from license_updater import (
    get_package_license,
    is_newer_source,
    update_licenses_from_dnf
)


class TestGetPackageLicense(unittest.TestCase):
    """Test cases for get_package_license function"""

    @patch('license_updater.subprocess.run')
    def test_successful_single_package(self, mock_run):
        """Test successful retrieval of license for a single package"""
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = """Name         : test-package
Version      : 1.0.0
Release      : 1.fc40
Architecture : x86_64
Source       : test-package-1.0.0-1.fc40.src.rpm
License      : MIT
Summary      : A test package"""
        mock_result.stderr = ""
        mock_run.return_value = mock_result

        result = get_package_license("test-package")
        
        self.assertEqual(result, "MIT")
        mock_run.assert_called_once_with(
            ["dnf", "repoquery", "--info", "test-package"],
            capture_output=True, text=True, check=False
        )

    @patch('license_updater.subprocess.run')
    def test_multiple_packages_latest_version(self, mock_run):
        """Test retrieval when multiple versions exist"""
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = """Name         : test-package
Version      : 1.0.0
Release      : 1.fc40
Architecture : x86_64
Source       : test-package-1.0.0-1.fc40.src.rpm
License      : MIT

Name         : test-package
Version      : 1.0.0
Release      : 3.fc40
Architecture : x86_64
Source       : test-package-1.0.0-3.fc40.src.rpm
License      : MIT AND Apache-2.0"""
        mock_result.stderr = ""
        mock_run.return_value = mock_result

        result = get_package_license("test-package")
        
        self.assertEqual(result, "MIT AND Apache-2.0")

    @patch('license_updater.subprocess.run')
    def test_no_license_found(self, mock_run):
        """Test when no license information is found"""
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = """Name         : test-package
Version      : 1.0.0
Release      : 1.fc40
Architecture : x86_64
Summary      : A test package"""
        mock_result.stderr = ""
        mock_run.return_value = mock_result

        result = get_package_license("test-package")
        
        self.assertEqual(result, "N/A")

    @patch('license_updater.subprocess.run')
    def test_command_failure(self, mock_run):
        """Test when dnf command fails"""
        mock_result = MagicMock()
        mock_result.returncode = 1
        mock_result.stdout = ""
        mock_result.stderr = "No matching packages"
        mock_run.return_value = mock_result

        with patch('sys.stderr', new=io.StringIO()) as fake_stderr:
            result = get_package_license("nonexistent-package")
            
        self.assertEqual(result, "Error: Command Failed")
        self.assertIn("Warning: Command failed", fake_stderr.getvalue())

    @patch('license_updater.subprocess.run')
    def test_dnf_not_found(self, mock_run):
        """Test when dnf command is not found"""
        mock_run.side_effect = FileNotFoundError()

        with patch('sys.stderr', new=io.StringIO()) as fake_stderr:
            result = get_package_license("test-package")
            
        self.assertEqual(result, "Error: dnf not found")
        self.assertIn("dnf' command not found", fake_stderr.getvalue())

    @patch('license_updater.subprocess.run')
    def test_unexpected_exception(self, mock_run):
        """Test handling of unexpected exceptions"""
        mock_run.side_effect = Exception("Unexpected error")

        with patch('sys.stderr', new=io.StringIO()) as fake_stderr:
            result = get_package_license("test-package")
            
        self.assertEqual(result, "Error: Unexpected")
        self.assertIn("An unexpected error occurred", fake_stderr.getvalue())


class TestIsNewerSource(unittest.TestCase):
    """Test cases for is_newer_source function"""

    def test_newer_release_number(self):
        """Test comparison with different release numbers"""
        source1 = "boost-1.83.0-5.fc40.src.rpm"
        source2 = "boost-1.83.0-3.fc40.src.rpm"
        
        self.assertTrue(is_newer_source(source1, source2))
        self.assertFalse(is_newer_source(source2, source1))

    def test_same_release_number(self):
        """Test comparison with same release numbers"""
        source1 = "boost-1.83.0-3.fc40.src.rpm"
        source2 = "boost-1.83.0-3.fc40.src.rpm"
        
        self.assertFalse(is_newer_source(source1, source2))

    def test_different_architectures(self):
        """Test comparison with different architectures"""
        source1 = "package-1.0-5.fc40.x86_64.rpm"
        source2 = "package-1.0-3.fc40.noarch.rpm"
        
        self.assertTrue(is_newer_source(source1, source2))

    def test_no_rpm_suffix(self):
        """Test comparison without .rpm suffix"""
        source1 = "package-1.0-5.fc40"
        source2 = "package-1.0-3.fc40"
        
        self.assertTrue(is_newer_source(source1, source2))

    def test_malformed_source_names(self):
        """Test comparison with malformed source names"""
        source1 = "invalid-source-name"
        source2 = "another-invalid"
        
        # Should fall back to string comparison
        result = is_newer_source(source1, source2)
        self.assertIsInstance(result, bool)

    def test_complex_version_strings(self):
        """Test with complex version strings"""
        source1 = "package-2.1.5-10.el9.src.rpm"
        source2 = "package-2.1.5-8.el9.src.rpm"
        
        self.assertTrue(is_newer_source(source1, source2))


class TestUpdateLicensesFromDnf(unittest.TestCase):
    """Test cases for update_licenses_from_dnf function"""

    def setUp(self):
        """Set up test data"""
        self.test_csv_data = """UBI?,package,License
no,boost-atomic.x86_64,
yes,ubi-package,
no,test-package,Old License"""
        
        self.expected_df = pd.DataFrame({
            'UBI?': ['no', 'yes', 'no'],
            'package': ['boost-atomic.x86_64', 'ubi-package', 'test-package'],
            'License': ['', '', 'Old License']
        })

    @patch('license_updater.get_package_license')
    @patch('pandas.read_csv')
    def test_successful_processing(self, mock_read_csv, mock_get_license):
        """Test successful CSV processing"""
        mock_read_csv.return_value = self.expected_df.copy()
        mock_get_license.side_effect = ["MIT", "Apache-2.0"]
        
        with patch('sys.stdout', new=io.StringIO()) as fake_stdout:
            update_licenses_from_dnf("test.csv")
            
        # Verify get_package_license was called for 'no' packages only
        expected_calls = [
            unittest.mock.call('boost-atomic.x86_64'),
            unittest.mock.call('test-package')
        ]
        mock_get_license.assert_has_calls(expected_calls)
        
        output = fake_stdout.getvalue()
        self.assertIn("Processing package: boost-atomic.x86_64", output)
        self.assertIn("Skipping package ubi-package", output)
        self.assertIn("Processing package: test-package", output)

    @patch('pandas.read_csv')
    def test_file_not_found(self, mock_read_csv):
        """Test handling when CSV file is not found"""
        mock_read_csv.side_effect = FileNotFoundError()
        
        with patch('sys.stderr', new=io.StringIO()) as fake_stderr:
            update_licenses_from_dnf("nonexistent.csv")
            
        self.assertIn("was not found", fake_stderr.getvalue())

    @patch('pandas.read_csv')
    def test_csv_read_error(self, mock_read_csv):
        """Test handling of CSV read errors"""
        mock_read_csv.side_effect = Exception("CSV parse error")
        
        with patch('sys.stderr', new=io.StringIO()) as fake_stderr:
            update_licenses_from_dnf("test.csv")
            
        self.assertIn("Error reading CSV file", fake_stderr.getvalue())

    @patch('license_updater.get_package_license')
    @patch('pandas.read_csv')
    def test_output_to_file(self, mock_read_csv, mock_get_license):
        """Test saving output to file"""
        df = self.expected_df.copy()
        mock_read_csv.return_value = df
        mock_get_license.return_value = "MIT"
        
        with patch.object(df, 'to_csv') as mock_to_csv:
            with patch('sys.stdout', new=io.StringIO()):
                update_licenses_from_dnf("test.csv", "output.csv")
                
        mock_to_csv.assert_called_once_with("output.csv", index=False)

    @patch('license_updater.get_package_license')
    @patch('pandas.read_csv')
    def test_output_file_save_error(self, mock_read_csv, mock_get_license):
        """Test handling of file save errors"""
        df = self.expected_df.copy()
        mock_read_csv.return_value = df
        mock_get_license.return_value = "MIT"
        
        with patch.object(df, 'to_csv', side_effect=Exception("Save error")):
            with patch('sys.stderr', new=io.StringIO()) as fake_stderr:
                with patch('sys.stdout', new=io.StringIO()):
                    update_licenses_from_dnf("test.csv", "output.csv")
                    
        self.assertIn("Error saving updated CSV", fake_stderr.getvalue())

    @patch('license_updater.get_package_license')
    @patch('pandas.read_csv')
    def test_console_output(self, mock_read_csv, mock_get_license):
        """Test console output format"""
        df = self.expected_df.copy()
        mock_read_csv.return_value = df
        mock_get_license.return_value = "MIT"
        
        with patch('sys.stdout', new=io.StringIO()) as fake_stdout:
            update_licenses_from_dnf("test.csv")
            
        output = fake_stdout.getvalue()
        self.assertIn("Updated DataFrame (first 20 rows)", output)
        self.assertIn("Updated DataFrame (last 20 rows)", output)


class TestIntegration(unittest.TestCase):
    """Integration tests"""

    @patch('license_updater.subprocess.run')
    @patch('pandas.read_csv')
    def test_end_to_end_processing(self, mock_read_csv, mock_subprocess):
        """Test end-to-end processing with mocked dependencies"""
        # Setup test data
        test_df = pd.DataFrame({
            'UBI?': ['no', 'yes', 'no'],
            'package': ['package1', 'package2', 'package3'],
            'License': ['', '', '']
        })
        mock_read_csv.return_value = test_df
        
        # Mock subprocess responses
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stderr = ""
        
        def mock_stdout_response(command, **kwargs):
            package_name = command[3]  # Extract package name from command
            if package_name == 'package1':
                mock_result.stdout = "Source: pkg-1.0-1.fc40.src.rpm\nLicense: MIT"
            elif package_name == 'package3':
                mock_result.stdout = "Source: pkg-1.0-2.fc40.src.rpm\nLicense: GPL-2.0"
            return mock_result
            
        mock_subprocess.side_effect = mock_stdout_response
        
        with patch('sys.stdout', new=io.StringIO()) as fake_stdout:
            update_licenses_from_dnf("test.csv")
            
        output = fake_stdout.getvalue()
        self.assertIn("Processing package: package1", output)
        self.assertIn("Updated license for package1: MIT", output)
        self.assertIn("Skipping package package2", output)
        self.assertIn("Processing package: package3", output)
        self.assertIn("Updated license for package3: GPL-2.0", output)


if __name__ == '__main__':
    # Create a test suite
    unittest.main(verbosity=2) 