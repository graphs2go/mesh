from collections.abc import Iterable

from graphs2go.models import interchange, skos
from rdflib import SKOS, URIRef
from returns.maybe import Some
from returns.pipeline import is_successful

from mesh.models import Concept, Label, ReleaseGraph

_CONCEPT_BATCH_SIZE = 100


def __transform_labels(model: skos.LabeledModel) -> Iterable[interchange.Model]:
    for label_type, label in model.lexical_labels():
        assert isinstance(label, Label)
        yield interchange.Label.builder(
            literal_form=label.literal_form,
            subject=model,
            type_=Some(label_type),
            iri=Some(label.iri),
        ).set_created(label.created.value_or(None)).set_modified(
            label.modified.value_or(None)
        ).build()


def __transform_concept(
    *, concept: Concept, concept_scheme_iri: URIRef
) -> Iterable[interchange.Model]:
    yield interchange.Node.builder(iri=concept.iri).add_type(SKOS.Concept).set_created(
        concept.created.value_or(None)
    ).set_modified(concept.modified.value_or(None)).build()

    yield from __transform_labels(concept)

    # concept, skos:inScheme, concept scheme
    yield interchange.Relationship.builder(
        object_=concept_scheme_iri, predicate=SKOS.inScheme, subject=concept
    ).build()

    # Handle skos:definition specially since it's a subgraph and not a literal
    for definition in concept.definitions():
        definition_value = definition.value
        if not is_successful(definition_value):
            continue
        yield interchange.Property.builder(
            object_=definition_value.unwrap(),
            predicate=SKOS.definition,
            subject=concept,
            iri=Some(definition.iri),
        ).set_created(definition.created.value_or(None)).set_modified(
            definition.modified.value_or(None)
        ).set_source(
            definition.source.value_or(None)
        ).build()

    # skos:notation statements
    for notation in concept.notations():
        yield interchange.Property.builder(
            object_=notation, predicate=SKOS.notation, subject=concept
        ).build()

    # All skos:note sub-properties
    for note_predicate, note in concept.notes():
        yield interchange.Property.builder(
            object_=note, predicate=note_predicate, subject=concept
        ).build()

    # All skos:semanticRelation sub-properties
    for semantic_relation_predicate, related_concept in concept.semantic_relations():
        relationship_builder = interchange.Relationship.builder(
            object_=related_concept,
            predicate=semantic_relation_predicate,
            subject=concept,
        )
        if isinstance(related_concept, Concept):
            relationship_builder.set_created(
                related_concept.created.value_or(None)
            ).set_modified(related_concept.modified.value_or(None))
        yield relationship_builder.build()


# def _transform_concept_consumer(
#     input_: tuple[URIRef, ReleaseGraph.Descriptor],
#     output_queue: Queue,
#     work_queue: JoinableQueue,
# ) -> None:
#     (concept_scheme_iri, release_graph_descriptor) = input_
#
#     with ReleaseGraph.open(release_graph_descriptor, read_only=True) as release_graph:
#         while True:
#             concept_iris: tuple[URIRef, ...] | None = work_queue.get()
#
#             if concept_iris is None:
#                 work_queue.task_done()
#                 break  # Signal from the producer there's no more work
#
#             interchange_models: list[interchange.Model] = []  # type: ignore
#             for concept_iri in concept_iris:
#                 interchange_models.extend(
#                     __transform_concept(
#                         concept_scheme_iri=concept_scheme_iri,
#                         concept=release_graph.concept_by_iri(concept_iri),
#                     )
#                 )
#             output_queue.put(tuple(interchange_models))
#             work_queue.task_done()
#
#
# def _transform_concept_producer(
#     input_: ReleaseGraph.Descriptor, work_queue: JoinableQueue
# ) -> None:
#     concept_iris_batch: list[URIRef] = []
#     with ReleaseGraph.open(input_, read_only=True) as release_graph:
#         for concept_iri in release_graph.concept_iris:
#             concept_iris_batch.append(concept_iri)
#             if len(concept_iris_batch) == _CONCEPT_BATCH_SIZE:
#                 work_queue.put(tuple(concept_iris_batch))
#                 concept_iris_batch = []
#
#     if concept_iris_batch:
#         work_queue.put(tuple(concept_iris_batch))


def transform_release_graph_to_interchange_models(
    release_graph_descriptor: ReleaseGraph.Descriptor,
) -> Iterable[interchange.Model]:
    with ReleaseGraph.open(release_graph_descriptor, read_only=True) as release_graph:
        concept_scheme = release_graph.concept_scheme
        yield interchange.Node.builder(iri=concept_scheme.iri).add_type(
            SKOS.ConceptScheme
        ).set_modified(concept_scheme.modified).build()
        yield from __transform_labels(concept_scheme)

        for concept in release_graph.concepts():
            yield from __transform_concept(
                concept=concept, concept_scheme_iri=concept_scheme.iri
            )

    # yield from parallel_transform(
    #     consumer=_transform_concept_consumer,
    #     consumer_input=(concept_scheme.iri, release_graph_descriptor),
    #     producer=_transform_concept_producer,
    #     producer_input=release_graph_descriptor,
    # )
