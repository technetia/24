#! /usr/bin/env python
# 24.py
#
# A module for having a computer play the card game '24'.
#
# Written for Python 2.6, 2.7
# For conversion to 3.x:
# - change the raw_input() in main() to input()
# - remove the __future__ import (optional)
#
# How to play 24:
# - There are two players, plus a judge.
# - Four cards are randomly drawn from a deck and placed on a table.
# - Each player tries to figure out, as quickly as possible, a way to create
# the value 24 using the cards' values (A = 1, face cards = 10) and the four
# basic arithmetic operations (+, -, *, /), without regard to order of
# operations. The first person to come up with a solution wins the round.
# - If it is impossible to create the value 24, the first player to say so
# will have their claim verified by the judge.
# - Repeat as desired.
#
# For example:
# - 2 K 8 8 are the cards drawn. One possible solution is:
# 8 + 8 + K - 2 (since K is worth 10)
# - A 2 3 4 are the cards drawn. One possible solution is:
# 4 * 3 * 2 * A (24 = 4!)
# - A A A A are the cards drawn. This is impossible to solve.
#
#
# An obvious generalization of this game is to consider an arbitrary target
# value (as opposed to 24) and to consider an arbitrary number of playing cards
# (as opposed to 4). The functions provided in this module provide support
# for such generalizations.

from __future__ import print_function

import itertools
OPERATOR_MAPPING = {
    "+" : int.__add__,
    "-" : int.__sub__,
    "*" : int.__mul__,
    "/" : int.__div__,
}

class Card(object):
    """
    A simple representation of a single playing card.
    """
    __slots__ = ("rank", "suit", "value")

    # {rank : value}
    RANKS = {
        "A" : 1,
        "2" : 2,
        "3" : 3,
        "4" : 4,
        "5" : 5,
        "6" : 6,
        "7" : 7,
        "8" : 8,
        "9" : 9,
        "10" : 10,
        "J" : 10,
        "Q" : 10,
        "K" : 10,
    }
    SUITS = (
        "h",
        "c",
        "d",
        "s",
    )
    
    def __init__(self, rank, suit):
        if rank not in Card.RANKS:
            raise ValueError("{0} is not a valid rank".format(rank))
        if suit not in Card.SUITS:
            raise ValueError("{0} is not a valid suit".format(suit))
        self.rank = rank
        self.suit = suit
        self.value = Card.RANKS[rank]

    def __repr__(self):
        return "Card('{0}', '{1}')".format(self.rank, self.suit)

    def __str__(self):
        return "{0}{1}".format(self.rank, self.suit)
    
    def __hash__(self):
        return hash(str(self))
    
    def __eq__(self, other):
        return self.rank == other.rank and self.suit == other.suit

    def __ne__(self, other):
        return self.rank != other.rank or self.suit != other.suit


def get_value(cards, operators):
    """
    Computes the value the given cards generate with the given operators.

    Note that the order of the operators specified is important, as the
    operations on the cards are done in the order they are given.
    """
    assert len(cards) == len(operators)+1, "expected {0} operators for {1} cards".format(len(cards)-1, len(cards))

    value = cards[0].value
    for i, c in enumerate(cards[1:]):
        # do not permit non-integer division, as per the rules of the game
        if operators[i] == "/" and value % c.value != 0:
            raise ValueError("non-integer division committed")

        # apply next operator to total value
        op_func = OPERATOR_MAPPING[operators[i]]
        value = op_func(value, c.value)
    return value

def get_possible_ops(cards, target_value):
    """
    Returns a list of the operator permutations that yield exactly
    the target value for the given cards, IN THE GIVEN ORDER.

    An empty list will be returned if there are no permutations.
    """
    possibilities = []
    for op_list in itertools.combinations_with_replacement(OPERATOR_MAPPING, len(cards)-1):
        try:
            value = get_value(cards, op_list)
        except(ValueError):
            # non-integer division committed, ignore
            pass
        else:
            if value == target_value:
                possibilities.append(op_list)
        
    return possibilities

def solve(cards, target_value):
    """
    Returns a set of all possible solutions to the general game with the
    given cards and target value.
    
    Solutions with cards of identical rank are counted together
    (despite differing suits).
    """
    solutions = set()
    for card_list in itertools.permutations(cards):
        for op_list in get_possible_ops(card_list, target_value):
            # create a string representating the solution
            s = []
            for i, op in enumerate(op_list):
                s.append(card_list[i].rank)
                s.append(op)
            s.append(card_list[-1].rank)
            
            solutions.add(" ".join(s))
            
    return solutions


def main():
    """
    Quick test run of the functions: a solution finder.
    """
    import random
    print("--- 24 solution finder ---\n")
    print("Enter each card's rank.")
    print("For example: A, 2, 3, 4")

    cards = []
    while len(cards) < 4:
        c = raw_input("Card: ")
        try:
            cards.append(Card(c, random.choice(Card.SUITS)))
        except(ValueError):
            print("Invalid rank. Try again.")

    print()
    solutions = solve(cards, 24)
    if len(solutions) == 0:
        print("Impossible to make 24.")
    else:
        for i, s in enumerate(solutions):
            print("Solution {0}: {1}".format(i+1, s))
            

if __name__ == "__main__":
    main()
