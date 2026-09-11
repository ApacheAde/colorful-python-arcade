#!/usr/bin/env python3
"""Colorful Python Arcade — pick a game."""
import os
import subprocess
import sys

import pygame

GAMES = [
    ("Brick Bros", "Mario-style platformer", "brick_bros.py", (80, 180, 80)),
    ("Neon Blackjack", "Casino 21 with chips", "neon_blackjack.py", (20, 90, 40)),
    ("Sunset Solitaire", "Klondike card game", "sunset_solitaire.py", (180, 70, 40)),
    ("Lucky Slots", "Three-reel slot machine", "lucky_slots.py", (140, 30, 90)),
    ("Neon Roulette", "Red / black / number bets", "neon_roulette.py", (90, 20, 20)),
    ("Pipe Panic", "Flappy-style pipe runner", "pipe_panic.py", (40, 140, 200)),
    ("Ruby Poker", "Jacks-or-better video poker", "ruby_poker.py", (140, 20, 60)),
    ("Neon Memory", "Match the neon pairs", "neon_memory.py", (90, 50, 180)),
    ("Star Blaster", "Colour space shooter", "star_blaster.py", (20, 40, 110)),
]

W, H = 900, 720


def run_game(filename):
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
    subprocess.call([sys.executable, path])


def main():
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Colorful Python Arcade")
    clock = pygame.time.Clock()
    title = pygame.font.SysFont("arial", 42, bold=True)
    body = pygame.font.SysFont("arial", 20, bold=True)
    small = pygame.font.SysFont("arial", 15)
    hover = -1

    while True:
        mx, my = pygame.mouse.get_pos()
        hover = -1
        cards = []
        for i, (name, desc, file, color) in enumerate(GAMES):
            col = i % 3
            row = i // 3
            rect = pygame.Rect(40 + col * 290, 130 + row * 185, 260, 165)
            cards.append(rect)
            if rect.collidepoint(mx, my):
                hover = i

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and hover >= 0:
                pygame.quit()
                run_game(GAMES[hover][2])
                pygame.init()
                screen = pygame.display.set_mode((W, H))
                pygame.display.set_caption("Colorful Python Arcade")
                title = pygame.font.SysFont("arial", 42, bold=True)
                body = pygame.font.SysFont("arial", 20, bold=True)
                small = pygame.font.SysFont("arial", 15)

        screen.fill((18, 16, 32))
        pygame.draw.rect(screen, (40, 30, 70), (0, 0, W, 100))
        t = title.render("COLORFUL PYTHON ARCADE", True, (255, 220, 80))
        screen.blit(t, (W // 2 - t.get_width() // 2, 16))
        s = small.render("Click a game  •  ESC to quit  •  https://x.com/ElbowOS", True, (200, 180, 255))
        screen.blit(s, (W // 2 - s.get_width() // 2, 66))

        for i, (name, desc, file, color) in enumerate(GAMES):
            rect = cards[i]
            c = tuple(min(255, x + 40) for x in color) if i == hover else color
            pygame.draw.rect(screen, c, rect, border_radius=16)
            pygame.draw.rect(screen, (255, 255, 255), rect, 3, border_radius=16)
            n = body.render(name, True, (255, 255, 255))
            d = small.render(desc, True, (240, 240, 240))
            screen.blit(n, (rect.x + 16, rect.y + 50))
            screen.blit(d, (rect.x + 16, rect.y + 86))

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
