#!/usr/bin/env python3
"""Neon Blackjack — colourful casino 21."""
import random
import pygame

W, H = 960, 620
SUITS = [("♥", (220, 30, 50)), ("♦", (220, 80, 30)), ("♣", (30, 40, 40)), ("♠", (20, 20, 40))]
RANKS = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]


def new_deck():
    deck = [(r, s, c) for r in RANKS for s, c in SUITS]
    random.shuffle(deck)
    return deck


def value(hand):
    total, aces = 0, 0
    for r, _, _ in hand:
        if r == "A":
            total += 11
            aces += 1
        elif r in "JQK":
            total += 10
        else:
            total += int(r)
    while total > 21 and aces:
        total -= 10
        aces -= 1
    return total


def draw_card(screen, card, x, y, font, small):
    r, s, col = card
    rect = pygame.Rect(x, y, 90, 126)
    pygame.draw.rect(screen, (250, 248, 240), rect, border_radius=10)
    pygame.draw.rect(screen, (40, 40, 40), rect, 2, border_radius=10)
    t = font.render(r, True, col)
    su = font.render(s, True, col)
    screen.blit(t, (x + 8, y + 6))
    screen.blit(su, (x + 8, y + 34))
    big = pygame.font.SysFont("arial", 36, bold=True)
    screen.blit(big.render(s, True, col), (x + 32, y + 52))


def button(screen, rect, label, font, hot):
    pygame.draw.rect(screen, (255, 210, 70) if hot else (30, 120, 70), rect, border_radius=10)
    pygame.draw.rect(screen, (255, 255, 255), rect, 2, border_radius=10)
    t = font.render(label, True, (10, 20, 10) if hot else (255, 255, 255))
    screen.blit(t, (rect.centerx - t.get_width() // 2, rect.centery - t.get_height() // 2))


def main():
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Neon Blackjack")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("arial", 22, bold=True)
    big = pygame.font.SysFont("arial", 40, bold=True)
    small = pygame.font.SysFont("arial", 16)

    bank = 500
    bet = 25
    deck = new_deck()
    player, dealer = [], []
    phase = "bet"
    msg = "Place a bet"

    def deal():
        nonlocal deck, player, dealer, phase, msg, bank, bet
        if bank < bet:
            msg = "Not enough chips"
            return
        bank -= bet
        if len(deck) < 15:
            deck = new_deck()
        player = [deck.pop(), deck.pop()]
        dealer = [deck.pop(), deck.pop()]
        phase = "play"
        msg = "Hit, stand or double"
        if value(player) == 21:
            phase = "dealer"

    def finish():
        nonlocal phase, msg, bank, bet
        phase = "over"
        pv, dv = value(player), value(dealer)
        if pv > 21:
            msg = "Bust — dealer wins"
        elif dv > 21 or pv > dv:
            win = bet * 2
            if pv == 21 and len(player) == 2:
                win = int(bet * 2.5)
                msg = "Blackjack!"
            else:
                msg = "You win"
            bank += win
        elif pv == dv:
            bank += bet
            msg = "Push"
        else:
            msg = "Dealer wins"
        bet = min(25, max(5, bet if bet <= 25 else 25))

    btns = {
        "deal": pygame.Rect(40, 540, 120, 48),
        "hit": pygame.Rect(180, 540, 120, 48),
        "stand": pygame.Rect(320, 540, 120, 48),
        "double": pygame.Rect(460, 540, 140, 48),
        "minus": pygame.Rect(640, 540, 50, 48),
        "plus": pygame.Rect(780, 540, 50, 48),
    }

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
                if btns["minus"].collidepoint(mx, my) and phase in ("bet", "over"):
                    bet = max(5, bet - 5)
                if btns["plus"].collidepoint(mx, my) and phase in ("bet", "over"):
                    bet = min(100, bet + 5)
                if btns["deal"].collidepoint(mx, my) and phase in ("bet", "over"):
                    deal()
                if phase == "play":
                    if btns["hit"].collidepoint(mx, my):
                        player.append(deck.pop())
                        if value(player) >= 21:
                            phase = "dealer"
                    if btns["stand"].collidepoint(mx, my):
                        phase = "dealer"
                    if btns["double"].collidepoint(mx, my) and len(player) == 2 and bank >= bet:
                        bank -= bet
                        bet *= 2
                        player.append(deck.pop())
                        phase = "dealer"

        if phase == "dealer":
            while value(dealer) < 17:
                dealer.append(deck.pop())
            finish()

        screen.fill((8, 70, 36))
        pygame.draw.ellipse(screen, (12, 100, 50), (40, 40, W - 80, H - 160))
        pygame.draw.ellipse(screen, (200, 170, 40), (40, 40, W - 80, H - 160), 6)
        screen.blit(big.render("NEON BLACKJACK", True, (255, 230, 80)), (40, 16))
        screen.blit(font.render(f"Bank  ${bank}     Bet  ${bet}", True, (255, 255, 255)), (40, 70))
        screen.blit(font.render(msg, True, (255, 240, 160)), (500, 70))
        screen.blit(small.render("https://x.com/ElbowOS", True, (180, 220, 180)), (760, 20))

        screen.blit(font.render("DEALER", True, (255, 255, 255)), (80, 120))
        for i, c in enumerate(dealer if phase in ("over",) else dealer[:1] + [None] * (len(dealer) - 1)):
            if c is None:
                pygame.draw.rect(screen, (80, 20, 90), (80 + i * 100, 150, 90, 126), border_radius=10)
            else:
                draw_card(screen, c, 80 + i * 100, 150, font, small)
        if phase == "over":
            screen.blit(font.render(str(value(dealer)), True, (255, 230, 80)), (80, 284))

        screen.blit(font.render("YOU", True, (255, 255, 255)), (80, 320))
        for i, c in enumerate(player):
            draw_card(screen, c, 80 + i * 100, 350, font, small)
        if player:
            screen.blit(font.render(str(value(player)), True, (255, 230, 80)), (80, 484))

        button(screen, btns["deal"], "DEAL", font, btns["deal"].collidepoint(mx, my))
        button(screen, btns["hit"], "HIT", font, btns["hit"].collidepoint(mx, my))
        button(screen, btns["stand"], "STAND", font, btns["stand"].collidepoint(mx, my))
        button(screen, btns["double"], "DOUBLE", font, btns["double"].collidepoint(mx, my))
        button(screen, btns["minus"], "-", font, btns["minus"].collidepoint(mx, my))
        screen.blit(font.render(f"${bet}", True, (255, 255, 255)), (700, 552))
        button(screen, btns["plus"], "+", font, btns["plus"].collidepoint(mx, my))

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
