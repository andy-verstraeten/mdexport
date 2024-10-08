import markdown2
import frontmatter
from pathlib import Path


def extract_md_metadata(md_file: Path) -> dict:
    return frontmatter.load(md_file).metadata


def read_md_file(md_file: Path) -> str:
    return frontmatter.load(md_file).content


def convert_md_to_html(md_content: str) -> str:
    return markdown2.markdown(md_content)
