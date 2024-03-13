import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *


class GameCube:
    def __init__(self):
        self.num_of_tiles = 8
        self.tile_size = 100
        self.tiles_3d = [
            [[0] * self.num_of_tiles for _ in range(self.num_of_tiles)] for _ in range(self.num_of_tiles)]


vertices = ((1, -1, -1),
            (1, 1, -1),
            (-1, 1, -1),
            (-1, -1, -1),
            (1, -1, 1),
            (1, 1, 1),
            (-1, -1, 1),
            (-1, 1, 1)
            )

edges = ((0, 1),
         (0, 3),
         (0, 4),
         (2, 1),
         (2, 3),
         (2, 7),
         (6, 3),
         (6, 4),
         (6, 7),
         (5, 1),
         (5, 4),
         (5, 7)
         )

surfaces = (
    (0, 1, 2, 3),
    (3, 2, 7, 6),
    (6, 7, 5, 4),
    (4, 5, 1, 0),
    (1, 5, 7, 2),
    (4, 0, 3, 6)
)

colors = (
    (0.6, 0.8, 1.0, 0.5),  # Light blue color with 50% opacity for all surfaces
    (0.6, 0.8, 1.0, 0.5),
    (0.6, 0.8, 1.0, 0.5),
    (0.6, 0.8, 1.0, 0.5),
    (0.6, 0.8, 1.0, 0.5),
    (0.6, 0.8, 1.0, 0.5),
    (0.0, 0.0, 0.4, 1.0),  # Dark blue color with 100% opacity for edges
    (0.0, 0.0, 0.4, 1.0),
    (0.0, 0.0, 0.4, 1.0),
    (0.0, 0.0, 0.4, 1.0),
    (0.0, 0.0, 0.4, 1.0),
    (0.0, 0.0, 0.4, 1.0),
)

grab = False


def Cube():
    glLineWidth(2.0)  # Set the line width for edges
    for i, surface in enumerate(surfaces):
        glBegin(GL_POLYGON)
        glColor4fv(colors[i])
        for vertex in surface:
            glVertex3fv(vertices[vertex])
        glEnd()

    glBegin(GL_LINES)
    glColor4fv((0.0, 0.0, 0.4, 1.0))  # Set color for edges
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()
    glLineWidth(1.0)  # Reset the line width to default


rotation_speed = 0.5


def update_rotation(mouse_pos):
    global rotation_speed
    x, y = mouse_pos
    # Adjust the rotation angles based on the mouse movement
    rotation_angle_x = x * rotation_speed
    rotation_angle_y = y * rotation_speed
    glRotatef(rotation_angle_x, 0, 1, 0)
    glRotatef(rotation_angle_y, 1, 0, 0)


def main():
    pygame.init()
    window = (800, 800)
    pygame.display.set_mode(window, DOUBLEBUF | OPENGL)

    glDisable(GL_BLEND)  # Disable blending for solid appearance
    glDisable(GL_CULL_FACE)  # Disable face culling

    gluPerspective(45, (window[0] / window[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -5)  # viewer's perspective
    glRotatef(0, 0, 0, 0)

    global grab  # Declare grab as a global variable

    running = True
    clock = pygame.time.Clock()

    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    grab = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    grab = False
            if grab and event.type == MOUSEMOTION:
                update_rotation(event.rel)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        Cube()
        pygame.display.flip()

    pygame.quit()


main()
