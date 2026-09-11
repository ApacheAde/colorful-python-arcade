#!/usr/bin/env python3
"""Star Blaster — colourful space shooter. Arrow keys move, space fires."""
import random
import pygame

W, H = 480, 720


def main():
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Star Blaster")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("arial", 22, bold=True)
    big = pygame.font.SysFont("arial", 40, bold=True)
    small = pygame.font.SysFont("arial", 16)

    def reset():
        return {
            "px": W // 2,
            "py": H - 70,
            "bullets": [],
            "enemies": [],
            "stars": [[random.randrange(W), random.randrange(H), random.uniform(1, 3)] for _ in range(70)],
            "cooldown": 0,
            "spawn": 0,
            "score": 0,
            "lives": 3,
            "alive": True,
        }

    g = reset()

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
                    g = reset()

        keys = pygame.key.get_pressed()
        if g["alive"]:
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                g["px"] = max(24, g["px"] - 6)
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                g["px"] = min(W - 24, g["px"] + 6)
            if g["cooldown"] > 0:
                g["cooldown"] -= 1
            if (keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]) and g["cooldown"] == 0:
                g["bullets"].append([g["px"], g["py"] - 20])
                g["cooldown"] = 10

            g["spawn"] -= 1
            if g["spawn"] <= 0:
                g["enemies"].append([random.randint(30, W - 30), -20, random.choice((3, 3, 4, 5))])
                g["spawn"] = max(18, 50 - g["score"] // 80)

            for b in g["bullets"]:
                b[1] -= 10
            g["bullets"] = [b for b in g["bullets"] if b[1] > -10]

            ship = pygame.Rect(g["px"] - 16, g["py"] - 12, 32, 28)
            kept = []
            for e in g["enemies"]:
                e[1] += e[2]
                hit = False
                er = pygame.Rect(e[0] - 16, e[1] - 12, 32, 24)
                for b in g["bullets"]:
                    if er.collidepoint(b[0], b[1]):
                        hit = True
                        g["score"] += 10
                        b[1] = -99
                        break
                if hit:
                    continue
                if er.colliderect(ship):
                    g["lives"] -= 1
                    continue
                if e[1] < H + 30:
                    kept.append(e)
            g["enemies"] = kept
            if g["lives"] <= 0:
                g["alive"] = False

        for s in g["stars"]:
            s[1] += s[2]
            if s[1] > H:
                s[0] = random.randrange(W)
                s[1] = 0

        screen.fill((8, 10, 28))
        for s in g["stars"]:
            pygame.draw.circle(screen, (200, 220, 255), (int(s[0]), int(s[1])), 1 if s[2] < 2 else 2)

        for b in g["bullets"]:
            pygame.draw.rect(screen, (80, 255, 180), (b[0] - 2, b[1] - 10, 4, 14))

        for e in g["enemies"]:
            pts = [(e[0], e[1] + 14), (e[0] - 16, e[1] - 12), (e[0] + 16, e[1] - 12)]
            pygame.draw.polygon(screen, (255, 70, 90), pts)
            pygame.draw.polygon(screen, (255, 200, 80), pts, 2)

        if g["alive"]:
            nose = (g["px"], g["py"] - 22)
            pygame.draw.polygon(
                screen,
                (70, 200, 255),
                [nose, (g["px"] - 18, g["py"] + 16), (g["px"] + 18, g["py"] + 16)],
            )
            pygame.draw.rect(screen, (255, 180, 60), (g["px"] - 4, g["py"] + 16, 8, 10))

        hud = font.render(f"SCORE {g['score']}    LIVES {max(0, g['lives'])}", True, (255, 230, 120))
        screen.blit(hud, (16, 12))
        tip = small.render("Arrows / AD move  Space fire  R restart  https://x.com/ElbowOS", True, (160, 170, 220))
        screen.blit(tip, (16, H - 28))
        if not g["alive"]:
            msg = big.render("SHIP DOWN", True, (255, 80, 80))
            screen.blit(msg, (W // 2 - msg.get_width() // 2, H // 2 - 30))
            again = font.render("Press R", True, (255, 255, 255))
            screen.blit(again, (W // 2 - again.get_width() // 2, H // 2 + 20))

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
