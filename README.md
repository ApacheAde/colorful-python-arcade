# Colorful Python Arcade

Full-colour **Python 3** mini-games written with [pygame](https://www.pygame.org/).
Each title is original and self-contained.

**Featured on X:** [https://x.com/ElbowOS](https://x.com/ElbowOS)

Repo: https://github.com/ApacheAde/colorful-python-arcade

## Games

| Game | File | What it is |
| --- | --- | --- |
| Brick Bros | `brick_bros.py` | Mario-style side scroller: jump, stomp walkers, grab coins, reach the flag |
| Neon Blackjack | `neon_blackjack.py` | Casino 21 with hit / stand / double and a chip bank |
| Sunset Solitaire | `sunset_solitaire.py` | Klondike cards, drag-and-drop, foundations |
| Lucky Slots | `lucky_slots.py` | Three-reel slot machine with colour symbols |
| Neon Roulette | `neon_roulette.py` | Red / black / single-number bets and a spinning wheel |
| Pipe Panic | `pipe_panic.py` | Flappy-style pipe runner |
| Ruby Poker | `ruby_poker.py` | Jacks-or-better video poker |
| Neon Memory | `neon_memory.py` | Match the neon pairs |
| Star Blaster | `star_blaster.py` | Colour space shooter |

Menu: `launcher.py`.

## Run

```bash
python3 -m pip install -r requirements.txt
python3 launcher.py
```

Or launch any game directly:

```bash
python3 brick_bros.py
```

Needs Python 3.9+ and a display (pygame window).

## Controls

- **Brick Bros** — A/D or arrows move, Space / W jump, R restart, Esc quit
- **Blackjack / Slots / Roulette / Poker** — click the on-screen buttons
- **Solitaire** — click stock to draw, drag stacks, N new game
- **Pipe Panic** — Space or click to flap
- **Neon Memory** — click cards, N new game
- **Star Blaster** — arrows / AD move, Space fire, R restart

## Notes

Brick Bros is a *tiny original platformer* inspired by classic mascot jumpers. It is **not** a Mario Bros ROM emulator and includes no Nintendo assets.

Casino games are for fun only — no real money.

## License

MIT. See `LICENSE`.
