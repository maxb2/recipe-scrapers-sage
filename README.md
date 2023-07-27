# recipe-scrapers-sage


[![GitHub Workflow Status (with branch)](https://img.shields.io/github/actions/workflow/status/maxb2/recipe-scrapers-sage/ci.yml?branch=main&style=flat-square)](https://github.com/maxb2/recipe-scrapers-sage/actions/workflows/ci.yml)
[![codecov](https://codecov.io/github/maxb2/recipe-scrapers-sage/branch/main/graph/badge.svg?token=UAPS01UJEG)](https://codecov.io/github/maxb2/recipe-scrapers-sage)
[![PyPI](https://img.shields.io/pypi/v/recipe-scrapers-sage?style=flat-square)](https://pypi.org/project/recipe-scrapers-sage/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/recipe-scrapers-sage?style=flat-square)](https://pypi.org/project/recipe-scrapers-sage/#history)
[![Libraries.io dependency status for latest release](https://img.shields.io/librariesio/release/pypi/recipe-scrapers-sage?style=flat-square)](https://libraries.io/pypi/recipe-scrapers-sage)

This is a helper package to save data acquired through [recipe-scrapers](https://github.com/hhursev/recipe-scrapers/) in a format that is importable by [RecipeSage](https://github.com/julianpoy/RecipeSage) ([JSON-LD](https://en.wikipedia.org/wiki/JSON-LD), [implemented here](https://github.com/julianpoy/RecipeSage/blob/master/packages/backend/src/services/json-ld.js#L3-L34)).


## Install

```bash
pip install recipe-scrapers-sage
```

## Usage

To directly export a scraped recipe, use the `export_recipe` function:

```python
from recipe_scrapers import scrape_me
from recipe_scrapers_sage import export_recipe

scraper = scrape_me("<RECIPE URL>")

sage_json: dict = export_recipe(scraper)

# write `sage_json` to a file that RecipeSage can import
```

If you wish to modify a scraped recipe, use the `RecipeSage` class:

```python
from recipe_scrapers import scrape_me
from recipe_scrapers_sage import RecipeSage

scraper = scrape_me("<RECIPE URL>")

recipe_sage = RecipeSage.from_scraper(scraper)

recipe_sage.creditText = "<CREDIT TEXT>"

sage_json: dict = recipe_sage.to_json_ld()

# write `sage_json` to a file that RecipeSage can import
```