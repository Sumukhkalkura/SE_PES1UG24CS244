import random

import pygame

from game.rope import Rope
from game.player import Puller


class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.rope = Rope(width, height)

        self.player = Puller(
            90,
            height // 2,
            (50, 120, 220),
            "PLAYER (A/D)"
        )

        self.computer = Puller(
            width - 90,
            height // 2,
            (220, 80, 50),
            "COMPUTER"
        )

        self.last_key = None
        self.is_pull_locked = False

        self.winner = None
        self.game_state = "PLAYING"

        # Task 4: 45-second timer and Sudden Death
        self.match_duration = 45000
        self.match_start_time = pygame.time.get_ticks()
        self.sudden_death = False

        self.computer_pull_cooldown = 180
        self.last_computer_pull = pygame.time.get_ticks()

        self.font_big = pygame.font.SysFont(None, 48)
        self.font_small = pygame.font.SysFont(None, 26)

    def handle_event(self, event):
        if self.game_state != "PLAYING":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self.reset()
            return

        # Task 1: Reliable alternating A/D input
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_a, pygame.K_d):
                if event.key != self.last_key:

                    # Task 4:
                    # Player pulling power doubles in Sudden Death
                    player_strength = (
                        2.0 if self.sudden_death else 1.0
                    )

                    self.rope.pull_left(player_strength)
                    self.last_key = event.key

    def update(self):
        if self.game_state != "PLAYING":
            return

        now = pygame.time.get_ticks()

        # Task 4:
        # Enter Sudden Death after 45 seconds.
        elapsed_time = now - self.match_start_time

        if elapsed_time >= self.match_duration:
            self.sudden_death = True

        # Task 2:
        # Dynamic AI Panic Surge.
        # When the player approaches the green winning line,
        # the computer reacts faster and more aggressively.
        panic_threshold = self.rope.left_win_x + 100
        panic_mode = self.rope.marker_x <= panic_threshold

        if panic_mode:
            computer_cooldown = 90
            computer_variance = random.uniform(1.0, 1.5)
        else:
            computer_cooldown = self.computer_pull_cooldown
            computer_variance = random.uniform(0.7, 1.2)

        # Task 4:
        # Computer pulling POWER doubles during Sudden Death.
        # Its cooldown is left unchanged so Task 2 still controls
        # how frequently the computer pulls.
        if self.sudden_death:
            computer_variance *= 2.0

        if now - self.last_computer_pull >= computer_cooldown:
            self.rope.pull_right(computer_variance)
            self.last_computer_pull = now

        # Existing win detection
        result = self.rope.check_winner()

        if result:
            self.winner = result
            self.game_state = "GAME_OVER"

    def reset(self):
        # Reset rope position
        self.rope.reset()

        # Reset input
        self.last_key = None
        self.is_pull_locked = False

        # Reset game state
        self.winner = None
        self.game_state = "PLAYING"

        # Task 4:
        # Start a fresh regulation period
        self.sudden_death = False
        self.match_start_time = pygame.time.get_ticks()

        # Reset computer timing
        self.last_computer_pull = pygame.time.get_ticks()

    def render(self, screen):
        screen.fill((30, 32, 36))

        # Mud / center area
        mud_rect = pygame.Rect(
            self.width // 2 - 120,
            self.height // 2 - 80,
            240,
            160
        )

        pygame.draw.rect(
            screen,
            (45, 38, 30),
            mud_rect,
            border_radius=12
        )

        # Task 3:
        # Calculate visual tension based on how far the
        # rope marker is from the center.
        center_x = self.width // 2
        max_distance = center_x - self.rope.left_win_x
        current_distance = abs(
            self.rope.marker_x - center_x
        )

        tension = min(
            current_distance / max_distance,
            1.0
        )

        # Task 3: animated rope
        self.rope.render(screen, tension)

        # Task 3: puller leaning
        lean_amount = int(10 * tension)

        self.player.render(
            screen,
            -lean_amount
        )

        self.computer.render(
            screen,
            lean_amount
        )

        # Existing instruction text
        inst_surf = self.font_small.render(
            "Alternate [A] and [D] keys rapidly to pull!",
            True,
            (210, 210, 210)
        )

        screen.blit(
            inst_surf,
            (
                self.width // 2 - inst_surf.get_width() // 2,
                40
            )
        )

        # Task 4:
        # Calculate remaining regulation time.
        now = pygame.time.get_ticks()
        elapsed_time = now - self.match_start_time
        remaining_time = max(
            0,
            self.match_duration - elapsed_time
        )

        # Round upward so a new match visibly begins at 45.
        seconds_remaining = (
            remaining_time + 999
        ) // 1000

        timer_surf = self.font_small.render(
            f"Time: {seconds_remaining}",
            True,
            (240, 240, 240)
        )

        screen.blit(
            timer_surf,
            (
                self.width // 2
                - timer_surf.get_width() // 2,
                70
            )
        )

        # Task 4:
        # Clearly display Sudden Death once regulation expires.
        if self.sudden_death and self.game_state == "PLAYING":
            sudden_death_surf = self.font_big.render(
                "SUDDEN DEATH",
                True,
                (255, 80, 80)
            )

            screen.blit(
                sudden_death_surf,
                (
                    self.width // 2
                    - sudden_death_surf.get_width() // 2,
                    100
                )
            )

        # Existing Game Over screen
        if self.game_state == "GAME_OVER":
            overlay = pygame.Surface(
                (self.width, self.height),
                pygame.SRCALPHA
            )

            overlay.fill((0, 0, 0, 180))
            screen.blit(overlay, (0, 0))

            win_text = f"{self.winner} WINS!"

            color = (
                (80, 220, 80)
                if self.winner == "PLAYER"
                else (240, 80, 80)
            )

            text_surf = self.font_big.render(
                win_text,
                True,
                color
            )

            screen.blit(
                text_surf,
                (
                    self.width // 2
                    - text_surf.get_width() // 2,
                    self.height // 2 - 50
                )
            )

            restart_surf = self.font_small.render(
                "Press [R] to Play Again",
                True,
                (240, 240, 240)
            )

            screen.blit(
                restart_surf,
                (
                    self.width // 2
                    - restart_surf.get_width() // 2,
                    self.height // 2 + 10
                )
            )