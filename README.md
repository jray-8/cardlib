# 🃏♥️♠️ cardlib ♦️♣️🎲

A lightweight, extensible Python library for **cards and dice**.  

Designed for text-based games like poker, custom card games, and probability simulations.

## Features 🎯
- `Card` — immutable rank/suit pair
	- Subclass to make custom cards with mutable attributes
- `Deck` — **full-featured container** built on `collections.deque`
	- O(1) draw and add-to-top/bottom operations
	- Shuffle, deal, split, copy, slice, iterate
	- Full Python container interface (`len()`, `in`, indexing, slicing, iteration)
	- Arithmetic operations (`+`, `-`, `*`, `/`, `//`, `<<`, `>>`)
	- Built-in comparison and sorting based on custom rank/suit order
	- Fast filtering and functional-style methods (`filter`, `remove`, `count`)
	- Jokers, custom rank values, and custom suit order supported
- `Die` — single die of arbitrary sides
- `Dice` — collection of dice
- `WeightedDie` — roll with custom side probabilities
- `ExplodingDie` — rolls again when max side is hit, sums total

## 📦 Installation

```bash
pip install cardlib
```

- Downloads the library into `site-packages`
- Ready to import from anywhere

## 🃏 Deck Example

```python
from cardlib import Deck, Suit, Rank

# Create a standard shuffled deck (include jokers if desired)
deck = Deck(include_jokers=True)

# Draw cards
hand = deck.draw(5)
print('Dealt hand:', hand)

# Add cards back to the bottom
deck.add(hand, position='bottom')

# Split deck into two equal piles
p1, p2 = deck // 2

# Cut deck
deck << 10 # move top 10 cards to bottom

# Filter all non-heart cards
deck.filter(lambda c: c.suit == Suit.HEARTS)

# Sort cards
deck.sort(ascending=True)
```

## 🎲 Dice Example

```python
from cardlib import Die, Dice, ExplodingDie

# Roll a single d6
d6 = Die(6)
print('d6:', d6.roll())

# Roll a dice pool
dice_pool = Dice(6, 6, 8)
total = dice_pool.roll()
print('Dice pool roll:', dice_pool, 'Total:', total)

# Exploding die (re-roll on max)
xd6 = ExplodingDie(6)
print('Exploding d6 roll:', xd6.roll(), 'Explosions:', xd6.explosions)
```

## 📐 Advanced Deck Operations

| Operation | Description |
|------------|--------------|
| `deck.copy(deep=True)` | Clone deck (optionally deep copy cards) |
| `deck.reset(shuffle=True)` | Restore to new-deck order |
| `deck.deal(num_hands, cards_each)` | Deal cards into hands |
| `deck.add(*cards, position='top'/'bottom'/'random')` | Add cards dynamically |
| `deck.remove(lambda c: c.rank == Rank.ACE)` | Remove all Aces |
| `deck / 3` | Split deck loosely into 3 parts |
| `deck // 2` | Split deck strictly into 2 even halves |
| `deck << n` / `deck >> n` | Rotate (cut) cards |
| `deck1 + deck2` | Combine decks |
| `deck - Suit.HEARTS` | Remove all hearts |

- Use `help(Deck)` for the full docs.

## 📎 Notes

- Internally uses a `deque` for **O(1)** top/bottom operations.
- Slicing and arbitrary indexing are less efficient **O(n)**.
- `deck[0]` is the top of the deck.
- Customizable suit and rank order via `suit_order` (tuple) and `rank_values` (dict).
- Ideal for both simulation and **game logic** applications.

## 📄 License

MIT License © Jeffrey Ray