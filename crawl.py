class Crawler():
    def __init__(self, slack):
        self.slack = slack
        self.min_messages = 100
        self.max_messages = 1000
        self.channel_limit = 1000

    def channel_message_sample(self, channel_id, max_messages):
        history = self.slack.channels.history(channel_id, count=self.max_messages)
        messages = history.body["messages"]
        return [m for m in messages if m["type"] == "message" and "subtype" not in m]

    def crawl(self, texts):

        response = self.slack.channels.list()

        for channel in response.body["channels"][:self.channel_limit]:
            name = channel["name"]
            if channel["is_archived"]:
                print("Ignoring %s (archived)" % name)
            else:
                text_messages = self.channel_message_sample(channel["id"], self.max_messages)

                if len(text_messages) >= self.min_messages:
                    print("Found {0} messages in {1}".format(len(text_messages), name))
                    texts.add_messages_for_channel(name, text_messages)
                else:
                    print("Ignoring {0} (not enough text messages, {1})".format(name, len(text_messages)))
