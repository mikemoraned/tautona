from channeltexts import ChannelTexts
import unittest


class ChannelTextsTest(unittest.TestCase):
    def test_tokenises_message_by_space(self):
        texts = ChannelTexts()
        message = {
            "text": "some text  with\nspaces"
        }
        texts.add_messages_for_channel("channel_name", [message])
        self.assertEqual([["some", "text", "with", "spaces"]], texts.texts_only())

    def test_ignores_special_words(self):
        texts = ChannelTexts()
        message = {
            "text": "some text with <stuff>"
        }
        texts.add_messages_for_channel("channel_name", [message])
        self.assertEqual([["some", "text", "with"]], texts.texts_only())

    def test_ignores_stop_words(self):
        texts = ChannelTexts()
        message = {
            "text": "some text with a stop word"
        }
        texts.add_messages_for_channel("channel_name", [message])
        self.assertEqual([["some", "text", "with", "stop", "word"]], texts.texts_only())

    def test_ignores_short_words(self):
        texts = ChannelTexts()
        message = {
            "text": "a bb ccc dddd eeeee ffffff"
        }
        texts.add_messages_for_channel("channel_name", [message])
        self.assertEqual([["dddd", "eeeee", "ffffff"]], texts.texts_only())


if __name__ == '__main__':
    unittest.main()
