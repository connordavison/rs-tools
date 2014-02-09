# -*- coding: utf-8 -*-
import unittest

from metaphone.word import Word


class WordTestCase(unittest.TestCase):
    """
    """
    def test_init(self):
        word = Word("stupendous")
        self.assertEqual(word.original, "stupendous")
        self.assertEqual(word.decoded, "stupendous")
        self.assertEqual(word.normalized, "stupendous")
        self.assertEqual(word.upper, "STUPENDOUS")
        self.assertEqual(word.length, 10)
        self.assertEqual(word.buffer, u"--STUPENDOUS------")

    def test_init_unicode(self):
        word = Word("naïve")
        self.assertEqual(word.original, "na\xc3\xafve")
        self.assertEqual(word.decoded, u"na\xefve")
        self.assertEqual(word.normalized, "naive")
        self.assertEqual(word.upper, "NAIVE")
        self.assertEqual(word.length, 5)
        self.assertEqual(word.buffer, u"--NAIVE------")

    def test_is_slavo_germanic(self):
        word = Word("Berkowitz")
        self.assertTrue(word.is_slavo_germanic)
        word = Word("Czeck")
        self.assertTrue(word.is_slavo_germanic)
        word = Word("Bob")
        self.assertFalse(word.is_slavo_germanic)

    def test_get_first_letter(self):
        word = Word("naïve")
        self.assertEqual(word.get_letters(), "N")
        self.assertEqual(word.get_letters(0), "N")
        self.assertEqual(word.get_letters(0, 1), "N")

    def test_first_2_letters(self):
        word = Word("naïve")
        self.assertEqual(word.get_letters(0, 2), "NA")

    def test_first_3_letters(self):
        word = Word("naïve")
        self.assertEqual(word.get_letters(0, 3), "NAI")

    def test_get_4th_letter(self):
        word = Word("naïve")
        self.assertEqual(word.get_letters(3), "V")
