import re

from channeltotextmapping import ChannelToTextMapping


class AlreadySeenChannel(Exception):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return "Already seen channel " + self.name


class ChannelTexts():
    SPECIAL = re.compile("<.+?>")
    STOPLIST = set('for a of the and to in'.split())

    def __init__(self, channel_to_text_mapping=None, texts=None):
        if channel_to_text_mapping is None:
            channel_to_text_mapping = ChannelToTextMapping()
        self.channel_to_text_mapping = channel_to_text_mapping

        if texts is None:
            texts = []
        self.texts = texts

    def add_messages_for_channel(self, name, text_messages):
        if self.channel_to_text_mapping.contains_channel(name):
            raise AlreadySeenChannel(name)

        self.channel_to_text_mapping.increment_channels(name)

        self.texts.append(self.messages_to_text(text_messages))

    def texts_only(self):
        return self.texts

    def messages_to_text(self, messages):
        text = list()
        for m in messages:
            for word in m["text"].lower().split():
                if word not in self.STOPLIST and not self.SPECIAL.match(word) and len(word) >= 4:
                    text.append(word)
        return text

    def save(self, mapping_outfile_name, texts_outfile_name):
        self.channel_to_text_mapping.save(mapping_outfile_name)
        with open(texts_outfile_name, 'w') as texts_outfile:
            for text in self.texts:
                texts_outfile.write(" ".join(text))
                texts_outfile.write("\n")

    @classmethod
    def load(cls, mapping_infile_name, texts_infile_name):
        channel_to_text_mapping = ChannelToTextMapping.load(mapping_infile_name)
        texts = []
        with open(texts_infile_name, 'r') as texts_infile:
            for line in texts_infile.readlines():
                texts.append(line.split())
        return ChannelTexts(channel_to_text_mapping, texts)
