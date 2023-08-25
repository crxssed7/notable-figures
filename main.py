"""scrape wikipedia with a list of notable figures"""
import os
import re
import urllib.parse
import wikipediaapi
from figures import FIGURES

def write_sections(sections, outp, level=0):
    """write each section and any child sections"""
    for section in sections:
        heading = "#" * (level + 1)
        outp.write(f"{heading} {section.title}\n")
        outp.write(section.text.replace("\n", "\n\n"))
        outp.write("\n\n")
        write_sections(section.sections, outp, level + 1)

def sync():
    """syncs all figures with their Wikipedia articles"""
    wiki = wikipediaapi.Wikipedia('Notable Figures (notable@crxssed.dev)', 'en')

    for figure in FIGURES:
        wiki_id = dict(figure).get("id")
        image = dict(figure).get("image")
        if not wiki_id:
            continue

        figure_wiki = wiki.page(wiki_id)

        if not figure_wiki.exists():
            print(f"{wiki_id} does not exist on Wikipedia. Continuing...")
            continue

        filename = f"figures/{figure_wiki.title}.md"

        with open(filename, "w", encoding="utf8") as file:
            file.write(f"# {figure_wiki.title}\n\n")
            file.write(f"*{figure_wiki.summary}*\n\n")
            if image:
                file.write(f"<img src='{image}' width='300px'>\n\n")
            write_sections(figure_wiki.sections, file)

def update_readme():
    """updates the README with the new table of contents"""
    block_start = "<!-- TOC -->"
    block_end = "<!-- END-TOC -->"

    files = os.listdir("figures/")
    files.sort()
    files.remove(".keep")

    contents = [block_start]
    for file in files:
        contents.append(f"[{file.removesuffix('.md')}](figures/{urllib.parse.quote(file)})")
    contents.append(block_end)

    markdown = "\n".join(contents)

    with open("README.md", "rt", encoding="utf8") as fin:
        readme_contents = fin.read()

    pattern = f"{block_start}[\\s\\S]+{block_end}"
    new_contents = re.sub(
        pattern=pattern,
        repl=markdown,
        string=readme_contents
    )

    with open("README.md", "w", encoding="utf8") as fin:
        fin.write(new_contents)

if __name__ == "__main__":
    sync()
    update_readme()
