#!/usr/bin/env python3
"""Brick Bros — a tiny Super Mario-inspired platformer. Original fan tribute, not an emulator."""
import pygame

W, H = 960, 540
TILE = 40
GRAVITY = 0.55
JUMP = -11.5


class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 28, 36)
        self.vx = 0
        self.vy = 0
        self.on_ground = False
        self.facing = 1
        self.alive = True
        self.won = False

    def update(self, solids, enemies, coins, goal):
        keys = pygame.key.get_pressed()
        self.vx = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vx = -4.2
            self.facing = -1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vx = 4.2
            self.facing = 1
        if (keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]) and self.on_ground:
            self.vy = JUMP
            self.on_ground = False

        self.vy += GRAVITY
        if self.vy > 14:
            self.vy = 14

        self.rect.x += int(self.vx)
        for s in solids:
            if self.rect.colliderect(s):
                if self.vx > 0:
                    self.rect.right = s.left
                elif self.vx < 0:
                    self.rect.left = s.right

        self.on_ground = False
        self.rect.y += int(self.vy)
        for s in solids:
            if self.rect.colliderect(s):
                if self.vy > 0:
                    self.rect.bottom = s.top
                    self.vy = 0
                    self.on_ground = True
                elif self.vy < 0:
                    self.rect.top = s.bottom
                    self.vy = 0

        for e in enemies:
            if e.alive and self.rect.colliderect(e.rect):
                if self.vy > 0 and self.rect.bottom - e.rect.top < 18:
                    e.alive = False
                    self.vy = JUMP * 0.55
                else:
                    self.alive = False

        got = []
        for i, c in enumerate(coins):
            if self.rect.colliderect(c):
                got.append(i)
        for i in reversed(got):
            coins.pop(i)

        if self.rect.colliderect(goal):
            self.won = True
        if self.rect.top > H + 80:
            self.alive = False


class Walker:
    def __init__(self, x, y, left, right):
        self.rect = pygame.Rect(x, y, 30, 28)
        self.left = left
        self.right = right
        self.dir = 1
        self.alive = True

    def update(self):
        if not self.alive:
            return
        self.rect.x += self.dir * 2
        if self.rect.x <= self.left or self.rect.x >= self.right:
            self.dir *= -1


def build_level():
    solids = []
    for x in range(0, 2400, TILE):
        if 720 <= x <= 800:
            continue
        solids.append(pygame.Rect(x, H - TILE, TILE, TILE))
    platforms = [
        (200, 380, 160),
        (420, 300, 160),
        (680, 360, 80),
        (900, 280, 200),
        (1180, 340, 160),
        (1400, 260, 120),
        (1600, 380, 200),
        (1880, 300, 160),
        (2100, 360, 200),
    ]
    for x, y, w in platforms:
        solids.append(pygame.Rect(x, y, w, 20))
    pipes = [(560, H - TILE - 80, 48, 80), (1040, H - TILE - 120, 48, 120), (1720, H - TILE - 80, 48, 80)]
    for p in pipes:
        solids.append(pygame.Rect(*p))
    coins = [
        pygame.Rect(230, 340, 16, 16),
        pygame.Rect(270, 340, 16, 16),
        pygame.Rect(460, 260, 16, 16),
        pygame.Rect(500, 260, 16, 16),
        pygame.Rect(940, 240, 16, 16),
        pygame.Rect(980, 240, 16, 16),
        pygame.Rect(1020, 240, 16, 16),
        pygame.Rect(1220, 300, 16, 16),
        pygame.Rect(1440, 220, 16, 16),
        pygame.Rect(1640, 340, 16, 16),
        pygame.Rect(1920, 260, 16, 16),
        pygame.Rect(2140, 320, 16, 16),
    ]
    enemies = [
        Walker(300, H - TILE - 28, 40, 540),
        Walker(920, H - TILE - 28, 840, 1020),
        Walker(1280, 340 - 28, 1180, 1320),
        Walker(1640, H - TILE - 28, 1540, 1780),
        Walker(2000, H - TILE - 28, 1920, 2200),
    ]
    goal = pygame.Rect(2280, H - TILE - 140, 16, 140)
    return solids, coins, enemies, goal, pipes


