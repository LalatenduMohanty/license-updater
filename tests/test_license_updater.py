import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
import sys
import io
from license_updater.core import (
    get_package_license,
    is_newer_package,
    update_licenses_from_dnf
)


class MockPackage:
    """Mock DNF package object for testing"""
    def __init__(self, name, epoch=0, version="1.0.0", release="1.fc40", 
                 license_str="MIT", arch="x86_64"):
        self.name = name
        self.epoch = epoch
        self.version = version
        self.release = release
        self.license = license_str
        self.arch = arch
        self.evr = f"{epoch}:{version}-{release}" if epoch > 0 else f"{version}-{release}"
    
    def __str__(self):
        return f"{self.name}-{self.evr}.{self.arch}"


class TestGetPackageLicense(unittest.TestCase):
    """Test cases for get_package_license function"""

    @patch('license_updater.core.dnf.Base')
    def test_successful_single_package(self, mock_dnf_base):
        """Test successful retrieval of license for a single package"""
        # Setup mock DNF base and query
        mock_base = MagicMock()
        mock_dnf_base.return_value = mock_base
        
        mock_sack = MagicMock()
        mock_base.sack = mock_sack
        
        mock_query = MagicMock()
        mock_sack.query.return_value = mock_query
        
        mock_available_query = MagicMock()
        mock_query.available.return_value = mock_available_query
        
        mock_filtered_query = MagicMock()
        mock_available_query.filter.return_value = mock_filtered_query
        
        # Create mock package
        mock_package = MockPackage("test-package", license_str="MIT")
        mock_filtered_query.__iter__ = lambda x: iter([mock_package])
        
        result = get_package_license("test-package")
        
        self.assertEqual(result, "MIT")
        mock_base.read_all_repos.assert_called_once()
        mock_base.fill_sack.assert_called_once()
        mock_available_query.filter.assert_called_once_with(name="test-package")

    @patch('license_updater.core.dnf.Base')
    def test_package_with_architecture_suffix(self, mock_dnf_base):
        """Test that architecture suffixes are stripped correctly"""
        mock_base = MagicMock()
        mock_dnf_base.return_value = mock_base
        
        mock_sack = MagicMock()
        mock_base.sack = mock_sack
        
        mock_query = MagicMock()
        mock_sack.query.return_value = mock_query
        
        mock_available_query = MagicMock()
        mock_query.available.return_value = mock_available_query
        
        mock_filtered_query = MagicMock()
        mock_available_query.filter.return_value = mock_filtered_query
        
        # Create mock package
        mock_package = MockPackage("boost-atomic", license_str="BSL-1.0 AND MIT")
        mock_filtered_query.__iter__ = lambda x: iter([mock_package])
        
        # Test with .x86_64 suffix
        result = get_package_license("boost-atomic.x86_64")
        
        self.assertEqual(result, "BSL-1.0 AND MIT")
        # Should query for "boost-atomic" without the architecture suffix
        mock_available_query.filter.assert_called_with(name="boost-atomic")

    @patch('license_updater.core.dnf.Base')
    def test_multiple_packages_latest_version(self, mock_dnf_base):
        """Test retrieval when multiple versions exist"""
        mock_base = MagicMock()
        mock_dnf_base.return_value = mock_base
        
        mock_sack = MagicMock()
        mock_base.sack = mock_sack
        
        mock_query = MagicMock()
        mock_sack.query.return_value = mock_query
        
        mock_available_query = MagicMock()
        mock_query.available.return_value = mock_available_query
        
        mock_filtered_query = MagicMock()
        mock_available_query.filter.return_value = mock_filtered_query
        
        # Create mock packages with different versions
        pkg1 = MockPackage("test-package", version="1.0.0", release="1.fc40", license_str="MIT")
        pkg2 = MockPackage("test-package", version="1.0.0", release="3.fc40", license_str="MIT AND Apache-2.0")
        
        mock_filtered_query.__iter__ = lambda x: iter([pkg1, pkg2])
        
        # Mock the latest() method to return the newer package
        mock_latest_query = MagicMock()
        mock_filtered_query.latest.return_value = mock_latest_query
        mock_latest_query.__iter__ = lambda x: iter([pkg2])
        
        result = get_package_license("test-package")
        
        self.assertEqual(result, "MIT AND Apache-2.0")

    @patch('license_updater.core.dnf.Base')
    def test_no_packages_found(self, mock_dnf_base):
        """Test when no packages are found"""
        mock_base = MagicMock()
        mock_dnf_base.return_value = mock_base
        
        mock_sack = MagicMock()
        mock_base.sack = mock_sack
        
        mock_query = MagicMock()
        mock_sack.query.return_value = mock_query
        
        mock_available_query = MagicMock()
        mock_query.available.return_value = mock_available_query
        
        mock_filtered_query = MagicMock()
        mock_available_query.filter.return_value = mock_filtered_query
        
        # No packages found
        mock_filtered_query.__iter__ = lambda x: iter([])
        
        result = get_package_license("nonexistent-package")
        
        self.assertEqual(result, "N/A")

    @patch('license_updater.core.dnf.Base')
    def test_package_without_license(self, mock_dnf_base):
        """Test when package exists but has no license"""
        mock_base = MagicMock()
        mock_dnf_base.return_value = mock_base
        
        mock_sack = MagicMock()
        mock_base.sack = mock_sack
        
        mock_query = MagicMock()
        mock_sack.query.return_value = mock_query
        
        mock_available_query = MagicMock()
        mock_query.available.return_value = mock_available_query
        
        mock_filtered_query = MagicMock()
        mock_available_query.filter.return_value = mock_filtered_query
        
        # Package with no license
        mock_package = MockPackage("test-package", license_str=None)
        mock_filtered_query.__iter__ = lambda x: iter([mock_package])
        
        result = get_package_license("test-package")
        
        self.assertEqual(result, "N/A")

    @patch('license_updater.core.dnf.Base')
    def test_dnf_initialization_error(self, mock_dnf_base):
        """Test when DNF initialization fails"""
        mock_base = MagicMock()
        mock_dnf_base.return_value = mock_base
        
        # Simulate DNF initialization error
        mock_base.read_all_repos.side_effect = Exception("DNF initialization failed")
        
        with patch('sys.stderr', new=io.StringIO()) as fake_stderr:
            result = get_package_license("test-package")
            
        self.assertEqual(result, "Error: Unexpected")
        self.assertIn("An unexpected error occurred", fake_stderr.getvalue())

    def test_reused_base_object(self):
        """Test using a pre-existing DNF base object"""
        mock_base = MagicMock()
        
        mock_sack = MagicMock()
        mock_base.sack = mock_sack
        
        mock_query = MagicMock()
        mock_sack.query.return_value = mock_query
        
        mock_available_query = MagicMock()
        mock_query.available.return_value = mock_available_query
        
        mock_filtered_query = MagicMock()
        mock_available_query.filter.return_value = mock_filtered_query
        
        mock_package = MockPackage("test-package", license_str="GPL-2.0")
        mock_filtered_query.__iter__ = lambda x: iter([mock_package])
        
        result = get_package_license("test-package", base=mock_base)
        
        self.assertEqual(result, "GPL-2.0")
        # Should not call read_all_repos or fill_sack when base is provided
        mock_base.read_all_repos.assert_not_called()
        mock_base.fill_sack.assert_not_called()


