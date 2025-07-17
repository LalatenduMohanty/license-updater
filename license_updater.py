import pandas as pd
import dnf
import argparse
import sys


def get_package_license(package_name, base=None):
    """
    Uses DNF API to query package information and extract the License.

    Args:
        package_name (str): The name of the package.
        base (dnf.Base, optional): Reusable DNF Base object.

    Returns:
        str: The extracted license string, or 'N/A' if not found or
             an error occurred.
    """
    try:
        # Create DNF base if not provided
        if base is None:
            base = dnf.Base()
            base.read_all_repos()
            base.fill_sack()
        
        # Strip architecture suffix from package name for DNF API query
        # e.g., "boost-atomic.x86_64" -> "boost-atomic"
        clean_package_name = package_name
        if '.' in package_name:
            # Check if the part after the last dot looks like an architecture
            parts = package_name.rsplit('.', 1)
            if len(parts) == 2:
                name_part, arch_part = parts
                # Common architectures
                common_archs = ['x86_64', 'i686', 'noarch', 'aarch64', 'ppc64le', 's390x']
                if arch_part in common_archs:
                    clean_package_name = name_part
        
        # Query for packages by name
        q = base.sack.query()
        available_packages = q.available().filter(name=clean_package_name)
        
        # Convert to list to evaluate the query
        packages = list(available_packages)
        
        if not packages:
            return "N/A"
        
        # If only one package, return its license
        if len(packages) == 1:
            return packages[0].license or "N/A"
        
        # If multiple packages, find the latest version using DNF's latest() method
        latest_packages = available_packages.latest()
        latest_packages_list = list(latest_packages)
        
        if latest_packages_list:
            return latest_packages_list[0].license or "N/A"
        
        # Fallback: manually find the newest package
        latest_package = packages[0]
        for pkg in packages[1:]:
            if is_newer_package(pkg, latest_package):
                latest_package = pkg
        
        return latest_package.license or "N/A"
        
    except Exception as e:
        error_msg = (f"An unexpected error occurred for package "
                     f"'{package_name}': {e}")
        print(error_msg, file=sys.stderr)
        return "Error: Unexpected"


def is_newer_package(pkg1, pkg2):
    """
    Compare two package objects to determine if pkg1 is newer than pkg2.
    Uses EVR (Epoch, Version, Release) comparison.

    Args:
        pkg1 (dnf.package.Package): First package object
        pkg2 (dnf.package.Package): Second package object

    Returns:
        bool: True if pkg1 is newer than pkg2
    """
    try:
        # Compare epochs first
        if pkg1.epoch != pkg2.epoch:
            return pkg1.epoch > pkg2.epoch
        
        # If epochs are equal, compare versions
        if pkg1.version != pkg2.version:
            # Use DNF's built-in version comparison by comparing the full EVR
            return pkg1.evr > pkg2.evr
        
        # If versions are equal, compare releases
        return pkg1.release > pkg2.release
        
    except Exception:
        # Fall back to string comparison of full EVR
        try:
            return pkg1.evr > pkg2.evr
        except Exception:
            return str(pkg1) > str(pkg2)


def update_licenses_from_dnf(csv_file_path, output_file_path=None):
    """
    Reads a CSV, updates 'License' column based on DNF API queries,
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

    # Initialize DNF base once for efficiency
    try:
        print("Initializing DNF base and loading repository metadata...")
        base = dnf.Base()
        base.read_all_repos()
        base.fill_sack()
        print("DNF initialization complete.")
    except Exception as e:
        print(f"Error initializing DNF: {e}", file=sys.stderr)
        return

    # Iterate through the DataFrame rows
    # Using .loc for safe assignment based on index
    for index, row in df.iterrows():
        if row['UBI?'].lower() == 'no':
            package_name = row['package']
            print(f"Processing package: {package_name}...")
            new_license = get_package_license(package_name, base)
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
                     "DNF API queries.")
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
