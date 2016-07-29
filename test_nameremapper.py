from nameremapper import NameRemapper
import unittest


class NameRemapperTest(unittest.TestCase):
    @staticmethod
    def always_same(population, sample_size):
        return population[:sample_size]

    def test_remaps_single_word(self):
        replacements = ["melba", "peach"]
        remapper = NameRemapper(sample_fn=NameRemapperTest.always_same, replacement_word_source=replacements)
        input_names = ["mary"]
        remapper_for_names = remapper.for_names(input_names)

        remapped = remapper_for_names.remap_name("mary")

        self.assertEqual("melba", remapped)

    def test_words_in_phrase_remapped_separately_to_sorted_replacements(self):
        presorted_replacements = \
            ["melba", "peach",   "strawberry", "vanilla"]
        input_names = \
            ["double-barrelled", "foop",       "mary"]
        remapper = NameRemapper(sample_fn=NameRemapperTest.always_same, replacement_word_source=presorted_replacements)

        remapper_for_names = remapper.for_names(input_names)

        self.assertEqual("strawberry", remapper_for_names.remap_name("foop"))
        self.assertEqual("peach-melba", remapper_for_names.remap_name("double-barrelled"))
        self.assertEqual("vanilla", remapper_for_names.remap_name("mary"))

    def test_name_parts_mapped_to_same_replacement(self):
        presorted_replacements = \
            ["melba", "peach",   "strawberry", "vanilla"]
        input_names = \
            ["double-barrelled", "double-ended", "ended-up"]
        remapper = NameRemapper(sample_fn=NameRemapperTest.always_same, replacement_word_source=presorted_replacements)

        remapper_for_names = remapper.for_names(input_names)

        self.assertEqual("peach-melba", remapper_for_names.remap_name("double-barrelled"))
        self.assertEqual("peach-strawberry", remapper_for_names.remap_name("double-ended"))
        self.assertEqual("strawberry-vanilla", remapper_for_names.remap_name("ended-up"))


if __name__ == '__main__':
    unittest.main()
