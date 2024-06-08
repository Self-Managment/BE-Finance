import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "finance.settings")
django.setup()

from broker.redis.consumers.user_consumer import UserConsumer


if __name__ == "__main__":
    user_consumer = UserConsumer()
    user_consumer.listen()
