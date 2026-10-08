"""Run the project's command-line example."""

import argparse


def main() -> None:
    """Print a greeting using the name supplied on the command line."""
    parser = argparse.ArgumentParser(description="Print a greeting.")
    parser.add_argument("--name", default="World", help="Name to greet.")
    args = parser.parse_args()
    print(f"Hello, {args.name}!")


if __name__ == "__main__":
    main()
