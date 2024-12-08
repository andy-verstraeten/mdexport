import markdown2
import frontmatter
from bs4 import BeautifulSoup
from pathlib import Path
import re
from mdexport.templates import get_variables_from_template
from mdexport.config import get_attachment_dir
from mdexport.exporter import write_render_html
from typing import Callable


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


def filter_depth(toc_html: str, depth: int) -> str:
    soup = BeautifulSoup(toc_html, "html.parser")

    def prune_ul(tag, current_depth):
        # Print the current depth (optional)
        print("Tag:", tag.name, "Depth:", current_depth)

        # If the current tag is a <ul> and exceeds the specified depth, remove it
        if tag.name == "ul" and current_depth > depth:
            tag.decompose()  # Remove the deeply nested <ul>
        else:
            # Recursively go through all children (not just <ul> tags)
            for child in tag.find_all(True, recursive=False):  # Only direct children
                prune_ul(child, current_depth + (1 if child.name == "ul" else 0))

    # Loop through all top-level tags and start pruning from each one
    for tag in soup.find_all(True, recursive=False):  # Find all tags at the top level
        prune_ul(tag, 1)

    return str(soup)


def generate_toc(
    renderer: Callable, md_content: str, md_path: Path, depth: int, template: str | None
):
    toc_html = markdown2.markdown(md_content, extras=MARKDOWN_EXTRAS).toc_html
    # TODO: feed empty file and solve error
    toc_html = filter_depth(toc_html, depth)

    test_render_toc = f"""<section class="mdexport-toc-container">
        {toc_html}
</section>
"""

    renderable_content = renderer(md_content, md_path, template, test_render_toc)
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
        return f'<a href="{href}" class="mdexport-toc-item"><span>{text}</span> <span>p.{page_number}</span></a>'

    updated_toc = re.sub(r'<a href="([^"]+)">([^<]+)</a>', replace_link, str(toc_html))
    combined_no_page_nr_style = generate_no_page_nr_css(offset) if offset else ""
    return f"""
    {combined_no_page_nr_style}
    <section class="mdexport-toc-container">
        {updated_toc}
</section>"""


def generate_no_page_nr_css(offset: int):
    selectors = map(lambda x: f"@page:nth({x})", range(1, offset + 1))

    style = """ {
    counter-reset: page 0;
    @bottom-right {
        content: none; 
    }
}"""
    return (
        "<style>"
        + "\n".join(map(lambda selector: selector + style, selectors))
        + "</style>"
    )


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
