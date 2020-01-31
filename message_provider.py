import utils


class MessageProvider(object):
    def __init__(self):
        self.path_to_messages_file = "messages.txt"
        self.messages_map = {}

    def clean_lines(self, lines):
        result_lines = []
        for line in lines:
            if line[0] == "#":
                pass
            else:
                result_lines.append(line.split("#", maxsplit=1)[0].strip())
        return result_lines

    def parse_messages(self):
        lines_no_comments = self.clean_lines(utils.read_lines(self.path_to_messages_file))
        for line in lines_no_comments:
            parts = line.split("=")
            if len(parts) != 2:
                raise Exception(f"Invalid line in messages.txt: {line}")
            else:
                message_code = parts[0]
                message_text = parts[1]
                self.messages_map[message_code] = message_text

    def get_message_text(self, message_code):
        if len(self.messages_map) == 0:
            raise Exception("Messages map is empty. Have you called parse_messages()?")
        else:
            return self.messages_map.get(message_code)

    def get_formatted_message(self, message_code, **namespace):
        return self.get_message_text(message_code).format(**namespace)
