import pandas as pd
import subprocess
import argparse
import sys


def get_package_license(package_name):
    """
    Runs 'dnf repoquery --info <package_name>' and extracts the License.

    Args:
        package_name (str): The name of the package.

    Returns:
        str: The extracted license string, or 'N/A' if not found or
             an error occurred.
    """
    try:
        # Construct the command to run
        command = ["dnf", "repoquery", "--info", package_name]

        # Execute the command and capture output
        # Using text=True to decode stdout/stderr as strings
        # Using capture_output=True to get stdout and stderr
        result = subprocess.run(command, capture_output=True, text=True,
                                check=False)

        # Check for errors in the command execution
        if result.returncode != 0:
            error_msg = (f"Warning: Command failed for package "
                         f"'{package_name}'. Error: {result.stderr.strip()}")
            print(error_msg, file=sys.stderr)
            return "Error: Command Failed"

        # Split the output into lines and parse Source/License pairs
        lines = result.stdout.splitlines()

        # Collect all Source/License pairs
        source_license_pairs = []
        current_source = None

        for line in lines:
            line = line.strip()
            if line.startswith("Source") and ":" in line:
                current_source = line.split(":", 1)[1].strip()
            elif (line.startswith("License") and ":" in line and
                  current_source):
                current_license = line.split(":", 1)[1].strip()
                source_license_pairs.append((current_source,
                                             current_license))
                current_source = None  # Reset for next pair

        if not source_license_pairs:
            return "N/A"

        # If only one pair, return it
        if len(source_license_pairs) == 1:
            return source_license_pairs[0][1]

        # Find the latest source by comparing version/release numbers
        latest_source, latest_license = source_license_pairs[0]
        for source, license_info in source_license_pairs[1:]:
            if is_newer_source(source, latest_source):
                latest_source = source
                latest_license = license_info

        return latest_license

    except FileNotFoundError:
        error_msg = ("Error: 'dnf' command not found. Please ensure dnf is "
                     "installed and in your PATH.")
        print(error_msg, file=sys.stderr)
        return "Error: dnf not found"
    except Exception as e:
        error_msg = (f"An unexpected error occurred for package "
                     f"'{package_name}': {e}")
        print(error_msg, file=sys.stderr)
        return "Error: Unexpected"


def is_newer_source(source1, source2):
    """
    Compare two RPM source names to determine if source1 is newer than
    source2.

    Args:
        source1 (str): First source RPM name
                      (e.g., "boost-1.83.0-5.fc40.src.rpm")
        source2 (str): Second source RPM name
                      (e.g., "boost-1.83.0-3.fc40.src.rpm")

    Returns:
        bool: True if source1 is newer than source2
    """
    try:
        # Extract version-release from source RPM names
        # Format: name-version-release.architecture.rpm
        def parse_source_rpm(source):
            # Remove .src.rpm suffix
            if source.endswith('.src.rpm'):
                source = source[:-8]
            elif source.endswith('.rpm'):
                source = source[:-4]

            # Split by dots to separate architecture
            parts = source.split('.')
            if len(parts) > 1:
                # Remove architecture part (like x86_64, noarch, etc.)
                source = '.'.join(parts[:-1])

            # Find the last two hyphens to separate name-version-release
            hyphens = [i for i, char in enumerate(source) if char == '-']
            if len(hyphens) >= 2:
                # Get version-release part
                version_release = source[hyphens[-2]+1:]
                return version_release
            return source

        vr1 = parse_source_rpm(source1)
        vr2 = parse_source_rpm(source2)

        # Try to extract release numbers for comparison
        # Look for pattern like "version-release" where release is typically
        # numeric
        def extract_release_number(version_release):
            parts = version_release.split('-')
            if len(parts) >= 2:
                release_part = parts[-1]
                # Extract numeric part from release (e.g., "5.fc40" -> 5)
                numeric_part = ""
                for char in release_part:
                    if char.isdigit():
                        numeric_part += char
                    else:
                        break
                if numeric_part:
                    return int(numeric_part)
            return 0

        release1 = extract_release_number(vr1)
        release2 = extract_release_number(vr2)

        # Compare release numbers
        return release1 > release2

    except Exception:
        # If parsing fails, fall back to string comparison
        return source1 > source2


def update_licenses_from_dnf(csv_file_path, output_file_path=None):
    """
    Reads a CSV, updates 'License' column based on 'dnf repoquery',
    and optionally saves the updated DataFrame to a new CSV.

    Args:
        csv_file_path (str): Path to the input CSV file.
        output_file_path (str, optional): Path to save the updated CSV.
                                          If None, the updated DataFrame is
                                          printed.
    """
    try:
        df = pd.read_csv(csv_file_path)
    except FileNotFoundError:
        print(f"Error: The file '{csv_file_path}' was not found.",
              file=sys.stderr)
        return
    except Exception as e:
        print(f"Error reading CSV file '{csv_file_path}': {e}",
              file=sys.stderr)
        return

    # Iterate through the DataFrame rows
    # Using .loc for safe assignment based on index
    for index, row in df.iterrows():
        if row['UBI?'].lower() == 'no':
            package_name = row['package']
            print(f"Processing package: {package_name}...")
            new_license = get_package_license(package_name)
            df.loc[index, 'License'] = new_license
            print(f"  Updated license for {package_name}: {new_license}")
        else:
            print(f"Skipping package {row['package']} "
                  "(UBI? is not 'no').")

    if output_file_path:
        try:
            df.to_csv(output_file_path, index=False)
            print(f"\nUpdated data saved to '{output_file_path}'")
        except Exception as e:
            print(f"Error saving updated CSV to '{output_file_path}': {e}",
                  file=sys.stderr)
    else:
        print("\n--- Updated DataFrame (first 20 rows) ---")
        print(df.head(20).to_markdown(index=False, numalign="left",
                                      stralign="left"))
        print("\n--- Updated DataFrame (last 20 rows) ---")
        print(df.tail(20).to_markdown(index=False, numalign="left",
                                      stralign="left"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=("Update 'License' column in a CSV based on "
                     "'dnf repoquery' output.")
    )
    parser.add_argument(
        "input_csv",
        type=str,
        help=("Path to the input CSV file (e.g., 'AIPCC base containers "
              "(2025-06-17) - CUDA 12.8 _ RHEL 9.4.csv')")
    )
    parser.add_argument(
        "-o", "--output_csv",
        type=str,
        help=("Optional: Path to save the updated CSV file. If not "
              "provided, the updated data will be printed to console.")
    )

    args = parser.parse_args()

    # Call the main function with provided arguments
    update_licenses_from_dnf(args.input_csv, args.output_csv)
