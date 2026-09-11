#!/usr/bin/env python3
"""Sunset Solitaire — colourful Klondike."""
import random
import pygame

W, H = 1000, 700
SUITS = [("♥", True), ("♦", True), ("♣", False), ("♠", False)]
RANKS = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
RANK_I = {r: i for i, r in enumerate(RANKS)}
CW, CH = 78, 108


def make_deck():
    deck = [(r, s, red) for r in RANKS for s, red in SUITS]
    random.shuffle(deck)
    return deck


class Pile:
    def __init__(self, x, y, kind):
        self.x, self.y, self.kind = x, y, kind
        self.cards = []

    def top(self):
        return self.cards[-1] if self.cards else None

    def hit(self, pos):
        if self.kind == "tableau":
            for i, c in enumerate(self.cards):
                rect = pygame.Rect(self.x, self.y + i * 24, CW, CH)
                if rect.collidepoint(pos) and c[3]:
                    return i
            if not self.cards:
                return -1 if pygame.Rect(self.x, self.y, CW, CH).collidepoint(pos) else None
            return None
        r = pygame.Rect(self.x, self.y, CW, CH)
        return len(self.cards) - 1 if r.collidepoint(pos) and self.cards else (-1 if r.collidepoint(pos) else None)


def can_stack_tab(card, onto):
    if onto is None:
        return card[0] == "K"
    return card[2] != onto[2] and RANK_I[card[0]] == RANK_I[onto[0]] - 1


def can_stack_found(card, onto):
    if onto is None:
        return card[0] == "A"
    return card[1] == onto[1] and RANK_I[card[0]] == RANK_I[onto[0]] + 1


def draw_card(screen, card, x, y, font):
    rank, suit, red, face = card
    rect = pygame.Rect(x, y, CW, CH)
    if not face:
        pygame.draw.rect(screen, (40, 50, 140), rect, border_radius=8)
        pygame.draw.rect(screen, (90, 140, 220), rect.inflate(-10, -10), border_radius=6)
        pygame.draw.rect(screen, (255, 220, 80), rect, 2, border_radius=8)
        return
    col = (200, 30, 40) if red else (25, 25, 40)
    pygame.draw.rect(screen, (250, 246, 235), rect, border_radius=8)
    pygame.draw.rect(screen, (40, 40, 40), rect, 2, border_radius=8)
    screen.blit(font.render(rank, True, col), (x + 6, y + 4))
    screen.blit(font.render(suit, True, col), (x + 6, y + 24))
    big = pygame.font.SysFont("arial", 28, bold=True)
    screen.blit(big.render(suit, True, col), (x + 28, y + 44))


def deal_new():
    deck = make_deck()
    stock = Pile(30, 30, "stock")
    waste = Pile(120, 30, "waste")
    foundations = [Pile(430 + i * 90, 30, "found") for i in range(4)]
    tableaus = [Pile(30 + i * 90, 170, "tableau") for i in range(7)]
    for i, t in enumerate(tableaus):
        for j in range(i + 1):
            r, s, red = deck.pop()
            t.cards.append((r, s, red, j == i))
    stock.cards = [(r, s, red, False) for r, s, red in deck]
    return stock, waste, foundations, tableaus


def main():
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Sunset Solitaire")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("arial", 18, bold=True)
    title = pygame.font.SysFont("arial", 28, bold=True)

    stock, waste, foundations, tableaus = deal_new()
    holding = []
    hold_from = None
    hold_index = 0

    def grab(pos):
        nonlocal holding, hold_from, hold_index
        i = stock.hit(pos)
        if i is not None:
            if stock.cards:
                c = stock.cards.pop()
                waste.cards.append((c[0], c[1], c[2], True))
            else:
                stock.cards = [(c[0], c[1], c[2], False) for c in reversed(waste.cards)]
                waste.cards = []
            return
        i = waste.hit(pos)
        if i is not None and i >= 0:
            holding = [waste.cards.pop()]
            hold_from = waste
            hold_index = 0
            return
        for f in foundations:
            i = f.hit(pos)
            if i is not None and i >= 0:
                holding = [f.cards.pop()]
                hold_from = f
                hold_index = 0
                return
        for t in tableaus:
            i = t.hit(pos)
            if i is not None and i >= 0:
                holding = t.cards[i:]
                t.cards = t.cards[:i]
                hold_from = t
                hold_index = i
                return

    def drop(pos):
        nonlocal holding, hold_from
        target = None
        for f in foundations:
            if pygame.Rect(f.x, f.y, CW, CH).collidepoint(pos) and len(holding) == 1:
                if can_stack_found(holding[0], f.top()):
                    target = f
        if target is None:
            for t in tableaus:
                h = CH if not t.cards else 24 * (len(t.cards) - 1) + CH
                if pygame.Rect(t.x, t.y, CW, h).collidepoint(pos):
                    if can_stack_tab(holding[0], t.top()):
                        target = t
        if target is not None:
            target.cards.extend(holding)
            if hold_from.kind == "tableau" and hold_from.cards and not hold_from.cards[-1][3]:
                c = hold_from.cards[-1]
                hold_from.cards[-1] = (c[0], c[1], c[2], True)
        else:
            hold_from.cards.extend(holding)
        holding = []
        hold_from = None

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return
                if event.key == pygame.K_n:
                    stock, waste, foundations, tableaus = deal_new()
                    holding = []
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if not holding:
                    grab(event.pos)
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if holding:
                    drop(event.pos)

        for y in range(H):
            t = y / H
            r = int(40 + 140 * t)
            g = int(30 + 40 * t)
            b = int(70 + 20 * (1 - t))
            pygame.draw.line(screen, (r, g, b), (0, y), (W, y))
        pygame.draw.circle(screen, (255, 160, 60), (820, 90), 50)

        screen.blit(title.render("SUNSET SOLITAIRE", True, (255, 230, 180)), (700, 20))
        screen.blit(font.render("N new   ESC quit   click stock to draw", True, (255, 230, 200)), (700, 56))
        screen.blit(font.render("https://x.com/ElbowOS", True, (255, 210, 160)), (700, 80))

        def pile_draw(p):
            if not p.cards:
                pygame.draw.rect(screen, (255, 255, 255), (p.x, p.y, CW, CH), 2, border_radius=8)
                return
            if p.kind == "tableau":
                for i, c in enumerate(p.cards):
                    draw_card(screen, c, p.x, p.y + i * 24, font)
            else:
                draw_card(screen, p.cards[-1], p.x, p.y, font)

        pile_draw(stock)
        pile_draw(waste)
        for p in foundations + tableaus:
            pile_draw(p)

        if holding:
            mx, my = pygame.mouse.get_pos()
            for i, c in enumerate(holding):
                draw_card(screen, c, mx - 30, my - 20 + i * 24, font)

        if all(len(f.cards) == 13 for f in foundations):
            win = title.render("YOU WIN", True, (255, 230, 80))
            screen.blit(win, (W // 2 - win.get_width() // 2, 640))

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
