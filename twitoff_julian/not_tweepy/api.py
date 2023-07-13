from not_tweepy.user import User


class API:

    """
        The `API` class represents the Not Tweepy API.

        Methods:
        - `get_user(screen_name: str)`: Retrieves a user from the Not Twitter API based on the screen name.

        Example Usage:
        ```python
        api = API()
        user = api.get_user('screen_name')
        ```
        """

    def __init__(self, *args, **kwargs):
        pass

    def get_user(self, screen_name: str):
        return User({"screen_name": screen_name})
