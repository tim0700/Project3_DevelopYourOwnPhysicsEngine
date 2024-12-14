import math
def CollisionCalculation(ball1, ball2):
    """
    두 공 사이의 충돌(겹침)을 감지하고, 겹침을 해소합니다.
    :param ball1: 첫 번째 공 객체
    :param ball2: 두 번째 공 객체
    :return: 겹침이 발생하면 True, 그렇지 않으면 False
    """
    dx = ball2.x - ball1.x
    dy = ball2.y - ball1.y
    distance = math.sqrt(dx**2 + dy**2)

    if distance < ball1.radius + ball2.radius:
        # 겹침(Overlap) 계산 및 위치 조정
        overlap = ball1.radius + ball2.radius - distance
        nx, ny = dx / distance, dy / distance
        ball1.x -= nx * overlap / 2
        ball1.y -= ny * overlap / 2
        ball2.x += nx * overlap / 2
        ball2.y += ny * overlap / 2
        return True  # 충돌이 발생했음을 반환
    return False  # 충돌이 발생하지 않음


def ClculateElasticCollision(ball1, ball2, elasticity=1.0):
    """
    두 공 사이의 탄성 충돌 계산.
    :param ball1: 첫 번째 공 객체
    :param ball2: 두 번째 공 객체
    :param elasticity: 탄성 계수 (기본값은 1.0)
    """
    dx = ball2.x - ball1.x
    dy = ball2.y - ball1.y
    distance = math.sqrt(dx**2 + dy**2)

    if distance == 0:  # 두 공의 중심이 같은 경우(비정상 상태)
        return

    # 충돌 방향 계산
    nx, ny = dx / distance, dy / distance

    # 운동량 교환 계산
    p = (1 + elasticity) * (ball1.vx * nx + ball1.vy * ny - ball2.vx * nx - ball2.vy * ny) / (ball1.mass + ball2.mass)

    # 각 공의 속도 업데이트
    ball1.vx -= p * ball2.mass * nx
    ball1.vy -= p * ball2.mass * ny
    ball2.vx += p * ball1.mass * nx
    ball2.vy += p * ball1.mass * ny