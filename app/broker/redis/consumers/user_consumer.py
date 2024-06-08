import json

import redis
from broker.commands import Commands

from users.models import User

class UserConsumer:
    channel = "users"

    def __init__(self):
        self.redis_client = redis.Redis(host='redis', port=6379, db=0)

    def listen(self):
        print("UserConsumer listen start")
        pubsub = self.redis_client.pubsub()
        pubsub.subscribe(self.channel)
        for message in pubsub.listen():
            if message['type'] == 'message':
                data = json.loads(message['data'].decode('utf-8'))
                command = data.get("command")
                
                if command is None:
                    continue
                
                elif command == Commands.create_user:
                    create_user(data.get("data"))
                
                
def create_user(data: dict):
    user = User(**data)
    user.save()
