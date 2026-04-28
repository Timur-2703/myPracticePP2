import pygame
import random
import json
from db import save_result, get_top_scores, get_personal_best

WIDTH, HEIGHT = 600, 600
CELL = 20
FPS = 10

WHITE = (255, 255, 255)
BLACK = (20, 20, 20)
GRAY = (50, 50, 50)
GREEN = (0, 255, 0)
RED = (220, 40, 40)
DARK_RED = (120, 0, 0)
BLUE = (0, 120, 255)
YELLOW = (255, 220, 0)
PURPLE = (180, 80, 255)


class SnakeGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("TSIS4 Snake")
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = "menu"

        self.username = ""
        self.input_active = True

        self.load_settings()
        self.reset_game()

    def load_settings(self):
        try:
            with open("settings.json", "r") as f:
                self.settings = json.load(f)
        except:
            self.settings = {
                "snake_color": [0, 255, 0],
                "grid": True,
                "sound": False
            }

    def save_settings(self):
        with open("settings.json", "w") as f:
            json.dump(self.settings, f, indent=4)

    def reset_game(self):
        self.snake = [(300, 300), (280, 300), (260, 300)]
        self.direction = (CELL, 0)
        self.next_direction = (CELL, 0)

        self.score = 0
        self.level = 1
        self.food_eaten = 0
        self.saved = False

        self.obstacles = []

        self.food = self.random_empty_cell()
        self.poison = self.random_empty_cell()

        self.powerup = None
        self.powerup_type = None
        self.powerup_spawn_time = 0
        self.active_powerup = None
        self.powerup_end_time = 0

    def random_empty_cell(self):
        while True:
            x = random.randrange(0, WIDTH, CELL)
            y = random.randrange(0, HEIGHT, CELL)
            pos = (x, y)

            if pos not in self.snake and pos not in self.obstacles:
                return pos

    def spawn_powerup(self):
        if self.powerup is None:
            self.powerup = self.random_empty_cell()
            self.powerup_type = random.choice(["speed", "slow", "shield"])
            self.powerup_spawn_time = pygame.time.get_ticks()

    def generate_obstacles(self):
        self.obstacles = []

        if self.level < 3:
            return

        count = min(5 + self.level, 15)

        while len(self.obstacles) < count:
            pos = self.random_empty_cell()

            head = self.snake[0]
            distance = abs(pos[0] - head[0]) + abs(pos[1] - head[1])

            if distance > 80 and pos != self.food and pos != self.poison:
                self.obstacles.append(pos)

    def draw_text(self, text, x, y, size=28, color=WHITE):
        font = pygame.font.SysFont(None, size)
        img = font.render(text, True, color)
        self.screen.blit(img, (x, y))

    def draw_button(self, text, x, y, w, h):
        rect = pygame.Rect(x, y, w, h)
        pygame.draw.rect(self.screen, GRAY, rect)
        pygame.draw.rect(self.screen, WHITE, rect, 2)

        font = pygame.font.SysFont(None, 30)
        img = font.render(text, True, WHITE)
        self.screen.blit(img, (
            x + (w - img.get_width()) // 2,
            y + (h - img.get_height()) // 2
        ))

        return rect

    def handle_menu_click(self, pos):
        play = pygame.Rect(200, 230, 200, 45)
        leaderboard = pygame.Rect(200, 290, 200, 45)
        settings = pygame.Rect(200, 350, 200, 45)
        quit_btn = pygame.Rect(200, 410, 200, 45)

        if play.collidepoint(pos) and self.username.strip():
            self.personal_best = get_personal_best(self.username)
            self.reset_game()
            self.personal_best = get_personal_best(self.username)
            self.state = "game"

        elif leaderboard.collidepoint(pos):
            self.state = "leaderboard"

        elif settings.collidepoint(pos):
            self.state = "settings"

        elif quit_btn.collidepoint(pos):
            self.running = False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if self.state == "menu":
                    if event.key == pygame.K_BACKSPACE:
                        self.username = self.username[:-1]
                    elif event.key == pygame.K_RETURN:
                        if self.username.strip():
                            self.personal_best = get_personal_best(self.username)
                            self.reset_game()
                            self.personal_best = get_personal_best(self.username)
                            self.state = "game"
                    else:
                        if len(self.username) < 12 and event.unicode.isprintable():
                            self.username += event.unicode

                elif self.state == "game":
                    if event.key == pygame.K_UP and self.direction != (0, CELL):
                        self.next_direction = (0, -CELL)
                    elif event.key == pygame.K_DOWN and self.direction != (0, -CELL):
                        self.next_direction = (0, CELL)
                    elif event.key == pygame.K_LEFT and self.direction != (CELL, 0):
                        self.next_direction = (-CELL, 0)
                    elif event.key == pygame.K_RIGHT and self.direction != (-CELL, 0):
                        self.next_direction = (CELL, 0)

                elif self.state == "game_over":
                    if event.key == pygame.K_r:
                        self.reset_game()
                        self.personal_best = get_personal_best(self.username)
                        self.state = "game"
                    elif event.key == pygame.K_m:
                        self.state = "menu"

                elif self.state in ["leaderboard", "settings"]:
                    if event.key == pygame.K_ESCAPE:
                        self.state = "menu"

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.state == "menu":
                    self.handle_menu_click(event.pos)

                elif self.state == "settings":
                    self.handle_settings_click(event.pos)

    def handle_settings_click(self, pos):
        grid_btn = pygame.Rect(180, 220, 240, 45)
        color_btn = pygame.Rect(180, 280, 240, 45)
        sound_btn = pygame.Rect(180, 340, 240, 45)
        back_btn = pygame.Rect(180, 420, 240, 45)

        if grid_btn.collidepoint(pos):
            self.settings["grid"] = not self.settings["grid"]
            self.save_settings()

        elif color_btn.collidepoint(pos):
            colors = [[0, 255, 0], [0, 180, 255], [255, 120, 0], [180, 80, 255]]
            current = self.settings["snake_color"]
            index = colors.index(current) if current in colors else 0
            self.settings["snake_color"] = colors[(index + 1) % len(colors)]
            self.save_settings()

        elif sound_btn.collidepoint(pos):
            self.settings["sound"] = not self.settings["sound"]
            self.save_settings()

        elif back_btn.collidepoint(pos):
            self.state = "menu"

    def update_game(self):
        self.direction = self.next_direction
        head_x, head_y = self.snake[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)

        now = pygame.time.get_ticks()

        if self.active_powerup in ["speed", "slow"] and now > self.powerup_end_time:
            self.active_powerup = None

        if self.powerup and now - self.powerup_spawn_time > 8000:
            self.powerup = None
            self.powerup_type = None

        if random.randint(1, 120) == 1:
            self.spawn_powerup()

        hit_wall = (
            new_head[0] < 0 or new_head[0] >= WIDTH or
            new_head[1] < 0 or new_head[1] >= HEIGHT
        )

        hit_self = new_head in self.snake
        hit_obstacle = new_head in self.obstacles

        if hit_wall or hit_self or hit_obstacle:
            if self.active_powerup == "shield":
                self.active_powerup = None
                return
            self.state = "game_over"
            self.save_game_result()
            return

        self.snake.insert(0, new_head)

        if new_head == self.food:
            self.score += 10
            self.food_eaten += 1
            self.food = self.random_empty_cell()

            if self.food_eaten % 3 == 0:
                self.level += 1
                self.generate_obstacles()

        elif new_head == self.poison:
            self.score = max(0, self.score - 5)

            for _ in range(2):
                if len(self.snake) > 1:
                    self.snake.pop()

            self.poison = self.random_empty_cell()

            if len(self.snake) <= 1:
                self.state = "game_over"
                self.save_game_result()
                return
        else:
            self.snake.pop()

        if self.powerup and new_head == self.powerup:
            self.active_powerup = self.powerup_type

            if self.powerup_type == "speed":
                self.powerup_end_time = now + 5000
            elif self.powerup_type == "slow":
                self.powerup_end_time = now + 5000

            self.powerup = None
            self.powerup_type = None

    def save_game_result(self):
        if not self.saved and self.username.strip():
            save_result(self.username, self.score, self.level)
            self.saved = True
            self.personal_best = get_personal_best(self.username)

    def draw_grid(self):
        if not self.settings.get("grid", True):
            return

        for x in range(0, WIDTH, CELL):
            pygame.draw.line(self.screen, (35, 35, 35), (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, CELL):
            pygame.draw.line(self.screen, (35, 35, 35), (0, y), (WIDTH, y))

    def draw_game(self):
        self.screen.fill(BLACK)
        self.draw_grid()

        snake_color = tuple(self.settings.get("snake_color", [0, 255, 0]))

        for segment in self.snake:
            pygame.draw.rect(self.screen, snake_color, (*segment, CELL, CELL))

        pygame.draw.rect(self.screen, RED, (*self.food, CELL, CELL))
        pygame.draw.rect(self.screen, DARK_RED, (*self.poison, CELL, CELL))

        for obs in self.obstacles:
            pygame.draw.rect(self.screen, GRAY, (*obs, CELL, CELL))

        if self.powerup:
            color = BLUE
            if self.powerup_type == "slow":
                color = PURPLE
            elif self.powerup_type == "shield":
                color = YELLOW
            pygame.draw.rect(self.screen, color, (*self.powerup, CELL, CELL))

        self.draw_text(f"User: {self.username}", 10, 10, 22)
        self.draw_text(f"Score: {self.score}", 10, 35, 22)
        self.draw_text(f"Level: {self.level}", 10, 60, 22)
        self.draw_text(f"Best: {self.personal_best}", 10, 85, 22)

        if self.active_powerup:
            self.draw_text(f"Power: {self.active_powerup}", 410, 10, 22)

    def draw_menu(self):
        self.screen.fill(BLACK)
        self.draw_text("TSIS4 SNAKE", 190, 110, 42)
        self.draw_text("Enter username:", 190, 170, 26)
        self.draw_text(self.username + "|", 230, 200, 26)

        self.draw_button("Play", 200, 230, 200, 45)
        self.draw_button("Leaderboard", 200, 290, 200, 45)
        self.draw_button("Settings", 200, 350, 200, 45)
        self.draw_button("Quit", 200, 410, 200, 45)

    def draw_game_over(self):
        self.screen.fill(BLACK)
        self.draw_text("GAME OVER", 190, 170, 42)
        self.draw_text(f"Score: {self.score}", 220, 230, 30)
        self.draw_text(f"Level: {self.level}", 220, 270, 30)
        self.draw_text(f"Best: {self.personal_best}", 220, 310, 30)
        self.draw_text("Press R to Retry", 185, 370, 28)
        self.draw_text("Press M for Menu", 185, 410, 28)

    def draw_leaderboard(self):
        self.screen.fill(BLACK)
        self.draw_text("TOP 10 LEADERBOARD", 150, 60, 34)

        try:
            scores = get_top_scores()
        except:
            scores = []

        y = 120
        for i, row in enumerate(scores):
            username, score, level, date = row
            self.draw_text(f"{i+1}. {username} | {score} | L{level}", 120, y, 24)
            y += 35

        self.draw_text("ESC - Back", 230, 540, 24)

    def draw_settings(self):
        self.screen.fill(BLACK)
        self.draw_text("SETTINGS", 220, 120, 40)

        grid_text = f"Grid: {'ON' if self.settings.get('grid') else 'OFF'}"
        sound_text = f"Sound: {'ON' if self.settings.get('sound') else 'OFF'}"

        self.draw_button(grid_text, 180, 220, 240, 45)
        self.draw_button("Change snake color", 180, 280, 240, 45)
        self.draw_button(sound_text, 180, 340, 240, 45)
        self.draw_button("Save & Back", 180, 420, 240, 45)

    def draw(self):
        if self.state == "menu":
            self.draw_menu()
        elif self.state == "game":
            self.draw_game()
        elif self.state == "game_over":
            self.draw_game_over()
        elif self.state == "leaderboard":
            self.draw_leaderboard()
        elif self.state == "settings":
            self.draw_settings()

    def run(self):
        while self.running:
            self.handle_events()

            if self.state == "game":
                self.update_game()

            self.draw()
            pygame.display.flip()

            current_fps = FPS + self.level
            if self.active_powerup == "speed":
                current_fps += 5
            elif self.active_powerup == "slow":
                current_fps = max(5, current_fps - 5)

            self.clock.tick(current_fps)