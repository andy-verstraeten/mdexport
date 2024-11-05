import markdown2
import frontmatter
from pathlib import Path
import re

ATTACHMENT_DIRECTORY = "attachments"


def convert_metadata_to_html(metadata):
    html = markdown2.markdown(metadata, extras=["tables"])
    if html.startswith("<p>"):
        html = html[3:]
    if html.endswith("</p>\n"):
        html = html[:-5]
    return html


def extract_md_metadata(md_file: Path) -> dict:
    # TODO: figure out all md works as values
    metadata = frontmatter.load(md_file).metadata
    return {key: convert_metadata_to_html(md) for key, md in metadata.items()}


def read_md_file(md_file: Path) -> str:
    return frontmatter.load(md_file).content


def convert_md_to_html(md_content: str, md_path: Path) -> str:
    attachment_path = get_base_path(md_path)
    md_content = embed_to_img_tag(md_content, attachment_path)
    html_text = markdown2.markdown(md_content, extras=["tables"])
    return html_text


def get_base_path(md_path: Path) -> Path:
    return md_path.parent.resolve() / ATTACHMENT_DIRECTORY


def embed_to_img_tag(markdown: str, base_path) -> str:
    # Regular expression pattern to match ![[filename]]
    pattern = r"!\[\[(.*\.(?:jpg|jpeg|png|gif|bmp|tiff|tif|webp|svg|ico|heif|heic|raw|psd|ai|eps|indd|jfif))\]\]"

    def replace_with_img_tag(match):
        file_name = match.group(1)
        return f'<img src="{base_path}/{file_name}" alt="{file_name}" />'

    return re.sub(pattern, replace_with_img_tag, markdown)
