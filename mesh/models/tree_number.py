from typing import TYPE_CHECKING

from rdflib import RDFS

from graphs2go.models import rdf

if TYPE_CHECKING:
    from mesh.models.category import Category
    from mesh.models.thesaurus import Thesaurus


class TreeNumber(rdf.NamedModel):
    def __init__(self, resource: rdf.NamedResource, thesaurus: "Thesaurus"):
        super().__init__(resource)
        self.__thesaurus = thesaurus

    @property
    def category(self) -> "Category":
        category_letter = self.label.split(".", 1)[0][0]
        for category in self.__thesaurus.top_concepts():
            if category_letter == category.letter:
                return category
        raise KeyError("no category found for tree number " + self.label)

    @property
    def label(self) -> str:
        return self.resource.required_value(RDFS.label, rdf.Resource.ValueMappers.str)
