import pygame
import math
from CollisionFramework import CollisionCalculation, ClculateElasticCollision

# 초기화
pygame.init()

# 화면 설정
WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Korean 4-Ball Billiards")

# 색상 정의
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# 공 클래스 정의
class Ball:
    def __init__(self, x, y, radius, color, mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass
        self.vx = 0
        self.vy = 0

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

    def update_position(self):
        self.x += self.vx
        self.y += self.vy

        # 마찰 효과
        self.vx *= 0.98
        self.vy *= 0.98

        # 벽 충돌 감지
        if self.x - self.radius < 0:
            self.x = self.radius
            self.vx = -self.vx * 0.9
        if self.x + self.radius > WIDTH:
            self.x = WIDTH - self.radius
            self.vx = -self.vx * 0.9
        if self.y - self.radius < 0:
            self.y = self.radius
            self.vy = -self.vy * 0.9
        if self.y + self.radius > HEIGHT:
            self.y = HEIGHT - self.radius
            self.vy = -self.vy * 0.9

    def is_stationary(self):
        return abs(self.vx) < 0.1 and abs(self.vy) < 0.1

# 공 초기화
white_ball = Ball(200, 200, 15, WHITE, 1)
red_ball_1 = Ball(400, 150, 15, RED, 1)
red_ball_2 = Ball(400, 250, 15, RED, 1)
balls = [white_ball, red_ball_1, red_ball_2]

# 점수 및 게임 상태
player_score = 0
hit_red1 = False
hit_red2 = False
turn_active = False
font = pygame.font.SysFont(None, 36)

# 점선 그리기 함수
def draw_dotted_line(screen, start_pos, end_pos, color, dash_length=10):
    dx, dy = end_pos[0] - start_pos[0], end_pos[1] - start_pos[1]
    distance = math.sqrt(dx**2 + dy**2)
    if distance == 0:
        return
    dx, dy = dx / distance, dy / distance

    for i in range(0, int(distance / dash_length), 2):
        start_x = start_pos[0] + dx * i * dash_length
        start_y = start_pos[1] + dy * i * dash_length
        end_x = start_pos[0] + dx * (i + 1) * dash_length
        end_y = start_pos[1] + dy * (i + 1) * dash_length
        pygame.draw.line(screen, color, (start_x, start_y), (end_x, end_y), 2)

# 메인 루프
running = True
clock = pygame.time.Clock()
dragging = False
while running:
    screen.fill(BLACK)

    # 모든 공이 멈췄는지 확인
    if all(ball.is_stationary() for ball in balls):
        turn_active = False

    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and not turn_active:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            distance = math.sqrt((mouse_x - white_ball.x)**2 + (mouse_y - white_ball.y)**2)
            if distance <= white_ball.radius:
                dragging = True
        elif event.type == pygame.MOUSEBUTTONUP and dragging and not turn_active:
            dragging = False
            mouse_x, mouse_y = pygame.mouse.get_pos()
            dx = white_ball.x - mouse_x
            dy = white_ball.y - mouse_y
            force = math.sqrt(dx**2 + dy**2) / 10
            angle = math.atan2(dy, dx)
            white_ball.vx = math.cos(angle) * force
            white_ball.vy = math.sin(angle) * force
            turn_active = True
            hit_red1 = False
            hit_red2 = False

    # 공 드래그
    if dragging:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        dx = white_ball.x - mouse_x
        dy = white_ball.y - mouse_y
        angle = math.atan2(dy, dx)
        drag_length = min(math.sqrt(dx**2 + dy**2), 300)  # 드래그 길이에 비례, 최대 300 제한
        guide_end_x = white_ball.x + math.cos(angle) * drag_length
        guide_end_y = white_ball.y + math.sin(angle) * drag_length
        draw_dotted_line(screen, (white_ball.x, white_ball.y), (guide_end_x, guide_end_y), WHITE)

    # 공 업데이트 및 공-공 충돌 처리
    for ball in balls:
        ball.update_position()

    for i in range(len(balls)):
        for j in range(i + 1, len(balls)):
            if CollisionCalculation(balls[i], balls[j]):
                ClculateElasticCollision(balls[i], balls[j], elasticity=0.8)  # 자연스러운 탄성
                # 적구 맞음 감지
                if turn_active and balls[i] == white_ball and balls[j] == red_ball_1:
                    hit_red1 = True
                elif turn_active and balls[i] == white_ball and balls[j] == red_ball_2:
                    hit_red2 = True

    # 득점 조건 체크
    if turn_active and hit_red1 and hit_red2:
        player_score += 1
        turn_active = False

    # 점수 표시
    score_text = font.render(f"Score: {player_score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    # 공 그리기
    for ball in balls:
        ball.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
