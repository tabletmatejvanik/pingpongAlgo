
import pygame
from random import choice

pygame.init()

# =========================================================
# WINDOW
# =========================================================

WIN_WIDTH = 900
WIN_HEIGHT = 600
FPS = 60

window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("NEON PONG")

clock = pygame.time.Clock()

# =========================================================
# COLORS
# =========================================================

BLACK = (0, 0, 0)

CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)

WHITE = (255, 255, 255)

DARK_CYAN = (0, 80, 80)
DARK_MAGENTA = (80, 0, 80)

# =========================================================
# FONTS
# =========================================================

score_font = pygame.font.SysFont("consolas", 80, bold=True)
small_font = pygame.font.SysFont("consolas", 22, bold=True)

# =========================================================
# BALL IMAGE
# =========================================================

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

ball_image = pygame.image.load(
    os.path.join(BASE_DIR, "tenis_ball.png")
).convert_alpha()

BALL_SIZE = 40

ball_image = pygame.transform.scale(
    ball_image,
    (BALL_SIZE, BALL_SIZE)
)

ball = ball_image.get_rect(
    center=(WIN_WIDTH // 2, WIN_HEIGHT // 2)
)

# =========================================================
# BALL
# =========================================================

ball_speed_x = choice([-6, 6])
ball_speed_y = choice([-4, -3, 3, 4])

# =========================================================
# PADDLES
# =========================================================

PADDLE_WIDTH = 25
PADDLE_HEIGHT = 140
PADDLE_SPEED = 9

left_paddle = pygame.Rect(
    45,
    WIN_HEIGHT // 2 - PADDLE_HEIGHT // 2,
    PADDLE_WIDTH,
    PADDLE_HEIGHT
)

right_paddle = pygame.Rect(
    WIN_WIDTH - 45 - PADDLE_WIDTH,
    WIN_HEIGHT // 2 - PADDLE_HEIGHT // 2,
    PADDLE_WIDTH,
    PADDLE_HEIGHT
)

# =========================================================
# SCORE
# =========================================================

left_score = 0
right_score = 0

# =========================================================
# NEON GLOW
# =========================================================

def draw_neon_rect(surface, rect, color, radius=12, glow=20):

    # Glow layers
    for i in range(glow, 0, -4):

        alpha = max(5, 80 - i * 3)

        glow_surface = pygame.Surface(
            (rect.width + i * 2, rect.height + i * 2),
            pygame.SRCALPHA
        )

        pygame.draw.rect(
            glow_surface,
            (*color, alpha),
            (
                i,
                i,
                rect.width,
                rect.height
            ),
            border_radius=radius
        )

        surface.blit(
            glow_surface,
            (
                rect.x - i,
                rect.y - i
            )
        )

    # Main paddle
    pygame.draw.rect(
        surface,
        color,
        rect,
        border_radius=radius
    )

    # Bright inner edge
    inner = rect.inflate(-8, -8)

    pygame.draw.rect(
        surface,
        WHITE,
        inner,
        width=2,
        border_radius=max(2, radius - 4)
    )


def draw_neon_circle(surface, position, radius, color):

    # Outer glow
    for i in range(25, 0, -3):

        alpha = max(5, 70 - i * 2)

        glow = pygame.Surface(
            (radius * 2 + i * 2, radius * 2 + i * 2),
            pygame.SRCALPHA
        )

        pygame.draw.circle(
            glow,
            (*color, alpha),
            (
                radius + i,
                radius + i
            ),
            radius
        )

        surface.blit(
            glow,
            (
                position[0] - radius - i,
                position[1] - radius - i
            )
        )

    pygame.draw.circle(
        surface,
        color,
        position,
        radius
    )

# =========================================================
# RESET BALL
# =========================================================

def reset_ball(direction):

    global ball_speed_x
    global ball_speed_y

    ball.center = (
        WIN_WIDTH // 2,
        WIN_HEIGHT // 2
    )

    ball_speed_x = direction * 6

    ball_speed_y = choice(
        [-4, -3, 3, 4]
    )


# =========================================================
# MAIN LOOP
# =========================================================

run = True

while run:

    # =====================================================
    # EVENTS
    # =====================================================

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            run = False

    # =====================================================
    # CONTROLS
    # =====================================================

    keys = pygame.key.get_pressed()

    # LEFT PLAYER
    if keys[pygame.K_w]:
        left_paddle.y -= PADDLE_SPEED

    if keys[pygame.K_s]:
        left_paddle.y += PADDLE_SPEED

    # RIGHT PLAYER
    if keys[pygame.K_UP]:
        right_paddle.y -= PADDLE_SPEED

    if keys[pygame.K_DOWN]:
        right_paddle.y += PADDLE_SPEED

    # =====================================================
    # PADDLE LIMITS
    # =====================================================

    if left_paddle.top < 0:
        left_paddle.top = 0

    if left_paddle.bottom > WIN_HEIGHT:
        left_paddle.bottom = WIN_HEIGHT

    if right_paddle.top < 0:
        right_paddle.top = 0

    if right_paddle.bottom > WIN_HEIGHT:
        right_paddle.bottom = WIN_HEIGHT

    # =====================================================
    # BALL MOVEMENT
    # =====================================================

    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # =====================================================
    # WALL COLLISION
    # =====================================================

    if ball.top <= 0:

        ball.top = 0
        ball_speed_y *= -1

    if ball.bottom >= WIN_HEIGHT:

        ball.bottom = WIN_HEIGHT
        ball_speed_y *= -1

    # =====================================================
    # LEFT PADDLE
    # =====================================================

    if (
        ball.colliderect(left_paddle)
        and ball_speed_x < 0
    ):

        ball.left = left_paddle.right

        ball_speed_x *= -1

        hit = (
            ball.centery - left_paddle.centery
        ) / (PADDLE_HEIGHT / 2)

        ball_speed_y = hit * 7

    # =====================================================
    # RIGHT PADDLE
    # =====================================================

    if (
        ball.colliderect(right_paddle)
        and ball_speed_x > 0
    ):

        ball.right = right_paddle.left

        ball_speed_x *= -1

        hit = (
            ball.centery - right_paddle.centery
        ) / (PADDLE_HEIGHT / 2)

        ball_speed_y = hit * 7

    # =====================================================
    # SCORE
    # =====================================================

    if ball.right < 0:

        right_score += 1

        reset_ball(1)

    if ball.left > WIN_WIDTH:

        left_score += 1

        reset_ball(-1)

    # =====================================================
    # DRAW
    # =====================================================

    # PURE BLACK
    window.fill(BLACK)

    # =====================================================
    # CYBERPUNK CENTER LINE
    # =====================================================

    for y in range(0, WIN_HEIGHT, 35):

        line_rect = pygame.Rect(
            WIN_WIDTH // 2 - 2,
            y,
            4,
            18
        )

        pygame.draw.rect(
            window,
            DARK_CYAN,
            line_rect,
            border_radius=2
        )

    # =====================================================
    # NEON BORDER
    # =====================================================

    border_rect = pygame.Rect(
        8,
        8,
        WIN_WIDTH - 16,
        WIN_HEIGHT - 16
    )

    pygame.draw.rect(
        window,
        DARK_CYAN,
        border_rect,
        width=2,
        border_radius=8
    )

    # =====================================================
    # PADDLES
    # =====================================================

    draw_neon_rect(
        window,
        left_paddle,
        CYAN,
        radius=12,
        glow=24
    )

    draw_neon_rect(
        window,
        right_paddle,
        MAGENTA,
        radius=12,
        glow=24
    )

    # =====================================================
    # BALL
    # =====================================================

    # Neon glow behind tennis.png
    draw_neon_circle(
        window,
        ball.center,
        23,
        CYAN
    )

    window.blit(
        ball_image,
        ball
    )

    # =====================================================
    # SCORE
    # =====================================================

    left_text = score_font.render(
        str(left_score),
        True,
        CYAN
    )

    right_text = score_font.render(
        str(right_score),
        True,
        MAGENTA
    )

    window.blit(
        left_text,
        (WIN_WIDTH // 2 - 130, 25)
    )

    window.blit(
        right_text,
        (WIN_WIDTH // 2 + 80, 25)
    )

    # =====================================================
    # TITLE
    # =====================================================

    title = small_font.render(
        "N E O N   P O N G",
        True,
        WHITE
    )

    title_rect = title.get_rect(
        center=(WIN_WIDTH // 2, 115)
    )

    window.blit(
        title,
        title_rect
    )

    # =====================================================
    # CONTROLS
    # =====================================================

    controls = small_font.render(
        "W/S",
        True,
        CYAN
    )

    controls2 = small_font.render(
        "UP/DOWN",
        True,
        MAGENTA
    )

    window.blit(
        controls,
        (30, WIN_HEIGHT - 40)
    )

    window.blit(
        controls2,
        (WIN_WIDTH - 120, WIN_HEIGHT - 40)
    )

    # =====================================================
    # UPDATE
    # =====================================================

    pygame.display.flip()

    clock.tick(FPS)


pygame.quit()
