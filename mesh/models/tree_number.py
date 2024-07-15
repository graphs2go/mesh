from functools import cache
from typing import TYPE_CHECKING

from graphs2go.models import rdf
from rdflib import RDFS

if TYPE_CHECKING:
    from mesh.models.category import Category
    from mesh.models.thesaurus import Thesaurus


class TreeNumber(rdf.NamedModel):
    def __init__(self, resource: rdf.NamedResource, thesaurus: "Thesaurus"):
        super().__init__(resource)
        self.__thesaurus = thesaurus

    @property
    @cache
    def category(self) -> "Category":
        category_letter = self.label.split(".", 1)[0][0]
        for category in self.__thesaurus.categories:
            if category_letter == category.letter:
                return category
        raise KeyError("no category found for tree number " + self.label)

    @property
    def label(self) -> str:
        return self.resource.required_value(RDFS.label, rdf.Resource.ValueMappers.str)
