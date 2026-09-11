#!/usr/bin/env python3
"""Neon Roulette — red / black / number bets."""
import math
import random
import pygame

W, H = 980, 640
REDS = {1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36}
ORDER = [
    0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13, 36, 11, 30, 8, 23, 10,
    5, 24, 16, 33, 1, 20, 14, 31, 9, 22, 18, 29, 7, 28, 12, 35, 3, 26,
]


def color_of(n):
    if n == 0:
        return (20, 140, 60)
    return (200, 30, 40) if n in REDS else (20, 20, 25)


def main():
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Neon Roulette")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("arial", 18, bold=True)
    big = pygame.font.SysFont("arial", 32, bold=True)

    bank = 400
    bet_amt = 10
    choice = ("color", "red")
    spinning = False
    angle = 0
    speed = 0
    result = None
    msg = "Pick a bet, then SPIN"

    buttons = []
    buttons.append(("RED", ("color", "red"), pygame.Rect(620, 120, 140, 50), (180, 30, 40)))
    buttons.append(("BLACK", ("color", "black"), pygame.Rect(780, 120, 140, 50), (30, 30, 40)))
    buttons.append(("GREEN 0", ("number", 0), pygame.Rect(620, 180, 140, 50), (20, 120, 50)))
    buttons.append(("SPIN", "spin", pygame.Rect(780, 180, 140, 50), (200, 160, 30)))
    num_btns = []
    for n in range(1, 37):
        r = pygame.Rect(620 + ((n - 1) % 6) * 54, 250 + ((n - 1) // 6) * 42, 50, 38)
        num_btns.append((n, r))
    minus = pygame.Rect(620, 520, 50, 44)
    plus = pygame.Rect(760, 520, 50, 44)

    while True:
        mx, my = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not spinning:
                if minus.collidepoint(mx, my):
                    bet_amt = max(5, bet_amt - 5)
                if plus.collidepoint(mx, my):
                    bet_amt = min(50, bet_amt + 5)
                for label, val, rect, col in buttons:
                    if rect.collidepoint(mx, my):
                        if val == "spin":
                            if bank >= bet_amt:
                                bank -= bet_amt
                                spinning = True
                                speed = 18 + random.random() * 8
                                result = None
                                msg = "Ball is rolling..."
                        else:
                            choice = val
                for n, r in num_btns:
                    if r.collidepoint(mx, my):
                        choice = ("number", n)

        if spinning:
            angle = (angle + speed) % 360
            speed *= 0.985
            if speed < 0.15:
                spinning = False
                idx = int((360 - angle) / (360 / 37)) % 37
                result = ORDER[idx]
                won = 0
                kind, val = choice
                if kind == "color":
                    if result != 0 and ((val == "red" and result in REDS) or (val == "black" and result not in REDS)):
                        won = bet_amt * 2
                elif kind == "number" and result == val:
                    won = bet_amt * 36
                bank += won
                msg = f"Landed on {result} — {'WIN $' + str(won) if won else 'lose'}"

        screen.fill((12, 12, 24))
        pygame.draw.rect(screen, (40, 10, 20), (0, 0, W, 70))
        screen.blit(big.render("NEON ROULETTE", True, (255, 210, 80)), (24, 16))
        screen.blit(font.render("https://x.com/ElbowOS", True, (220, 180, 200)), (780, 26))

        cx, cy, rad = 300, 340, 230
        pygame.draw.circle(screen, (180, 150, 50), (cx, cy), rad + 12)
        slice_a = 360 / 37
        for i, n in enumerate(ORDER):
            pts = [(cx, cy)]
            for k in range(6):
                a = math.radians(i * slice_a + k * slice_a / 5 - 90)
                pts.append((cx + rad * math.cos(a), cy + rad * math.sin(a)))
            pygame.draw.polygon(screen, color_of(n), pts)
        pygame.draw.circle(screen, (30, 20, 10), (cx, cy), 50)
        pygame.draw.polygon(screen, (255, 230, 80), [(cx - 10, cy - rad - 18), (cx + 10, cy - rad - 18), (cx, cy - rad + 8)])
        a = math.radians(angle - 90)
        bx = cx + (rad - 18) * math.cos(a)
        by = cy + (rad - 18) * math.sin(a)
        pygame.draw.circle(screen, (240, 240, 240), (int(bx), int(by)), 8)

        screen.blit(font.render(f"Bank ${bank}   Bet ${bet_amt}", True, (255, 255, 255)), (620, 80))
        kind, val = choice
        screen.blit(font.render(f"Bet on: {kind} {val}", True, (255, 220, 120)), (620, 100))
        screen.blit(font.render(msg, True, (200, 255, 180)), (40, 80))

        for label, val, rect, col in buttons:
            hot = rect.collidepoint(mx, my)
            pygame.draw.rect(screen, tuple(min(255, c + 40) for c in col) if hot else col, rect, border_radius=8)
            t = font.render(label, True, (255, 255, 255))
            screen.blit(t, (rect.centerx - t.get_width() // 2, rect.centery - t.get_height() // 2))
        for n, r in num_btns:
            pygame.draw.rect(screen, color_of(n), r, border_radius=4)
            t = font.render(str(n), True, (255, 255, 255))
            screen.blit(t, (r.centerx - t.get_width() // 2, r.centery - t.get_height() // 2))
        pygame.draw.rect(screen, (80, 80, 80), minus, border_radius=6)
        pygame.draw.rect(screen, (80, 80, 80), plus, border_radius=6)
        screen.blit(font.render("-", True, (255, 255, 255)), (minus.x + 18, minus.y + 12))
        screen.blit(font.render("+", True, (255, 255, 255)), (plus.x + 16, plus.y + 12))
        screen.blit(font.render(f"${bet_amt}", True, (255, 255, 255)), (690, 530))

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
