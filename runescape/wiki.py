#!/usr/bin/env python

import cli.app
import wikia


class App(cli.app.CommandLineApp):
    def main(self):
        """
        Search for an article and return a short excerpt.
        """
        topics = wikia.search("Runescape", self.params.title)

        if isinstance(topics, list) and len(topics) > 0:
            article = wikia.page("Runescape", topics[0])

            print("- " + article.title + "\n")

            if self.params.more:
                print(article.content + "\n")
            else:
                print(article.summary + "\n")
            print(article.url)

    def setup(self):
        """
        Initialise the parameter list for this CommandLineApp.
        """
        cli.app.CommandLineApp.setup(self)

        self.add_param(
            'title',
            help="the title of the article to display", type=str
        )

        self.add_param(
            '-m', '--more',
            default=False, help="show more details", action='store_true'
        )

if "__main__" == __name__:
    wiki = App()
    wiki.run()
