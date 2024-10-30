import re

import pytest
from recipe_scrapers import scrape_html

from recipe_scrapers_sage import RecipeSage, export_recipe
from recipe_scrapers_sage.models import Comment


@pytest.fixture
def testhtml():
    with open("tests/test_data/foodnetwork.testhtml", "r") as f:
        return f.read()


RESULT = {
    "@context": "http://schema.org",
    "@type": "Recipe",
    "datePublished": "2015-09-04T13:16:56Z",
    "description": "",
    "image": "https://d2v9mhsiek5lbq.cloudfront.net/eyJidWNrZXQiOiJsb21hLW1lZGlhLXVrIiwia2V5IjoiZm9vZG5ldHdvcmstaW1hZ2UtZGVmYXVsdC1wbGFjZWhvbGRlci5qcGciLCJlZGl0cyI6eyJyZXNpemUiOnsiZml0IjoiY292ZXIiLCJ3aWR0aCI6MTkyMCwiaGVpZ2h0IjoxMDgwfSwianBlZyI6eyJxdWFsaXR5Ijo3NSwicHJvZ3Jlc3NpdmUiOnRydWV9fX0=",
    "name": "Chicken Marsala",
    "prepTime": "PT15M",
    "recipeIngredient": [
        "4 (225g) boneless skinless chicken breasts",
        "Plain flour, for dredging, plus 2 tbsp",
        "85g butter",
        "1 tbsp olive oil",
        "80g sliced mushrooms",
        "2 tbsp minced garlic",
        "4 tbsp Marsala wine",
        "500ml beef stock",
    ],
    "recipeInstructions": [
        {
            "@type": "HowToStep",
            "text": "1) Put the chicken breasts between 2 pieces of waxed paper and flatten with a meat pounder until thin. Cut each chicken breast into 4 pieces.",
        },
        {
            "@type": "HowToStep",
            "text": "2) Add some flour to a shallow bowl. Dredge the chicken in the flour and shake off the excess flour.",
        },
        {
            "@type": "HowToStep",
            "text": "3) Add the butter and olive oil to a large saute pan over high heat and heat until it sizzles, do NOT let it brown. Add the chicken and saute until brown on both sides.",
        },
        {
            "@type": "HowToStep",
            "text": "4) Stir in the sliced mushrooms and saute briefly, then add the garlic. Add the Marsala and simmer for 3 minutes, then stir in the remaining 2 tbsp of flour.",
        },
        {
            "@type": "HowToStep",
            "text": "5) Pour in the beef stock and leave to simmer until the sauce thickens, about 3 to 5 minutes. Transfer the chicken to a serving platter and serve.",
        },
        {
            "@type": "HowToStep",
            "text": "This recipe was provided by professional chefs and has been scaled down from a bulk recipe provided by a restaurant. The Food Network kitchens chefs have not tested this recipe, in the proportions indicated, and therefore we cannot make any representation as to the results.",
        },
    ],
    "recipeYield": "4",
    "totalTime": "",
    "recipeCategory": ["main-course", "lunch"],
    "creditText": "",
    "isBasedOn": "",
    "comment": [],
}


def test_export(testhtml):
    scraper = scrape_html(testhtml)

    out = export_recipe(scraper)

    assert out == RESULT


def test_comment(testhtml):
    scraper = scrape_html(testhtml)

    sage = RecipeSage.from_scraper(scraper)

    sage.comment = [Comment("Author Notes", "A note.")]

    assert sage.to_json_ld().get("comment") == [
        {
            "@type": "Comment",
            "name": "Author Notes",
            "text": "A note.",
        }
    ]


def test_instruction(testhtml):
    scraper = scrape_html(testhtml)

    _ins = [
        {"text": ins}
        for ins in re.sub(
            r"\n+", "\n", scraper.schema.data["recipeInstructions"]
        ).splitlines()
    ]

    scraper.schema.data["recipeInstructions"] = _ins

    sage = RecipeSage.from_scraper(scraper)

    assert sage.to_json_ld() == RESULT

    scraper.schema.data["recipeInstructions"].append(10)

    with pytest.raises(ValueError, match="got a bad value"):
        RecipeSage.from_scraper(scraper)
