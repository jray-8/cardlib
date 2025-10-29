# cardlib :black_joker::game_die:

A lightweight, reusable Python library for **cards and dice**.  
Designed for text-based games like poker, custom card games, and probability simulations.

## Features

- `Card` — represents a single playing card (immutable rank/suit)
- `Deck` — standard 52-card deck, optional jokers, shuffle/deal/sort, compare cards
- `Die` — single die of arbitrary sides
- `Dice` — collection of dice
- `ExplodingDie` — rolls again when max side is hit, sums total
- `WeightedDie` — roll with custom side probabilities

## Installation

```bash
pip install git+https://github.com/jray-8/cardlib.git
```

- Downloads the library into `site-packages`
- Ready to import from anywhere

## Usage

```python
from cardlib import Deck, Dice, Die, ExplodingDie

# --- Cards ---
deck = Deck(include_jokers=True)
deck.shuffle()
hand = deck.deal(5)
print('Dealt hand:', hand)

# --- Dice ---
d6 = Die(6)
dice_pool = Dice(6, 6, 8)
total = dice_pool.roll()
print('Dice pool roll:', dice_pool, 'Total:', total)

exploding_d6 = ExplodingDie(6)
print('Exploding d6 roll:', exploding_d6.roll(), 'Explosions:', exploding_d6.explosions)
```
