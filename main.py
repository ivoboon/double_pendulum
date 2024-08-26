import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'
import pygame
import math

def A(m1, m2, l1):
    """
    Computes coefficient A in DEs
    """
    return (m1 + m2) * l1


def B(m2, l2, theta1, theta2):
    """
    Computes coefficient B in DEs
    """
    return m2 * l2 * math.cos(theta1 - theta2)


def C(m1, m2, l2, g, theta1, theta2, omega2):
    """
    Computes coefficient C in DEs
    """
    return m2 * l2 * omega2 ** 2 * math.sin(theta1 - theta2) + (m1 + m2) * g * math.sin(theta1)


def K(m2, l2):
    """
    Computes coefficient K in DEs
    """
    return m2 * l2


def L(m2, l1, theta1, theta2):
    """
    Computes coefficient L in DEs
    """
    return m2 * l1 * math.cos(theta1 - theta2)


def M(m2, l1, g, theta1, theta2, omega1):
    """
    Computes coefficient M in DEs
    """
    return -m2 * l1 * omega1 ** 2 * math.sin(theta1 - theta2) + m2 * g * math.sin(theta2)


def omega1dot(A, B, C, K, L, M):
    """
    Computes angular acceleration of the first pendulum
    """
    return (B * M - C * K) / (A * K - B * L)


def omega2dot(A, B, C, K, L, M):
    """
    Computes angular acceleration of the second pendulum
    """
    return (C * L - A * M) / (A * K - B * L)


def main():
    """
    Main function
    """
    # Input variables

    # Screen dimensions
    screen_width = 1000
    screen_height = 1000

    # Colours
    background_colour = (0, 0, 0)
    pendulum_colour = (255, 255, 255)
    text_colour = (255, 255, 255)

    # Pivot point for double pendulum
    pivot = [500, 500]

    # Time step
    dt = 0.01

    # Pendulum variables
    m1 = 1
    m2 = 1
    g = 9.81
    l1 = 200
    l2 = 200

    # Initial conditions
    theta1 = 1
    theta2 = 1
    omega1 = 0.2
    omega2 = 0

    # Initialising PyGame
    pygame.init()
    surface = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('Double Pendulum')
    font = pygame.font.Font(None, 50)

    # PyGame loop
    run = True

    while run:

        surface.fill(background_colour)

        # Half-step update for velocities (omega1 and omega2)
        omega1 += 0.5 * dt * omega1dot(A(m1, m2, l1), B(m2, l2, theta1, theta2), 
                                    C(m1, m2, l2, g, theta1, theta2, omega2), K(m2, l2), 
                                    L(m2, l1, theta1, theta2), 
                                    M(m2, l1, g, theta1, theta2, omega1))
        omega2 += 0.5 * dt * omega2dot(A(m1, m2, l1), B(m2, l2, theta1, theta2), 
                                    C(m1, m2, l2, g, theta1, theta2, omega2), K(m2, l2), 
                                    L(m2, l1, theta1, theta2), 
                                    M(m2, l1, g, theta1, theta2, omega1))
        
        # Full-step update for angles (theta1 and theta2)
        theta1 += dt * omega1
        theta2 += dt * omega2

        # Full-step update for velocities (omega1 and omega2)
        omega1 += 0.5 * dt * omega1dot(A(m1, m2, l1), B(m2, l2, theta1, theta2), 
                                    C(m1, m2, l2, g, theta1, theta2, omega2), K(m2, l2), 
                                    L(m2, l1, theta1, theta2), 
                                    M(m2, l1, g, theta1, theta2, omega1))
        omega2 += 0.5 * dt * omega2dot(A(m1, m2, l1), B(m2, l2, theta1, theta2), 
                                    C(m1, m2, l2, g, theta1, theta2, omega2), K(m2, l2), 
                                    L(m2, l1, theta1, theta2), 
                                    M(m2, l1, g, theta1, theta2, omega1))

        # Calculate the position of the masses
        x1 = l1 * math.sin(theta1)
        y1 = -l1 * math.cos(theta1)
        x2 = x1 + l2 * math.sin(theta2)
        y2 = y1 - l2 * math.cos(theta2)

        x1y1 = [pivot[0] + x1, pivot[1] - y1]
        x2y2 = [pivot[0] + x2, pivot[1] - y2]

        # Draw pivot
        pygame.draw.circle(surface, pendulum_colour, pivot, 5, 0)

        # Draw arm 1
        pygame.draw.aaline(surface, pendulum_colour, pivot, x1y1)
        pygame.draw.circle(surface, pendulum_colour, x1y1, 5, 0)

        # Draw arm 2
        pygame.draw.aaline(surface, pendulum_colour, x1y1, x2y2)
        pygame.draw.circle(surface, pendulum_colour, x2y2, 5, 0)

        # Calculate total energy and display on screen
        T = m1 * l1 ** 2 * omega1 ** 2 / 2 + m2 * (l1 ** 2 * omega1 ** 2 + l2 ** 2 * omega2 ** 2 + 2 * l1 * l2 * omega1 * omega2 * math.cos(theta1 - theta2)) / 2
        V = -m1 * g * l1 * math.cos(theta1) - m2 * g * l1 * math.cos(theta1) - m2 * g * l2 * math.cos(theta2)
        text = font.render(f"Total energy: {str(int(T + V))} J", True, text_colour)
        surface.blit(text, [0, 0])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        pygame.display.flip()

if __name__ == "__main__":
    main()