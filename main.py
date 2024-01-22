import math

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *


vertices = [
    [1, -1, -1],
    [1, -1, 1],
    [-1, -1, 1],
    [-1, -1, -1],
    [0, 1, 0]
]

# Współrzędne tekstur
tex_coords = [
    [1, 0],
    [1, 1],
    [0, 1],
    [0, 0]
]
def draw_sphere(radius, slices=30, stacks=30):
    for i in range(stacks):
        lat0 = math.pi * (-0.5 + (i / stacks))
        z0 = math.sin(lat0) * radius
        zr0 = math.cos(lat0) * radius

        lat1 = math.pi * (-0.5 + ((i + 1) / stacks))
        z1 = math.sin(lat1) * radius
        zr1 = math.cos(lat1) * radius

        glBegin(GL_TRIANGLE_STRIP)
        for j in range(slices + 1):
            long = 2 * math.pi * (j / slices)
            x = math.cos(long) * zr0
            y = math.sin(long) * zr0
            glVertex3f(x, y, z0)

            x = math.cos(long) * zr1
            y = math.sin(long) * zr1
            glVertex3f(x, y, z1)
        glEnd()

def draw_3d_base():
    glBegin(GL_QUADS)
    glVertex3fv([2,-1,-2])  # Prawy dolny róg
    glVertex3fv([2,-1,2])  # Prawy górny róg
    glVertex3fv([-2,-1,2])  # Lewy górny róg
    glVertex3fv([-2,-1,-2])  # Lewy dolny róg
    glEnd()

def draw_pyramid_on_sphere(radius, theta, phi, depth, use_texture=False):
    x = radius * math.sin(theta) * math.cos(phi)
    y = radius * math.sin(theta) * math.sin(phi)
    z = radius * math.cos(theta)

    glTranslatef(x, y, z)
    draw_sphere(0.5)
    glTranslatef(-x, -y, -z)


texture_path = "crack.png"  # Dodaj ścieżkę do pliku z teksturą
light_direction = [2.0, -2.0, -2.0, 0.0]
light_position = [2.0, 2.0, 2.0, 1.0]
light_color = [1.0, 1.0, 1.0, 1.0]

def setup_lighting():
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHT1)

    glLightfv(GL_LIGHT0, GL_POSITION, light_direction)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.0, 1.0, 1.0, 1.0])

    glLightfv(GL_LIGHT1, GL_POSITION, light_position)
    glLightfv(GL_LIGHT1, GL_DIFFUSE, light_color)

def change_lighting():
    glLightfv(GL_LIGHT1, GL_POSITION, light_position)
    glLightfv(GL_LIGHT1, GL_DIFFUSE, light_color)

def handle_light_controls():
    global light_position, light_color

    keys = pygame.key.get_pressed()

    if keys[K_a]:
        light_position[0] -= 0.1
    if keys[K_d]:
        light_position[0] += 0.1
    if keys[K_w]:
        light_position[1] += 0.1
    if keys[K_s]:
        light_position[1] -= 0.1
    if keys[K_q]:
        light_position[2] -= 0.1
    if keys[K_e]:
        light_position[2] += 0.1

    if keys[K_r]:
        light_color = [1.0, 0.0, 0.0, 1.0]  # Czerwony
    if keys[K_g]:
        light_color = [0.0, 1.0, 0.0, 1.0]  # Zielony
    if keys[K_b]:
        light_color = [0.0, 0.0, 1.0, 1.0]  # Niebieski
    if keys[K_y]:
        light_color = [1.0, 1.0, 0.0, 1.0]  # Żółty
    if keys[K_p]:
        light_color = [1.0, 0.0, 1.0, 1.0]  # Purpurowy
    if keys[K_c]:
        light_color = [0.0, 1.0, 1.0, 1.0]  # Turkusowy
    if keys[K_w] and keys[K_r]:
        light_color = [1.0, 1.0, 1.0, 1.0]  # Biały



def load_texture():
    texture_surface = pygame.image.load(texture_path)
    texture_data = pygame.image.tostring(texture_surface, "RGBA", 1)
    width, height = texture_surface.get_size()

    glEnable(GL_TEXTURE_2D)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glBindTexture(GL_TEXTURE_2D, glGenTextures(1))
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, texture_data)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

