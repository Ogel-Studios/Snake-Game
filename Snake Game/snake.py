#Manages the snake's body, movement, direction, and growth.


import settings

class Snake:
    def __init__(self):
        self.direction = (1,0)
        self.body = self.create_body()

        self.grow_next_move = False    #Tells the body to grow or not

    def create_body(self):
        body = []

        for segment in range(settings.STARTING_SNAKE_LENGTH):  #Creates the length of the snake
            x = settings.SNAKE_START_X - segment
            y = settings.SNAKE_START_Y

            body.append((x,y))

        return body

    def move(self):
        headX, headY = self.body[0]

        directionX, directionY = self.direction

        new_headX = headX + directionX
        new_headY = headY + directionY

        self.body.insert(0, (new_headX, new_headY))

        if self.grow_next_move:    #resets to growth variable
            self.grow_next_move = False

        else:
            self.body.pop()

    def grow(self):
        self.grow_next_move = True


    def change_direction(self, new_direction):
        opposite_direction = (-self.direction[0],-self.direction[1])  #Calculates the opposite direction of the snake

        if new_direction != opposite_direction:
            self.direction = new_direction



