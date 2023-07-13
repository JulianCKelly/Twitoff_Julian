# Twitoff Application Documentation

"""
This documentation provides an overview of the Twitoff application and its main functionalities.
"""

from os import getenv
from flask import Flask, render_template, request
from .predict import predict_user
from .models import DB, User
from .twitter import add_or_update_user, update_all_users


def create_app():
    """
    The main app function for twitoff.
    Brings everything together.
    """
    # __name__ is the name of the current path module
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URI")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    DB.init_app(app)

    @app.route('/')
    def root():
        """
        This route displays the home page of the application, showing a base template with a list of all users stored in the database.

        HTTP Method: GET

        Returns:
        - `base.html`: The base template with the list of users
        """
        return render_template('base.html', title="Home", users=User.query.all())

    @app.route('/update')
    def update():
        """
        This route triggers the update of all users in the database. It calls the `update_all_users()` function to fetch the latest data from Twitter and updates the database accordingly.

        HTTP Method: GET

        Returns:
        - None
        """
        usernames = update_all_users()
        for username in usernames:
            add_or_update_user(username)

    @app.route('/reset')
    def reset():
        """
        This route resets the database by dropping all tables and recreating them. It is used for database maintenance or to start with a clean slate.

        HTTP Method: GET

        Returns:
        - `base.html`: The base template indicating that the database has been reset
        """
        DB.drop_all()
        DB.create_all()
        return render_template("base.html", title="Reset Database")

    @app.route('/user', methods=["POST"])
    @app.route('/user/<name>', methods=["GET"])
    def user(name=None, message=''):
        """
        These routes handle user-related functionality, including adding or updating a user and retrieving user information.

        HTTP Method: POST (for adding/updating a user), GET (for retrieving user information)

        Parameters:
        - `name` (optional): The username of the user to retrieve or add/update

        Returns:
        - `user.html`: The user template with user-specific information, including their tweets and a message indicating the success or failure of the operation
        """
        name = name or request.values['user_name']
        try:
            if request.method == 'POST':
                add_or_update_user(name)
                message = "User {} Successfully added!".format(name)

            tweets = User.query.filter(User.username == name).one().tweets

        except Exception as e:
            message = "Error adding {}: {}".format(name, e)
            tweets = []

        return render_template("user.html", title=name, tweets=tweets, message=message)

    @app.route('/compare', methods=["POST"])
    def compare():
        """
        This route handles the comparison of two users based on a provided tweet. It calls the `predict_user()` function to predict which user is more likely to have authored the tweet.

        HTTP Method: POST

        Returns:
        - `prediction.html`: The prediction template displaying the prediction message indicating the more likely author of the tweet
        """
        user0, user1 = sorted([request.values['user0'], request.values["user1"]])

        if user0 == user1:
            message = "Cannot compare users to themselves!"
        else:
            prediction = predict_user(user0, user1, request.values["tweet_text"])
            message = "'{}' is more likely to be said by {} than {}!".format(
                request.values["tweet_text"],
                user1 if prediction else user0,
                user0 if prediction else user1
            )

        return render_template('prediction.html', title="Prediction", message=message)

    return app
