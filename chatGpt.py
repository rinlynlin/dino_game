import pygame
import random
import os

# 게임 초기화
pygame.init()

# 화면 크기 설정
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 300
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Google Dinosaur Game")

# 시계 설정
clock = pygame.time.Clock()

# 게임 변수
GRAVITY = 1.5
INITIAL_JUMP_VELOCITY = -15
RUNNING_SPEED = 5
SCORE = 0
GAME_OVER = False

# 게임 리소스 로드
dino_img = pygame.image.load(os.path.join("Assets/Dino", "DinoRun1.png"))
cactus_img = pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus1.png"))
bird_img = pygame.image.load(os.path.join("Assets/Bird", "Bird1.png"))
cloud_img = pygame.image.load(os.path.join("Assets/Other", "Cloud.png"))
ground_img = pygame.image.load(os.path.join("Assets/Other", "Track.png"))
life_img = pygame.image.load(os.path.join("Assets/Life", "Life1.png"))



# 공룡 클래스
class Dinosaur:
    def __init__(self):
        self.step_index = 0
        self.jump_vel = INITIAL_JUMP_VELOCITY
        self.image = dino_img
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = 50
        self.dino_rect.y = SCREEN_HEIGHT - self.dino_rect.height - 50
        self.life_image = [life_img, life_img, life_img]
        self.life_index = 0

    def update(self):
        self.step_index += 1
        self.dino_rect.y += self.jump_vel
        if self.dino_rect.y >= SCREEN_HEIGHT - self.dino_rect.height - 50:
            self.dino_rect.y = SCREEN_HEIGHT - self.dino_rect.height - 50
            self.jump_vel = INITIAL_JUMP_VELOCITY

        self.jump_vel += GRAVITY

    def run(self):
        self.image = dino_img
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = 50
        self.dino_rect.y = SCREEN_HEIGHT - self.dino_rect.height - 50

    def jump(self):
        self.jump_vel = INITIAL_JUMP_VELOCITY

    def draw(self):
        screen.blit(self.image, (self.dino_rect.x, self.dino_rect.y))

    def draw_life(self):
        life_img = self.life_image[self.life_index % len(self.life_image)]
        screen.blit(life_img, (10, 10))
# 구름 클래스
class Cloud:
    def __init__(self):
        self.x = SCREEN_WIDTH + random.randint(100, 300)
        self.y = random.randint(50, 100)
        self.image = cloud_img
        self.width = self.image.get_width()

    def update(self):
        self.x -= RUNNING_SPEED
        if self.x < -self.width:
            self.x = SCREEN_WIDTH + random.randint(100, 300)
            self.y = random.randint(50, 100)

    def draw(self):
        screen.blit(self.image, (self.x, self.y))


# 장애물 클래스
class Obstacle:
    def __init__(self, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH

    def update(self):
        self.rect.x -= RUNNING_SPEED

    def draw(self):
        screen.blit(self.image, self.rect)


# 작은 선인장 클래스
class SmallCactus(Obstacle):
    def __init__(self):
        super().__init__(cactus_img)
        self.rect.y = SCREEN_HEIGHT - self.rect.height - 50


# 큰 선인장 클래스
class LargeCactus(Obstacle):
    def __init__(self):
        super().__init__(cactus_img)
        self.image = pygame.transform.scale(self.image, (self.rect.width * 2, self.rect.height))
        self.rect = self.image.get_rect()
        self.rect.y = SCREEN_HEIGHT - self.rect.height - 50


# 새 클래스
class Bird(Obstacle):
    def __init__(self):
        super().__init__(bird_img)
        self.bird_height = [SCREEN_HEIGHT - self.rect.height - 100, SCREEN_HEIGHT - self.rect.height - 200]
        self.rect.y = random.choice(self.bird_height)

    def update(self):
        super().update()
        if pygame.time.get_ticks() % 700 < 350:
            self.rect.y = self.bird_height[0]
        else:
            self.rect.y = self.bird_height[1]


# 배경 클래스
class Background:
    def __init__(self):
        self.image = ground_img
        self.x_pos = 0
        self.y_pos = SCREEN_HEIGHT - self.image.get_height()
        self.speed = RUNNING_SPEED

    def update(self):
        self.x_pos -= self.speed
        if self.x_pos <= -self.image.get_width():
            self.x_pos = 0

    def draw(self):
        screen.blit(self.image, (self.x_pos, self.y_pos))
        screen.blit(self.image, (self.x_pos + self.image.get_width(), self.y_pos))


# 게임 오브젝트 생성
dinosaur = Dinosaur()
clouds = [Cloud() for _ in range(3)]
obstacles = []
background = Background()

# 게임 루프
running = True
while running:
    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and dinosaur.dino_rect.y == SCREEN_HEIGHT - dinosaur.dino_rect.height - 50:
                dinosaur.jump()

    # 게임 업데이트
    dinosaur.update()
    background.update()

    # 장애물 생성
    if len(obstacles) == 0:
        choice = random.randint(0, 2)
        if choice == 0:
            obstacles.append(SmallCactus())
        elif choice == 1:
            obstacles.append(LargeCactus())
        elif choice == 2:
            obstacles.append(Bird())
    else:
        for obstacle in obstacles:
            obstacle.update()

    # 장애물 충돌 체크
    for obstacle in obstacles:
        if dinosaur.dino_rect.colliderect(obstacle.rect):
            dinosaur.life_index += 1
            if dinosaur.life_index == 3:
                GAME_OVER = True
                running = False
            obstacles.remove(obstacle)

    # 화면 그리기
    screen.fill((255, 255, 255))
    background.draw()
    for obstacle in obstacles:
        obstacle.draw()
    dinosaur.draw()
    for cloud in clouds:
        cloud.draw()
    dinosaur.draw_life()

    # 게임 종료 체크
    if GAME_OVER:
        font = pygame.font.Font(None, 36)
        text = font.render("GAME OVER", True, (255, 0, 0))
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))

    # 화면 업데이트
    pygame.display.update()
    clock.tick(30)

# 게임 종료
pygame.quit()
