import unittest
from footnotes import get_footnote_indices, extract_footnotes


class GetFootnotesTest(unittest.TestCase):
    def test_can_find_footnote(self):
        """Using real SICP text, make sure we can find a single footnote."""

        test_text = "d to communication.@footnote{For distributed systems, this perspective was pursued by Lamport " \
                    "(1978), who showed how to use communication to establish ``global clocks'' that can be used to " \
                    "establish orderings on events in distributed systems.} It is intriguing "
        self.assertEqual({29: 242}, get_footnote_indices(test_text))

    def test_nested_footnote(self):
        """I don't know if nested footnotes ever happen but we can allow for it."""

        test_text = "@footnote{--@footnote{++}--}"
        self.assertEqual({10: 27, 22: 24}, get_footnote_indices(test_text))

    def test_sequential_footnote(self):
        """Test sequential footnotes and empty footnotes."""

        test_text = "....@footnote{}  @footnote{ooooo}"
        self.assertEqual({14: 14, 27: 32}, get_footnote_indices(test_text))


class ExtractFootnotesTest(unittest.TestCase):
    def test_can_extract_footnotes(self):
        """Test that we can identify a footnote and separate it from some text."""

        test_text = "something something @footnote{this is the footnote} something else"
        processed_text, footnote_dict = extract_footnotes(test_text)
        self.assertEqual("something something  something else", processed_text)
        self.assertEqual({1: "this is the footnote"}, footnote_dict)
