"""Entrypoint to the application."""
from dotenv import load_dotenv

from app import decode_sudoku


def main():
    """Set up entry point into the application."""
    load_dotenv()  # loads environment variables from .env file if present.

    decode_sudoku.main()


if __name__ == "__main__":
    main()
