import random
from .card import Card

# Default rank-to-value mapping
DEFAULT_RANK_VALUES = {
	'2': 2, '3': 3, '4': 4, '5': 5, '6': 6,
	'7': 7, '8': 8, '9': 9, '10': 10,
	'J': 11, 'Q': 12, 'K': 13, 'A': 14, 
	'JOKER': 15
}

# Default English alphabetical suit order
ENGLISH_ALPH_ORDER = ('clubs', 'diamonds', 'hearts', 'spades', 'black', 'red')


class Deck:
	'''Represents a deck of cards with shared rank/suit rules.'''

	def __init__(self, include_jokers=False, rank_values=None, suit_order=ENGLISH_ALPH_ORDER, shuffle=False):
		# Shared rules for this deck
		self.rank_values = rank_values or DEFAULT_RANK_VALUES
		self.suit_order = suit_order
		self.include_jokers = include_jokers

		# Map suits to their indices in the ordering
		if self.suit_order is None:
			self._suit_index = {}
		else:
			self._suit_index = {s: i for i, s in enumerate(self.suit_order)}

		# Build deck
		self._build_cards()

		if shuffle:
			self.shuffle()

	def _build_cards(self):
		'''Create a deck in New Deck Order.'''
		# New deck order: A-K Hearts, A-K Clubs, K-A Diamonds, K-A Spades (bottom)
		up_ranks = ['A', *map(str, range(2, 11)), 'J', 'Q', 'K']
		down_ranks = ['K', 'Q', 'J', *map(str, range(10, 1, -1)), 'A']

		self.cards = [Card(rank, suit) for suit in ['hearts', 'clubs'] for rank in up_ranks]
		self.cards.extend(Card(rank, suit) for suit in ['diamonds', 'spades'] for rank in down_ranks)
		
		if self.include_jokers:
			self.cards.append(Card('JOKER', 'black'))
			self.cards.append(Card('JOKER', 'red'))


	# --- Deck operations ---
	def shuffle(self):
		'''Shuffle deck in place.'''
		random.shuffle(self.cards)

	def deal(self, n=1, strict=False):
		'''Return a list of up to n cards from the top of the deck and remove them.
		
		- If strict and fewer than n cards remain, ValueError is raised.
		- Always returns a list (possibly shorter than n if not strict).
		'''
		if strict and n > len(self.cards):
			raise ValueError('Not enough cards left to deal')
		dealt = self.cards[:n]
		self.cards = self.cards[n:]
		return dealt
	
	def reset(self, shuffle=True):
		'''Reset deck to full of cards.'''
		self._build_cards()
		if shuffle:
			self.shuffle()

	def __repr__(self):
		return f'Deck({len(self.cards)} cards)'
	
	def __str__(self):
		return f'Deck({len(self.cards)} cards)'

	# --- Container-style magic ---
	def __len__(self):
		return len(self.cards)
	
	def __getitem__(self, position):
		return self.cards[position]
	
	def __iter__(self):
		return iter(self.cards)
	
	# --- Card comparison ---
	def value(self, card):
		'''get numeric value of card according to deck rules.'''
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
	
	def cmp_key(self, card):
		'''Return a tuple key suitable for sorting: (rank_value, suit_index).  
		Unknown suits get -1. If suits are unordered, suit_index is 0.'''
		rank_val = self.value(card)
		suit_index = 0
		if self.suit_order:
			suit_index = self._suit_index.get(card.suit, -1)
		return (rank_val, suit_index)
	
	def sort(self, desc=False):
		'''Sort deck in place using deck rules, descending from top-bottom.'''
		self.cards.sort(reverse=desc, key=self.cmp_key)
