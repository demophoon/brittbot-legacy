#!/usr/bin/env python
# encoding: utf-8

import random
# import re

from modules.brittbot.filters import smart_ignore

room = '##brittslittlesliceofheaven'

games = {}


class CoupException:

    def __init__(self, error):
        self.error = error

    def __str__(self):
        return self.error


class CoupCard:

    def __init__(self, role, action, reaction=None):
        self.role = role
        self.action = action
        self.reaction = reaction
        if not self.action:
            self.action = lambda **kw: None
        if not self.reaction:
            self.reaction = lambda **kw: None
        self.revealed = False

    def __eq__(self, b):
        return self.role == b

    def __repr__(self):
        return "{} card".format(self.role)


class DukeCard(CoupCard):

    def __init__(self):
        CoupCard.__init__(self, 'duke', self.action, self.reaction)

    @classmethod
    def action(self, **kwargs):
        kwargs['world'].current_player.coins += 3

    @classmethod
    def reaction(self, **kwargs):
        if kwargs['world'].last_player.last_action == 'aid':
            kwargs['world'].last_player.coins -= 2


class CaptainCard(CoupCard):

    def __init__(self):
        CoupCard.__init__(self, 'captain', self.action, self.reaction)

    @classmethod
    def action(self, **kwargs):
        kwargs['world'].current_player.coins += 2
        kwargs['target'].coins -= 2

    @classmethod
    def reaction(self, **kwargs):
        if kwargs['world'].last_player.last_action == 'captain':
            kwargs['world'].last_player -= 2
            kwargs['world'].last_player.last_target += 2


class CoupGame:

    card_types2 = [DukeCard, 'assassin', 'contessa', 'captain', 'ambassador']
    card_types = [DukeCard, CaptainCard]

    def __init__(self):
        self.players = []
        self.cards = []
        self.current_player = None
        self.last_player = None
        self.started = False
        self.phase = None
        self._player_index = 0

    def __contains__(self, item):
        return item in [x.name for x in self.players]

    def __repr__(self):
        return ', '.join(str(x) for x in self.players)

    def _generate_coup_cards(self):
        for card in self.card_types:
            for _ in range(3):
                self.cards.append(card())

    def join(self, name):
        if name not in self.players:
            self.players.append(CoupPlayer(self, name))

    def part(self, name):
        self.players = [x for x in self.players if x.name != name]

    def start(self):
        self.started = True
        self.current_player = self.players[self._player_index]
        self._generate_coup_cards()
        random.shuffle(self.cards)
        for player in self.players:
            for _ in range(2):
                player.cards.append(self.cards.pop())
            player.coins = 2


class CoupPlayer:

    def __init__(self, world, name):
        self.world = world
        self.name = name
        self.cards = []
        self.coins = 0
        self.msg = lambda msg: None
        self.last_action = None
        self.last_target = None

    def __repr__(self):
        return "Player {} with {} coins".format(self.name, self.coins)

    def income(self, **kwargs):
        self.coins += 1
        self.last_action = 'income'
        self.last_target = None

    def aid(self, **kwargs):
        self.coins += 2
        self.last_action = 'aid'
        self.last_target = None

    def reveal(self, card):
        cards = filter(lambda item: item == card, self.cards)
        if not cards:
            raise CoupException("Player does not have {}.".format(card))
        cards[0].revealed = True

    def action(self, role, target=None):
        actions = {
            'income': self.income,
            'aid': self.aid,
            'duke': DukeCard.action,
            'captain': CaptainCard.action,
        }
        action = actions.get(role)
        if not action:
            raise CoupException("Role {} does not exist.".format(role))
        if target:
            target = filter(lambda x: target == x.name, self.world.players)[0]
        action(world=self.world, target=target)
        print "{} took action {}".format(self, role)
        self.world._player_index += 1
        self.world._player_index %= len(self.world.players)
        self.world.last_player = self.world.current_player
        self.world.current_player = self.world.players[self.world._player_index]


@smart_ignore
def play_coup(jenni, msg):
    global games
    room = msg.sender
    if games.get(room):
        jenni.reply("A game of coup has started, say `!coup help` for help.")
        return
    games[room] = CoupGame()
play_coup.rule = r'!play coup$'
