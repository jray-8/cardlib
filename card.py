
# Unicode suit symbols for nice display
SUIT_SYMBOLS = {
	'spades': '♠',
	'hearts': '♥',
	'diamonds': '♦',
	'clubs': '♣',
	'red': 'Red',
	'black': 'Black'
}


class Card:
	'''Represents a single playing card.'''

	__slots__ = ('_rank', '_suit')

	def __init__(self, rank, suit):
		self._rank = rank
		self._suit = suit

	@property
	def rank(self):
		return self._rank
	
	@property
	def suit(self):
		return self._suit
	
	@property
	def is_red(self):
		return self._suit in ('hearts', 'diamonds', 'red')
	
	@property
	def is_black(self):
		return self._suit in ('spades', 'clubs', 'black')

	@property
	def value(self):
		raise NotImplementedError('card value depends on deck rules')

	def __repr__(self):
		return f'Card({self.rank}, {self.suit})'
	
	def __str__(self):
		if self.rank == 'JOKER':
			return f'{self.suit.capitalize()} JOKER'
		return f'{self.rank}{SUIT_SYMBOLS.get(self.suit, self.suit)}'
	
	# Equality comparison
	def __eq__(self, other):
		return isinstance(other, Card) and self.rank == other.rank and self.suit == other.suit
	
	# Less-than comparison (requires deck context)
	def __lt__(self, other):
		raise NotImplementedError('Use Deck.compare(card1, card2) for ordering')
	
	def __hash__(self):
		return hash((self.rank, self.suit))