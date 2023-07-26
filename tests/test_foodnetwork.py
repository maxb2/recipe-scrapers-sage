from recipe_scrapers import scrape_html

from recipe_scrapers_sage import export_recipe

def test_foodnetwork():

    with open("tests/test_data/foodnetwork.testhtml", "r") as f:
        scraper = scrape_html(f.read())

    out = export_recipe(scraper)

    assert out