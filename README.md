# Description

Mdexport is CLI tool to publish Markdown files as PDF using Jinja2 templates. You can use Frontmatter metadata as custom values to be filled into your template.

Designed to work with Obsidian.

# Installation

```bash
pip3 install mdexport
```

# Usage

## Setup an html templates directory

Create a directory where you will store your templates. Each template should be a subdirectory named with the desired template name.

```
templates/
├──invoice/
│   ├──template.html
│   └──(any files or images that template.html depends on)
└── thesis/
   ├──template.html
   └──(any files or images that template.html depends on)
```

## Update the config of mdexport

Set the path of your template directory in the mdexport config.

```bash
mdexport settemplatedir /path/to/templates
```

## Create your template

Create a template.html file with a Jinja2 template.

```jinja
<html>
    <body>
        <section>
            <b>Date: {{date}}</b>
            <b>To: {{to}}</b>
        </section>
        <section>
            <p>{{body}}</p>
        </section>
</body>
</html>
```

## Create your MD file

Write your Markdown file. Provide Frontmatter metadata(compatible with Obsidian properties) as the keys that shall be rendered in your template.

```markdown
---
date: 14/10/2024
to: Bob
---

Body of my markdown file.
```

## Generate pdf

```bash
mdexport publish file.md -o output.pdf -t invoice
```

# Dependencies

Mdexport makes use of Weasyprint to generate PDF files. Installation of Weasyprint
seems to be not straight forward on some systems. If you encounter issues please
follow the steps in the link below.

[https://doc.courtbouillon.org/weasyprint/stable/first_steps.html#installation]

## Issue with weasyprint on Mac

```
echo 'export DYLD_LIBRARY_PATH=$(brew --prefix)/lib' >> ~/.bashrc

sudo ln -s /opt/homebrew/opt/glib/lib/libgobject-2.0.0.dylib /usr/local/lib/gobject-2.0
sudo ln -s /opt/homebrew/opt/pango/lib/libpango-1.0.dylib /usr/local/lib/pango-1.0
sudo ln -s /opt/homebrew/opt/harfbuzz/lib/libharfbuzz.dylib /usr/local/lib/harfbuzz
sudo ln -s /opt/homebrew/opt/fontconfig/lib/libfontconfig.1.dylib /usr/local/lib/fontconfig-1
sudo ln -s /opt/homebrew/opt/pango/lib/libpangoft2-1.0.dylib /usr/local/lib/pangoft2-1.0
```
