from os import getenv
from typing import Dict
import requests
from dotenv import load_dotenv

load_dotenv()
URL = getenv("NOT_TWITTER_URL")


class Tweet:
    """
    The `Tweet` class represents a tweet from the Not Twitter API.

    Attributes:
    - `full_text`: The full text of the tweet.

    Methods:
    - `__repr__()`: Returns a string representation of the tweet object.
    - `__str__()`: Returns the full text of the tweet.

    Example Usage:
    ```python
    tweet = Tweet({"full_text": "This is a tweet"})
    print(tweet)  # Output: "This is a tweet"
    ```
    """
    def __init__(self, data: Dict):
        self.full_text = ""
        self.__dict__.update(data)

    def __repr__(self):
        return "\n".join(f"{k}: {v}" for k, v in vars(self).items())

    def __str__(self):
        return self.full_text


class User:
    """
    The `User` class represents a user from the Not Twitter API.

    Attributes:
    - `screen_name`: The screen name of the user.

    Methods:
    - `timeline(*args, **kwargs)`: Retrieves the timeline of the user.

    Example Usage:
    ```python
    user = User({"screen_name": "username"})
    tweets = user.timeline()
    for tweet in tweets:
        print(tweet)
    ```
    """
    def __init__(self, data: Dict):
        self.screen_name = data.get('screen_name')
        user_data = requests.get(f"{URL}/user/{self.screen_name}",
                                 timeout=5).json()
        self.__dict__.update(user_data)

    def timeline(self, *args, **kwargs):
        return [
            Tweet(tweet)
            for tweet in requests.get(f"{URL}/read/{self.screen_name}",
                                      timeout=5).json()
        ]

    def __repr__(self):
        return "\n".join(f"{k}: {v}" for k, v in vars(self).items())

    def __str__(self):
        return self.screen_name