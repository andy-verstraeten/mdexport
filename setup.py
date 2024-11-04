from setuptools import setup

setup(
    name="mdexport",
    version="0.0.1",
    py_modules=["mdexport"],
    install_requires=[
        "click",
        "markdown2",
        "weasyprint",
        "jinja2",
        "python-frontmatter",
        "pytest",
        "pytest-cov",
    ],
    entry_points={"console_scripts": ["mdexport = mdexport.mdexport:cli"]},
)
