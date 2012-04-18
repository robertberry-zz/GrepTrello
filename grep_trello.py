#!/usr/bin/env python

import sys
import json
import re

from optparse import OptionParser

def print_card(card):
    print (u"""%s
=========================
%s
""" % (card.name, card.description or "[No description]")).encode("utf8")

def print_comment(comment):
    print "--"
    print comment["data"]["text"]
    print "--"
    
def get_match_function(expr, options):
    """Given search expression and a list of options (inc. regex,
    case_insensitive), returns a match function for searching with.
    """
    if options.regex:
        re_args = []
        if options.case_insensitive:
            re_args.append(re.IGNORECASE)
        expr = re.compile(expr)
        return lambda s: expr.match(s)
    else:
        if options.case_insensitive:
            expr = expr.lower()
            return lambda s: expr in s.lower()
        else:
            return lambda s: args[0] in s

class Dump(object):
    """Represents a trello dump.
    """
    def __init__(self, json):
        self.json = json

    @property
    def cards(self):
        return (Card(card, self) for card in self.json["cards"])

    def actions_for(self, card):
        return [action for action in self.json["actions"] if \
                    "card" in action["data"] and \
                    action["data"]["card"]["id"] == card.json["id"]]

class Card(object):
    """Represents a Trello card.
    """
    def __init__(self, json, dump):
        self.json = json
        self.dump = dump

    @property
    def name(self):
        return self.json["name"]

    @property
    def description(self):
        return self.json["desc"]

    @property
    def actions(self):
        """All actions associated with card (inc. comments)
        """
        return self.dump.actions_for(self)

    @property
    def comments(self):
        """All comments associated with card.
        """
        return [action for action in self.actions if \
                    action["type"] == "commentCard"]
        
def main():
    parser = OptionParser()
    parser.add_option("-r", "--regex-mode", dest="regex", \
                          help="Search using reg ex instead of string",
                      action="store_true")
    parser.add_option("-i", "--case-insensitive", dest="case_insensitive", \
                          help="Perform a case insensitive search",
                      action="store_true")
    (options, args) = parser.parse_args()

    if len(args) != 1:
        parser.error("You must supply a search %s." % \
                         ("regex" if options.regex else "string"))

    matches = get_match_function(args[0], options)
        
    dump = Dump(json.load(sys.stdin))

    for card in dump.cards:
        matched_comments = [comment for comment in card.comments if \
                        matches(comment["data"]["text"])]
        
        if matched_comments or matches(card.name) or matches(card.description):
            print_card(card)
            for comment in matched_comments:
                print_comment(comment)

if __name__ == "__main__": main()
