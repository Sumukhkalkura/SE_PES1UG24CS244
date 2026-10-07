import pygame


class Rope:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.center_y = screen_height // 2
        self.marker_x = screen_width // 2

        self.left_win_x = 180
        self.right_win_x = screen_width - 180

        self.pull_step = 12

    def pull_left(self, strength=1.0):
        self.marker_x -= int(self.pull_step * strength)

    def pull_right(self, strength=1.0):
        self.marker_x += int(self.pull_step * strength)

    def check_winner(self):
        if self.marker_x <= self.left_win_x:
            return "PLAYER"
        if self.marker_x >= self.right_win_x:
            return "COMPUTER"
        return None

    def reset(self):
        self.marker_x = float(self.screen_width // 2)
        self.velocity = 0.0

    def render(self, surface, tension=0.0):
        # Animated rope vibration.
        # Higher tension makes the rope vibrate more strongly.
        time = pygame.time.get_ticks()
        vibration = int(4 * tension)

        rope_points = []

        for x in range(60, self.screen_width - 59, 20):
            offset = 0

            if vibration > 0:
                phase = (x // 20 + time // 60) % 2
                offset = vibration if phase == 0 else -vibration

            rope_points.append((x, self.center_y + offset))

        pygame.draw.lines(
            surface,
            (180, 140, 90),
            False,
            rope_points,
            10
        )

        # Player winning line
        pygame.draw.line(
            surface,
            (50, 200, 50),
            (self.left_win_x, self.center_y - 40),
            (self.left_win_x, self.center_y + 40),
            4
        )

        # Computer winning line
        pygame.draw.line(
            surface,
            (200, 50, 50),
            (self.right_win_x, self.center_y - 40),
            (self.right_win_x, self.center_y + 40),
            4
        )

        # Center line
        pygame.draw.line(
            surface,
            (120, 120, 120),
            (self.screen_width // 2, self.center_y - 20),
            (self.screen_width // 2, self.center_y + 20),
            2
        )

        # Rope marker / flag
        flag_rect = pygame.Rect(
            int(self.marker_x) - 12,
            self.center_y - 24,
            24,
            48
        )

        pygame.draw.rect(
            surface,
            (230, 40, 40),
            flag_rect,
            border_radius=4
        )

        pygame.draw.rect(
            surface,
            (255, 255, 255),
            flag_rect,
            width=2,
            border_radius=4
        )