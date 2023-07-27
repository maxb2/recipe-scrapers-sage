"""Convert recipe scrapers to RecipeSage models appropriate for import/export."""

from recipe_scrapers import AbstractScraper

from ._types import JSON_LD
from .models import RecipeSage


def export_recipe(scraper: AbstractScraper) -> JSON_LD:
    """Export recipe to RecipeSage JSON-LD format.

    Args:
        scraper (AbstractScraper): recipe scraper

    Returns:
        JSON_LD: output
    """
    return RecipeSage.from_scraper(scraper).to_json_ld()


__all__ = ["export_recipe", "RecipeSage"]
