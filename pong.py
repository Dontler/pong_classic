import pygame, random
from pygame.locals import *

pygame.init()

SIZE = WIDTH, HEIGHT = 640, 480

_display_surf = pygame.display.set_mode(SIZE, pygame.HWSURFACE | pygame.DOUBLEBUF)

FONT = pygame.font.Font(None, 36)


class App:

    class Ball:
        def __init__(self):
            self._center = [int(WIDTH / 2) - 10, int(HEIGHT / 2) - 10]
            self.horDir = True
            self.vertDir = 1
            self._radius = 10
            self._ball = pygame.draw.circle(_display_surf, (255, 255, 255), self._center, self._radius)

        def render(self):
            self._ball = pygame.draw.circle(_display_surf, (255, 255, 255), self._ball.center, self._radius)

        def move_right(self):
            self._ball = self._ball.move(3, 7 * self.vertDir)

        def move_left(self):
            self._ball = self._ball.move(-3, 7 * self.vertDir)

        def top(self):
            return self._ball.top

        def border_collision(self):
            if self._ball.top <= 0 or self._ball.top > HEIGHT - 2*self._radius:
                return True
            else:
                return False

        def platform_collision(self, platform):
            if self._ball.colliderect(platform):
                return True
            else: 
                return False

        def left_goal_collision(self):
            if self._ball.x <= 0:
                return True
            else:
                return False

        def right_goal_collision(self):
            if self._ball.x >= WIDTH - 15:
                return True
            else:
                return False

        def back_to_origin(self):
            self._ball = pygame.draw.circle(_display_surf, (255, 255, 255), self._center, self._radius)
            
    
    FPS = 30

    def __init__(self):
        self._leftScore, self._rightScore = 0, 0
        self._text_score = None
        self._text_place = None
        self._running = True
        self._play = False
        self._move_leftPlatform = False
        self._move_rightPlatform = False
        self._dirRight = 1
        self._dirLeft = 1
        self._clock = pygame.time.Clock()
        self._leftPlatform = pygame.Rect([15, int(HEIGHT / 2) - 50, 15, 80])
        self._rightPlatform = pygame.Rect([WIDTH - 30, int(HEIGHT / 2) - 50, 15, 80])
        self._ball = App.Ball()
        

    def on_init(self):
        pygame.display.set_caption("Pong")
        self._text_score = FONT.render(str(self._leftScore) + " : " + str(self._rightScore), 0, (255, 255, 255))
        self._text_place = self._text_score.get_rect(center=(305, 15))
        self._running = True

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self._dirRight = -1
                self._move_rightPlatform = True
            elif event.key == pygame.K_DOWN:
                self._dirRight = 1
                self._move_rightPlatform = True
            if event.key == pygame.K_s:
                self._dirLeft = 1
                self._move_leftPlatform = True
            elif event.key == pygame.K_w:
                self._dirLeft = -1
                self._move_leftPlatform = True
            elif event.key == pygame.K_SPACE:
                self.start()
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_s:
                self._move_leftPlatform = False
            elif event.key == pygame.K_w:
                self._move_leftPlatform = False
            if event.key == pygame.K_UP:
                self._move_rightPlatform = False
            elif event.key == pygame.K_DOWN:
                self._move_rightPlatform = False

    
    def __move_leftPlatform(self, dir=1):
        self._leftPlatform = self._leftPlatform.move(0, 5 * dir)

    
    def __move_rightPlatform(self, dir=1):
        self._rightPlatform = self._rightPlatform.move(0, 5 * dir)

    def goal_check(self):
        if self._ball.left_goal_collision():
            self._play = False
            self._leftScore += 1
            self._ball.back_to_origin()
            self.update_score()
        if self._ball.right_goal_collision():
            self._play = False
            self._rightScore += 1
            self._ball.back_to_origin()
            self.update_score()

    def update_score(self):
        self._text_score = FONT.render(str(self._leftScore) + " : " + str(self._rightScore), 0, (255, 255, 255))

    def start(self):
        self._play = True
        num = random.randint(1, 100)
        print(num)
        if num > 50:
            self._ball.horDir = 1
            self._ball.move_left()
        else:
            self._ball.horDir = 0
            self._ball.move_right()


    def on_loop(self):
        if self._move_leftPlatform and ((self._leftPlatform.top > 0 and self._dirLeft == -1) or (self._leftPlatform.top < HEIGHT - 80 and self._dirLeft == 1)):
            self.__move_leftPlatform(self._dirLeft)
        if self._move_rightPlatform and ((self._rightPlatform.top > 0 and self._dirRight == -1) or (self._rightPlatform.top < HEIGHT - 80 and self._dirRight == 1)):
            self.__move_rightPlatform(self._dirRight)
        if self._play:
            if self._ball.horDir:
                if self._ball.border_collision():
                    self._ball.vertDir = - self._ball.vertDir
                self._ball.move_left()
            if not self._ball.horDir:
                if self._ball.border_collision():
                    self._ball.vertDir = - self._ball.vertDir
                self._ball.move_right()
            if self._ball.platform_collision(self._leftPlatform):
                self._ball.horDir = 0
                self._ball.move_right()
            if self._ball.platform_collision(self._rightPlatform):
                self._ball.horDir = 1
                self._ball.move_left()
        self.goal_check()
        pygame.display.update()
        _display_surf.fill((0, 0, 0))

    def on_render(self):
        pygame.draw.rect(_display_surf, pygame.Color(255, 255, 255), self._leftPlatform)
        pygame.draw.rect(_display_surf, pygame.Color(255, 255, 255), self._rightPlatform)
        self._ball.render()
        _display_surf.blit(self._text_score, self._text_place)

    def on_cleanup(self):
        pygame.quit()
    
    def on_execute(self):
        if self.on_init == False:
            self._running = False
        
        while( self._running ):
            for event in pygame.event.get():
                self.on_event(event)
            self.on_render()
            self.on_loop()
            self._clock.tick(self.FPS)
        self.on_cleanup()


if __name__ == "__main__":
    theApp = App()
    theApp.on_init()
    theApp.on_execute()
