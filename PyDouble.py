# Created by Abdughafur

import hashlib
from pathlib import Path
from collections import defaultdict


# ============================================================
# DUPLICATE FILE FINDER
# ============================================================

CHUNK_SIZE = 1024 * 1024  # 1 MB


def calculate_hash(file_path):
    """Calculate SHA-256 hash of a file."""

    sha256 = hashlib.sha256()

    try:
        with open(file_path, "rb") as file:
            while True:
                chunk = file.read(CHUNK_SIZE)

                if not chunk:
                    break

                sha256.update(chunk)

        return sha256.hexdigest()

    except (PermissionError, OSError) as error:
        print(f"⚠️ Could not read: {file_path}")
        print(f"   {error}")
        return None


def scan_files(folder):
    """Find all files inside a folder recursively."""

    files = []

    for path in Path(folder).rglob("*"):
        if path.is_file():
            files.append(path)

    return files


def find_duplicates(folder):
    """Find duplicate files."""

    print()
    print("=" * 60)
    print("🔎 DUPLICATE FILE FINDER")
    print("=" * 60)

    print(f"\n📁 Scanning: {folder}")

    files = scan_files(folder)

    print(f"📄 Files found: {len(files)}")

    # --------------------------------------------------------
    # Group files by size
    # --------------------------------------------------------

    size_groups = defaultdict(list)

    for file_path in files:
        try:
            size = file_path.stat().st_size
            size_groups[size].append(file_path)

        except (PermissionError, OSError):
            pass

    # Only files with the same size can be duplicates
    candidates = [
        group
        for group in size_groups.values()
        if len(group) > 1
    ]

    print(f"🔍 Possible duplicate groups: {len(candidates)}")

    # --------------------------------------------------------
    # Compare hashes
    # --------------------------------------------------------

    duplicates = []

    for group in candidates:

        hash_groups = defaultdict(list)

        for file_path in group:

            file_hash = calculate_hash(file_path)

            if file_hash:
                hash_groups[file_hash].append(file_path)

        for same_files in hash_groups.values():

            if len(same_files) > 1:
                duplicates.append(same_files)

    return duplicates


def display_duplicates(duplicates):
    """Display duplicate files."""

    print()
    print("=" * 60)
    print("📋 DUPLICATES")
    print("=" * 60)

    if not duplicates:
        print("\n✅ No duplicate files found.")
        return

    total_duplicates = 0

    for number, group in enumerate(duplicates, start=1):

        print()
        print(f"Group {number}:")
        print("-" * 50)

        for file_path in group:
            print(f"📄 {file_path}")

        total_duplicates += len(group) - 1

    print()
    print("=" * 60)
    print(f"🗑️ Duplicate copies: {total_duplicates}")
    print("=" * 60)


def main():

    folder = input(
        "\nEnter folder path: "
    ).strip()

    if not folder:
        print("❌ No folder specified.")
        return

    folder_path = Path(folder)

    if not folder_path.exists():
        print("❌ Folder does not exist.")
        return

    if not folder_path.is_dir():
        print("❌ Path is not a folder.")
        return

    duplicates = find_duplicates(folder_path)

    display_duplicates(duplicates)


if __name__ == "__main__":
    main()
