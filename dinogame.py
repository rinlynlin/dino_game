import pygame
import os
import random

pygame.init()

SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1400
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

#이미지 불러오기
RUNNING = [pygame.image.load(os.path.join("Assets/Dino", "DinoRun1.png")),
           pygame.image.load(os.path.join("Assets/Dino", "DinoRun2.png"))]

JUMPING = pygame.image.load(os.path.join("Assets/Dino", "DinoJump.png"))

SMALL_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus3.png"))]
LARGE_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus3.png"))]
BIRD = [pygame.image.load(os.path.join("Assets/Bird", "Bird1.png")),
        pygame.image.load(os.path.join("Assets/Bird", "Bird2.png"))]

CLOUD = pygame.image.load(os.path.join("Assets/Other", "Cloud.png"))
BG = pygame.image.load(os.path.join("Assets/Other", "Track.png"))

LIFE = [pygame.image.load(os.path.join("Assets/Life", "Life1.png")),
        pygame.image.load(os.path.join("Assets/Life", "Life2.png")),
        pygame.image.load(os.path.join("Assets/Life", "Life3.png"))]


# 공룡 Class
class Dinosaur:
    X_POS = 80
    Y_POS = 310
    JUMP_VEL = 8.5

    def __init__(self):
        self.run_img = RUNNING
        self.jump_img = JUMPING

        self.dino_run = True
        self.dino_jump = False

        self.step_index = 0 #달리는 이미지 구현
        self.jump_vel = self.JUMP_VEL
        self.image = self.run_img[0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS

        self.life_img = LIFE
        self.life_index = 2

    def update(self, userInput):
        if self.dino_run:
            self.run()
        if self.dino_jump:
            self.jump()
        if self.step_index >= 10:
            self.step_index = 0

        # jump 구현
        if userInput[pygame.K_UP] and not self.dino_jump:
            self.dino_jump = True
            self.dino_run = False

        # 달리기 구현
        elif not self.dino_jump:
            self.dino_jump = False
            self.dino_run = True

    def run(self):
        self.image = self.run_img[self.step_index // 5] #달리는 애니메이션 구현
        self.dino_rect = self.image.get_rect() #충돌 판정을 위한 사각형 설정
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.step_index += 1

    def jump(self):
        self.image = self.jump_img
        if self.dino_jump:
            self.dino_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
        if self.jump_vel < - self.JUMP_VEL:
            self.dino_jump = False
            self.jump_vel = self.JUMP_VEL

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.dino_rect.x, self.dino_rect.y))

    def draw_life(self,SCREEN):
        life_img = self.life_img[self.life_index]
        SCREEN.blit(life_img, (SCREEN_WIDTH - life_img.get_width(), 10))

#배경 구름 클래스 만들기
class Cloud:
    def __init__(self):
        self.x_pos = SCREEN_WIDTH + random.randint(800, 1000)
        self.y_pos = random.randint(50, 100)
        self.image = CLOUD
        self.width = self.image.get_width()

    def update(self):
        self.x_pos -= game_speed
        if self.x_pos < - self.width:
            self.x_pos = SCREEN_WIDTH + random.randint(2500, 3000)
            self.y_pos = random.randint(50, 100)

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.x_pos, self.y_pos))

#장애물 구현
class Obstacle:
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < - self.rect.width:
            obstacles.pop()

    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)

#작은 선인장 구현
class SmallCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type) # 상속
        self.rect.y = 325

# 큰 선인장 구현
class LargeCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 300
# 새 구현
class Bird(Obstacle):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = 250
        self.index = 0

    def draw(self, SCREEN):
        if self.index >= 9:
            self.index = 0
        SCREEN.blit(self.image[self.index // 5], self.rect)
        self.index += 1

#배경 클래스 만들기
class Background:
    def __init__(self):
        self.image = BG
        self.x_pos = 0
        self.y_pos = 380
        self.speed = 20

    def update(self):
        self.x_pos -= self.speed
        if self.x_pos <= -self.image.get_width():
            self.x_pos = 0

    def draw(self,SCREEN):
        SCREEN.blit(self.image, (self.x_pos, self.y_pos))
        SCREEN.blit(self.image, (self.x_pos + self.image.get_width(), self.y_pos))

# 메인 함수
def main():
    global game_speed, points, obstacles #전역변수 설정
    run = True
    invulnerableMode = False
    invulnerableStartTime = 0
    INVULNTIME = 2000
    clock = pygame.time.Clock()
    cloud = Cloud()
    bg = Background()
    player = Dinosaur()
    game_speed = 20
    points = 0
    font = pygame.font.Font('freesansbold.ttf', 20)
    obstacles = []
    life = 3

    def score():
        global points, game_speed
        points += 1
        if points % 100 == 0:
            game_speed += 1

        text = font.render("Points: " + str(points), True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (1330, 50) # 점수 표시를 오른쪽 끝에
        SCREEN.blit(text, textRect)

    while run:
        if invulnerableMode and pygame.time.get_ticks() - invulnerableStartTime > INVULNTIME:
            invulnerableMode = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        SCREEN.fill((255, 255, 255))
        userInput = pygame.key.get_pressed()
        player.draw(SCREEN)
        player.update(userInput)
        player.draw_life(SCREEN)


        # random 수가 0이나오면 작은 선인장, 1이나오면 큰 선인장, 2가 나오면 새가 나오게
        if len(obstacles) == 0:
            if random.randint(0, 2) == 0:
                obstacles.append(SmallCactus(SMALL_CACTUS))
            elif random.randint(0, 2) == 1:
                obstacles.append(LargeCactus(LARGE_CACTUS))
            elif random.randint(0, 2) == 2:
                obstacles.append(Bird(BIRD))

        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            obstacle.update()

            # 충돌감지 무적모드가 아닐때
            if not invulnerableMode:
                if player.dino_rect.colliderect(obstacle.rect):
                    pygame.time.delay(1000) #장애물에 부딛히면 1초 딜레이, 생명 1개 줄어들기
                    life -= 1
                    if life == 0:
                        menu(life)
                    else:
                        player.life_index = life - 1
                    invulnerableMode = True
                    invulnerableStartTime = pygame.time.get_ticks()

        cloud.draw(SCREEN)
        cloud.update()
        bg.draw(SCREEN)
        bg.update()
        score()
        pygame.display.update()
        clock.tick(60)
        pygame.display.update()

#게임이 끝났을 시 재시작용 메뉴 함수
def menu(life):
    global points
    run = True
    while run:
        SCREEN.fill((255, 255, 255))
        font = pygame.font.Font('freesansbold.ttf', 30)

        if life == 0:
            text = font.render("Press any key", True, (0, 0, 0))
            score = font.render("Your Score: " + str(points), True, (0, 0, 0))
            scoreRect = score.get_rect()
            scoreRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
            SCREEN.blit(score, scoreRect)

        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        SCREEN.blit(text, textRect)
        SCREEN.blit(RUNNING[0], (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 140))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                main()

    pygame.quit()

if __name__ == "__main__":
    main()