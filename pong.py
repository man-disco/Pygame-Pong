# Pong project made by Tech With Tim -> https://yewtu.be/watch?v=vVGTZlnnX3U
# Sound credits: https://freesound.org/people/NoiseCollector/sounds/4385/

import pygame
pygame.init()
pygame.mixer.init()

w_width, w_height = 700, 500
win = pygame.display.set_mode((w_width, w_height))
pygame.display.set_caption("Pong")

fps = 60

white = (255, 255, 255)
black = (0, 0, 0)

# Sounds
paddle_width, paddle_height = 20, 100
hitsound_p1 = pygame.mixer.Sound("data/sounds/pong1.wav")
hitsound_p2 = pygame.mixer.Sound("data/sounds/pong2.wav")
win_sound = pygame.mixer.Sound("data/sounds/win.wav")
score_sound = pygame.mixer.Sound("data/sounds/score.wav")

ball_radius = 7

wining_score = 10
score_font = pygame.font.Font("data/font/PressStart2P-vaV7.ttf", 20)

class Paddle:
    color = white
    vel = 4
    def __init__(self, x, y, width, height):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.width = width
        self.height = height


    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))

    def move(self, up=True):
        if up:
            self.y += self.vel
        else:
            self.y -= self.vel

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y


class Ball:
    max_vel = 5
    def __init__(self, x, y, radius):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.radius = ball_radius
        self.x_vel = self.max_vel
        self.y_vel = 0
        self.color = white

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.y_vel = 0
        self.x_vel *= -1

def draw(win, paddles, ball, left_score, right_score):
    win.fill(black)

    left_score_text = score_font.render(f"{left_score}", True, white)
    right_score_text = score_font.render(f"{right_score}", True, white)

    win.blit(left_score_text, (w_width//4 - left_score_text.get_width()//2, 20))
    win.blit(right_score_text, (w_width * (3/4) - right_score_text.get_width()//2, 20))
    for paddle in paddles:
        paddle.draw(win)

    for i in range(10, w_height, w_height//20):
        if i % 2 == 1:
            continue
        pygame.draw.rect(win, white, (w_width//2 - 5, i, 10, w_height//20))

    ball.draw(win)

    pygame.display.update()

def handle_collision(ball, left_paddle, right_paddle):
    if ball.y + ball.radius >= w_height:
        ball.y_vel *= -1

    elif ball.y - ball.radius <= 0:
        ball.y_vel *= -1

    if ball.x_vel < 0:
        # left paddle
        if ball.y >= left_paddle.y and ball.y <= left_paddle.y + left_paddle.height:
            if ball.x - ball.radius <= left_paddle.x + left_paddle.width:
                pygame.mixer.Sound.play(hitsound_p1)
                ball.x_vel *= -1

                # Y variation calculus
                middle_y = left_paddle.y + left_paddle.height / 2
                diference_in_y = middle_y - ball.y
                reduction_factor = (left_paddle.height / 2 ) / ball.max_vel
                y_vel = diference_in_y / reduction_factor
                ball.y_vel = -1 * y_vel

    else:
        # right paddle
         if ball.y >= right_paddle.y and ball.y <= right_paddle.y + right_paddle.height:
            if ball.x + ball.radius >= right_paddle.x:
                pygame.mixer.Sound.play(hitsound_p2)
                ball.x_vel *= -1

                middle_y = right_paddle.y + right_paddle.height / 2
                diference_in_y = middle_y - ball.y
                reduction_factor = (right_paddle.height / 2 ) / ball.max_vel
                y_vel = diference_in_y / reduction_factor
                ball.y_vel = -1 * y_vel
                
def handle_paddle_movement(keys, left_paddle, right_paddle):

    if keys[pygame.K_w] and left_paddle.y - left_paddle.vel >= 0:
        left_paddle.move(up=False)
    if keys[pygame.K_s] and left_paddle.y + left_paddle.vel + left_paddle.height <= w_height:
        left_paddle.move(up=True)

    if keys[pygame.K_UP] and right_paddle.y - right_paddle.vel >= 0:
        right_paddle.move(up=False)
    if keys[pygame.K_DOWN] and right_paddle.y + right_paddle.vel + right_paddle.height <= w_height:
        right_paddle.move(up=True)

def main():
    run = True
    clock = pygame.time.Clock()
    left_score = 0
    right_score = 0

    ball = Ball(w_width//2, w_height//2, ball_radius)

    left_paddle = Paddle(10, w_height//2 - paddle_height//2, paddle_width, paddle_height)
    right_paddle = Paddle(w_width - 10 - paddle_width, w_height//2 - paddle_height//2, paddle_width, paddle_height)

    while run:
        clock.tick(fps)
        draw(win, [left_paddle, right_paddle], ball, left_score, right_score)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed()
        handle_paddle_movement(keys, left_paddle, right_paddle)
        
        ball.move()

        handle_collision(ball, left_paddle, right_paddle)

        if ball.x < 0:
            right_score += 1
            pygame.mixer.Sound.play(score_sound)
            ball.reset()
            right_paddle.reset()
            left_paddle.reset()

        elif ball.x > w_width:
            left_score += 1
            pygame.mixer.Sound.play(score_sound)
            ball.reset()
            right_paddle.reset()
            left_paddle.reset()
        
        won = False
        if left_score >= wining_score:
            won = True
            win_text = "Left Player Won!"
        elif right_score >= wining_score:
            win_text = "Right Player Won!"
            won = True
        
        if won:
            text = score_font.render(win_text, 1, white)
            win.blit(text, (w_width//2 - text.get_width()//2, w_height//2 - text.get_height()//2))
            pygame.display.update()
            pygame.mixer.Sound.play(win_sound)
            pygame.time.delay(5000)
            ball.reset()
            right_paddle.reset()
            left_paddle.reset()
            left_score = 0
            right_score = 0
        

    pygame.quit()


if __name__ == '__main__':
    main()