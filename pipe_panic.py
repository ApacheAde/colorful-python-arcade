#!/usr/bin/env python3
"""Pipe Panic — colourful flappy-style runner."""
import random
import pygame

W, H = 480, 720
GRAVITY = 0.38
FLAP = -7.2


def main():
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Pipe Panic")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("arial", 28, bold=True)
    small = pygame.font.SysFont("arial", 16)

    def reset():
        return pygame.Rect(90, H // 2, 34, 28), 0, [], 0, True, 0

    bird, vy, pipes, score, alive, frame = reset()

    while True:
        flap = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return
                if event.key in (pygame.K_SPACE, pygame.K_UP):
                    if not alive:
                        bird, vy, pipes, score, alive, frame = reset()
                    else:
                        flap = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not alive:
                    bird, vy, pipes, score, alive, frame = reset()
                else:
                    flap = True

        if alive:
            if flap:
                vy = FLAP
            vy += GRAVITY
            bird.y += int(vy)
            frame += 1
            if frame % 90 == 0:
                gap_y = random.randint(140, 480)
                pipes.append([W + 10, gap_y, False])
            for p in pipes:
                p[0] -= 3
            pipes[:] = [p for p in pipes if p[0] > -70]
            if bird.top < 0 or bird.bottom > H - 70:
                alive = False
            for p in pipes:
                x, gy, scored = p
                top = pygame.Rect(x, 0, 64, gy - 90)
                bot = pygame.Rect(x, gy + 90, 64, H)
                if bird.colliderect(top) or bird.colliderect(bot):
                    alive = False
                if not scored and x + 64 < bird.left:
                    p[2] = True
                    score += 1

        for y in range(H):
            screen.fill((70 + y // 20, 160 + y // 30, 255 - y // 8), (0, y, W, 1))
        pygame.draw.circle(screen, (255, 230, 90), (380, 90), 40)
        pygame.draw.rect(screen, (40, 170, 70), (0, H - 70, W, 70))
        pygame.draw.rect(screen, (30, 130, 50), (0, H - 78, W, 10))

        for x, gy, _ in pipes:
            pygame.draw.rect(screen, (30, 180, 70), (x, 0, 64, gy - 90))
            pygame.draw.rect(screen, (20, 140, 50), (x - 4, gy - 108, 72, 20))
            pygame.draw.rect(screen, (30, 180, 70), (x, gy + 90, 64, H - (gy + 90) - 70))
            pygame.draw.rect(screen, (20, 140, 50), (x - 4, gy + 90, 72, 20))

        pygame.draw.ellipse(screen, (255, 220, 40), bird)
        pygame.draw.circle(screen, (20, 20, 20), (bird.x + 24, bird.y + 10), 3)
        pygame.draw.polygon(screen, (255, 120, 40), [(bird.right - 2, bird.centery), (bird.right + 10, bird.centery - 4), (bird.right + 10, bird.centery + 4)])

        screen.blit(font.render(str(score), True, (255, 255, 255)), (W // 2 - 10, 20))
        screen.blit(small.render("SPACE / click to flap   https://x.com/ElbowOS", True, (20, 40, 40)), (16, H - 28))
        if not alive:
            t = font.render("CRASH — tap to retry", True, (180, 20, 20))
            screen.blit(t, (W // 2 - t.get_width() // 2, H // 2))

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
