import itertools
from passlib.hash import md5_crypt

TARGET = "$1$de4df4ce$1pZYBMgWLPXg1tZo6pke20"

bases = [
    "princess", "pinkprincess", "pink_princess", "pink-princess",
    "disneyprincess", "disney_princess", "disney-princess",
    "fairyprincess", "fairy_princess", "fairy-princess",
    "tiara", "magicwand", "magic_wand", "magic-wand", "wand",
    "crown", "queen", "royal", "castle", "glassslipper", "glass_slipper",
    "cinderella", "aurora", "belle", "snowwhite", "snow_white",
    "jasmine", "ariel", "rapunzel", "sleepingbeauty", "sleeping_beauty",
    "disney", "pink", "sparkle", "sparkly", "fairy", "fairygodmother",
    "princessparty", "princess_party", "pinkdress", "pink_dress",
    "halloween", "halloweencostume", "halloween_costume",
]

suffixes = [
    "", "1", "2", "3", "12", "21", "69", "99", "00", "01", "04", "05", "06",
    "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18",
    "19", "20", "21", "22", "23", "24", "25", "26",
    "123", "1234", "12345", "123456", "007", "911",
    "!", "!!", "!!!", "!1", "1!", "123!", "!123", "2024", "2025", "2026",
    "2000", "2001", "2002", "2003", "2004", "2005", "2006", "2007", "2008",
    "2009", "2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017",
    "2018", "2019", "2020", "2021", "2022", "2023",
    "2004!", "2005!", "2006!", "2007!",
    "4ever", "4life", "forever", "forlife", "4eva",
]

candidates = set()
for base in bases:
    variants = {base, base.capitalize(), base.upper(), base.title()}
    # snake/kebab -> TitleCase variants already covered partially
    for v in variants:
        for suf in suffixes:
            candidates.add(v + suf)
    # common separators before a numeric suffix
    for sep in ["_", "-", ".", "@", "#"]:
        for num in ["1", "12", "123", "1234", "2004", "2005", "2006", "2007", "2024", "2025", "2026"]:
            candidates.add(base + sep + num)
            candidates.add(base.capitalize() + sep + num)

# Names from the thread's Disney-princess theme
for name in ["cinderella", "aurora", "belle", "snowwhite", "jasmine", "ariel", "rapunzel", "tiana", "merida", "moana", "elsa", "anna"]:
    for v in {name, name.capitalize(), name.upper()}:
        for suf in ["", "1", "123", "!", "2004", "2005", "2024", "2025", "2026"]:
            candidates.add(v + suf)

print(f"trying {len(candidates)} candidates")
for c in sorted(candidates):
    if md5_crypt.verify(c, TARGET):
        print("FOUND:", c)
        break
else:
    print("no match")