def draw_player(screen, p, cam):
    r = p.rect.move(-cam, 0)
    body = pygame.Rect(r.x + 4, r.y + 10, 20, 20)
    pygame.draw.rect(screen, (220, 40, 40), body)
    pygame.draw.rect(screen, (40, 80, 200), (r.x + 4, r.y + 22, 20, 14))
    pygame.draw.ellipse(screen, (255, 210, 160), (r.x + 6, r.y, 16, 14))
    pygame.draw.rect(screen, (220, 40, 40), (r.x + 4, r.y - 4, 20, 8))
    eye_x = r.x + (18 if p.facing > 0 else 8)
    pygame.draw.circle(screen, (20, 20, 20), (eye_x, r.y + 6), 2)


def main():
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Brick Bros")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("arial", 22, bold=True)
    big = pygame.font.SysFont("arial", 48, bold=True)

    def reset():
        solids, coins, enemies, goal, pipes = build_level()
        player = Player(60, H - TILE - 50)
        return solids, coins, enemies, goal, pipes, player, 0

    solids, coins, enemies, goal, pipes, player, score = reset()
    cam = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return
                if event.key == pygame.K_r:
                    solids, coins, enemies, goal, pipes, player, score = reset()

        prev = len(coins)
        if player.alive and not player.won:
            player.update(solids, enemies, coins, goal)
            for e in enemies:
                e.update()
        score += (prev - len(coins)) * 100
        for e in enemies:
            if not e.alive and getattr(e, "_scored", False) is False:
                score += 200
                e._scored = True

        cam = max(0, min(player.rect.centerx - W // 3, 2400 - W))

        screen.fill((92, 168, 255))
        pygame.draw.circle(screen, (255, 240, 120), (120, 80), 36)
        for i, cx in enumerate((180, 340, 620, 880)):
            pygame.draw.ellipse(screen, (255, 255, 255), (cx - cam * 0.15, 50 + i * 7, 90, 34))

        pygame.draw.ellipse(screen, (60, 170, 80), (40 - cam * 0.2, 360, 280, 160))
        pygame.draw.ellipse(screen, (50, 150, 70), (300 - cam * 0.2, 380, 340, 180))

        for s in solids:
            r = s.move(-cam, 0)
            if r.right < 0 or r.left > W:
                continue
            if s.height == 20:
                pygame.draw.rect(screen, (180, 90, 40), r)
                pygame.draw.rect(screen, (230, 160, 70), r, 2)
            elif s.height > TILE:
                continue
            else:
                pygame.draw.rect(screen, (70, 170, 50), r)
                pygame.draw.line(screen, (40, 120, 30), (r.x, r.y + 8), (r.right, r.y + 8), 6)

        for p in pipes:
            r = pygame.Rect(p).move(-cam, 0)
            pygame.draw.rect(screen, (20, 170, 50), r)
            pygame.draw.rect(screen, (30, 210, 70), (r.x - 6, r.y, r.w + 12, 18))
            pygame.draw.rect(screen, (10, 90, 30), r, 2)

        for c in coins:
            r = c.move(-cam, 0)
            pygame.draw.circle(screen, (255, 210, 40), r.center, 9)
            pygame.draw.circle(screen, (255, 255, 180), r.center, 5)

        for e in enemies:
            if not e.alive:
                continue
            r = e.rect.move(-cam, 0)
            pygame.draw.ellipse(screen, (160, 90, 40), r)
            pygame.draw.circle(screen, (20, 20, 20), (r.x + 8, r.y + 10), 3)
            pygame.draw.circle(screen, (20, 20, 20), (r.x + 20, r.y + 10), 3)

        g = goal.move(-cam, 0)
        pygame.draw.rect(screen, (240, 240, 240), (g.x + 6, g.y, 6, g.h))
        pygame.draw.polygon(screen, (40, 200, 70), [(g.x + 12, g.y), (g.x + 50, g.y + 16), (g.x + 12, g.y + 32)])

        draw_player(screen, player, cam)
        hud = font.render(f"COINS  {score // 100}     SCORE  {score}     R restart   ESC quit", True, (20, 30, 50))
        screen.blit(hud, (16, 12))

        if not player.alive:
            msg = big.render("OUCH — press R", True, (200, 20, 20))
            screen.blit(msg, (W // 2 - msg.get_width() // 2, H // 2 - 30))
        if player.won:
            msg = big.render("WORLD CLEAR!", True, (255, 230, 40))
            screen.blit(msg, (W // 2 - msg.get_width() // 2, H // 2 - 30))

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
