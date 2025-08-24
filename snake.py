import random
import tkinter as tk
from config_snake import *
import time


class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Snake")
        self.root.resizable(False, False)
        self.canvas = tk.Canvas(root, width=WIGHT, height=HEIGHT, bg=BG)
        self.canvas.pack()
        self.menu_frame = tk.Frame(root)
        self.level = tk.StringVar(value="Medium")
        self.score = 0
        self.running = False
        self.paused = False
        self.after_id = None
        self.create_menu()

    def create_menu(self):
        self.clear_canvas()
        tk.Label(self.menu_frame, text="Snake", font=("Arial", 24)).pack()
        tk.Button(self.menu_frame, text="Start", font=("Arial", 14), command=self.start_game).pack(pady=5)
        tk.OptionMenu(self.menu_frame, self.level, *SPEEDS.keys()).pack(pady=5)
        tk.Button(self.menu_frame, text="Exit", font=("Arial", 14), command=self.root.destroy).pack(pady=5)
        self.menu_frame.pack()

    def start_game(self):
        self.menu_frame.pack_forget()
        self.running = True
        self.paused = False
        self.score = 0
        self.snake = [(5, 5), (4, 5), (3, 5)]
        self.direction = "Right"
        self.food = None
        self.canvas.delete("all")
        self.draw_board()
        self.draw_snake()
        self.span_food()
        self.draw_score()

        self.root.bind("<Key>", self.change_direction)
        self.root.bind("<Escape>", self.toggle_pause)
        self.update()

    def draw_board(self):
        self.canvas.create_rectangle(1, 1, WIGHT, HEIGHT, outline="white", width=2)

    def draw_snake(self):
        self.canvas.delete("snake")
        for x, y in self.snake:
            self.draw_cell(x, y, COLOR_SNAKE, tag="snake")

    def draw_cell(self, x, y, color, tag=""):
        x1 = x * SIZE_SELL
        y1 = y * SIZE_SELL
        x2 = x1 + SIZE_SELL
        y2 = y1 + SIZE_SELL
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, tag=tag)

    def span_food(self):
        self.canvas.delete("food")
        while True:
            x = random.randint(1, (WIGHT // SIZE_SELL) - 2)
            y = random.randint(1, (HEIGHT // SIZE_SELL) - 2)
            if (x, y) not in self.snake:
                self.food = (x, y)
                self.draw_cell(x, y, COLOR_APPLE, tag="food")
                break

    def draw_score(self):
        self.canvas.delete("score")
        self.canvas.create_text(50, 20, text=f"Score {self.score}", fill="white", font=("Arial", 16), tag="score")

    def change_direction(self, event):
        new_direction = event.keysym
        opposition = {"Left": "Right", "Right": "Left", "Up": "Down", "Down": "Up"}
        if new_direction in DIRECTIONS and new_direction != opposition.get(self.direction):
            self.direction = new_direction

    def toggle_pause(self, event=None):
        if not self.running:
            return
        self.paused = not self.paused

        if self.paused:
            if self.after_id is not None:
                self.root.after_cancel(self.after_id)
                self.after_id = None

            self.canvas.create_text(WIGHT // 2, HEIGHT // 2, text="Pause", fill="yellow", font=("Arial", 24),
                                    tag="pause")
        else:
            self.canvas.delete("pause")
            self.update()

    def snake_move(self):
        dx, dy = DIRECTIONS[self.direction]
        head_x, head_y = self.snake[0]
        new_head = (head_x + dx, head_y + dy)

        if (
                new_head in self.snake or
                new_head[0] < 0 or new_head[1] < 0 or
                new_head[0] >= WIGHT // SIZE_SELL or
                new_head[1] >= HEIGHT // SIZE_SELL
        ):
            self.game_over()
            return
        self.snake.insert(0, new_head)
        if new_head == self.food:
            self.score += 1
            self.span_food()
        else:
            self.snake.pop()

    def game_over(self):
        self.running = False
        if self.after_id is not None:
            self.root.after_cancel(self.after_id)
            self.after_id = None
        self.canvas.create_text(WIGHT // 2, HEIGHT // 2, text=f"Game over\nScore {self.score}", fill="white",
                                font=("Arial", 20))
        self.root.after(3000, self.create_menu)

    def update(self):
        if not self.running or self.paused:
            return
        # self.span_food()
        self.snake_move()

        if self.running:
            self.draw_snake()
            self.draw_score()
            speed = SPEEDS[self.level.get()]
            self.after_id = self.root.after(speed, self.update)

    def clear_canvas(self):
        self.canvas.delete("all")


if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()
