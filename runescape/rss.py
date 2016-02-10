#!/usr/bin/env python

import cli.app
import feedparser

from . import config


class App(cli.app.CommandLineApp):
    """
    An RSS printer application.
    """

    def main(self):
        """
        Retrieve the most recent news posts from an RSS feed, and output the
        result.
        """
        if self.params.number < 1:
            raise ValueError(
                "Number of items to output should be more than zero."
            )

        rss = self.get_rss()

        rss.entries.reverse()

        for i in range(0, min(self.params.number, len(rss.entries))):
            self.print_entry(rss.entries[i])

    def setup(self):
        """
        Initialise the parameter list for this CommandLineApp.
        """
        cli.app.CommandLineApp.setup(self)

        self.add_param(
            '-n', '--number',
            default=3, help="specify number of posts to show", type=int
        )

        self.add_param(
            '-m', '--more',
            default=False, help="show entry summaries", action='store_true'
        )

    def get_rss(self):
        """
        Obtain the RSS data for this printer.
        """
        url = input("Enter RSS feed URL: ")

        return feedparser.parse(url)

    def print_entry(self, entry):
        """
        Print an entry to stdout.

        :param entry: An RSS dictionary as per :meth:`feedparser.parse`.
        """
        print(entry['published'] + " -- " + entry['title'])

        if self.params.more:
            print("\t" + entry['summary'])

class NewsApp(App):
    def get_rss(self):
        """
        Obtain the RSS data for this printer.
        """
        return feedparser.parse(config.get('runescape.com', 'News'))

    def print_entry(self, entry):
        App.print_entry(self, entry)

        print("\t" + entry['link'])

class AdventurersLogApp(App):
    def get_rss(self):
        """
        Obtain the RSS data for this printer.
        """
        url = config.get('runescape.com', 'AdventurersLog') \
            + "?searchName=" + self.params.user

        return feedparser.parse(url)

    def setup(self):
        App.setup(self)
        self.add_param('user', help="the user to lookup")

if __name__ == "__main__":
    rss = App()
    rss.run()