class TestIsNewerPackage(unittest.TestCase):
    """Test cases for is_newer_package function"""

    def test_newer_release_number(self):
        """Test comparison with different release numbers"""
        pkg1 = MockPackage("test", version="1.0.0", release="5.fc40")
        pkg2 = MockPackage("test", version="1.0.0", release="3.fc40")
        
        self.assertTrue(is_newer_package(pkg1, pkg2))
        self.assertFalse(is_newer_package(pkg2, pkg1))

    def test_newer_version(self):
        """Test comparison with different versions"""
        pkg1 = MockPackage("test", version="2.0.0", release="1.fc40")
        pkg2 = MockPackage("test", version="1.0.0", release="1.fc40")
        
        self.assertTrue(is_newer_package(pkg1, pkg2))
        self.assertFalse(is_newer_package(pkg2, pkg1))

    def test_newer_epoch(self):
        """Test comparison with different epochs"""
        pkg1 = MockPackage("test", epoch=2, version="1.0.0", release="1.fc40")
        pkg2 = MockPackage("test", epoch=1, version="1.0.0", release="1.fc40")
        
        self.assertTrue(is_newer_package(pkg1, pkg2))
        self.assertFalse(is_newer_package(pkg2, pkg1))

    def test_same_packages(self):
        """Test comparison with identical packages"""
        pkg1 = MockPackage("test", version="1.0.0", release="1.fc40")
        pkg2 = MockPackage("test", version="1.0.0", release="1.fc40")
        
        self.assertFalse(is_newer_package(pkg1, pkg2))

    def test_complex_evr_comparison(self):
        """Test EVR comparison fallback"""
        pkg1 = MagicMock()
        pkg2 = MagicMock()
        
        # Mock epoch, version, release attributes
        pkg1.epoch = 1
        pkg1.version = "2.0.0"
        pkg1.release = "1.fc40"
        pkg1.evr = "1:2.0.0-1.fc40"
        
        pkg2.epoch = 1
        pkg2.version = "1.0.0"
        pkg2.release = "5.fc40"
        pkg2.evr = "1:1.0.0-5.fc40"
        
        result = is_newer_package(pkg1, pkg2)
        self.assertTrue(result)

    def test_exception_handling(self):
        """Test exception handling in version comparison"""
        pkg1 = MagicMock()
        pkg2 = MagicMock()
        
        # Make all attribute access raise exceptions
        pkg1.epoch = property(lambda self: exec('raise Exception()'))
        pkg1.evr = "2.0.0"
        pkg2.evr = "1.0.0"
        
        # Should fall back to string comparison
        result = is_newer_package(pkg1, pkg2)
        self.assertIsInstance(result, bool)


