import random


class RemapperForNames():
    def __init__(self, replacements):
        self.replacements = replacements

    def remap_name(self, name):
        return self.replacements[name]

    def remap_names(self, names):
        for name in names:
            yield self.remap_name(name)


def builtin_random_boolean():
    return random.random() < 0.5


class NameRemapper():
    def __init__(self, random_boolean, replacement_word_source):
        self.random_boolean = random_boolean
        self.replacement_word_source = replacement_word_source

    @staticmethod
    def from_words_file(words_file):
        word_selection = []
        with open(words_file, 'r') as words:
            for word in words:
                if 3 < len(word) < 5:
                    word_selection.append(word)
        return NameRemapper(random_boolean=builtin_random_boolean, replacement_word_source=word_selection)

    def for_names(self, names):
        replacements = self.select_random(names)
        return RemapperForNames(replacements)

    def select_random(self, names):
        replacements = []
        for replacement in self.replacement_word_source:
            if len(replacements) < len(names) and self.random_boolean:
                replacements.append(replacement)
        replacement_map = {}
        for (name, replacement) in zip(names, replacements):
            replacement_map[name] = replacement
        return replacement_map
