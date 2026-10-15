import sys


def exit_now(msg="Exiting the program immediately (for debugging purposes)") -> None:
    """Exits the program immediately."""
    sys.exit(msg)

def display_clean_success(what: str) -> None:
    """Prints a success message."""
    print(f"✅ Success: `{what}` cleaned successfully.")