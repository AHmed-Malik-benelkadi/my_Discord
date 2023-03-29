class Channel:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.messages = []

    def add_message(self, message):
        self.messages.append(message)
