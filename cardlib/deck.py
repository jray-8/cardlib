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
	Represents a face-down deck of cards.

	- `deck[0]` = top card
	- Internally: deque with left = top, right = bottom
	- O(1) draw, and add to top/bottom
	'''

	def __init__(self,
		*,
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
				If False, cards remain in "New Deck Order" `A-K Hearts, Clubs, K-A Diamonds, Spades (bottom)`.
			empty (bool): If True, the deck is not initialized with any cards.
		'''

		# Shared rules for this deck
		self.rank_values = rank_values or DEFAULT_RANK_VALUES
		'''Dictionary mapping Ranks to their scores (int).'''
		self.suit_order = suit_order
		'''Ascending order of Suits or None.'''
		self.include_jokers = include_jokers

		# Fast access to suit order values
		self._suit_index = {s: i for i, s in enumerate(self.suit_order)} if self.suit_order else {}
		'''Map suits to their indices in the ordering.'''

		# Add cards in new deck order
		self._cards = deque() if empty else self._build_cards()
		'''Ordered from bottom [0] to top [-1].'''

		if shuffle:
			self.shuffle()

	def _build_cards(self):
		'''
		Returns a deque in New Deck Order:

		`Hearts (A-K), Clubs (A-K), Diamonds (K-A), Spades (K-A), (bottom)`
		'''
		cards = deque()
		# Hearts & Clubs: A-K
		for suit in (Suit.HEARTS, Suit.CLUBS):
			for rank in UP_RANKS:
				cards.append(Card(rank, suit))
		# Diamonds & Spades: K-A
		for suit in (Suit.DIAMONDS, Suit.SPADES):
			for rank in reversed(UP_RANKS):
				cards.append(Card(rank, suit))
		if self.include_jokers:
			cards.append(Card(Rank.JOKER, Suit.BLACK))
			cards.append(Card(Rank.JOKER, Suit.RED))
		return cards

	@classmethod
	def from_cards(cls,
		cards,
		*,
		include_jokers=False,
		rank_values=None,
		suit_order=ENGLISH_ALPH_ORDER,
		shuffle=False,
		_no_copy=False
	):
		'''
		Create a deck from an existing list of cards.

		Assumes top-bottom (left to right) order of cards.

		Parameters:
			cards: iterable of card instances (top-bottom)
			include_jokers (bool):
			rank_values (dict):
			suit_order (tuple or None):
			shuffle (bool): Whether to shuffle after creation
			_no_copy (bool): INTERNAL FLAG: skip making a copy of the deque container (for performance)
		'''
		deck = cls(empty=True, include_jokers=include_jokers, 
				rank_values=rank_values, suit_order=suit_order)
		# Reference the same deque object, assuming caller guarantees safety
		if _no_copy:
			deck._cards = cards
		else:
			deck._cards.extend(cards)
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
		# Always make a new card container (deque); optionally make copies of the cards.
		new_cards = copy.deepcopy(self._cards) if deep else deque(self._cards)
		deck = Deck(empty=True, include_jokers=self.include_jokers,
					rank_values=self.rank_values, suit_order=self.suit_order)
		deck._cards = new_cards
		return deck
	
	def __repr__(self):
		return f"Deck({len(self._cards)} card{'s' if len(self._cards) != 1 else ''})"
	
	def __str__(self):
		return repr(self)
	

	# --- Deck operations ---
	def shuffle(self):
		'''Shuffle deck in place.'''
		cards = list(self._cards) # temp list
		random.shuffle(cards)
		self._cards = deque(cards)

	def reset(self, shuffle=True):
		'''Rebuild deck to its original state.'''
		self._cards = self._build_cards()
		if shuffle:
			self.shuffle()

	def show(self, start=0, stop=None, step=1):
		'''Print cards in specified range; supports full Python slicing.'''
		cards_to_show = list(self._cards)[start:stop:step]
		print(', '.join(map(str, cards_to_show)) or '(empty)')

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
		return [self._cards.popleft() for _ in range(to_draw)]
	
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
		if num_hands < 0 or cards_each < 0:
			raise ValueError('deal parameters cannot be negative')

		total = num_hands * cards_each
		if strict and total > len(self._cards):
			raise ValueError('not enough cards left to deal')
		
		hands = [[] for _ in range(num_hands)]
		for _ in range(cards_each):
			for hand in hands:
				if not self._cards: # ran out of cards
					break
				hand.append(self._cards.popleft())
		return hands
	
	def split(self, n=2, strict=False):
		'''
		Split the deck into `n` sub-decks as evenly as possible using all cards.
		
		If strict=True, sub-decks will have an equal number of cards  
		(extras on bottom will be discarded).

		Returns:
			list[Deck]: A list of Decks cut from the top of this one (left-right).
		'''
		if n < 2:
			raise ValueError('n must be >= 2')
		if n > len(self._cards):
			raise ValueError('n cannot exceed deck size')
		
		total = len(self._cards)
		k = total // n # cards per group
		remainder = total % n # r groups will get 1 extra card

		result = []
		temp = deque(self._cards)

		for i in range(n):
			chunk_size = k if strict else k + (1 if i < remainder else 0)
			cards = deque(temp.popleft() for _ in range(chunk_size))
			result.append(Deck.from_cards(cards,
					include_jokers=self.include_jokers, 
					rank_values=self.rank_values,
					suit_order=self.suit_order,
					_no_copy=True
			))
		return result
	

	# --- Container magic ---
	def __len__(self):
		return len(self._cards)
	
	def __getitem__(self, i):
		if isinstance(i, slice):
			return list(self._cards)[i]
		return self._cards[i]
	
	def __setitem__(self, i, card):
		if not isinstance(card, Card):
			raise TypeError('Deck can only contain Card instances')
		temp = list(self._cards)
		temp[i] = card
		self._cards = deque(temp)

	def __delitem__(self, i):
		temp = list(self._cards)
		del temp[i]
		self._cards = deque(temp)
	
	def __iter__(self):
		return iter(self._cards) # top to bottom

	# --- Container methods ---
	def clear(self):
		'''Remove all cards from deck.'''
		self._cards.clear()

	def reverse(self):
		'''Reverse the order of the deck.'''
		self._cards.reverse()

	def pop(self, index=0):
		'''Remove and return card at index (0 = top).  
		O(n) for arbitrary index.'''
		if index == 0:
			return self._cards.popleft()
		elif index == -1:
			return self._cards.pop()
		else:
			temp = list(self._cards)
			card = temp.pop(index)
			self._cards = deque(temp)
			return card
	
	def insert(self, index, card):
		'''Insert card before index (top of deck = 0).'''
		if not isinstance(card, Card):
			raise TypeError('can only insert Card instances')
		temp = list(self._cards)
		temp.insert(index, card)
		self._cards = deque(temp)

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
				for c in (reversed(item) if position=='top' else item):
					if not isinstance(c, Card):
						raise TypeError('all items in iterable must be Card instances')
					flat_cards.append(c)
			else:
				raise TypeError('must be Card or iterable of Cards')
		
		if position == 'top':
			self._cards.extendleft(flat_cards)
		elif position == 'bottom':
			self._cards.extend(flat_cards)
		elif position == 'random':
			temp = list(self._cards)
			for c in flat_cards:
				temp.insert(random.randint(0, len(temp)), c)
			self._cards = deque(temp)
		else:
			raise ValueError("position must be 'top', 'bottom', or 'random'")

	def remove_card(self, card):
		'''
		Remove the first occurrence of a specific card from the deck.
		
		Raises:
			ValueError if the card is not found.
		'''
		self._cards.remove(card)
	
	def index(self, card, start=0, stop=None):
		'''
		Return the first index of a specific card (from top-bottom).

		Raises:
			ValueError if not found.
		'''
		if stop is None:
			stop = len(self._cards)
		return self._cards.index(card, start, stop)

	def filter(self, predicate):
		'''
		Keep only cards where `predicate(card)` is True.
		
		Example (keep cards with a value above 7):
			`deck.filter(lambda c: deck.value(c) > 7)`
		'''
		self._cards = deque(c for c in self._cards if predicate(c))

	def remove(self, predicate):
		'''
		Remove cards matching a condition.
		
		Example (remove all hearts): 
			`deck.remove(lambda c: c.suit == Suit.HEARTS)`
		'''
		self._cards = deque(c for c in self._cards if not predicate(c))

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
		raise TypeError('count() expects Card or predicate function')


	# --- Deck arithmetic ---
	def __add__(self, other):
		'''
		Returns a new deck with the same cards/rules as the first deck,  
		followed by the cards of a second deck.

		Cards are referenced (not copied).
		'''
		if not isinstance(other, Deck):
			return NotImplemented
		new = self.copy()
		new._cards.extend(other._cards)
		return new

	def __iadd__(self, other):
		'''Add cards from another deck to the bottom of this one.'''
		if not isinstance(other, Deck):
			return NotImplemented
		self._cards.extend(other._cards)
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
		to_remove = set()
		if isinstance(other, Card):
			to_remove.add(other)
		elif isinstance(other, Deck):
			to_remove = to_remove.update(other._cards)
		elif isinstance(other, Iterable):
			to_remove = to_remove.update(other)
		else:
			return NotImplemented
		
		new_cards = deque(c for c in self._cards if 
					c not in to_remove and c.suit not in to_remove and c.rank not in to_remove)
		return Deck.from_cards(
			new_cards, # container already created
			include_jokers=self.include_jokers,
			rank_values=self.rank_values,
			suit_order=self.suit_order,
			shuffle=False,
			_no_copy=True
		)
	
	def __isub__(self, other):
		'''Remove certain cards, suits, or ranks from this deck.'''
		to_remove = set()
		if isinstance(other, Card):
			to_remove.add(other)
		elif isinstance(other, Deck):
			to_remove = to_remove.update(other._cards)
		elif isinstance(other, Iterable):
			to_remove = to_remove.update(other)
		else:
			return NotImplemented

		self._cards = deque(c for c in self._cards if 
					c not in to_remove and c.suit not in to_remove and c.rank not in to_remove)
		return self
	
	def __mul__(self, n):
		'''Return a new deck repeated `n` times (cards are referenced, not cloned).'''
		if not isinstance(n, int):
			return NotImplemented
		if n < 1:
			raise ValueError('Deck multiplication requires a positive int')
		return Deck.from_cards(
			self._cards * n, # produces a new deque object
			include_jokers=self.include_jokers,
			rank_values=self.rank_values,
			suit_order=self.suit_order,
			shuffle=False,
			_no_copy=True
		)
	
	__rmul__ = __mul__
	
	def __imul__(self, n):
		'''Repeat this deck's cards `n` times.'''
		if not isinstance(n, int):
			return NotImplemented
		if n < 1:
			raise ValueError('Deck multiplication requires a positive int')
		self._cards *= n
		return self
	
	def __truediv__(self, n):
		'''
		Loosely split into `n` decks, distributing all cards
		
		Equivalent to `deck.split(n, strict=False)`
		'''
		return self.split(n, strict=False)
	
	def __floordiv__(self, n):
		'''
		Strictly split into `n` evenly sized decks (discarding extras)
		
		Equivalent to `deck.split(n, strict=True)`
		'''
		return self.split(n, strict=True)
	
	def __lshift__(self, n):
		'''Rotate the top `n` cards to the bottom (cut).'''
		self._cards.rotate(-n)
		return self

	def __rshift__(self, n):
		'''Rotate the bottom `n` cards to the top (reverse cut).'''
		self._cards.rotate(n)
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
		'''Sort deck according to rank/suit order (in descending order).'''
		temp = list(self._cards)
		temp.sort(key=self._cmp_key, reverse=ascending)
		self._cards = deque(temp)
