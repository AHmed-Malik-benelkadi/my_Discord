class Message:
    def __init__(self, id, channel_id, user_id, content, timestamp):
        self.id = id
        self.channel_id = channel_id
        self.user_id = user_id
        self.content = content
        self.timestamp = timestamp
