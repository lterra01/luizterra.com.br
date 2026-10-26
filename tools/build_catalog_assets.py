"""Convert the two approved promotional covers; never copy paid content."""

import argparse
from pathlib import Path

from PIL import Image


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-root", type=Path, required=True)
    args = parser.parse_args()
    destination = Path(__file__).resolve().parents[1] / "public" / "ebooks"
    for folder, slug in (("indicadores", "indicadores-de-atendimento-na-pratica"), ("qualidade", "qualidade-e-feedback-no-atendimento")):
        with Image.open(args.source_root / folder / "Capa_Hotmart_v1.0.png") as cover:
            cover.convert("RGB").save(destination / f"{slug}.webp", "WEBP", quality=86, method=6)


if __name__ == "__main__":
    main()
