
import tkinter as tk
import random

# 初始化窗口
window = tk.Tk()
window.title("Breakout Game")

# 游戏画布
canvas = tk.Canvas(window, width=400, height=500, bd=0, highlightthickness=0)
canvas.pack()
window.update()

# 全局变量
score = 0
lives = 3

# 画板
score_text = canvas.create_text(50, 10, text="Score: 0", font=("Helvetica", 12))
lives_text = canvas.create_text(350, 10, text="Lives: 3", font=("Helvetica", 12))

# 球类
class Ball:
    def __init__(self, canvas, paddle, bricks):
        self.canvas = canvas
        self.paddle = paddle
        self.bricks = bricks
        self.id = canvas.create_oval(10, 10, 25, 25, fill='red')
        self.canvas.move(self.id, 190, 300)
        self.dx = random.choice([-3, 3])
        self.dy = -3

    def hit_paddle(self, pos):
        paddle_pos = self.canvas.coords(self.paddle.id)
        return (pos[2] >= paddle_pos[0] and pos[0] <= paddle_pos[2]) and (pos[3] >= paddle_pos[1] and pos[3] <= paddle_pos[3])

    def hit_brick(self, pos):
        for brick in self.bricks:
            brick_pos = self.canvas.coords(brick.id)
            if (pos[2] >= brick_pos[0] and pos[0] <= brick_pos[2]) and (pos[3] >= brick_pos[1] and pos[1] <= brick_pos[3]):
                self.canvas.delete(brick.id)
                self.bricks.remove(brick)
                return True
        return False

    def draw(self):
        global score, lives
        self.canvas.move(self.id, self.dx, self.dy)
        pos = self.canvas.coords(self.id)
        if pos[0] <= 0 or pos[2] >= 400:
            self.dx = -self.dx
        if pos[1] <= 0:
            self.dy = -self.dy
        if self.hit_paddle(pos):
            self.dy = -self.dy
        elif self.hit_brick(pos):
            self.dy = -self.dy
            score += 10
            canvas.itemconfig(score_text, text=f"Score: {score}")
        elif pos[3] >= 500:
            lives -= 1
            canvas.itemconfig(lives_text, text=f"Lives: {lives}")
            if lives == 0:
                canvas.create_text(200, 250, text="Game Over", font=("Helvetica", 20), fill='red')
                return False
            else:
                self.canvas.coords(self.id, 190, 300, 205, 315)
                self.dy = -3
        return True

# 挡板类
class Paddle:
    def __init__(self, canvas):
        self.canvas = canvas
        self.id = canvas.create_rectangle(150, 480, 250, 490, fill='blue')
        self.x = 0
        canvas.bind_all("<Left>", self.move_left)
        canvas.bind_all("<Right>", self.move_right)

    def draw(self):
        self.canvas.move(self.id, self.x, 0)
        pos = self.canvas.coords(self.id)
        if pos[0] <= 0 or pos[2] >= 400:
            self.x = 0

    def move_left(self, evt):
        self.x = -4

    def move_right(self, evt):
        self.x = 4

# 砖块类
class Brick:
    def __init__(self, canvas, x, y):
        self.canvas = canvas
        self.id = canvas.create_rectangle(x, y, x+50, y+20, fill='green')

# 创建砖块
bricks = []
for i in range(5):
    for j in range(7):
        bricks.append(Brick(canvas, 5 + j*55, 30 + i*25))

# 实例化挡板和球
paddle = Paddle(canvas)
ball = Ball(canvas, paddle, bricks)

# 游戏循环
def game_loop():
    if ball.draw():
        paddle.draw()
        window.after(20, game_loop)

game_loop()
window.mainloop()
