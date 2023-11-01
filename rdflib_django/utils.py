"""
Utility functions for using rdflib_django.
"""
from rdflib.graph import ConjunctiveGraph, Graph
from rdflib.store import VALID_STORE
from rdflib.term import URIRef

from .store import DEFAULT_STORE, DjangoStore


def get_conjunctive_graph(store_id=DEFAULT_STORE, identifier=None):
    """
    Returns an open conjunctive graph.

    The returned graph reads triples from all graphs in the store.
    Write operations happen on the graph specified by the identifier parameter
    or a graph identified by a blank node if the identifier is not provided.
    """
    store = DjangoStore(identifier=store_id)
    graph = ConjunctiveGraph(store=store, identifier=identifier)
    if graph.open(None) != VALID_STORE:
        raise ValueError(
            "The store identified by {} is not a valid store".format(store_id)
        )
    return graph


def get_named_graph(identifier, store_id=DEFAULT_STORE, create=True):
    """
    Returns an open named graph.
    """
    if not isinstance(identifier, URIRef):
        identifier = URIRef(identifier)

    store = DjangoStore(identifier=store_id)
    graph = Graph(store, identifier=identifier)
    if graph.open(None, create=create) != VALID_STORE:
        raise ValueError(
            "The store identified by {} is not a valid store".format(
                store_id
            )
        )
    return graph
