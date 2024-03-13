import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from itertools import product


class SmallCube:
    def __init__(self, x, y, z, visibility):
        self.x = x
        self.y = y
        self.z = z
        self.visibility = visibility

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getZ(self):
        return self.z

    def getVisibility(self):
        return self.visibility


cubes_per_row = 1
num_of_cubes = cubes_per_row ** 3
small_cube_length = 10 / cubes_per_row
grab = False

small_cubes = [
    SmallCube(
        x=-(cubes_per_row - 1) * small_cube_length +
        xx * 2 * small_cube_length,
        y=-(cubes_per_row - 1) * small_cube_length +
        yy * 2 * small_cube_length,
        z=-(cubes_per_row - 1) * small_cube_length +
        zz * 2 * small_cube_length,
        visibility=0
    )
    for xx, yy, zz in product(range(cubes_per_row), repeat=3)
]

# Set Randoom Cubes
############################################
# for x in range(len(small_cubes)):
#     random_number = random.choice([0, 1])
#     small_cubes[x].visibility = random_number
############################################

vertices = ((10, -10, -10), (10, 10, -10), (-10, 10, -10), (-10, -10, -10),
            (10, -10, 10), (10, 10, 10), (-10, -10, 10), (-10, 10, 10))

edges = ((0, 1), (0, 3), (0, 4), (2, 1), (2, 3), (2, 7),
         (6, 3), (6, 4), (6, 7), (5, 1), (5, 4), (5, 7))

surfaces = (
    (0, 1, 2, 3), (3, 2, 7, 6), (6, 7, 5, 4),
    (4, 5, 1, 0), (1, 5, 7, 2), (4, 0, 3, 6)
)

colors = (
    (0.6, 0.8, 1.0, 0.5),) * 5 + ((0.0, 0.0, 0.4, 1.0),) * 6

small_cube_vertices = [
    (small_cube_length, -small_cube_length, -small_cube_length),
    (small_cube_length, small_cube_length, -small_cube_length),
    (-small_cube_length, small_cube_length, -small_cube_length),
    (-small_cube_length, -small_cube_length, -small_cube_length),
    (small_cube_length, -small_cube_length, small_cube_length),
    (small_cube_length, small_cube_length, small_cube_length),
    (-small_cube_length, -small_cube_length, small_cube_length),
    (-small_cube_length, small_cube_length, small_cube_length)
]


def draw_cube(vertices):
    glLineWidth(1.0)
    glBegin(GL_LINES)
    glColor4fv((0.0, 0.0, 0.4, 1.0))  # Set color for edges
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()


def draw_small_cubes():
    for cube in small_cubes:
        # comment out to reome small cube borders
        ############################
        glPushMatrix()
        glTranslatef(cube.x, cube.y, cube.z)
        draw_cube(small_cube_vertices)
        glPopMatrix()
        ############################

        if cube.visibility == 1:
            for i, surface in enumerate(surfaces):
                glBegin(GL_POLYGON)
                glColor4fv(colors[i])
                for vertex_index in surface:
                    scaled_vertex = (
                        small_cube_vertices[vertex_index][0],
                        small_cube_vertices[vertex_index][1],
                        small_cube_vertices[vertex_index][2]
                    )
                    translated_vertex = (
                        scaled_vertex[0] + cube.x,
                        scaled_vertex[1] + cube.y,
                        scaled_vertex[2] + cube.z
                    )
                    glVertex3fv(translated_vertex)
                glEnd()


def updateStates():
    global small_cubes
    new_cubes = []

    for cube in small_cubes:
        this_X, this_Y, this_Z = cube.getX(), cube.getY(), cube.getZ()
        this_visibility = cube.getVisibility()
        visible_neighbors = 0
        new_visibility = 0

        for i, j, k in [(-1, -1, -1), (-1, -1, 0), (-1, -1, 1),
                        (-1, 0, -1),  (-1, 0, 0),  (-1, 0, 1),
                        (-1, 1, -1),  (-1, 1, 0),  (-1, 1, 1),
                        (0, -1, -1),  (0, -1, 0),  (0, -1, 1),
                        (0, 0, -1),                (0, 0, 1),
                        (0, 1, -1),   (0, 1, 0),   (0, 1, 1),
                        (1, -1, -1),  (1, -1, 0),  (1, -1, 1),
                        (1, 0, -1),   (1, 0, 0),   (1, 0, 1),
                        (1, 1, -1),   (1, 1, 0),   (1, 1, 1)]:
            new_row, new_col, new_depth = this_X + i, this_Y + j, this_Z + k

            # index = x + ( y × width ) + ( z × width × height )
            neighbor_index = new_row + (new_col * (cubes_per_row - 1)) + (
                new_depth * (cubes_per_row - 1) * (cubes_per_row - 1))
            print(cube.getX(), cube.getY(), cube.getZ())
            neighbor_index = int(neighbor_index)

            visible_neighbors += small_cubes[neighbor_index].getVisibility()

       # update state based on rules

        if this_visibility == 0 and 8 <= visible_neighbors <= 12:
            new_visibility = 1

        elif this_visibility == 1 and (visible_neighbors <= 5 or visible_neighbors >= 13):
            new_visibility = 0

        elif this_visibility == 1 and (5 <= visible_neighbors == 12):
            new_visibility = 1

        new_cubes.append(SmallCube(x=this_X, y=this_Y,
                         z=this_Z, visibility=new_visibility))

    small_cubes = new_cubes


def update_rotation(mouse_pos):
    rotation_speed = 0.5
    x, y = mouse_pos
    # Adjust the rotation angles based on the mouse movement
    rotation_angle_x = x * rotation_speed
    rotation_angle_y = y * rotation_speed
    glRotatef(rotation_angle_x, 0, 1, 0)
    glRotatef(rotation_angle_y, 1, 0, 0)


frame_counter = 0


def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluPerspective(45, (display[0] / display[1]), 0.1, 100.0)
    glTranslatef(0.0, 0.0, -50)
    glEnable(GL_BLEND)
    glEnable(GL_DEPTH_TEST)
    # glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA) # transparency
    global grab
    clock = pygame.time.Clock()
    global frame_counter

    while True:
        clock.tick(20)
        frame_counter += 1

        glRotatef(1, 0, 1, 0)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    grab = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    grab = False
            if grab and event.type == MOUSEMOTION:
                update_rotation(event.rel)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        draw_cube(vertices)
        draw_small_cubes()

        if frame_counter == 20:
            updateStates()
            frame_counter = 0

        pygame.display.flip()


if __name__ == "__main__":
    main()

#####################
## features to add ##
#####################

# if a square has just appeared I want to draw it yellow, And if it existed already in the old state I want it to be orange
# make code more efficient
# no matter how much I optimise python is just to slow
