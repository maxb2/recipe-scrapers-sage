"""RecipeSage data models."""

from dataclasses import dataclass
from datetime import timedelta
from typing import Iterable, Optional, Type

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

    def to_json_ld(self: "Instruction") -> JSON_LD:
        """Export to JSON-LD.

        Returns:
            JSON_LD: output
        """
        return {"@type": self._type, "text": self.text}


@dataclass
class Comment:
    """Recipe comment."""

    name: str
    text: str

    def to_json_ld(self: "Comment") -> JSON_LD:
        """Export to JSON-LD.

        Returns:
            JSON_LD: output
        """
        return {
            **COMMENT_CONTEXT,
            "name": self.name or "Author Notes",
            "text": self.text,
        }


@dataclass
class RecipeSage:
    """RecipeSage data model."""

    datePublished: Optional[Date]
    description: Optional[str]
    image: Iterable[URL]
    name: str
    prepTime: Optional[Duration]
    recipeIngredient: Iterable[str]
    recipeInstructions: Iterable[Instruction]
    recipeYield: Optional[str]
    totalTime: Optional[Duration]
    recipeCategory: Iterable[str]
    creditText: Optional[str]
    isBasedOn: Optional[URL]
    comment: Iterable[Comment]

    @classmethod
    def from_scraper(cls: "Type[RecipeSage]", scraper: AbstractScraper) -> "RecipeSage":
        """Create RecipeSage from scraper.

        Args:
            scraper (AbstractScraper): scraper to convert

        Returns:
            RecipeSage: RecipeSage model
        """

        return cls(
            datePublished=scraper.schema.data.get("datePublished", None),
            description=scraper.schema.data.get("description", None),
            image=scraper.schema.image(),
            name=scraper.schema.data.get("name"),
            prepTime=scraper.schema.data.get("prepTime", None),
            recipeIngredient=scraper.schema.ingredients(),
            recipeInstructions=[
                Instruction(ins.get("@type", "HowToStep"), ins.get("text", ""))
                for ins in scraper.schema.data.get("recipeInstructions", [])
            ],
            recipeYield=scraper.schema.data.get("recipeYield", None),
            totalTime=scraper.schema.data.get("totalTime", None),
            recipeCategory=scraper.schema.data.get("recipeCategory", []),
            creditText=None,
            isBasedOn=scraper.url,
            comment=[],
        )

    def to_json_ld(self: "RecipeSage") -> JSON_LD:
        """Convert to JSON-LD for import/export.

        Returns:
            JSON_LD: JSON-LD data model
        """

        # TODO: refactor this
        _prepTime: str = ""

        if isinstance(self.prepTime, timedelta):
            _prepTime = f"PT{self.prepTime.total_seconds()//60}M"
        elif isinstance(self.prepTime, str):
            _prepTime = self.prepTime

        _totalTime: str = ""

        if isinstance(self.totalTime, timedelta):
            _totalTime = f"PT{self.totalTime.total_seconds()//60}M"
        elif isinstance(self.totalTime, str):
            _totalTime = self.totalTime

        return {
            **RECIPE_SAGE_CONTEXT,
            "datePublished": self.datePublished or "",
            "description": self.description or "",
            "image": self.image,
            "name": self.name,
            "prepTime": _prepTime,
            "recipeIngredient": [
                ingredient for ingredient in self.recipeIngredient if ingredient
            ],
            "recipeInstructions": [
                instruction.to_json_ld() for instruction in self.recipeInstructions
            ],
            "recipeYield": self.recipeYield or "",
            "totalTime": _totalTime,
            "recipeCategory": self.recipeCategory or [],
            "creditText": self.creditText or "",
            "isBasedOn": self.isBasedOn or "",
            "comment": [comment.to_json_ld() for comment in self.comment],
        }
