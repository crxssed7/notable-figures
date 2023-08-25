"""scrape wikipedia with a list of notable figures"""
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

wiki = wikipediaapi.Wikipedia('Notable Figures (notable@crxssed.dev)', 'en')

for figure in FIGURES:
    WIKI_ID = dict(figure).get("id")
    IMAGE = dict(figure).get("image")
    if not WIKI_ID:
        continue

    figure_wiki = wiki.page(WIKI_ID)

    if not figure_wiki.exists():
        print(f"{WIKI_ID} does not exist on Wikipedia. Continuing...")
        continue

    filename = f"figures/{figure_wiki.title}.md"

    with open(filename, "w", encoding="utf8") as file:
        file.write(f"# {figure_wiki.title}\n\n")
        file.write(f"*{figure_wiki.summary}*\n\n")
        if IMAGE:
            file.write(f"<img src='{IMAGE}' width='300px'>\n\n")
        write_sections(figure_wiki.sections, file)
