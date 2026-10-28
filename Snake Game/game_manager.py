#Creating the game world and its canvas.
#Creating the snake.
#Spawning fruit at random locations.
#Drawing the snake and fruit.
#Handling keyboard input.
#Updating the snake's movement.
#Detecting collisions.
#Updating the score.
#Handling game-over conditions.
#Running the game loop.


import tkinter as tk
import settings
from snake import Snake
from fruit import Fruit



class GameManager:
    def __init__(self, window):
        self.window = window
        self.game_over = False
        self.score = 0

        self.canvas = tk.Canvas(self.window, width=settings.WINDOW_WIDTH, height=settings.WINDOW_HEIGHT)

        self.canvas.pack()

        self.window.bind("<KeyPress>", self.Input_Handler) #allows the program to prosses key presses

        self.game_started = False

        self.create_background()
        self.draw_margin()

        self.snake = Snake()

        self.fruit = Fruit(self.snake.body)

        self.draw_fruit()
        self.draw_snake()
        self.draw_score()
        self.create_start_button()

    def create_background(self):
        columns = settings.WINDOW_WIDTH // settings.CELL_SIZE
        rows = settings.PLAY_AREA_HEIGHT // settings.CELL_SIZE

        for row in range(rows):
            for column in range(columns):

                x1 = column * settings.CELL_SIZE
                y1 = settings.MARGIN_HEIGHT + row * settings.CELL_SIZE

                x2 = x1 + settings.CELL_SIZE
                y2 = y1 + settings.CELL_SIZE

                if (row + column) % 2 == 0:
                    color = settings.BACKGROUND_COLOR_1
                else:
                    color = settings.BACKGROUND_COLOR_2

                self.canvas.create_rectangle(x1, y1, x2, y2,fill=color,outline=color)

    def create_start_button(self):
        self.start_button = tk.Button(self.canvas,text="Start",command=self.start_game)

        self.start_button_window = self.canvas.create_window(settings.WINDOW_WIDTH - 70,settings.MARGIN_HEIGHT // 2,window=self.start_button)

        self.restart_button = tk.Button(self.canvas,text="Restart",command=self.restart_game)

        self.restart_button_window = self.canvas.create_window(settings.WINDOW_WIDTH - 70,settings.MARGIN_HEIGHT // 2,window=self.restart_button)

        self.canvas.itemconfigure(self.restart_button_window, state="hidden")

    def draw_margin(self):
        self.canvas.create_rectangle(0,0,settings.WINDOW_WIDTH,settings.MARGIN_HEIGHT,fill=settings.MARGIN_COLOR,tags="margin")

    def draw_snake(self):

        self.canvas.delete("snake")  # clears the snake when it is re drawn

        for index, segment in enumerate(self.snake.body):  # Loops through the body of the snake
            grid_x, grid_y = segment  # Gets the cords of the segment

            x1 = grid_x * settings.CELL_SIZE  # Makes every thing pixels
            y1 = grid_y * settings.CELL_SIZE

            x2 = x1 + settings.CELL_SIZE
            y2 = y1 + settings.CELL_SIZE

            if index == 0:
                color = settings.SNAKE_HEAD_COLOR
                tag = "snake_head"
            else:
                color = settings.SNAKE_COLOR
                tag = "snake_body"

            self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline=color, tags=("snake", tag))

    def draw_fruit(self):

        gridX, gridY = self.fruit.position

        x1 = gridX * settings.CELL_SIZE
        y1 = gridY * settings.CELL_SIZE

        x2 = x1 + settings.CELL_SIZE
        y2 = y1 + settings.CELL_SIZE


        self.canvas.create_oval(x1, y1, x2, y2, fill=settings.FRUIT_COLOR, outline=settings.FRUIT_COLOR, tags="fruit")

    def draw_score(self):
        self.canvas.delete("score")

        self.canvas.create_text(10,10,text=f"Score: {self.score}", font=settings.SCORE_FONT, fill=settings.SCORE_COLOR,anchor="nw",tags="score")

    def change_color(self, head_color, tail_color):
        self.canvas.itemconfig("snake_head", fill=head_color, outline=head_color)
        self.canvas.itemconfig("snake_body", fill=tail_color, outline=tail_color)

    def Input_Handler(self, event):

        if event.keysym == "Right":
            self.snake.change_direction((1,0))

        elif event.keysym == "Left":
            self.snake.change_direction((-1,0))

        elif event.keysym == "Up":
            self.snake.change_direction((0,-1))

        elif event.keysym == "Down":
            self.snake.change_direction((0,1))

    def wall_collision(self):
        headX, headY = self.snake.body[0] #Gets the position of the snakes head

        columns = settings.WINDOW_WIDTH // settings.CELL_SIZE
        rows = settings.PLAY_AREA_HEIGHT // settings.CELL_SIZE
        first_playable_row = settings.MARGIN_HEIGHT // settings.CELL_SIZE

        if headX < 0 or headX >= columns:
            return True

        if headY < first_playable_row or headY >= first_playable_row + rows:
            return True

        return False

    def self_collision(self):

        head = self.snake.body[0]
        body = self.snake.body[1:]

        if head in body:
            return True

        return False

    def fruit_collision(self):
        head = self.snake.body[0]

        if head == self.fruit.position:
            return True

        return False


    def update(self):

        if self.game_over:
            return

        self.snake.move()

        if self.wall_collision():
            self.game_over = True
            self.change_color(settings.SNAKE_HEAD_FAILE_COLOR,settings.SNAKE_TAIL_FAILE_COLOR)#How will I make the snake change to settings SNAKE_FAILE_COLOR  when game over
            print("Game Over")
            return

        if self.self_collision():
            self.game_over = True
            self.change_color(settings.SNAKE_HEAD_FAILE_COLOR,settings.SNAKE_TAIL_FAILE_COLOR)# How will I make the snake change to settings SNAKE_FAILE_COLOR  when game over
            print("Ouch! Game Over")
            return

        if self.fruit_collision():
            print("Fruit eaten!")

            self.score += 1
            self.draw_score() #redraws the score with the new score

            self.snake.grow()

            self.fruit.respawn(self.snake.body)
            self.canvas.delete("fruit")
            self.draw_fruit()

        self.draw_snake()

        self.window.after(settings.MOVEMENT_DELAY, self.update)

    def start_game(self):
        if self.game_started:
            return

        self.game_started = True

        self.canvas.itemconfigure(self.start_button_window, state="hidden")
        self.canvas.itemconfigure(self.restart_button_window, state="normal")

        self.update()

    def restart_game(self):
        self.game_over = False
        self.game_started = True
        self.score = 0

        #too restart the game you have to reset all varaibles to the their orignal forms

        self.snake = Snake()
        self.fruit = Fruit(self.snake.body)

        self.canvas.delete("snake")
        self.canvas.delete("fruit")

        self.draw_snake()
        self.draw_fruit()
        self.draw_score()

        self.update()

