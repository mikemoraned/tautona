import random
import re


class RemapperForNames():
    def __init__(self, replacements):
        self.replacements = replacements

    def remap_name(self, name):
        remapped = []
        for part in re.split('(\W+)', name):
            if part in self.replacements:
                remapped.append(self.replacements[part])
            else:
                remapped.append(part)
        return "".join(remapped)

    def remap_names(self, names):
        for name in names:
            yield self.remap_name(name)

    @classmethod
    def words_in_names(cls, names):
        unique_words = set()
        for name in names:
            unique_words |= cls.words_in_name(name)
        return list(unique_words)

    @classmethod
    def words_in_name(cls, name):
        return set(re.split('\W+', name))


class NotEnoughReplacementWordsInSource(Exception):
    def __init__(self, needed, actual):
        self.actual = actual
        self.needed = needed

    def __str__(self):
        return "needed: {}, actual: {}".format(self.needed, self.actual)


def builtin_sample(population, sample_size):
    return random.sample(population, sample_size)


class NameRemapper():
    def __init__(self, sample_fn, replacement_word_source):
        self.sample_fn = sample_fn
        self.replacement_word_source = replacement_word_source

    @classmethod
    def normalise(cls, word):
        return word.lower().rstrip()

    @classmethod
    def from_words_file(cls, words_file):
        word_selection = []
        with open(words_file, 'r') as words:
            for word in words.readlines():
                normalised = cls.normalise(word)
                if 5 <= len(normalised) <= 6:
                    word_selection.append(normalised)
        return NameRemapper(sample_fn=builtin_sample,
                            replacement_word_source=word_selection)

    def for_names(self, names):
        words = RemapperForNames.words_in_names(names)
        replacements = self.select_random(words)
        return RemapperForNames(replacements)

    def select_random(self, names):
        amount_required = len(names)

        replacements = self.sample_fn(self.replacement_word_source,
                                      amount_required)

        if len(replacements) < amount_required:
            raise NotEnoughReplacementWordsInSource(amount_required,
                                                    len(replacements))

        replacements = sorted(replacements)
        names = sorted(names)

        replacement_map = {}
        for (name, replacement) in zip(names, replacements):
            replacement_map[name] = replacement
        return replacement_map
