#!/usr/bin/env python3
"""Lucky Slots — three-reel colour slot machine."""
import random
import pygame

W, H = 820, 620
SYMBOLS = [
    ("CHERRY", (220, 30, 50), 5),
    ("LEMON", (240, 210, 40), 8),
    ("BELL", (255, 180, 40), 12),
    ("STAR", (80, 180, 255), 18),
    ("SEVEN", (255, 40, 80), 40),
    ("DIAMOND", (180, 80, 255), 80),
]


def payout(reels, bet):
    a, b, c = (s[0] for s in reels)
    if a == b == c:
        mult = {s[0]: s[2] for s in SYMBOLS}[a]
        return bet * mult, f"THREE {a}s!"
    if a == b or b == c or a == c:
        return bet * 2, "PAIR PAYS"
    return 0, "No luck"


def main():
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Lucky Slots")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("arial", 22, bold=True)
    huge = pygame.font.SysFont("arial", 34, bold=True)
    small = pygame.font.SysFont("arial", 16)

    bank = 200
    bet = 10
    reels = [SYMBOLS[0], SYMBOLS[1], SYMBOLS[2]]
    spinning = 0
    msg = "Press SPIN"
    last_win = 0

    spin_btn = pygame.Rect(310, 500, 200, 56)
    minus = pygame.Rect(80, 500, 60, 56)
    plus = pygame.Rect(180, 500, 60, 56)

    while True:
        mx, my = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and spinning == 0:
                if minus.collidepoint(mx, my):
                    bet = max(5, bet - 5)
                if plus.collidepoint(mx, my):
                    bet = min(25, bet + 5)
                if spin_btn.collidepoint(mx, my) and bank >= bet:
                    bank -= bet
                    spinning = 28
                    msg = "Good luck..."

        if spinning:
            reels = [random.choice(SYMBOLS) for _ in range(3)]
            spinning -= 1
            if spinning == 0:
                last_win, msg = payout(reels, bet)
                bank += last_win

        screen.fill((20, 8, 40))
        pygame.draw.rect(screen, (90, 20, 70), (0, 0, W, 90))
        screen.blit(huge.render("LUCKY SLOTS", True, (255, 210, 60)), (40, 24))
        screen.blit(small.render("https://x.com/ElbowOS", True, (230, 180, 255)), (620, 36))

        pygame.draw.rect(screen, (180, 140, 40), (70, 120, 680, 280), border_radius=20)
        pygame.draw.rect(screen, (30, 10, 40), (90, 140, 640, 240), border_radius=12)

        for i, sym in enumerate(reels):
            box = pygame.Rect(120 + i * 200, 165, 170, 190)
            pygame.draw.rect(screen, (15, 10, 30), box, border_radius=12)
            pygame.draw.rect(screen, sym[1], box.inflate(-20, -20), border_radius=10)
            label = font.render(sym[0], True, (255, 255, 255))
            screen.blit(label, (box.centerx - label.get_width() // 2, box.centery - 10))

        screen.blit(font.render(f"BANK  ${bank}", True, (255, 255, 255)), (80, 430))
        screen.blit(font.render(f"BET  ${bet}", True, (255, 230, 80)), (300, 430))
        col = (80, 255, 120) if last_win else (255, 200, 80)
        screen.blit(font.render(msg, True, col), (480, 430))

        def btn(rect, text):
            hot = rect.collidepoint(mx, my)
            pygame.draw.rect(screen, (255, 200, 50) if hot else (160, 30, 90), rect, border_radius=12)
            t = font.render(text, True, (20, 10, 20) if hot else (255, 255, 255))
            screen.blit(t, (rect.centerx - t.get_width() // 2, rect.centery - t.get_height() // 2))

        btn(minus, "-")
        btn(plus, "+")
        btn(spin_btn, "SPIN")

        pygame.display.flip()
        clock.tick(30 if spinning else 60)


if __name__ == "__main__":
    main()
