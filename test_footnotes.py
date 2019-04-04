import unittest
from footnotes import get_footnote_indices, extract_footnotes, get_tex_tags, check_for_nesting, move_footnotes_to_end


class GetTexTagsTest(unittest.TestCase):
    def test_something_harder(self):
        """Test with some nesting and other tex elements."""

        #            0        10        20        30        40        50        60        70        80        90
        #            012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345
        test_text = "a@footnote{b@footnote{d}@acronym{e}}f@footnote{g}"
        self.assertDictEqual({11: ("@footnote{", 35),
                              22: ("@footnote{", 23),
                              33: ("@acronym{", 34),
                              47: ("@footnote{", 48)}, get_tex_tags(test_text))


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

    def test_can_deal_with_other_markup(self):
        """There are other types of markup too"""

        test_text = "....@footnote{  @markup{ooooo}gg} @footnote{==}"
        self.assertEqual({14: 32, 44: 46}, get_footnote_indices(test_text))

    def test_something_harder(self):
        """Test with some nesting and other tex elements."""

        #            0        10        20        30        40        50        60        70        80        90
        #            012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345
        test_text = "a@footnote{b@footnote{d}@acronym{e}}f@footnote{g}"
        self.assertEqual({11: 35, 22: 23, 47: 48}, get_footnote_indices(test_text))


class ExtractFootnotesTest(unittest.TestCase):
    def test_can_extract_footnotes(self):
        """Test that we can identify a footnote and separate it from some text."""

        test_text = "something something @footnote{this is the footnote} something else"

        def foonote_linker(link_number):
            return "<a href='{}'></a>".format(link_number)

        processed_text, footnote_dict = extract_footnotes(test_text, foonote_linker)
        self.assertEqual("something something <a href='1'></a> something else", processed_text)
        self.assertEqual({1: ('@footnote{', 'this is the footnote')}, footnote_dict)

    def test_something_harder(self):
        """Test with some nesting and other tex elements."""

        #            0        10        20        30        40        50        60        70        80        90
        #            012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345
        test_text = "something @footnote{this is the footnote @footnote{oo} @acronym{MIT}} ending@footnote{last one}"

        def foonote_linker(link_number):
            return "{}".format(link_number)

        processed_text, footnote_dict = extract_footnotes(test_text, foonote_linker)
        self.assertEqual("something 12 ending3", processed_text)  # not ideal but we know there's no nesting
        self.assertDictEqual({1: ('@footnote{', 'this is the footnote @footnote{oo} @acronym{MIT}'),
                              2: ('@footnote{', 'oo'),
                              3: ('@footnote{', 'last one')}, footnote_dict)


class TestCheckForNesting(unittest.TestCase):
    def test_positive(self):
        test_text = "@footnote{ @footnote{} }"
        self.assertTrue(check_for_nesting(test_text))

    def test_negative(self):
        test_text = "@footnote{ } @footnote{ }"
        self.assertFalse(check_for_nesting(test_text))

    def test_ignores_other_tags(self):
        test_text = "@footnote{ @acronym{ } }"
        self.assertFalse(check_for_nesting(test_text))


class TestMoveFootnotesToEnd(unittest.TestCase):
    def test_move_single_note(self):

        test_text = "t @footnote{z} d\n{{footnotes}}\n@@"
        self.assertEqual('t <a id="footnote_link_2-47" class="footnote_link" href="#footnote_2-47">47</a> d\n'
                         '{{footnotes}}\n<div id="footnote_2-47" class="footnote">'
                         '<p> <a href="#footnote_link_2-47" class="footnote_backlink">47</a>z\n@@',
                         move_footnotes_to_end(test_text, 2, 47))


if __name__ == "__main__":
    unittest.main()
