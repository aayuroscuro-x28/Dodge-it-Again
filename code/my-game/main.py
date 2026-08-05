"""Dodge Fall — survive as long as you can. Difficulty ramps up fast."""

import math
import os
import random
import sys
from dataclasses import dataclass
from pathlib import Path

os.environ["SDL_VIDEO_CENTERED"] = "1"

import pygame

WIDTH, HEIGHT = 640, 480
PLAYER_SIZE = 36
BLOCK_SIZE = 28
POWERUP_SIZE = 28
PLAYER_SPEED = 7
POWERUP_DURATION = 5000
HIGHSCORE_FILE = Path(__file__).with_name("highscore.txt")

WHITE = (240, 240, 240)
SKY = (90, 155, 220)
SKY_INTENSE = (60, 110, 180)
SEA = (45, 110, 170)
SEA_HIGHLIGHT = (100, 170, 220)
SAND = (231, 193, 140)
PLAYER_COLOR = (80, 200, 120)
BLOCK_COLOR = (220, 80, 80)
FAST_BLOCK_COLOR = (255, 140, 40)
TEXT_COLOR = (255, 255, 255)
ACCENT = (255, 220, 80)


def create_cat_surface(size: int, color: tuple[int, int, int]) -> pygame.Surface:
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    w, h = size, size
    # Body
    body_color = (min(255, color[0] + 20), min(255, color[1] + 20), min(255, color[2] + 20))
    pygame.draw.ellipse(surf, body_color, (w * 0.15, h * 0.38, w * 0.7, h * 0.5))
    pygame.draw.ellipse(surf, color, (w * 0.12, h * 0.18, w * 0.76, h * 0.6))
    pygame.draw.ellipse(surf, (255, 255, 255), (w * 0.3, h * 0.5, w * 0.4, h * 0.24))
    # Ears
    ear_color = (min(255, color[0] + 20), max(0, color[1] - 30), max(0, color[2] - 10))
    pygame.draw.polygon(surf, ear_color, [(w * 0.18, h * 0.18), (w * 0.08, h * 0.02), (w * 0.32, h * 0.08)])
    pygame.draw.polygon(surf, ear_color, [(w * 0.82, h * 0.18), (w * 0.68, h * 0.08), (w * 0.92, h * 0.02)])
    pygame.draw.polygon(surf, (255, 170, 190), [(w * 0.2, h * 0.1), (w * 0.13, h * 0.04), (w * 0.28, h * 0.08)])
    pygame.draw.polygon(surf, (255, 170, 190), [(w * 0.8, h * 0.1), (w * 0.73, h * 0.04), (w * 0.88, h * 0.08)])
    # Face details
    face_outline = (245, 245, 245)
    pygame.draw.ellipse(surf, face_outline, (w * 0.12, h * 0.16, w * 0.76, h * 0.6), 2)
    eye_y = h * 0.4
    pygame.draw.ellipse(surf, (255, 255, 255), (w * 0.28, eye_y - w * 0.1, w * 0.18, w * 0.18))
    pygame.draw.ellipse(surf, (255, 255, 255), (w * 0.54, eye_y - w * 0.1, w * 0.18, w * 0.18))
    # Nose and mouth
    pygame.draw.polygon(
        surf,
        (255, 140, 175),
        [(w * 0.5, h * 0.52), (w * 0.46, h * 0.57), (w * 0.54, h * 0.57)],
    )
    pygame.draw.arc(
        surf,
        (170, 100, 140),
        (w * 0.38, h * 0.54, w * 0.1, h * 0.08),
        math.pi * 1.05,
        math.pi * 1.9,
        2,
    )
    pygame.draw.arc(
        surf,
        (170, 100, 140),
        (w * 0.52, h * 0.54, w * 0.1, h * 0.08),
        math.pi * 1.2,
        math.pi * 0.1,
        2,
    )
    # Whiskers
    whisker_y = h * 0.55
    pygame.draw.line(surf, (30, 30, 30), (w * 0.12, whisker_y), (w * 0.38, whisker_y - h * 0.02), 2)
    pygame.draw.line(surf, (30, 30, 30), (w * 0.12, whisker_y + h * 0.04), (w * 0.38, whisker_y + h * 0.02), 2)
    pygame.draw.line(surf, (30, 30, 30), (w * 0.62, whisker_y - h * 0.02), (w * 0.88, whisker_y), 2)
    pygame.draw.line(surf, (30, 30, 30), (w * 0.62, whisker_y + h * 0.02), (w * 0.88, whisker_y + h * 0.04), 2)
    # Face highlight
    pygame.draw.circle(surf, (255, 255, 255, 80), (int(w * 0.46), int(h * 0.28)), int(w * 0.1))
    # Base detail stripes
    for i, offset in enumerate([0.18, 0.32, 0.46]):
        pygame.draw.arc(surf, (220, 220, 220), (w * offset, h * 0.24, w * 0.12, h * 0.08), math.pi * 0.8, math.pi * 0.15, 2)
    return surf


