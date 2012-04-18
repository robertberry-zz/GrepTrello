# Grep Trello

Search through a JSON dump of Trello cards. Trello does not currently offer a
way to search through card contents (description, comments) - only their
titles. If you export a board as a JSON dump, you can use this script to
search through everything.

I do not intend to maintain this script. I needed it to search for something
at work and I thought it might help someone else. If it does, cool. Feel free
to modify it and do whatever you want with it (see the license).

## Usage

    ./grep_trello.py [options] "your search term" <the_dump.json

Options include -i (for case insensitive search) and -r (for Perl-compatible
regular expression search).
