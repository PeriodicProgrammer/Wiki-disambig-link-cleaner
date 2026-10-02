import pywikibot
import re
site = pywikibot.Site('en', 'wikipedia')
site.login()

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

for disambig in walk_category(root_cat):
    print("Disambiguation page:", disambig.title())
    targets = get_targets(disambig)
    for key, value in targets.items():
        print(f"{key}: {value}")
    # Get all pages linking to this disambiguation page
    for page in disambig.getReferences(namespaces=[0]):  # mainspace only
        print("  ->", page.title())