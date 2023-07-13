"""
This documentation provides an overview of the Twitoff application and its main functionalities.
"""

from .app import create_app

APP = create_app()

"""
The `APP` variable represents the Twitoff application instance created by the `create_app()` function.

Usage:
- `APP.run()`: Runs the Twitoff application.

Please refer to the documentation of the `create_app()` function for more details on the application structure and functionality.
"""
