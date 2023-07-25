"""RecipeSage data models."""

from dataclasses import dataclass
from typing import Iterable, Optional

from recipe_scrapers import AbstractScraper

from ._types import JSON_LD, URL, Date, Duration, InstructionType

RECIPE_SAGE_CONTEXT = {
    "@context": "http://schema.org",
    "@type": "Recipe",
}

COMMENT_CONTEXT = {
    "@type": "Comment",
}


@dataclass
class Instruction:
    """Recipe instruction."""

    _type: InstructionType
    text: str


@dataclass
class Comment:
    """Recipe comment."""

    name: str
    text: str


@dataclass
class RecipeSage:
    """RecipeSage data model."""

    datePublished: Optional[Date]
    description: Optional[str]
    image: Optional[Iterable[URL]]
    name: str
    prepTime: Optional[Duration]
    recipeIngredient: Iterable[str]
    recipeInstructions: Iterable[Instruction]
    recipeYield: Optional[str]
    totalTime: Optional[Duration]
    recipeCategory: Optional[Iterable[str]]
    creditText: Optional[str]
    isBasedOn: Optional[URL]
    comment: Optional[Iterable[Comment]]

    @classmethod
    def from_scraper(cls: "RecipeSage", scraper: AbstractScraper) -> "RecipeSage":
        """Create RecipeSage from scraper.

        Args:
            scraper (AbstractScraper): scraper to convert

        Returns:
            RecipeSage: RecipeSage model
        """
        raise NotImplementedError("This should be implemented.")  # noqa: EM101

    def to_jsonld(self: "RecipeSage") -> JSON_LD:
        """Convert to JSON-LD for import/export.

        Returns:
            JSON_LD: JSON-LD data model
        """
        raise NotImplementedError("This should be implemented.")  # noqa: EM101
