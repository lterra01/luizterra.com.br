"""Prepare public promotional covers; never copy paid content."""

import argparse
from pathlib import Path

from PIL import Image

from ebook_catalog import EBOOKS

ROOT = Path(__file__).resolve().parents[1]
COVER_WIDTHS = (320, 640, 960)


def build_responsive_covers():
    for book in EBOOKS:
        source = ROOT / book["cover"].lstrip("/")
        with Image.open(source) as cover:
            for width in COVER_WIDTHS:
                height = round(cover.height * width / cover.width)
                cover.convert("RGB").resize((width, height), Image.Resampling.LANCZOS).save(
                    source.with_name(f"{source.stem}-{width}.webp"),
                    "WEBP", quality=82, method=6,
                )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-root", type=Path)
    parser.add_argument("--responsive-only", action="store_true")
    args = parser.parse_args()
    if not args.responsive_only:
        if args.source_root is None:
            parser.error("--source-root is required unless --responsive-only is used")
        destination = ROOT / "public" / "ebooks"
        for folder, slug in (("indicadores", "indicadores-de-atendimento-na-pratica"), ("qualidade", "qualidade-e-feedback-no-atendimento")):
            with Image.open(args.source_root / folder / "Capa_Hotmart_v1.0.png") as cover:
                cover.convert("RGB").save(destination / f"{slug}.webp", "WEBP", quality=86, method=6)
    build_responsive_covers()


if __name__ == "__main__":
    main()
