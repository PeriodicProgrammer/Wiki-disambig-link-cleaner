import pywikibot
from pywikibot import textlib
import re

site = pywikibot.Site('en', 'wikipedia')
site.login()

def clear():
    print("\033c", end="")

def get_short_description(page_text):
    short_desc = re.search(r"\{\{short description\s*\|([^\}]+)}}", page_text)
    if short_desc is not None:
        return short_desc.group(1)
    return None


def get_targets(page):
    items = []
    for line in page.text.splitlines():
        if re.search(r"==\s*See also\s*==", line) is not None:
            break
        links = re.findall(r"\*+\s*\[\[([^\]\|]+)[^\]]*]", line)
        if links:
            items.append(links[0])
    i = 1
    item_dict = {}
    for item in items:
        item_dict[i] = item
        i+= 1
    return item_dict

root_cat = pywikibot.Category(site, "Category:Disambiguation pages with many incoming links")

def walk_category(cat):
    for page in cat.articles():
        yield page
    for subcat in cat.subcategories():
        yield from walk_category(subcat)

def get_section_with_link(page, target_title):
    data = textlib.extract_sections(page.text, page.site)
    for sec in data:
        # Check if the link appears in this section
        if re.search(r"\[\[([^\]\|]+)[^\]\|]*\]\]", sec):
                return sec
    return None

for disambig in walk_category(root_cat):
    print("Disambiguation page:", disambig.title())
    targets = get_targets(disambig)
    for key, value in targets.items():
        print(f"{key}: {value}")
    print()
    # Get all pages linking to this disambiguation page
    for page in disambig.getReferences(namespaces=[0]):  # mainspace only
        print(f"={page.title()}=")
        short_desc = get_short_description(page.text)
        if short_desc is not None:
            print(f"Short description: {short_desc}")
        print(get_section_with_link(page, disambig))
        option = input("Enter option: ")
        print()
        if option == "skip":
            clear()
            break
