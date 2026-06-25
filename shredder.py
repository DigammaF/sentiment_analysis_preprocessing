from __future__ import annotations

import argparse
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Create a _small version of a text file containing only one tenth "
            "of its lines by sampling every 10th line."
        )
    )
    parser.add_argument(
        "file",
        help="Path to the input text file to shrink.",
    )
    return parser.parse_args()


def build_output_path(input_path: Path) -> Path:
    return input_path.with_name(f"{input_path.stem}_small{input_path.suffix}")


def sample_lines(lines: list[str]) -> list[str]:
    return [line for index, line in enumerate(lines) if index % 10 == 0]


def main() -> None:
    args = parse_args()
    input_path = Path(args.file)

    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")
    if not input_path.is_file():
        raise ValueError(f"Input path is not a file: {input_path}")

    lines = input_path.read_text(encoding="utf-8").splitlines(keepends=True)
    sampled = sample_lines(lines)
    output_path = build_output_path(input_path)
    output_path.write_text("".join(sampled), encoding="utf-8")

    print(f"Created sampled copy: {output_path}")


if __name__ == "__main__":
    main()
