from enum import Enum

class Suit(Enum):
	SPADES = '♠' # Unicode symbols for nice display
	HEARTS = '♥'
	DIAMONDS = '♦'
	CLUBS = '♣'
	RED = 'Red'
	BLACK = 'Black'

class Rank(Enum):
	TWO = '2'
	THREE = '3'
	FOUR = '4'
	FIVE = '5'
	SIX = '6'
	SEVEN = '7'
	EIGHT = '8'
	NINE = '9'
	TEN = '10'
	JACK = 'J'
	QUEEN = 'Q'
	KING = 'K'
	ACE = 'A'
	JOKER = 'JOKER'


class Card:
	'''Represents a single immutable playing card.'''

	__slots__ = ('_rank', '_suit')

	def __init__(self, rank: Rank, suit: Suit):
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
		return self._suit in (Suit.HEARTS, Suit.DIAMONDS, Suit.RED)
	
	@property
	def is_black(self):
		return self._suit in (Suit.SPADES, Suit.CLUBS, Suit.BLACK)

	@property
	def value(self):
		raise NotImplementedError('card value depends on deck rules')

	def __repr__(self):
		return f'Card({self.rank}, {self.suit})'
	
	def __str__(self):
		rank = self.rank.value if isinstance(self.rank, Enum) else self.rank
		suit = self.suit.value if isinstance(self.suit, Enum) else self.suit
		return f'{rank}{suit}'
	
	# Equality comparison
	def __eq__(self, other):
		return isinstance(other, Card) and self.rank == other.rank and self.suit == other.suit
	
	# Less-than comparison (requires deck context)
	def __lt__(self, other):
		raise NotImplementedError('Use Deck.compare(card1, card2) for ordering')
	
	def __hash__(self):
		return hash((self.rank, self.suit))
	

# A collection of named constants that represent a fixed set of standard playing cards
class StandardCards:
	'''
	A library of predefined Card instances for all standard playing cards  
	(52 cards + 2 Jokers).
	
	Example:
		`StandardCards.ACE_SPADES`
		`StandardCards.RED_JOKER`
	'''
	# --- Spades ---
	ACE_SPADES = Card(Rank.ACE, Suit.SPADES)
	KING_SPADES = Card(Rank.KING, Suit.SPADES)
	QUEEN_SPADES = Card(Rank.QUEEN, Suit.SPADES)
	JACK_SPADES = Card(Rank.JACK, Suit.SPADES)
	TEN_SPADES = Card(Rank.TEN, Suit.SPADES)
	NINE_SPADES = Card(Rank.NINE, Suit.SPADES)
	EIGHT_SPADES = Card(Rank.EIGHT, Suit.SPADES)
	SEVEN_SPADES = Card(Rank.SEVEN, Suit.SPADES)
	SIX_SPADES = Card(Rank.SIX, Suit.SPADES)
	FIVE_SPADES = Card(Rank.FIVE, Suit.SPADES)
	FOUR_SPADES = Card(Rank.FOUR, Suit.SPADES)
	THREE_SPADES = Card(Rank.THREE, Suit.SPADES)
	TWO_SPADES = Card(Rank.TWO, Suit.SPADES)
	# --- Hearts ---
	ACE_HEARTS = Card(Rank.ACE, Suit.HEARTS)
	KING_HEARTS = Card(Rank.KING, Suit.HEARTS)
	QUEEN_HEARTS = Card(Rank.QUEEN, Suit.HEARTS)
	JACK_HEARTS = Card(Rank.JACK, Suit.HEARTS)
	TEN_HEARTS = Card(Rank.TEN, Suit.HEARTS)
	NINE_HEARTS = Card(Rank.NINE, Suit.HEARTS)
	EIGHT_HEARTS = Card(Rank.EIGHT, Suit.HEARTS)
	SEVEN_HEARTS = Card(Rank.SEVEN, Suit.HEARTS)
	SIX_HEARTS = Card(Rank.SIX, Suit.HEARTS)
	FIVE_HEARTS = Card(Rank.FIVE, Suit.HEARTS)
	FOUR_HEARTS = Card(Rank.FOUR, Suit.HEARTS)
	THREE_HEARTS = Card(Rank.THREE, Suit.HEARTS)
	TWO_HEARTS = Card(Rank.TWO, Suit.HEARTS)
	# --- Clubs ---
	ACE_CLUBS = Card(Rank.ACE, Suit.CLUBS)
	KING_CLUBS = Card(Rank.KING, Suit.CLUBS)
	QUEEN_CLUBS = Card(Rank.QUEEN, Suit.CLUBS)
	JACK_CLUBS = Card(Rank.JACK, Suit.CLUBS)
	TEN_CLUBS = Card(Rank.TEN, Suit.CLUBS)
	NINE_CLUBS = Card(Rank.NINE, Suit.CLUBS)
	EIGHT_CLUBS = Card(Rank.EIGHT, Suit.CLUBS)
	SEVEN_CLUBS = Card(Rank.SEVEN, Suit.CLUBS)
	SIX_CLUBS = Card(Rank.SIX, Suit.CLUBS)
	FIVE_CLUBS = Card(Rank.FIVE, Suit.CLUBS)
	FOUR_CLUBS = Card(Rank.FOUR, Suit.CLUBS)
	THREE_CLUBS = Card(Rank.THREE, Suit.CLUBS)
	TWO_CLUBS = Card(Rank.TWO, Suit.CLUBS)
	# --- Diamonds ---
	ACE_DIAMONDS = Card(Rank.ACE, Suit.DIAMONDS)
	KING_DIAMONDS = Card(Rank.KING, Suit.DIAMONDS)
	QUEEN_DIAMONDS = Card(Rank.QUEEN, Suit.DIAMONDS)
	JACK_DIAMONDS = Card(Rank.JACK, Suit.DIAMONDS)
	TEN_DIAMONDS = Card(Rank.TEN, Suit.DIAMONDS)
	NINE_DIAMONDS = Card(Rank.NINE, Suit.DIAMONDS)
	EIGHT_DIAMONDS = Card(Rank.EIGHT, Suit.DIAMONDS)
	SEVEN_DIAMONDS = Card(Rank.SEVEN, Suit.DIAMONDS)
	SIX_DIAMONDS = Card(Rank.SIX, Suit.DIAMONDS)
	FIVE_DIAMONDS = Card(Rank.FIVE, Suit.DIAMONDS)
	FOUR_DIAMONDS = Card(Rank.FOUR, Suit.DIAMONDS)
	THREE_DIAMONDS = Card(Rank.THREE, Suit.DIAMONDS)
	TWO_DIAMONDS = Card(Rank.TWO, Suit.DIAMONDS)
