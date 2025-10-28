#!/usr/bin/env python3
"""
caption.py — create or update caption sidecar files for images.

Examples:
  # Create new captions
  python caption.py ./dataset --caption_text "portrait of Talia, high quality"

  # Overwrite existing captions
  python caption.py ./dataset --caption_text "new caption" --overwrite

  # Append to existing captions
  python caption.py ./dataset --caption_text "" --append "[POSE] [EXPRESSION] [CLOTHING] [SETTING]"

  # Prepend to existing captions
  python caption.py ./dataset --caption_text "" --prepend "Talia,"
"""

import argparse
import os
import logging
from pathlib import Path


def create_caption_files(
    image_folder: Path,
    file_pattern: str,
    caption_text: str,
    caption_file_ext: str,
    overwrite: bool,
    append: str,
    prepend: str,
):
    """Create or update caption files alongside images matching the given pattern."""
    patterns = [pattern.strip() for pattern in file_pattern.split(",")]

    for pattern in patterns:
        for file in image_folder.glob(pattern):
            txt_file = file.with_suffix(caption_file_ext)

            if txt_file.exists():
                existing = txt_file.read_text().strip()
                if overwrite:
                    new_text = caption_text
                elif append:
                    new_text = (existing + " " + append).strip()
                elif prepend:
                    new_text = (prepend + " " + existing).strip()
                else:
                    logging.info(f"Skipped existing caption: {txt_file}")
                    continue
            else:
                new_text = caption_text

            txt_file.write_text(new_text)
            logging.info(f"Caption file written: {txt_file}")


def writable_dir(target_path):
    """Check if a path is a valid directory and writable."""
    path = Path(target_path)
    if path.is_dir():
        if os.access(path, os.W_OK):
            return path
        raise argparse.ArgumentTypeError(f"Directory '{path}' is not writable.")
    raise argparse.ArgumentTypeError(f"Directory '{path}' does not exist.")


def main():
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    parser = argparse.ArgumentParser(
        description="Create or update caption sidecar files for images."
    )
    parser.add_argument(
        "image_folder",
        type=writable_dir,
        help="The folder where the image files are located",
    )
    parser.add_argument(
        "--file_pattern",
        type=str,
        default="*.png, *.jpg, *.jpeg, *.webp",
        help="Comma-separated glob patterns for image files",
    )
    parser.add_argument(
        "--caption_file_ext",
        type=str,
        default=".caption",
        help="Extension to use for caption files (default: .caption)",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        default=False,
        help="Overwrite existing caption files with new text",
    )
    parser.add_argument(
        "--append",
        type=str,
        help="Append this text to existing captions (ignored if --overwrite is set)",
    )
    parser.add_argument(
        "--prepend",
        type=str,
        help="Prepend this text to existing captions (ignored if --overwrite is set)",
    )

    # Mutually exclusive: either inline text or a file containing text
    caption_group = parser.add_mutually_exclusive_group(required=True)
    caption_group.add_argument(
        "--caption_text", type=str, help="The text to include in new caption files"
    )
    caption_group.add_argument(
        "--caption_file",
        type=argparse.FileType("r"),
        help="A file containing the text to include in new caption files",
    )

    args = parser.parse_args()

    # Resolve caption text robustly
    if args.caption_text is not None:
        caption_text = args.caption_text
    elif args.caption_file:
        caption_text = args.caption_file.read()
    else:
        caption_text = ""

    create_caption_files(
        args.image_folder,
        args.file_pattern,
        caption_text,
        args.caption_file_ext,
        args.overwrite,
        args.append,
        args.prepend,
    )


if __name__ == "__main__":
    main()
