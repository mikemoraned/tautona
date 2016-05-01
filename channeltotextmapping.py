import json

class ChannelToTextMapping():
    def __init__(self, channel_to_text_id = {}, text_id_to_channel = {}):
        self.channel_to_text_id = channel_to_text_id
        self.text_id_to_channel = text_id_to_channel

    def contains_channel(self, name):
        return name in self.channel_to_text_id

    def increment_channels(self, name):
        id = len(self.channel_to_text_id)
        self.channel_to_text_id[name] = id
        self.text_id_to_channel[id] = name

    def items(self):
        return self.channel_to_text_id.items()

    def channel_name_for_id(self, id):
        return self.text_id_to_channel[id]

    def text_id_for_name(self, name):
        return self.channel_to_text_id[name]

    def save(self, outfile_name):
        with open(outfile_name, 'w') as outfile:
            json.dump(self.channel_to_text_id, outfile, sort_keys=True, indent=4, separators=(',', ': '))

    @classmethod
    def load(cls, infile_name):
        text_id_to_channel = []
        with open(infile_name, 'r') as infile:
            channel_to_text_id = json.load(infile)

        for (channel, text_id) in channel_to_text_id.items():
            text_id_to_channel.append("")
        for (channel, text_id) in channel_to_text_id.items():
            text_id_to_channel[text_id] = channel

        return ChannelToTextMapping(channel_to_text_id, text_id_to_channel)