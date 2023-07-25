"""Convert recipe scrapers to RecipeSage models appropriate for import/export."""

from recipe_scrapers import AbstractScraper

from .models import RecipeSage


def scraper_to_sage(scraper: AbstractScraper) -> RecipeSage:  # noqa: ARG001
    """Recipe scraper to RecipeSage model.

    Args:
        scraper (AbstractScraper): recipe scraper

    Raises:
        NotImplementedError: _description_

    Returns:
        RecipeSage: RecipeSage model
    """
    raise NotImplementedError("This should be implemented.")  # noqa: EM101
