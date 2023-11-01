"""
Unit tests for the utils module.
"""
from django import test
from rdflib import Namespace

from rdflib_django.utils import get_named_graph, get_conjunctive_graph

EX = Namespace("https://www.example.com/")


class GraphTest(test.TestCase):
    """
    Checks on the utils module.
    """

    def test_conjunctive_and_named_graphs(self):
        g1 = get_named_graph(EX.g1)
        g2 = get_conjunctive_graph()
        g1_s2 = get_named_graph(EX.g1, "s2")
        g3 = get_conjunctive_graph("s2")
        g4 = get_named_graph(EX.g4, store_id="s3")
        g5 = get_conjunctive_graph("s3", identifier=EX.g4)

        g1.add((EX.a, EX.a, EX.a))
        g2.add((EX.b, EX.b, EX.b))
        g1_s2.add((EX.c, EX.c, EX.c))
        g3.add((EX.d, EX.d, EX.d))
        g4.add((EX.x, EX.x, EX.x))
        g5.add((EX.y, EX.y, EX.y))

        self.assertEqual(len(g1), 1)
        self.assertEqual(len(g1_s2), 1)
        self.assertEqual(len(g2), 2)
        self.assertEqual(len(g3), 2)
        self.assertEqual(len(g4), 2)

        self.assertEqual(set(g1), {(EX.a, EX.a, EX.a)})
        self.assertEqual(set(g2), {(EX.a, EX.a, EX.a), (EX.b, EX.b, EX.b)})
        self.assertEqual(set(g1_s2), {(EX.c, EX.c, EX.c)})
        self.assertEqual(set(g3), {(EX.c, EX.c, EX.c), (EX.d, EX.d, EX.d)})
        self.assertEqual(set(g4), set(g5))

        g2.remove((None, None, None))

        self.assertEqual(list(g1), [])
        self.assertEqual(list(g2), [])
        self.assertEqual(list(g1_s2), [(EX.c, EX.c, EX.c)])