def draw_pyramid_recursion(vertex1, vertex2, vertex3, depth, use_texture=False):
    if depth == 0:
        glBegin(GL_TRIANGLES)
        if use_texture:
            glTexCoord2fv(tex_coords[0])
        glVertex3fv(vertex1)
        if use_texture:
            glTexCoord2fv(tex_coords[1])
        glVertex3fv(vertex2)
        if use_texture:
            glTexCoord2fv(tex_coords[2])
        glVertex3fv(vertex3)
        glEnd()
        draw_3d_base()
    else:
        mid1 = [(v1 + v2) / 2 for v1, v2 in zip(vertex1, vertex2)]
        mid2 = [(v2 + v3) / 2 for v2, v3 in zip(vertex2, vertex3)]
        mid3 = [(v1 + v3) / 2 for v1, v3 in zip(vertex1, vertex3)]

        draw_pyramid_recursion(vertex1, mid1, mid3, depth-1, use_texture)
        draw_pyramid_recursion(mid1, vertex2, mid2, depth-1, use_texture)
        draw_pyramid_recursion(mid3, mid2, vertex3, depth-1, use_texture)

def draw_sierpinski_pyramid(depth, use_texture=False):
    draw_pyramid_recursion(vertices[0], vertices[1], vertices[4], depth, use_texture)
    draw_pyramid_recursion(vertices[1], vertices[2], vertices[4], depth, use_texture)
    draw_pyramid_recursion(vertices[2], vertices[3], vertices[4], depth, use_texture)
    draw_pyramid_recursion(vertices[3], vertices[0], vertices[4], depth, use_texture)

def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL | pygame.OPENGLBLIT)

    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -5)

    rotation_speed = 1.0
    zoom_speed = 0.1
    auto_rotation_speed = 1.0
    texture_enabled = False  # Zmienna kontrolująca widoczność tekstury

    sphere_radius = 3.0  # Domyślny promień kuli
    sphere_theta = 0.0  # Kąt theta (polarny)
    sphere_phi = 0.0  # Kąt phi (azymutalny)
    sphere_theta_speed = 0.01  # Prędkość zmiany kąta theta

    glEnable(GL_DEPTH_TEST)

    depth = None
    rotating_left = rotating_right = rotating_up = rotating_down = False

    while depth is None:
        try:
            depth = int(input("Podaj liczbę poziomów (liczba całkowita): "))
        except ValueError:
            print("Nieprawidłowa liczba. Podaj liczbę całkowitą.")

    load_texture()
    setup_lighting()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    rotating_left = True
                elif event.key == pygame.K_RIGHT:
                    rotating_right = True
                elif event.key == pygame.K_UP:
                    rotating_up = True
                elif event.key == pygame.K_DOWN:
                    rotating_down = True
                elif event.key == pygame.K_KP_PLUS:
                    glScalef(1.0 + zoom_speed, 1.0 + zoom_speed, 1.0 + zoom_speed)
                elif event.key == pygame.K_KP_MINUS:
                    glScalef(1.0 - zoom_speed, 1.0 - zoom_speed, 1.0 - zoom_speed)
                elif event.key == pygame.K_t:
                    texture_enabled = not texture_enabled  # Przełączanie widoczności tekstury
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    rotating_left = False
                elif event.key == pygame.K_RIGHT:
                    rotating_right = False
                elif event.key == pygame.K_UP:
                    rotating_up = False
                elif event.key == pygame.K_DOWN:
                    rotating_down = False

            handle_light_controls()
            change_lighting()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        if rotating_left:
            glRotatef(rotation_speed, 0, 1, 0)
        if rotating_right:
            glRotatef(-rotation_speed, 0, 1, 0)
        if rotating_up:
            glRotatef(rotation_speed, 1, 0, 0)
        if rotating_down:
            glRotatef(-rotation_speed, 1, 0, 0)

        draw_sierpinski_pyramid(depth, use_texture=texture_enabled)

        draw_pyramid_on_sphere(sphere_radius, sphere_theta, sphere_phi, depth, use_texture=texture_enabled)

        # Automatyczny obrót wokół osi Y
        glRotatef(auto_rotation_speed, 0, 1, 0)

        pygame.display.flip()
        pygame.time.wait(10)
        sphere_theta += sphere_theta_speed

if __name__ == "__main__":
    main()
