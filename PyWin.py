# Created by Abdughafur Khujzoda
import os
import sys
import difflib
from pathlib import Path


# ============================================================
# Py WINDOWS LAUNCHER
# ============================================================

APP_EXTENSIONS = {".exe", ".lnk"}


def normalize(text):
    """Normalize text for better matching."""
    replacements = {
        "-": " ",
        "_": " ",
        ".": " ",
    }

    text = text.lower().strip()

    for old, new in replacements.items():
        text = text.replace(old, new)

    return " ".join(text.split())


def get_search_folders():
    """Get important Windows application locations."""

    folders = []

    # PATH
    path_variable = os.environ.get("PATH", "")

    for folder in path_variable.split(os.pathsep):
        if folder and os.path.isdir(folder):
            folders.append(folder)

    # Start Menu
    folders.extend([
        os.path.expandvars(
            r"%APPDATA%\Microsoft\Windows\Start Menu\Programs"
        ),
        os.path.expandvars(
            r"%PROGRAMDATA%\Microsoft\Windows\Start Menu\Programs"
        ),
    ])

    # Program locations
    folders.extend([
        os.environ.get("ProgramFiles", ""),
        os.environ.get("ProgramFiles(x86)", ""),
        os.environ.get("ProgramW6432", ""),
        os.path.expandvars(r"%LOCALAPPDATA%\Programs"),
    ])

    # Remove duplicates
    result = []
    seen = set()

    for folder in folders:
        if not folder:
            continue

        if not os.path.isdir(folder):
            continue

        folder = os.path.abspath(folder)
        key = folder.lower()

        if key not in seen:
            seen.add(key)
            result.append(folder)

    return result


def calculate_score(query, filename):
    """Calculate how closely a program name matches the query."""

    query = normalize(query)
    filename = normalize(filename)

    if not query or not filename:
        return 0

    # Exact
    if query == filename:
        return 100

    # Exact beginning
    if filename.startswith(query):
        return 95

    # Query contained in filename
    if query in filename:
        return 90

    # Words
    query_words = set(query.split())
    filename_words = set(filename.split())

    if query_words and query_words.issubset(filename_words):
        return 88

    # Similarity
    similarity = difflib.SequenceMatcher(
        None,
        query,
        filename
    ).ratio()

    return int(similarity * 100)


def search_programs(query):
    """Search for Windows programs."""

    query = normalize(query)

    results = []
    seen = set()

    search_folders = get_search_folders()

    path_folders = {
        os.path.abspath(x).lower()
        for x in os.environ.get("PATH", "").split(os.pathsep)
        if x
    }

    for base_folder in search_folders:

        # ----------------------------------------------------
        # PATH folders
        # ----------------------------------------------------
        if base_folder.lower() in path_folders:

            try:
                for filename in os.listdir(base_folder):

                    extension = Path(filename).suffix.lower()

                    if extension != ".exe":
                        continue

                    full_path = os.path.join(
                        base_folder,
                        filename
                    )

                    if not os.path.isfile(full_path):
                        continue

                    program_name = Path(filename).stem

                    score = calculate_score(
                        query,
                        program_name
                    )

                    if score >= 55:

                        key = full_path.lower()

                        if key not in seen:
                            seen.add(key)
                            results.append(
                                (score, full_path)
                            )

            except (PermissionError, OSError):
                pass

            continue

        # ----------------------------------------------------
        # Start Menu / Program Files
        # ----------------------------------------------------
        try:

            for root, dirs, files in os.walk(base_folder):

                # Skip unnecessary folders
                dirs[:] = [
                    d for d in dirs
                    if d.lower() not in {
                        "node_modules",
                        "__pycache__",
                        ".git",
                        "cache",
                        "caches"
                    }
                ]

                for filename in files:

                    extension = Path(
                        filename
                    ).suffix.lower()

                    if extension not in APP_EXTENSIONS:
                        continue

                    program_name = Path(
                        filename
                    ).stem

                    score = calculate_score(
                        query,
                        program_name
                    )

                    if score < 55:
                        continue

                    full_path = os.path.join(
                        root,
                        filename
                    )

                    key = full_path.lower()

                    if key not in seen:
                        seen.add(key)

                        results.append(
                            (score, full_path)
                        )

        except (PermissionError, OSError):
            pass

    results.sort(
        key=lambda item: item[0],
        reverse=True
    )

    return results


def open_program(path):
    """Open a Windows application."""

    try:
        os.startfile(path)
        return True

    except Exception as error:
        print()
        print("❌ Could not open program:")
        print(error)
        return False


def launch_program(program_name):
    """Search and launch a program."""

    print()
    print("=" * 55)
    print(f"🔎 Searching for: {program_name}")
    print("=" * 55)

    results = search_programs(program_name)

    if not results:
        print()
        print("❌ Program not found.")
        print("💡 Try another name.")
        return

    # --------------------------------------------------------
    # Strong match
    # --------------------------------------------------------

    best_score, best_path = results[0]

    if best_score >= 90:

        print()
        print(f"✅ Found: {best_path}")
        print(f"📊 Match: {best_score}%")
        print()
        print("🚀 Opening...")

        open_program(best_path)
        return

    # --------------------------------------------------------
    # Several possible results
    # --------------------------------------------------------

    print()
    print("🔎 Possible programs:")
    print()

    displayed = results[:10]

    for number, (score, path) in enumerate(
        displayed,
        start=1
    ):
        print(
            f"{number}. "
            f"[{score}%] "
            f"{Path(path).stem}"
        )
        print(
            f"   📁 {path}"
        )

    print()

    choice = input(
        "Choose number (Enter = first, q = cancel): "
    ).strip()

    if choice.lower() == "q":
        print("❌ Cancelled.")
        return

    if choice == "":
        selected_path = displayed[0][1]

    elif choice.isdigit():

        number = int(choice)

        if number < 1 or number > len(displayed):
            print("❌ Invalid number.")
            return

        selected_path = displayed[number - 1][1]

    else:
        print("❌ Invalid choice.")
        return

    print()
    print(f"🚀 Opening: {selected_path}")

    open_program(selected_path)


def main():

    print()
    print("=" * 55)
    print("🤖 AI WINDOWS LAUNCHER")
    print("=" * 55)
    print()
    print("Write a program name.")
    print("Type 'exit' to close.")
    print()

    while True:

        try:
            program_name = input(
                "💻 Enter program name: "
            ).strip()

        except KeyboardInterrupt:
            print()
            print("👋 Goodbye!")
            break

        except EOFError:
            print()
            break

        if not program_name:
            print("⚠️ Please enter a program name.")
            continue

        if program_name.lower() in {
            "exit",
            "quit",
            "q"
        }:
            print()
            print("👋 Goodbye!")
            break

        launch_program(program_name)

        print()


if __name__ == "__main__":
    main()
# Created by Abdughafur Khujzoda
