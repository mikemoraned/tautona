from nameremapper import NameRemapper
import unittest


class NameRemapperTest(unittest.TestCase):
    @staticmethod
    def always_true():
        return True

    def test_remaps_single_word(self):
        replacements = ["peach", "melba"]
        remapper = NameRemapper(random_boolean=NameRemapperTest.always_true, replacement_word_source=replacements)
        input_names = ["mary"]
        remapper_for_names = remapper.for_names(input_names)

        remapped = remapper_for_names.remap_name("mary")

        self.assertEqual("peach", remapped)


if __name__ == '__main__':
    unittest.main()
