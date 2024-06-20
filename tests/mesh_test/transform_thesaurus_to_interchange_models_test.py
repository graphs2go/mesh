import pytest
from graphs2go.models import interchange

from mesh.models.thesaurus import Thesaurus
from mesh.transform_thesaurus_to_interchange_models import (
    transform_thesaurus_to_interchange_models,
)


def test_transform(thesaurus_descriptor: Thesaurus.Descriptor) -> None:
    actual_interchange_model_class_set: set[type[interchange.Model]] = set()
    expected_interchange_model_class_set = {
        interchange.Label,
        interchange.Node,
        interchange.Relationship,
        interchange.Property,
    }
    for interchange_model in transform_thesaurus_to_interchange_models(
        thesaurus_descriptor
    ):
        actual_interchange_model_class_set.add(interchange_model.__class__)
        if expected_interchange_model_class_set == actual_interchange_model_class_set:
            return
    pytest.fail("not all interchange models represented")
