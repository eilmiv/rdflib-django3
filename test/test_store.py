"""
Unit tests for the store class.
Includes all unit tests that are hard or annoying to doctest.
"""
import datetime

import rdflib
from django import test
from rdflib.graph import Graph, ConjunctiveGraph
from rdflib.namespace import RDF, RDFS, Namespace
from rdflib.term import BNode, Literal, URIRef

from rdflib_django.store import DjangoStore

EX = Namespace("http://www.example.com/")


artis = URIRef("http://zoowizard.eu/resource/Artis")
berlin_zoo = URIRef("http://zoowizard.eu/resource/Berlin_Zoo")
zoo = URIRef("http://schema.org/Zoo")
org = URIRef("http://schema.org/Organisation")
anonymous = BNode()
artis_label = Literal("Artis")
date_literal = Literal(datetime.date.today())
number_literal = Literal(14)
bool_literal = Literal(True)
graph_context = Graph(identifier=EX["graph-context"])


class GraphTest(test.TestCase):
    """
    Several checks on the store by using
    it through the official Graph interface.
    """

    def setUp(self):
        self.graph = rdflib.Graph("Django")

    def test_add_uri_statement(self):
        """
        What happens if we add statements that are all URI's
        """
        self.graph.add((artis, RDF.type, zoo))
        self.assertEqual(len(self.graph), 1)

        self.graph.add((artis, RDF.type, org))
        self.assertEqual(len(self.graph), 2)

        self.graph.add((artis, RDF.type, zoo))
        self.assertEqual(len(self.graph), 2)

    def test_single_triple(self):
        """
        Returning the triples should give the correct result
        """
        self.graph.add((artis, RDF.type, zoo))
        triples = list(self.graph.triples((None, None, None)))
        self.assertEqual(len(triples), 1)

        self.assertTupleEqual(triples[0], (artis, RDF.type, zoo))

    def test_multiple_triples(self):
        """
        Returning the triples should give the correct result
        """
        self.graph.add((artis, RDF.type, zoo))
        self.graph.add((artis, RDF.type, org))
        self.graph.add((berlin_zoo, RDF.type, zoo))
        self.assertEqual(len(list(self.graph.triples((None, None, None)))), 3)

        self.assertEqual(len(list(self.graph.triples((artis, None, None)))), 2)
        self.assertEqual(
            len(list(self.graph.triples((None, RDF.type, None)))), 3
        )
        self.assertEqual(len(list(self.graph.triples((None, None, zoo)))), 2)
        self.assertEqual(len(list(self.graph.triples((None, None, org)))), 1)

    def test_blank_nodes(self):
        """
        Adding and querying for blank nodes should also work.
        """
        self.graph.add((artis, RDFS.seeAlso, anonymous))
        self.graph.add((anonymous, RDF.type, zoo))

        triple = list(self.graph.triples((None, None, zoo)))[0]
        self.assertTupleEqual(triple, (anonymous, RDF.type, zoo))

    def test_literals(self):
        """
        Adding and querying dates should also work.
        """
        self.graph.add((artis, RDFS.label, artis_label))
        self.graph.add((artis, EX["date"], date_literal))
        self.graph.add((artis, EX["bool"], bool_literal))
        self.graph.add((artis, EX["number"], number_literal))
        self.assertEqual(len(self.graph), 4)

        self.assertEqual(self.graph.value(artis, RDFS.label), artis_label)
        self.assertEqual(self.graph.value(artis, EX["date"]), date_literal)
        self.assertEqual(self.graph.value(artis, EX["bool"]), bool_literal)
        self.assertEqual(self.graph.value(artis, EX["number"]), number_literal)

    def test_falsy_literals(self):
        self.graph.add((artis, EX["prop"], Literal("")))
        self.graph.add((artis, EX["prop"], Literal(False)))

        self.assertEqual(
            list(self.graph.triples((artis, EX["prop"], Literal("")))),
            [(artis, EX["prop"], Literal(""))],
        )

        self.graph.remove((artis, EX["prop"], Literal("")))
        self.assertEqual(
            list(self.graph), [(artis, EX["prop"], Literal(False))]
        )

    def testConjunctiveGraph(self):
        ex = Namespace("https://www.example.org/")
        store1 = DjangoStore(identifier="store1")
        store2 = DjangoStore(identifier="store2")

        g1 = Graph(store1, identifier=ex.g1)
        g2 = ConjunctiveGraph(store1, identifier=ex.g2)
        g3 = Graph(store2, identifier=ex.g3)

        g1.add((ex.a, ex.a, ex.a))
        g2.add((ex.b, ex.b, ex.b))
        g3.add((ex.c, ex.c, ex.c))

        self.assertEquals(len(g1), 1)
        self.assertEquals(len(g2), 2)
        self.assertEquals(len(g3), 1)

        self.assertEquals(set(g1), {(ex.a, ex.a, ex.a)})
        self.assertEquals(set(g2), {(ex.a, ex.a, ex.a), (ex.b, ex.b, ex.b)})
        self.assertEquals(set(g3), {(ex.c, ex.c, ex.c)})

        g2.remove((None, None, None))

        self.assertEquals(list(g1), [])
        self.assertEquals(list(g2), [])
        self.assertEquals(list(g3), [(ex.c, ex.c, ex.c)])
