#!/usr/bin/env python

import cli.app
import requests

from . import config


def update_user(user):
    """
    Update a user's RuneTracker profile.

    :param user: The username of the user to update.
    :return: True if the user has been updated.
    """
    response = requests.get(
        config.get('runetracker.org', 'Update'), {'user': user}
    )

    response.raise_for_status()

    if 'CHANGED' == response.text:
        return True
    elif 'NOCHANGE' == response.text:
        return False
    else:
        raise ValueError("Could not update RuneTracker for user: " + user)

class App(cli.app.CommandLineApp):
    def main(self):
        """
        Update a user's RuneTracker profile.
        """
        for user in self.params.users:
            updated = update_user(user)

            if updated: print("User has been updated.") 
            else:       print("User has not changed.")

    def setup(self):
        self.add_param(
            'users',
            default=None, help="the users to update", nargs='+', type=str
        )


if __name__ == "__main__":
    tracker = App()
    tracker.run()
