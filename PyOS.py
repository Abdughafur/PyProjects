# Created by Abdughafur

import platform
import sys


# ============================================================
# OS INFORMATION
# ============================================================


def get_os_details():
    """Collect basic system information."""

    os_name = platform.system()
    os_release = platform.release()
    os_version = platform.version()
    architecture = platform.machine()
    processor = platform.processor() or "Unknown"
    python_version = sys.version.split()[0]

    return {
        "os_name": os_name,
        "os_release": os_release,
        "os_version": os_version,
        "architecture": architecture,
        "processor": processor,
        "python_version": python_version,
    }


def display_os_info(info):
    """Print the device operating system information."""

    print()
    print("=" * 42)
    print("🖥️  DEVICE OS INFORMATION")
    print("=" * 42)
    print(f"Operating System: {info['os_name']}")
    print(f"Version: {info['os_version']}")
    print(f"Release: {info['os_release']}")
    print(f"Architecture: {info['architecture']}")
    print(f"Processor: {info['processor']}")
    print(f"Python Version: {info['python_version']}")
    print("=" * 42)


def main():
    details = get_os_details()
    display_os_info(details)


if __name__ == "__main__":
    main()
