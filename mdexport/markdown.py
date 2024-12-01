import markdown2
import frontmatter
from pathlib import Path
import re
from mdexport.templates import get_variables_from_template
from mdexport.config import get_attachment_dir
from mdexport.exporter import write_render_html

ATTACHMENT_DIRECTORY = get_attachment_dir()
MARKDOWN_EXTRAS = ["tables", "toc", "fenced-code-blocks"]


def generate_empty_md(output_file: Path, template: str):
    variables = get_variables_from_template(template)
    md_text = "---\n"
    for variable in variables:
        md_text += f"{variable}:\n"
    md_text += "---\n"
    output_file.write_text(md_text)


def convert_metadata_to_html(metadata):
    html = markdown2.markdown(metadata, extras=MARKDOWN_EXTRAS)
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
    md_content = md_relative_img_to_absolute(md_content, md_path)
    html_text = markdown2.markdown(md_content, extras=MARKDOWN_EXTRAS)
    return html_text


def generate_toc(
    md_content: str, md_path: Path, renderable_content: str, template: str | None
):
    toc_html = markdown2.markdown(md_content, extras=MARKDOWN_EXTRAS).toc_html
    rendered_document = write_render_html(template, renderable_content)
    heading_pages = {}
    offset = None
    for page_number, page in enumerate(rendered_document.pages, start=1):
        for box in page._page_box.descendants():
            # Check for headings (e.g., H1, H2, ...)
            if box.element_tag in {"h1", "h2", "h3", "h4", "h5", "h6"}:
                if not offset:
                    offset = page_number - 1
                element_id = box.element.get("id")
                heading_pages[element_id] = page_number - offset

    def replace_link(match):
        href = match.group(1)  # The href value
        text = match.group(2)  # The inner text of the <a> tag
        # Extract the page number from the heading_pages using the href (without #)
        page_number = heading_pages.get(href.lstrip("#"), "N/A")
        return f'<a href="{href}">{text} p.{page_number}</a>'

    updated_toc = re.sub(r'<a href="([^"]+)">([^<]+)</a>', replace_link, toc_html)
    return updated_toc


def md_relative_img_to_absolute(md_content: str, md_path: Path) -> str:
    md_path = md_path.parent
    image_regex = r"!\[.*?\]\((.*?)\)"

    def replace_path(match):
        img_path = match.group(1)
        # Skip URLs
        if re.match(r"https?://", img_path):
            return match.group(0)
        # Check if the path is already absolute
        if Path(img_path).is_absolute():
            return match.group(0)
        # Prepend the absolute path to the relative path
        absolute_path = (md_path / img_path).resolve()
        return f"![{match.group(0).split('](')[0][2:]}]({absolute_path})"

    # Replace all matches with the updated paths
    updated_content = re.sub(image_regex, replace_path, md_content)
    return updated_content


def get_base_path(md_path: Path) -> Path:
    return md_path.parent.resolve() / ATTACHMENT_DIRECTORY


def embed_to_img_tag(markdown: str, base_path) -> str:
    # Regular expression pattern to match ![[filename]]
    pattern = r"!\[\[(.*\.(?:jpg|jpeg|png|gif|bmp|tiff|tif|webp|svg|ico|heif|heic|raw|psd|ai|eps|indd|jfif))\]\]"

    def replace_with_img_tag(match):
        file_name = match.group(1)
        return f'<img src="{base_path}/{file_name}" alt="{file_name}" />'

    return re.sub(pattern, replace_with_img_tag, markdown)