class TestUpdateLicensesFromDnf(unittest.TestCase):
    """Test cases for update_licenses_from_dnf function"""

    def setUp(self):
        """Set up test data"""
        self.expected_df = pd.DataFrame({
            'UBI?': ['no', 'yes', 'no'],
            'package': ['boost-atomic.x86_64', 'ubi-package', 'test-package'],
            'License': ['', '', 'Old License']
        })

    @patch('license_updater.core.get_package_license')
    @patch('license_updater.core.dnf.Base')
    @patch('pandas.read_csv')
    def test_successful_processing(self, mock_read_csv, mock_dnf_base, mock_get_license):
        """Test successful CSV processing"""
        mock_read_csv.return_value = self.expected_df.copy()
        mock_get_license.side_effect = ["MIT", "Apache-2.0"]
        
        # Mock DNF base initialization
        mock_base = MagicMock()
        mock_dnf_base.return_value = mock_base
        
        with patch('sys.stdout', new=io.StringIO()) as fake_stdout:
            update_licenses_from_dnf("test.csv")
            
        # Verify get_package_license was called for 'no' packages only
        expected_calls = [
            unittest.mock.call('boost-atomic.x86_64', mock_base),
            unittest.mock.call('test-package', mock_base)
        ]
        mock_get_license.assert_has_calls(expected_calls)
        
        output = fake_stdout.getvalue()
        self.assertIn("Processing package: boost-atomic.x86_64", output)
        self.assertIn("Skipping package ubi-package", output)
        self.assertIn("Processing package: test-package", output)
        self.assertIn("DNF initialization complete", output)

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

    @patch('license_updater.core.get_package_license')
    @patch('license_updater.core.dnf.Base')
    @patch('pandas.read_csv')
    def test_dnf_initialization_error(self, mock_read_csv, mock_dnf_base, mock_get_license):
        """Test handling of DNF initialization errors"""
        mock_read_csv.return_value = self.expected_df.copy()
        
        mock_base = MagicMock()
        mock_dnf_base.return_value = mock_base
        mock_base.read_all_repos.side_effect = Exception("DNF init error")
        
        with patch('sys.stderr', new=io.StringIO()) as fake_stderr:
            with patch('sys.stdout', new=io.StringIO()):
                update_licenses_from_dnf("test.csv")
                
        self.assertIn("Error initializing DNF", fake_stderr.getvalue())

    @patch('license_updater.core.get_package_license')
    @patch('license_updater.core.dnf.Base')
    @patch('pandas.read_csv')
    def test_output_to_file(self, mock_read_csv, mock_dnf_base, mock_get_license):
        """Test saving output to file"""
        df = self.expected_df.copy()
        mock_read_csv.return_value = df
        mock_get_license.return_value = "MIT"
        
        mock_base = MagicMock()
        mock_dnf_base.return_value = mock_base
        
        with patch.object(df, 'to_csv') as mock_to_csv:
            with patch('sys.stdout', new=io.StringIO()):
                update_licenses_from_dnf("test.csv", "output.csv")
                
        mock_to_csv.assert_called_once_with("output.csv", index=False)