def draw_cat(
    screen: pygame.Surface,
    base_surf: pygame.Surface,
    x: int,
    y: int,
    time_ms: int,
    direction: float,
) -> None:
    offset_y = int(math.sin(time_ms * 0.018) * 3)
    blink = (time_ms // 3600) % 10 in (0, 1)
    pupils = pygame.Surface(base_surf.get_size(), pygame.SRCALPHA)
    pupil_x = int(direction * 4)
    pupil_x = max(-4, min(4, pupil_x))
    eye_y = int(base_surf.get_height() * 0.4)
    pygame.draw.circle(pupils, (20, 20, 20), (int(base_surf.get_width() * 0.36) + pupil_x, eye_y), int(base_surf.get_width() * 0.04))
    pygame.draw.circle(pupils, (20, 20, 20), (int(base_surf.get_width() * 0.64) + pupil_x, eye_y), int(base_surf.get_width() * 0.04))

    if blink:
        blink_line = pygame.Surface(base_surf.get_size(), pygame.SRCALPHA)
        blink_y = eye_y
        pygame.draw.line(blink_line, (20, 20, 20), (base_surf.get_width() * 0.28, blink_y), (base_surf.get_width() * 0.38, blink_y), 4)
        pygame.draw.line(blink_line, (20, 20, 20), (base_surf.get_width() * 0.62, blink_y), (base_surf.get_width() * 0.72, blink_y), 4)
        pupils.blit(blink_line, (0, 0))

    draw_surf = base_surf.copy()
    draw_surf.blit(pupils, (0, 0))
    wobble = int(direction * 5)
    screen.blit(draw_surf, (x + wobble, y + offset_y))


def create_sushi_surface(size: int) -> pygame.Surface:
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    rice = pygame.Rect(0, size * 0.18, size, size * 0.64)
    pygame.draw.ellipse(surf, (240, 240, 220), rice)
    pygame.draw.rect(surf, (25, 60, 35), (0, size * 0.4, size, size * 0.28))
    pygame.draw.ellipse(surf, (230, 100, 100), (size * 0.12, size * 0.22, size * 0.76, size * 0.32))
    pygame.draw.ellipse(surf, (255, 190, 120), (size * 0.20, size * 0.26, size * 0.6, size * 0.16))
    for i in range(4):
        seed_x = int(size * (0.26 + i * 0.14))
        seed_y = int(size * 0.46)
        pygame.draw.circle(surf, (245, 220, 120), (seed_x, seed_y), 2)
    return surf


def create_wine_surface(size: int) -> pygame.Surface:
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    bottle_body = pygame.Rect(size * 0.28, size * 0.12, size * 0.44, size * 0.7)
    pygame.draw.rect(surf, (40, 20, 70), bottle_body, border_radius=8)
    pygame.draw.rect(surf, (70, 30, 110), (size * 0.32, size * 0.18, size * 0.36, size * 0.44), border_radius=6)
    pygame.draw.rect(surf, (210, 210, 210), (size * 0.33, size * 0.2, size * 0.34, size * 0.12), border_radius=4)
    pygame.draw.rect(surf, (180, 110, 90), (size * 0.36, size * 0.06, size * 0.28, size * 0.14), border_radius=4)
    pygame.draw.circle(surf, (255, 255, 255, 100), (int(size * 0.56), int(size * 0.24)), int(size * 0.06))
    pygame.draw.rect(surf, (120, 10, 60), (size * 0.32, size * 0.26, size * 0.36, size * 0.24), border_radius=4)
    return surf


def create_cherry_blossom_surface(size: int) -> pygame.Surface:
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    center = (size // 2, size // 2)
    pygame.draw.circle(surf, (255, 195, 220), center, int(size * 0.28))
    for angle in range(0, 360, 72):
        rad = math.radians(angle)
        petal_x = center[0] + int(math.cos(rad) * size * 0.28)
        petal_y = center[1] + int(math.sin(rad) * size * 0.28)
        pygame.draw.ellipse(surf, (245, 145, 200), (petal_x - size * 0.12, petal_y - size * 0.08, size * 0.24, size * 0.16))
    pygame.draw.circle(surf, (255, 235, 240), center, int(size * 0.16))
    pygame.draw.circle(surf, (255, 120, 170), center, int(size * 0.08))
    return surf


@dataclass
class PowerUp:
    rect: pygame.Rect
    effect: str
    duration_ms: int


@dataclass
class Block:
    rect: pygame.Rect
    speed: float
    fast: bool = False


def load_highscore() -> int:
    try:
        return max(0, int(HIGHSCORE_FILE.read_text().strip()))
    except (OSError, ValueError):
        return 0


def save_highscore(score: int) -> None:
    try:
        HIGHSCORE_FILE.write_text(str(score))
    except OSError:
        pass


def difficulty(elapsed_ms: int, dodged: int) -> tuple[int, float, int, int, float]:
    """Return tier, block speed, spawn interval ms, blocks per wave, fast-block chance."""
    seconds = elapsed_ms / 1000
    tier = int(seconds // 6) + dodged // 12

    block_speed = min(4.5 + tier * 1.1, 22.0)
    spawn_ms = max(int(650 - tier * 38), 90)
    blocks_per_wave = 1 + min(tier // 3, 3)
    fast_chance = min(0.05 + tier * 0.04, 0.55)

    return tier, block_speed, spawn_ms, blocks_per_wave, fast_chance


def spawn_wave(
    tier: int,
    block_speed: float,
    fast_chance: float,
    count: int,
    existing: list[Block],
) -> list[Block]:
    new_blocks: list[Block] = []
    occupied = {b.rect.centerx // BLOCK_SIZE for b in existing + new_blocks}

    for _ in range(count):
        slots = [x for x in range(0, WIDTH - BLOCK_SIZE, BLOCK_SIZE) if x // BLOCK_SIZE not in occupied]
        if not slots:
            x = random.randint(0, WIDTH - BLOCK_SIZE)
        else:
            x = random.choice(slots)
            occupied.add(x // BLOCK_SIZE)

        is_fast = random.random() < fast_chance
        speed = block_speed * (1.55 if is_fast else 1.0)
        size = BLOCK_SIZE - 2 if tier >= 8 else BLOCK_SIZE
        new_blocks.append(
            Block(
                rect=pygame.Rect(x, -size - random.randint(0, 80), size, size),
                speed=speed,
                fast=is_fast,
            )
        )
    return new_blocks


def spawn_powerup() -> PowerUp:
    x = random.randint(0, WIDTH - POWERUP_SIZE)
    effect = random.choice(["shield", "speed", "slow"])
    return PowerUp(
        rect=pygame.Rect(x, -POWERUP_SIZE - random.randint(0, 80), POWERUP_SIZE, POWERUP_SIZE),
        effect=effect,
        duration_ms=POWERUP_DURATION,
    )


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Dodge Fall — Reflex Mode")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 36)
    small_font = pygame.font.SysFont(None, 28)
    cat_surf = create_cat_surface(PLAYER_SIZE, PLAYER_COLOR)
    sushi_surf = create_sushi_surface(BLOCK_SIZE)
    wine_surf = create_wine_surface(BLOCK_SIZE)
    blossom_surf = create_cherry_blossom_surface(POWERUP_SIZE)

    highscore = load_highscore()
    player_x = WIDTH // 2 - PLAYER_SIZE // 2
    player_y = HEIGHT - PLAYER_SIZE - 20
    player_direction = 0.0
    blocks: list[Block] = []
    powerups: list[PowerUp] = []
    powerup_spawn_timer = 0
    powerup_spawn_interval = random.randint(9000, 15000)
    active_powerup: str | None = None
    powerup_end_time = 0
    powerup_speed_multiplier = 1.0
    dodged = 0
    spawn_timer = 0
    elapsed = 0
    streak = 0
    best_streak = 0
    game_started = False
    running = True
    game_over = False
    new_record = False

    while running:
        dt = clock.tick(60)
        if not game_over:
            elapsed += dt
            spawn_timer += dt

        tier, block_speed, spawn_ms, wave_size, fast_chance = difficulty(elapsed, dodged)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if game_over and event.key == pygame.K_r:
                    blocks.clear()
                    dodged = 0
                    spawn_timer = 0
                    elapsed = 0
                    streak = 0
                    best_streak = 0
                    tier = 0
                    game_started = False
                    game_over = False
                    new_record = False
                    player_x = WIDTH // 2 - PLAYER_SIZE // 2

        if not game_over:
            keys = pygame.key.get_pressed()
            move = 0.0
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                move -= 1.0
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                move += 1.0
            player_x += move * PLAYER_SPEED
            player_x = max(0, min(WIDTH - PLAYER_SIZE, player_x))
            if move != 0.0:
                player_direction = move

            powerup_spawn_timer += dt
            if powerup_spawn_timer >= powerup_spawn_interval:
                powerup_spawn_timer = 0
                powerup_spawn_interval = random.randint(9000, 15000)
                powerups.append(spawn_powerup())

            if spawn_timer >= spawn_ms:
                spawn_timer = 0
                blocks.extend(spawn_wave(tier, block_speed, fast_chance, wave_size, blocks))

            player_rect = pygame.Rect(player_x, player_y, PLAYER_SIZE, PLAYER_SIZE)
            for powerup in powerups[:]:
                powerup.rect.y += 2
                if powerup.rect.top > HEIGHT:
                    powerups.remove(powerup)
                elif powerup.rect.colliderect(player_rect):
                    active_powerup = powerup.effect
                    powerup_end_time = elapsed + powerup.duration_ms
                    if active_powerup == "speed":
                        powerup_speed_multiplier = 1.6
                    elif active_powerup == "slow":
                        powerup_speed_multiplier = 0.25
                    else:
                        powerup_speed_multiplier = 1.0
                    powerups.remove(powerup)

            for block in blocks[:]:
                block.rect.y += int(block.speed * powerup_speed_multiplier)
                if block.rect.top > HEIGHT:
                    blocks.remove(block)
                    dodged += 1
                    streak += 1
                    best_streak = max(best_streak, streak)
                elif block.rect.colliderect(player_rect):
                    if active_powerup == "shield":
                        blocks.remove(block)
                    else:
                        game_over = True
                        streak = 0
                        if dodged > highscore:
                            highscore = dodged
                            save_highscore(highscore)
                            new_record = True

            if active_powerup and elapsed >= powerup_end_time:
                active_powerup = None
                powerup_speed_multiplier = 1.0

        score = dodged + streak // 5
        sky_color = SKY_INTENSE if tier >= 6 else SKY
        if tier >= 10 and pygame.time.get_ticks() % 400 < 200:
            sky_color = (max(0, sky_color[0] - 8), max(0, sky_color[1] - 10), min(255, sky_color[2] + 16))

        screen.fill(sky_color)
        pygame.draw.rect(screen, SEA, (0, HEIGHT * 0.45, WIDTH, HEIGHT * 0.35))
        for i in range(5):
            wave_y = HEIGHT * 0.45 + i * 14
            pygame.draw.arc(screen, SEA_HIGHLIGHT, (0, wave_y, WIDTH, 28), 0, math.pi, 2)
        pygame.draw.rect(screen, SAND, (0, HEIGHT * 0.78, WIDTH, HEIGHT * 0.22))
        player_rect = pygame.Rect(player_x, player_y, PLAYER_SIZE, PLAYER_SIZE)
        draw_cat(screen, cat_surf, player_x, player_y, pygame.time.get_ticks(), player_direction)
        for powerup in powerups:
            screen.blit(blossom_surf, powerup.rect.topleft)
        for block in blocks:
            if block.fast:
                screen.blit(wine_surf, block.rect.topleft)
            else:
                screen.blit(sushi_surf, block.rect.topleft)

        screen.blit(font.render(f"Score: {score}", True, TEXT_COLOR), (16, 12))
        screen.blit(small_font.render(f"Best: {highscore}", True, ACCENT), (16, 46))
        screen.blit(small_font.render(f"Tier {tier + 1}", True, TEXT_COLOR), (WIDTH - 100, 12))
        screen.blit(small_font.render(f"Streak: {streak}", True, TEXT_COLOR), (WIDTH - 130, 40))
        if active_powerup:
            remaining = max(0, (powerup_end_time - elapsed) // 1000)
            label = f"Cherry Power: {active_powerup.title()} ({remaining}s)"
            screen.blit(small_font.render(label, True, ACCENT), (WIDTH // 2 - 130, 40))

        time_sec = elapsed // 1000
        screen.blit(small_font.render(f"Time: {time_sec}s", True, TEXT_COLOR), (WIDTH // 2 - 40, 12))

        if game_over:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 140))
            screen.blit(overlay, (0, 0))
            lines = [
                "GAME OVER",
                f"Score: {score}  |  Time: {time_sec}s  |  Tier {tier + 1}",
                f"Best streak: {best_streak}",
            ]
            if new_record:
                lines.append("NEW HIGH SCORE!")
            lines.append("Press R to retry  |  Esc to quit")
            y = HEIGHT // 2 - 70
            for i, line in enumerate(lines):
                color = ACCENT if "NEW HIGH" in line else WHITE
                f = font if i == 0 else small_font
                text = f.render(line, True, color)
                screen.blit(text, (WIDTH // 2 - text.get_width() // 2, y + i * 34))

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
