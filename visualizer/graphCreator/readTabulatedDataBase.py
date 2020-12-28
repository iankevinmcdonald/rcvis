""" Abstract base class for reading tabulated results """
import abc
import json

from visualizer import common
from . import rcvResult


class TabulatedResultsReaderBase():
    """ Override this and set self.graph and self.rounds and self.items:

        self.graph is a Graph object which is partially initialized (TODO how partially?)
        self.rounds is a list of Round objects
        self.items is a list of Item objects
        """
    graph: object
    rounds: list
    items: list
    eliminationOrder: list
    isJson: bool

    def __init__(self, fileObj):
        fileObj.seek(0)  # reset file position
        if self.isJson:
            data = json.load(fileObj)
        else:
            data = fileObj

        self.parse_data(data)
        self.set_elimination_order(self.rounds, self.items)

    @abc.abstractmethod
    def parse_data(self, data):
        """ Override this to parse the values into whatever data structure you like,
            as long as you set the required fields denoted by the class docstring """

    def get_graph(self):
        """ Returns the Graph object """
        return self.graph

    def get_rounds(self):
        """ Returns the list of rounds """
        return self.rounds

    def set_elimination_order(self, rounds, items):
        """ Sets the elimination order given each round and a list of Items """
        eliminationOrder = []
        itemsRemaining = set(items)
        for rnd in rounds:
            for elimination in rnd.transfers:
                if not isinstance(elimination, rcvResult.Elimination):
                    continue
                eliminationOrder.append(elimination.item)
                itemsRemaining.remove(elimination.item)

        # Winners are added last
        winners = []
        for rnd in rounds:
            for winner in rnd.winners:
                winners.append(winner)
                itemsRemaining.remove(winner)
        winners = reversed(winners)

        # Sort remaining items by the number of votes they received
        itemsRemaining = sorted(itemsRemaining, key=lambda x: self.graph.nodesPerRound[-1][x].count)
        eliminationOrder.extend(itemsRemaining)
        eliminationOrder.extend(winners)

        # Place "residual surplus" and "inactive ballots" at the end
        def move_to_front(candidateName):
            try:
                moveToFrontIndex = [
                    e.name for e in eliminationOrder].index(candidateName)
                if moveToFrontIndex:
                    eliminationOrder.insert(
                        0, eliminationOrder.pop(moveToFrontIndex))
            except ValueError:
                # not every election has these two
                pass

        move_to_front(common.RESIDUAL_SURPLUS_TEXT)
        move_to_front(common.INACTIVE_TEXT)

        self.eliminationOrder = eliminationOrder

    def get_elimination_order(self):
        """ Returns the elimination order:
            a list of names in the order in whhich they were eliminated """
        return self.eliminationOrder