class TestIntegration(unittest.TestCase):
    """Integration tests"""

    @patch('license_updater.core.dnf.Base')
    @patch('pandas.read_csv')
    def test_end_to_end_processing(self, mock_read_csv, mock_dnf_base):
        """Test end-to-end processing with mocked DNF API"""
        # Setup test data
        test_df = pd.DataFrame({
            'UBI?': ['no', 'yes', 'no'],
            'package': ['package1.x86_64', 'package2', 'package3.noarch'],
            'License': ['', '', '']
        })
        mock_read_csv.return_value = test_df
        
        # Mock DNF base and queries
        mock_base = MagicMock()
        mock_dnf_base.return_value = mock_base
        
        mock_sack = MagicMock()
        mock_base.sack = mock_sack
        
        def create_mock_query_for_package(expected_name):
            mock_query = MagicMock()
            mock_sack.query.return_value = mock_query
            
            mock_available_query = MagicMock()
            mock_query.available.return_value = mock_available_query
            
            mock_filtered_query = MagicMock()
            mock_available_query.filter.return_value = mock_filtered_query
            
            if expected_name == 'package1':
                pkg = MockPackage(expected_name, license_str="MIT")
            elif expected_name == 'package3':
                pkg = MockPackage(expected_name, license_str="GPL-2.0")
            else:
                pkg = None
                
            if pkg:
                mock_filtered_query.__iter__ = lambda x: iter([pkg])
            else:
                mock_filtered_query.__iter__ = lambda x: iter([])
                
            return mock_query
        
        # Configure mock to track calls
        call_count = [0]
        def mock_query_side_effect():
            call_count[0] += 1
            if call_count[0] == 1:
                return create_mock_query_for_package("package1")
            else:
                return create_mock_query_for_package("package3")
        
        mock_sack.query.side_effect = mock_query_side_effect
        
        with patch('sys.stdout', new=io.StringIO()) as fake_stdout:
            update_licenses_from_dnf("test.csv")
            
        output = fake_stdout.getvalue()
        self.assertIn("Processing package: package1.x86_64", output)
        self.assertIn("Skipping package package2", output)
        self.assertIn("Processing package: package3.noarch", output)
        self.assertIn("DNF initialization complete", output)


if __name__ == '__main__':
    # Create a test suite
    unittest.main(verbosity=2) 