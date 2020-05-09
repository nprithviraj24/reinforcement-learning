### Thnaks to https://towardsdatascience.com/create-your-own-reinforcement-learning-environment-beb12f4151ef


import turtle

# ---------- Creating the Screen
win = turtle.Screen()
win.title('Paddle')
win.bgcolor('black')
win.tracer(0)
win.setup(width=600, height=600)

## -------- Creating the Ball
ball = turtle.Turtle()      # Create a turtle object
ball.shape('circle')        # Select a circle shape
ball.speed(0)
ball.color('white')           # Set the color to red
ball.penup()
ball.goto(0, 10)           # Place the shape in middle


### ------ Creating the Paddle
paddle = turtle.Turtle()
paddle.shape('square')
paddle.speed(0)
paddle.shapesize(stretch_wid=1, stretch_len=5)
paddle.penup()
paddle.color('blue')
paddle.goto(0,-275)



### Paddle Movement
def paddle_right():
    # We take the x positioon and add it
    x = paddle.xcor()
    if x <225:
        paddle.setx(x+20)

def paddle_left():
    x = paddle.xcor()
    if x > -225:
        paddle.setx(x-20)

''' Keyboard Control '''
win.listen()
win.onkey(paddle_right, 'Right')  # call paddle_right on right arrow key
win.onkey(paddle_left, 'Left')

ball.dx = 3   # ball's x-axis velocity
ball.dy = -3  # ball's y-axis velocity

while True:   # same loop

     win.update()

     ball.setx(ball.xcor() + ball.dx)  # update the ball's x-location using velocity
     ball.sety(ball.ycor() + ball.dy)  # update the ball's y-location using velocity