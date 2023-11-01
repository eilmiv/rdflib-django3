"""
Unittests for namespace management.
"""
from django.test import TestCase
from rdflib import Namespace
from rdflib.graph import Graph, ConjunctiveGraph
from rdflib.term import URIRef
from rdflib_django.store import DjangoStore


XML_NAMESPACE = ("xml", URIRef("http://www.w3.org/XML/1998/namespace"))
RDF_NAMESPACE = ("rdf", URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#"))
RDFS_NAMESPACE = ("rdfs", URIRef("http://www.w3.org/2000/01/rdf-schema#"))


class NamespaceTest(TestCase):
    """
    Tests for the weird behavior of RDFlib graphs and the default
    namespaces.
    """

    def setUp(self):
        self.store = DjangoStore()

    def testDefaultNamespaces(self):
        """
        Test the presence of the default namespaces.
        """
        g = Graph(store=self.store)
        namespaces = list(g.namespaces())
        self.assertIn(XML_NAMESPACE, namespaces)
        self.assertIn(RDF_NAMESPACE, namespaces)
        self.assertIn(RDFS_NAMESPACE, namespaces)

        # and again; by default,
        # initializing the graph will re-bind the namespaces
        # using a naive implementation, this will fail.
        g = Graph(store=self.store)
        g_namespaces = list(g.namespaces())
        self.assertIn(XML_NAMESPACE, g_namespaces)
        self.assertIn(RDF_NAMESPACE, g_namespaces)
        self.assertIn(RDFS_NAMESPACE, g_namespaces)

    def testCannotUpdateDefaultNamespaces(self):
        """
        Binding the prefix OR the URI of a default namespaces is a no-op.
        """
        g = Graph(store=self.store)
        self.assertIn(XML_NAMESPACE, list(g.namespaces()))

        # breaks test
        g.bind("hello-world", XML_NAMESPACE[1])
        self.assertIn(XML_NAMESPACE, list(g.namespaces()))

        g.bind(XML_NAMESPACE, URIRef("http://example.com/xml"))
        self.assertIn(XML_NAMESPACE, list(g.namespaces()))

    def testBindingNamespaces(self):
        """
        Binding custom namespaces just works.
        """
        g = Graph(store=self.store)
        ns = ("prefix", URIRef("http://example.com/prefix"))

        self.assertNotIn(ns, list(g.namespaces()))

        g.bind(ns[0], ns[1])
        self.assertIn(ns, list(g.namespaces()))

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




