# RuneScape Toolkit

Command line utilities for [RuneScape](https://runescape.com).

## Installation

Ensure that both Python and Pip have been installed, then run:

```
$ git clone https://github.com/connordavison/rs-tools.git
$ cd rs-tools
$ pip install -e .
```

## Usage

After installation, the `rs` script should be available from the terminal:

```
$ rs -h
usage: main [-h] command

positional arguments:
  command     the command to execute, one of [adv|item|item-
              dump|news|track|user|wiki].

optional arguments:
  -h, --help  show this help message and exit
```

To obtain more information about the usage of a particular module, run `rs module-alias -h`. A brief description of each of the available modules follows:

| Module | Aliases | Description |
| --- | --- | --- |
| Adventurer's Log | `adv`, `alog`, `log` | Fetch a user's recent activity. |
| Price History | `ge`, `item` | Fetch a JSON representation of the recent price history of an item by its item ID. |
| Item ID Dump | `dump`, `item-dump`, `generate-id-list` | Generate a JSON dump of the entire list of tradeable items from RuneScape's Grand Exchange database. This command may run for a very long time. |
| News | `news` | Display the latest headlines on RuneScape news. |
| RuneTracker Updater | `track` | Update a RuneTracker profile. This is best used with a cronjob. |
| Highscores | `highscore`, `highscores`, `hs`, `user` | Obtain the most recent stats for a user. |
| Wiki | `wiki`, `wikia` | Read the introduction to a Wikia topic. Wikia's search feature is used, so input need not be precise: `rs wiki "abyssal wip"` would yield the [Abyssal Whip](http://runescape.wikia.com/wiki/Abyssal_whip) article. |
