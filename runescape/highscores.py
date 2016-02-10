#!/usr/bin/env python

import cli.app
import requests

from . import config

"""
:constants:
    - `COMBAT`: Skills belonging to the combat group.
    - `ARTISAN`: Skills belonging to the artisan group.
    - `GATHERING`: Skills belonging to the gathering group.
    - `OTHER`: Skills which do not fall into the other groups.
    - `ALL_SKILLS`: A list of skills in the order which they are given on the
        highscores
"""
COMBAT = [
    'attack', 'strength', 'defence', 'ranged', 'mage', 'constitution',
    'prayer', 'summoning'
]

ARTISAN = [
    'cooking', 'construction', 'crafting', 'firemaking', 'fletching',
    'herblore', 'runecrafting', 'smithing'
]

GATHERING = [
    'divination', 'farming', 'fishing', 'hunter', 'mining', 'woodcutting'
]

OTHER = ['agility', 'dungeoneering', 'slayer', 'thieving']

ALL_SKILLS = [
    'total', 'attack', 'strength', 'defence', 'constitution', 'ranged',
    'prayer', 'magic', 'cooking', 'woodcutting', 'fletching', 'fishing',
    'firemaking', 'crafting', 'smithing', 'mining', 'herblore', 'agility',
    'thieving', 'slayer', 'farming', 'runecrafting', 'hunter',
    'construction', 'summoning', 'dungeoneering', 'divination', 'invention'
]

def get_highscores(username):
    """
    Query highscores for a user.

    :param username: The username for which to search.
    :return: See :meth:`parse_highscore_data`.
    """
    response = requests.get(
        config.get('runescape.com', 'Highscores'), {'player': username}
    )

    response.raise_for_status()

    # Simplify the response data into a list of skills
    return parse_highscore_data(response.text)

def parse_highscore_data(data):
    """
    Parse highscore data for a particular user into a list of triplets,
    representing rank, level, and experience respectively.

    :param data: A CSV to parse.
    :return: A dictionary of skills, each containing three elements: rank, 
        level, and XP::

        {"attack":{"rank":1,"xp":200000000,"level":99}, ...}
    """
    data = data.split()
    data = map(lambda x: x.split(','), data)
    data = list(filter(lambda x: len(x) == 3, data))

    highscores = {}

    headers = ['rank', 'level', 'xp']

    for i, name in enumerate(ALL_SKILLS):
        highscores[name] = dict(zip(headers, data[i]))

    return highscores

class App(cli.app.CommandLineApp):
    """A CommandLineApp to parse RuneScape highscores."""

    def main(self):
        """
        Queries the highscore API for given users and outputs their stats.
        """
        display_skills = self.get_display_skills()
        try:
            # Iterate through each user and print each out
            for user in self.params.users:
                skills = get_highscores(user)
                print("\n- " + user)
                for display_skill in display_skills:
                    skill = skills[display_skill]
                    print(
                        display_skill.ljust(16) + skill['rank'] + \
                            "\t" + skill['level'] + \
                            "\t" + skill['xp']
                    )
        except Exception as e:
            import traceback
            traceback.print_tb(e.__traceback__)


    def get_display_skills(self):
        """
        Retrieve the skills to be displayed based on the given parameters. If
        no skills or skill groups are specified, all skills will be displayed.

        :return: A list of skills to display.
        """
        skills = []

        skills += ARTISAN if self.params.artisan else []
        skills += COMBAT if self.params.combat else []
        skills += GATHERING if self.params.gathering else []
        skills += OTHER if self.params.other else []
        skills += self.params.skills

        if [] == skills:
            skills = ALL_SKILLS

        # Standardise and take uniques from skill list
        return set(map(lambda x: x.lower(), skills))

    def setup(self):
        """
        Initialise the parameter list for this CommandLineApp.
        """
        cli.app.CommandLineApp.setup(self)

        self.add_param(
            '-c', '--combat',
            default=False, help="show combat skills", action='store_true'
        )

        self.add_param(
            '-a', '--artisan',
            default=False, help="show artisan skills", action='store_true'
        )

        self.add_param(
            '-g', '--gathering',
            default=False, help="show gathering skills", action='store_true'
        )

        self.add_param(
            '-o', '--other',
            default=False, help="show other skills", action='store_true'
        )

        self.add_param(
            '-s', '--skills',
            default=[], help="show specific skill(s)", nargs='+'
        )

        self.add_param(
            'users',
            default=None, help="The user(s) to display.", nargs='+', type=str
        )

if __name__ == "__main__":
    highscores = App()
    highscores.run()
