#!/usr/bin/env python3
"""Ruby Poker — colourful video poker (Jacks or Better). Fun chips only."""
import random
import pygame

W, H = 960, 620
RANKS = "A23456789TJQK"
SUITS = "SHDC"
SUIT_SYM = {"S": "♠", "H": "♥", "D": "♦", "C": "♣"}
RED = {"H", "D"}
PAY = [
    ("Royal flush", 250),
    ("Straight flush", 50),
    ("Four of a kind", 25),
    ("Full house", 9),
    ("Flush", 6),
    ("Straight", 4),
    ("Three of a kind", 3),
    ("Two pair", 2),
    ("Jacks or better", 1),
]


def rank_val(r):
    return "A23456789TJQK".index(r)


def hand_name(cards):
    ranks = [c[0] for c in cards]
    suits = [c[1] for c in cards]
    counts = {r: ranks.count(r) for r in set(ranks)}
    vals = sorted(rank_val(r) for r in ranks)
    flush = len(set(suits)) == 1
    unique = sorted(set(vals))
    straight = len(unique) == 5 and unique[-1] - unique[0] == 4
    if vals == [0, 9, 10, 11, 12]:
        straight = True
    freq = sorted(counts.values(), reverse=True)
    if flush and vals == [0, 9, 10, 11, 12]:
        return "Royal flush"
    if flush and straight:
        return "Straight flush"
    if freq[0] == 4:
        return "Four of a kind"
    if freq == [3, 2]:
        return "Full house"
    if flush:
        return "Flush"
    if straight:
        return "Straight"
    if freq[0] == 3:
        return "Three of a kind"
    if freq == [2, 2, 1]:
        return "Two pair"
    pairs = [r for r, n in counts.items() if n == 2]
    if pairs and pairs[0] in "AJQK":
        return "Jacks or better"
    return "Nothing"


def payout(name, bet):
    for n, m in PAY:
        if n == name:
            return m * bet
    return 0


def new_deck():
    d = [r + s for r in RANKS for s in SUITS]
    random.shuffle(d)
    return d


def draw_card(screen, card, rect, held, fonts):
    pygame.draw.rect(screen, (245, 240, 230), rect, border_radius=10)
    pygame.draw.rect(screen, (40, 20, 30), rect, 3, border_radius=10)
    if held:
        pygame.draw.rect(screen, (255, 210, 40), rect.inflate(8, 8), 4, border_radius=14)
    color = (200, 30, 40) if card[1] in RED else (25, 25, 35)
    rank = "10" if card[0] == "T" else card[0]
    face = fonts["big"].render(rank, True, color)
    suit = fonts["suit"].render(SUIT_SYM[card[1]], True, color)
    screen.blit(face, (rect.x + 12, rect.y + 10))
    screen.blit(suit, (rect.centerx - suit.get_width() // 2, rect.centery - 10))


def button(screen, rect, label, font, hot, enabled=True):
    c = (90, 180, 90) if enabled else (70, 70, 80)
    if hot and enabled:
        c = (120, 220, 110)
    pygame.draw.rect(screen, c, rect, border_radius=10)
    pygame.draw.rect(screen, (255, 255, 255), rect, 2, border_radius=10)
    t = font.render(label, True, (20, 20, 20) if enabled else (160, 160, 160))
    screen.blit(t, (rect.centerx - t.get_width() // 2, rect.centery - t.get_height() // 2))


def main():
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Ruby Poker")
    clock = pygame.time.Clock()
    fonts = {
        "title": pygame.font.SysFont("arial", 36, bold=True),
        "big": pygame.font.SysFont("arial", 32, bold=True),
        "suit": pygame.font.SysFont("arial", 40, bold=True),
        "body": pygame.font.SysFont("arial", 20, bold=True),
        "small": pygame.font.SysFont("arial", 16),
    }
    bank, bet = 200, 5
    phase = "ready"
    deck, hand, held = [], [], [False] * 5
    result, win = "", 0
    cards_rect = [pygame.Rect(40 + i * 185, 230, 160, 210) for i in range(5)]
    deal_btn = pygame.Rect(330, 500, 140, 48)
    draw_btn = pygame.Rect(490, 500, 140, 48)
    plus_btn = pygame.Rect(180, 500, 60, 48)
    minus_btn = pygame.Rect(110, 500, 60, 48)

    while True:
        mx, my = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if minus_btn.collidepoint(mx, my) and phase == "ready":
                    bet = max(1, bet - 1)
                if plus_btn.collidepoint(mx, my) and phase == "ready":
                    bet = min(10, bank, bet + 1)
                if deal_btn.collidepoint(mx, my) and phase in ("ready", "done") and bank >= bet:
                    bank -= bet
                    deck = new_deck()
                    hand = [deck.pop() for _ in range(5)]
                    held = [False] * 5
                    phase = "hold"
                    result, win = "", 0
                if draw_btn.collidepoint(mx, my) and phase == "hold":
                    for i in range(5):
                        if not held[i]:
                            hand[i] = deck.pop()
                    result = hand_name(hand)
                    win = payout(result, bet)
                    bank += win
                    phase = "done"
                if phase == "hold":
                    for i, r in enumerate(cards_rect):
                        if r.collidepoint(mx, my):
                            held[i] = not held[i]

        screen.fill((28, 8, 28))
        pygame.draw.rect(screen, (90, 16, 40), (0, 0, W, 90))
        title = fonts["title"].render("RUBY POKER  •  JACKS OR BETTER", True, (255, 210, 80))
        screen.blit(title, (W // 2 - title.get_width() // 2, 18))
        sub = fonts["small"].render("Click cards to HOLD  •  https://x.com/ElbowOS", True, (255, 200, 210))
        screen.blit(sub, (W // 2 - sub.get_width() // 2, 58))

        y = 100
        for name, mult in PAY:
            line = fonts["small"].render(f"{name:18}  {mult}x", True, (255, 230, 180))
            screen.blit(line, (40, y))
            y += 18

        info = fonts["body"].render(f"BANK  {bank}     BET  {bet}", True, (255, 255, 255))
        screen.blit(info, (620, 110))
        if result:
            col = (80, 255, 140) if win else (255, 160, 160)
            msg = fonts["body"].render(f"{result.upper()}   +{win}" if win else result.upper(), True, col)
            screen.blit(msg, (620, 150))

        if hand:
            for i, card in enumerate(hand):
                draw_card(screen, card, cards_rect[i], held[i] and phase == "hold", fonts)
                if held[i] and phase == "hold":
                    tag = fonts["small"].render("HOLD", True, (255, 220, 40))
                    screen.blit(tag, (cards_rect[i].centerx - tag.get_width() // 2, cards_rect[i].y - 22))
        else:
            hint = fonts["body"].render("Press DEAL to start", True, (230, 200, 220))
            screen.blit(hint, (W // 2 - hint.get_width() // 2, 320))

        button(screen, minus_btn, "\u2212", fonts["body"], minus_btn.collidepoint(mx, my), phase in ("ready", "done"))
        button(screen, plus_btn, "+", fonts["body"], plus_btn.collidepoint(mx, my), phase in ("ready", "done"))
        button(screen, deal_btn, "DEAL", fonts["body"], deal_btn.collidepoint(mx, my), phase in ("ready", "done") and bank >= bet)
        button(screen, draw_btn, "DRAW", fonts["body"], draw_btn.collidepoint(mx, my), phase == "hold")
        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
