from collections.abc import Iterable
from collections import deque
import random
import copy

from .card import Card, Suit, Rank

# Default rank-to-value mapping
DEFAULT_RANK_VALUES = {
	Rank.TWO: 2, Rank.THREE: 3, Rank.FOUR: 4, Rank.FIVE: 5, Rank.SIX: 6,
	Rank.SEVEN: 7, Rank.EIGHT: 8, Rank.NINE: 9, Rank.TEN: 10,
	Rank.JACK: 11, Rank.QUEEN: 12, Rank.KING: 13, Rank.ACE: 14, 
	Rank.JOKER: 15
}

# Default English alphabetical suit order
ENGLISH_ALPH_ORDER = (Suit.CLUBS, Suit.DIAMONDS, Suit.HEARTS, Suit.SPADES, Suit.BLACK, Suit.RED)

# Ranks from A-K
UP_RANKS = [Rank.ACE, Rank.TWO, Rank.THREE, Rank.FOUR, Rank.FIVE, Rank.SIX, 
			Rank.SEVEN, Rank.EIGHT, Rank.NINE, Rank.TEN, Rank.JACK, Rank.QUEEN, Rank.KING]


class Deck:
	'''
	Represents a face-down deck of cards with shared rank/suit rules.

	- The deck is ordered from top-bottom in user-facing access.

		`deck[0]` is top card.

	- Internally the cards are stored bottom-top  
	for O(1) draw operations from the top.

		`self._cards[0]` is bottom card.
	'''

	def __init__(self,
		include_jokers=False,
		rank_values=None,
		suit_order=ENGLISH_ALPH_ORDER,
		shuffle=True,
		empty=False
	):
		'''
		Initialize a new Deck of cards.

		Parameters:
			include_jokers (bool): Include two jokers (red and black) if True. Default False.
			rank_values (dict): Optional mapping of ranks (str) to numeric values. Defaults to standard `2-A + JOKER`.
			suit_order (tuple or None): Ascending order of suits for comparison. None means suits are equal. Default `ENGLISH_ALPH_ORDER`.
			shuffle (bool): If True, the deck is shuffled immediately after creation. Default True.  
				If False, cards remain in "new deck order" `A-K Hearts, A-K Clubs, K-A Diamonds, K-A Spades (bottom)`.
			empty (bool): If True, the deck is not initialized with any cards.
		'''

		# Shared rules for this deck
		self.rank_values = rank_values or DEFAULT_RANK_VALUES
		'''Dictionary mapping Ranks to their scores (int).'''
		self.suit_order = suit_order
		self.include_jokers = include_jokers

		# Map suits to their indices in the ordering
		if self.suit_order is None:
			self._suit_index = {}
		else:
			self._suit_index = {s: i for i, s in enumerate(self.suit_order)}

		# Add cards in new deck order
		self._cards = [] if empty else self._build_cards()
		'''Ordered from bottom [0] to top [-1].'''

		if shuffle:
			self.shuffle()

	def _build_cards(self):
		'''
		Build a standard deck in New Deck Order:  
		`A-K Hearts, A-K Clubs, K-A Diamonds, K-A Spades (bottom)`
		'''
		self._cards = [Card(rank, suit) for suit in [Suit.HEARTS, Suit.CLUBS] for rank in UP_RANKS]
		self._cards += [Card(rank, suit) for suit in [Suit.DIAMONDS, Suit.SPADES] for rank in reversed(UP_RANKS)]
		
		if self.include_jokers:
			self._cards += [Card(Rank.JOKER, Suit.BLACK), Card(Rank.JOKER, Suit.RED)]

	@classmethod
	def from_cards(cls,
		cards,
		include_jokers=False,
		rank_values=None,
		suit_order=ENGLISH_ALPH_ORDER,
		shuffle=False,
		_no_copy=False
	):
		'''
		Create a deck from an existing list of cards.

		Assumes top-bottom (from left to right) order of cards.

		Parameters:
			cards: iterable of card instances
			include_jokers (bool):
			rank_values (dict):
			suit_order (tuple or None):
			shuffle (bool): Whether to shuffle after creation
			_no_copy (bool): INTERNAL FLAG: skip making a reversed copy of the cards list (for performance)
		'''
		deck = cls(empty=True, include_jokers=include_jokers, rank_values=rank_values, suit_order=suit_order)
		# Reference the same list container, assuming caller guarantees safety and internal order 
		# (.append adds to both)
		if _no_copy:
			deck._cards = cards
		else: # Make a fresh list so this deck can modify its container independently
			deck._cards = cards[::-1] # reverse to match internal order (bottom-top)
		if shuffle:
			deck.shuffle()
		return deck
	
	def copy(self, deep=False):
		'''
		Return a new Deck object that copies this one.
		
		Parameters:
			deep (bool): If True, also clones each card object.  
				If False, cards are shared by reference (default).
		'''
		# Always make a new card container (list); optionally make copies of the cards.
		# Deck.from_cards will copy the list(self._cards)
		new_cards = copy.deepcopy(self._cards) if deep else self._cards
		return Deck.from_cards(
			new_cards,
			include_jokers=self.include_jokers,
			rank_values=self.rank_values,
			suit_order=self.suit_order,
			shuffle=False
		)
	
	def __repr__(self):
		if len(self._cards) == 1:
			return f'Deck(1 card)'
		return f'Deck({len(self._cards)} cards)'
	
	def __str__(self):
		return repr(self)
	

	# --- Deck operations ---
	def shuffle(self):
		'''Shuffle deck in place.'''
		random.shuffle(self._cards)

	def reset(self, shuffle=True):
		'''Rebuild deck to its original state.'''
		self._build_cards()
		if shuffle:
			self.shuffle()

	def show(self, start=0, stop=None, step=1):
		'''Print cards in specified range; supports full Python slicing.'''
		cards_to_show = self._cards[::-1][start:stop:step]
		if not cards_to_show:
			print('(empty)')
		else:
			print(', '.join(map(str, cards_to_show)))

	def draw(self, n=1, strict=True):
		'''Draw `n` cards from the top of the deck and remove them.
		
		- If strict and fewer than n cards remain, ValueError is raised.
		- Always returns a list (possibly shorter than n if not strict).
		'''
		if n < 0:
			raise ValueError('cannot draw a negative number of cards')
		if strict and n > len(self._cards):
			raise ValueError('not enough cards left to draw')
		to_draw = min(n, len(self._cards))
		drawn = [self._cards.pop() for _ in range(to_draw)]
		return drawn
	
	def deal(self, num_hands, cards_each, strict=True):
		'''
		Deal cards from the top of the deck into multiple hands.
		
		Parameters:
			num_hands (int): Number of card groups (or players).
			cards_each (int): Number of cards per group.
			strict (bool): If True, raises ValueError if not enough cards remain.
		
		Returns:
			list[list[Card]]: A list of hands, each a list of card objects.
		'''
		if num_hands < 1:
			raise ValueError('num_hands must be at least 1')
		if cards_each < 0:
			raise ValueError('cards_each must be positive')

		total_needed = num_hands * cards_each
		if strict and total_needed > len(self._cards):
			raise ValueError('not enough cards left to deal')
		
		hands = [[] for _ in range(num_hands)]
		for _ in range(cards_each):
			for j in range(num_hands):
				if not self._cards: # ran out of cards
					break
				hands[j].append(self._cards.pop())
		return hands
	
	def split(self, n=2, strict=False):
		'''
		Split the deck into `n` sub-decks as evenly as possible using all cards.
		
		If strict=True, sub-decks will have an equal number of cards  
		(extras on top will be discarded).

		Returns:
			list[Deck]: A list of Decks cut from the bottom of this one (from left-right).
		'''
		if n < 2 or n > len(self._cards):
			raise ValueError('n must be at least 2')
		k = len(self._cards) / n # cards per group (float)
		if strict:
			k = int(k)
		return [
			Deck.from_cards(
				self._cards[round(i*k):round((i+1)*k)], # a slice creates a new list object
				include_jokers=self.include_jokers,
				rank_values=self.rank_values,
				suit_order=self.suit_order,
				shuffle=False,
				_no_copy=True
			) 
		for i in range(n)]
	

	# --- Container magic ---
	def __len__(self):
		return len(self._cards)
	
	def _reverse_slice(self, s: slice, list_len):
		'''Returns a new slice object `t` such that `list[s] == list[::-1][t]`.'''
		indices = s.indices(list_len)
		start = list_len - 1 - indices[0]
		end = list_len - 1 - indices[1]
		if end < 0:
			end = None # -1 cannot mark end
		step = -indices[2]
		return slice(start, end, step)
	
	def _reverse_index(self, index):
		'''Returns the equivalent index for the internal list `self._cards`.'''
		if index < 0: # normalize negatives
			index += len(self._cards)
		return len(self._cards) - 1 - index # 0 <-> len(self._cards) - 1
	
	def __getitem__(self, key):
		if isinstance(key, slice):
			return self._cards[self._reverse_slice(key)]
		
		# Single index
		return self._cards[self._reverse_index(key)]
	
	def __setitem__(self, key, value):
		if not isinstance(value, Card):
			raise TypeError('Deck can only contain Card instances')
		
		if isinstance(key, slice):
			self._cards[self._reverse_slice(key)] = value

		# Single index
		self._cards[self._reverse_index(key)] = value

	def __delitem__(self, key):
		if isinstance(key, slice):
			del self._cards[self._reverse_slice(key)]

		# Single index
		del self._cards[self._reverse_index(key)]
	
	def __iter__(self):
		return reversed(self._cards)

	# --- Container methods ---
	def clear(self):
		'''Remove all cards from deck.'''
		self._cards = []

	def reverse(self):
		'''Reverse the order of the deck.'''
		self._cards.reverse()

	def pop(self, index=0):
		'''Remove and return card at index (default top of deck = 0).'''
		return self._cards.pop(self._reverse_index(index))
	
	def insert(self, index, card):
		'''Insert card before index (top of deck = 0).'''
		if not isinstance(card, Card):
			raise TypeError('Can only insert Card instances')
		# Add plus 1 because the left of elem in cards is the right of elem in cards[::-1]
		self._cards.insert(self._reverse_index(index) + 1, card)

	def add(self, *cards, position='bottom'):
		'''
		Add one or more cards (or groups of cards) to the deck one-by-one.

		- The last card in `*cards` ends up on top if position='top'.
		- Cards in iterables are treated as a single "packed" unit and preserve their internal order.
		
		Parameters:
			*cards: Card instances or iterables of them.
			position (str): 'top', 'bottom', or 'random' insertion.		
		'''
		flat_cards = []
		for item in cards:
			if isinstance(item, Card):
				flat_cards.append(item)
			elif (isinstance(item, Iterable)):
				for c in item:
					if not isinstance(c, Card):
						raise TypeError('All items in iterable must be Card instances')
					flat_cards.append(c)
			else:
				raise TypeError('Only Card instances or iterables of them can be added')
			
		if position == 'bottom':
			self._cards.extend(flat_cards)
			self._cards = flat_cards[::-1] + self._cards
		elif position == 'top':
			self._cards.extend(flat_cards)
		elif position == 'random':
			for c in flat_cards:
				idx = random.randint(0, len(self._cards))
				self._cards.insert(idx, c)
		else:
			raise ValueError("position must be 'top', 'bottom', or 'random'")

	def remove_card(self, card):
		'''
		Remove the first occurrence of a specific card from the deck.
		
		Raises:
			ValueError if the card is not found.
			
		Example:
			`deck.remove_card(StandardCards.ACE_SPADES)`
		'''
		if not isinstance(card, Card):
			raise TypeError('remove_card() requires a Card instance')
		for i in range(len(self._cards) - 1, -1, -1): # iterate backwards (from top-bottom of deck)
			if self._cards[i] == card:
				del self._cards[i]
				return
		# Card DNE in deck
		raise ValueError(f'{card} is not in deck')
	
	def index(self, card, start=0, end=None):
		'''
		Return the first index of a specific card (from top-bottom).

		Raises:
			ValueError if not found.
		'''
		if not isinstance(card, Card):
			raise TypeError('index() requires a Card instance')
		if end is None:
			end = len(self._cards)
		# Convert to reverse orientation
		start = self._reverse_index(start)
		end = self._reverse_index(end)
		for i in range(start, end, -1):
			if self._cards[i] == card:
				return i
		raise ValueError(f'{card} is not in deck')

	def filter(self, predicate):
		'''
		Keep only cards where `predicate(card)` is True.
		
		Example (keep cards with a value above 7):
			`deck.filter(lambda c: deck.value(c) > 7)`
		'''
		self._cards = [c for c in self._cards if predicate(c)]

	def remove(self, predicate):
		'''
		Remove cards matching a condition.
		
		Example (remove all hearts): 
			`deck.remove(lambda c: c.suit == Suit.HEARTS)`
		'''
		self._cards = [c for c in self._cards if not predicate(c)]

	def count(self, target):
		'''
		Return number of cards matching a given condition or specific card.

		Parameters:
			target:
				- Card: occurrences of a specific card.
				- Callable: counts how many cards satisfy the predicate.

		Example:
			`deck.count(StandardCards.ACE_SPADES)`  
			`deck.count(lambda c: c.is_red)`
		'''
		if isinstance(target, Card):
			return self._cards.count(target)
		elif callable(target):
			return sum(1 for c in self._cards if target(c))
		raise TypeError('count() expects a Card or a predicate function')


	# --- Deck arithmetic ---
	def __add__(self, other):
		'''
		Returns a new deck with the same cards/rules as the first deck,  
		followed by the cards of a second deck.

		Cards are referenced (not copied), but the Deck object is new.
		'''
		if not isinstance(other, Deck):
			return NotImplemented
		return Deck.from_cards(
			other._cards + self._cards, # new list created (interal order preserved)
			include_jokers=self.include_jokers,
			rank_values=self.rank_values,
			suit_order=self.suit_order,
			shuffle=False,
			_no_copy=True # safe to reuse container
		)

	def __iadd__(self, other):
		'''Add cards from another deck to the bottom of this one.'''
		if not isinstance(other, Deck):
			return NotImplemented
		self._cards = other._cards + self._cards
		return self
	
	def __sub__(self, other):
		'''
		Return a new deck with certain cards removed.
		
		`other` can be:
			- a single card
			- a Rank
			- a Suit
			- a list of any of the above
			- another Deck
		'''
		if isinstance(other, Card):
			to_remove = {other}
		elif isinstance(other, Deck):
			to_remove = set(other.cards)
		elif isinstance(other, Iterable):
			to_remove = set(other)
		else:
			return NotImplemented

		new_cards = [c for c in self._cards if not (
			c in to_remove or
			c.suit in to_remove or
			c.rank in to_remove
		)]
		return Deck.from_cards(
			new_cards,
			include_jokers=self.include_jokers,
			rank_values=self.rank_values,
			suit_order=self.suit_order,
			shuffle=False,
			_no_copy=True
		)
	
	def __isub__(self, other):
		'''Remove certain cards, suits, or ranks from this deck.'''
		if isinstance(other, Deck):
			to_remove = set(other.cards)
		elif isinstance(other, Iterable):
			to_remove = set(other)
		else:
			to_remove = {other}

		self._cards = [c for c in self._cards if not (
			c in to_remove or
			c.suit in to_remove or
			c.rank in to_remove
		)]
		return self
	
	def __mul__(self, n):
		'''Return a new deck repeated `n` times (cards are referenced, not cloned).'''
		if not isinstance(n, int):
			return NotImplemented
		if n < 1:
			raise ValueError('Deck multiplication requires a positive integer')
		return Deck.from_cards(
			self._cards * n, # produces a new list object
			include_jokers=self.include_jokers,
			rank_values=self.rank_values,
			suit_order=self.suit_order,
			shuffle=False,
			_no_copy=True
		)
	
	def __rmul__(self, n):
		return self.__mul__(n)
	
	def __imul__(self, n):
		'''Repeat this deck's cards `n` times.'''
		if not isinstance(n, int):
			return NotImplemented
		if n < 1:
			raise ValueError('Deck multiplication requires a positive integer')
		self._cards *= n
		return self
	
	def __truediv__(self, n):
		'''
		Loosely split into `n` decks, distributing all cards (uneven allowed)
		
		Equivalent to `deck.split(n, strict=False)`
		'''
		return self.split(n=n, strict=False)
	
	def __floordiv__(self, n):
		'''
		Strictly split into `n` evenly sized decks (discarding extras)
		
		Equivalent to `deck.split(n, strict=True)`
		'''
		return self.split(n=n, strict=True)
	
	def __lshift__(self, n):
		'''Rotate the top `n` cards to the bottom (cut).'''
		n = n % len(self._cards)
		self._cards = self._cards[-n:] + self._cards[:-n]
		return self

	def __rshift__(self, n):
		'''Rotate the bottom `n` cards to the top (reverse cut).'''
		n = n % len(self._cards)
		self._cards = self._cards[n:] + self._cards[:n]
		return self

	# --- Card comparison ---
	def value(self, card):
		'''Get numeric value of card according to deck rules.'''
		return self.rank_values.get(card.rank, 0)
	
	def compare(self, card1, card2):
		'''Compare two cards using deck rules. Returns -1, 0, or 1.'''
		
		# Compare ranks first
		v1 = self.value(card1)
		v2 = self.value(card2)
		if v1 != v2:
			return 1 if v1 > v2 else -1
		
		# If ranks are equal, compare suits
		if self.suit_order is None:
			return 0
		try:
			s1 = self._suit_index[card1.suit]
			s2 = self._suit_index[card2.suit]
		except KeyError: # Suits are incomparable
			return 0

		if s1 < s2:
			return -1
		elif s1 > s2:
			return 1

		# Equal values
		return 0
	
	def _cmp_key(self, card):
		'''Return a tuple key suitable for sorting: (rank_value, suit_index).  
		Unknown suits get -1. If suits are unordered, suit_index is 0.'''
		rank_val = self.value(card)
		suit_index = 0
		if self.suit_order:
			suit_index = self._suit_index.get(card.suit, -1)
		return (rank_val, suit_index)
	
	def sort(self, ascending=False):
		'''Sort deck according to rank/suit order (descending from top-bottom).'''
		# By default, sort makes ascending bottom-top (self._cards)
		# This is equivalent to descending top-bottom
		self._cards.sort(reverse=ascending, key=self._cmp_key)
