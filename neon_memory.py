#!/usr/bin/env python3
"""Neon Memory — colourful pair-matching card game."""
import random
import pygame

W, H = 900, 640
COLS, ROWS = 4, 4
GAP = 16
MARGIN_X, MARGIN_Y = 70, 110
CARD_W = (W - 2 * MARGIN_X - GAP * (COLS - 1)) // COLS
CARD_H = (H - MARGIN_Y - 50 - GAP * (ROWS - 1)) // ROWS

SYMBOLS = [
    ("\u2605", (255, 220, 60)),
    ("\u2665", (255, 70, 110)),
    ("\u2666", (255, 120, 40)),
    ("\u25cf", (80, 200, 255)),
    ("\u25a0", (160, 90, 255)),
    ("\u25b2", (90, 230, 130)),
    ("\u273f", (255, 150, 200)),
    ("\u2600", (255, 180, 40)),
]


def deal():
    pack = SYMBOLS * 2
    random.shuffle(pack)
    return pack


def main():
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Neon Memory")
    clock = pygame.time.Clock()
    title = pygame.font.SysFont("arial", 36, bold=True)
    face = pygame.font.SysFont("arial", 56, bold=True)
    body = pygame.font.SysFont("arial", 20, bold=True)
    small = pygame.font.SysFont("arial", 16)

    board = deal()
    revealed = [False] * 16
    matched = [False] * 16
    first = None
    lock_until = 0
    pending = None
    moves = 0
    won = False

    def rect_at(i):
        c, r = i % COLS, i // COLS
        return pygame.Rect(
            MARGIN_X + c * (CARD_W + GAP),
            MARGIN_Y + r * (CARD_H + GAP),
            CARD_W,
            CARD_H,
        )

    while True:
        now = pygame.time.get_ticks()
        if pending and now >= lock_until:
            a, b = pending
            if board[a][0] != board[b][0]:
                revealed[a] = revealed[b] = False
            else:
                matched[a] = matched[b] = True
            pending = None
            first = None
            if all(matched):
                won = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return
                if event.key == pygame.K_n:
                    board = deal()
                    revealed = [False] * 16
                    matched = [False] * 16
                    first = pending = None
                    moves = 0
                    won = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not pending and not won:
                pos = pygame.mouse.get_pos()
                for i in range(16):
                    if not matched[i] and not revealed[i] and rect_at(i).collidepoint(pos):
                        revealed[i] = True
                        if first is None:
                            first = i
                        else:
                            moves += 1
                            pending = (first, i)
                            lock_until = now + 650
                        break

        screen.fill((12, 16, 36))
        pygame.draw.rect(screen, (40, 20, 80), (0, 0, W, 88))
        t = title.render("NEON MEMORY", True, (180, 220, 255))
        screen.blit(t, (28, 16))
        s = small.render("Match the pairs   N new game   ESC quit   https://x.com/ElbowOS", True, (200, 180, 255))
        screen.blit(s, (28, 58))
        m = body.render(f"MOVES  {moves}", True, (255, 230, 80))
        screen.blit(m, (W - 180, 28))

        for i in range(16):
            r = rect_at(i)
            if matched[i] or revealed[i]:
                pygame.draw.rect(screen, (30, 28, 50), r, border_radius=14)
                pygame.draw.rect(screen, board[i][1], r, 4, border_radius=14)
                glyph = face.render(board[i][0], True, board[i][1])
                screen.blit(glyph, (r.centerx - glyph.get_width() // 2, r.centery - glyph.get_height() // 2))
            else:
                pygame.draw.rect(screen, (70, 50, 160), r, border_radius=14)
                pygame.draw.rect(screen, (160, 120, 255), r, 3, border_radius=14)
                q = face.render("?", True, (220, 200, 255))
                screen.blit(q, (r.centerx - q.get_width() // 2, r.centery - q.get_height() // 2))

        if won:
            banner = pygame.Rect(150, 280, 600, 90)
            pygame.draw.rect(screen, (20, 80, 50), banner, border_radius=16)
            msg = title.render(f"CLEARED IN {moves} MOVES", True, (255, 240, 80))
            screen.blit(msg, (W // 2 - msg.get_width() // 2, 300))

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
