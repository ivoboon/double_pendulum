import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'
import pygame
import math

# Initialising PyGame
pygame.init()

# Making surface
screen_width = 1000
screen_height = 1000
surface = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Double Pendulum')
font = pygame.font.Font(None, 50)

# Visualisation variables
colour = [255, 255, 255]
dt = 0.01

# Pivot point for double pendulum
pivot = [500, 500]

# Pendulum variables
m1 = 1
m2 = 1
g = 9.81
l1 = 200
l2 = 200

# Initial conditions
theta1 = 1
theta2 = 1
omega1 = 0
omega2 = 0

def A(m1, m2, l1):
    return (m1 + m2) * l1

def B(m2, l2, theta1, theta2):
    return m2 * l2 * math.cos(theta1 - theta2)

def C(m1, m2, l2, g, omega2):
    return m2 * l2 * omega2 ** 2 * math.sin(theta1 - theta2) + (m1 + m2) * g * math.sin(theta1)

def K(m2, l2):
    return m2 * l2

def L(m2, l1, theta1, theta2):
    return m2 * l1 * math.cos(theta1 - theta2)

def M(m2, l1, g, theta1, theta2, omega1):
    return -m2 * l1 * omega1 ** 2 * math.sin(theta1 - theta2) + m2 * g * math.sin(theta2)

def omega1dot(A, B, C, K, L, M):
    return (B * M - C * K) / (A * K - B * L)

def omega2dot(A, B, C, K, L, M):
    return (C * L - A * M) / (A * K - B * L)

# PyGame loop
run = True

while run:

    surface.fill((0, 0, 0))

    k1theta1 = dt * omega1
    k1theta2 = dt * omega2
    k1omega1 = dt * omega1dot(A(m1, m2, l1), B(m2, l2, theta1, theta2), C(m1, m2, l2, g, omega2), K(m2, l2), L(m2, l1, theta1, theta2), M(m2, l1, g, theta1, theta2, omega1))
    k1omega2 = dt * omega2dot(A(m1, m2, l1), B(m2, l2, theta1, theta2), C(m1, m2, l2, g, omega2), K(m2, l2), L(m2, l1, theta1, theta2), M(m2, l1, g, theta1, theta2, omega1))

    k2theta1 = dt * (omega1 + k1omega1 / 2)
    k2theta2 = dt * (omega2 + k1omega2 / 2)
    k2omega1 = dt * omega1dot(A(m1, m2, l1), B(m2, l2, theta1 + k1theta1 / 2, theta2 + k1theta2 / 2), C(m1, m2, l2, g, omega2 + k1omega2 / 2), K(m2, l2), L(m2, l1, theta1 + k1theta1 / 2, theta2 + k1theta2 / 2), M(m2, l1, g, theta1 + k1theta1 / 2, theta2 + k1theta2 / 2, omega1 + k1omega1 / 2))
    k2omega2 = dt * omega2dot(A(m1, m2, l1), B(m2, l2, theta1 + k1theta1 / 2, theta2 + k1theta2 / 2), C(m1, m2, l2, g, omega2 + k1omega2 / 2), K(m2, l2), L(m2, l1, theta1 + k1theta1 / 2, theta2 + k1theta2 / 2), M(m2, l1, g, theta1 + k1theta1 / 2, theta2 + k1theta2 / 2, omega1 + k1omega1 / 2))

    k3theta1 = dt * (omega1 + k2omega1 / 2)
    k3theta2 = dt * (omega2 + k2omega2 / 2)
    k3omega1 = dt * omega1dot(A(m1, m2, l1), B(m2, l2, theta1 + k2theta1 / 2, theta2 + k2theta2 / 2), C(m1, m2, l2, g, omega2 + k2omega2 / 2), K(m2, l2), L(m2, l1, theta1 + k2theta1 / 2, theta2 + k2theta2 / 2), M(m2, l1, g, theta1 + k2theta1 / 2, theta2 + k2theta2 / 2, omega1 + k2omega1 / 2))
    k3omega2 = dt * omega2dot(A(m1, m2, l1), B(m2, l2, theta1 + k2theta1 / 2, theta2 + k2theta2 / 2), C(m1, m2, l2, g, omega2 + k2omega2 / 2), K(m2, l2), L(m2, l1, theta1 + k2theta1 / 2, theta2 + k2theta2 / 2), M(m2, l1, g, theta1 + k2theta1 / 2, theta2 + k2theta2 / 2, omega1 + k2omega1 / 2))

    k4theta1 = dt * (omega1 + k3omega1)
    k4theta2 = dt * (omega2 + k3omega2)
    k4omega1 = dt * omega1dot(A(m1, m2, l1), B(m2, l2, theta1 + k3theta1, theta2 + k3theta2), C(m1, m2, l2, g, omega2 + k3omega2), K(m2, l2), L(m2, l1, theta1 + k3theta1, theta2 + k3theta2), M(m2, l1, g, theta1 + k3theta1, theta2 + k3theta2, omega1 + k3omega1))
    k4omega2 = dt * omega2dot(A(m1, m2, l1), B(m2, l2, theta1 + k3theta1, theta2 + k3theta2), C(m1, m2, l2, g, omega2 + k3omega2), K(m2, l2), L(m2, l1, theta1 + k3theta1, theta2 + k3theta2), M(m2, l1, g, theta1 + k3theta1, theta2 + k3theta2, omega1 + k3omega1))

    theta1 = theta1 + (k1theta1 + 2 * k2theta1 + 2 * k3theta1 + k4theta1) / 6
    theta2 = theta2 + (k1theta2 + 2 * k2theta2 + 2 * k3theta2 + k4theta2) / 6
    omega1 = omega1 + (k1omega1 + 2 * k2omega1 + 2 * k3omega1 + k4omega1) / 6
    omega2 = omega2 + (k1omega2 + 2 * k2omega2 + 2 * k3omega2 + k4omega2) / 6

    x1 = l1 * math.sin(theta1)
    y1 = -l1 * math.cos(theta1)
    x2 = x1 + l2 * math.sin(theta2)
    y2 = y1 - l2 * math.cos(theta2)

    x1y1 = [pivot[0] + x1, pivot[1] - y1]
    x2y2 = [pivot[0] + x2, pivot[1] - y2]

    # Draw pivot
    pygame.draw.circle(surface, colour, pivot, 5, 0)

    # Draw arm 1
    pygame.draw.aaline(surface, colour, pivot, x1y1)
    pygame.draw.circle(surface, colour, x1y1, 5, 0)

    # Draw arm 2
    pygame.draw.aaline(surface, colour, x1y1, x2y2)
    pygame.draw.circle(surface, colour, x2y2, 5, 0)

    # Calculate total energy and display on screen
    T = m1 * l1 ** 2 * omega1 ** 2 / 2 + m2 * (l1 ** 2 * omega1 ** 2 + l2 ** 2 * omega2 ** 2 + 2 * l1 * l2 * omega1 * omega2 * math.cos(theta1 - theta2)) / 2
    V = -m1 * g * l1 * math.cos(theta1) - m2 * g * l1 * math.cos(theta1) - m2 * g * l2 * math.cos(theta2)
    text = font.render(f"Total energy: {str(int(T + V))} J", True, colour)
    surface.blit(text, [0, 0])

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    pygame.display.flip()

pygame.quit