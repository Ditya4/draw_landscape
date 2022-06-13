import pygame
from math import sin


class Snowflake:

    def __init__(self, x, y, radius, surface, color, y_speed, window_height):
        """
            x, y is a center of the snowflake (crossline)
            :move_sin_x is gonna be a movement sinus like by x coordinate
            durring falling with :y_speed of y coordinate
        """
        self.x = x
        self.y = y
        self.radius = radius
        self.surface = surface
        self.color = color
        self.y_speed = y_speed
        self.window_height = window_height
        self.move_sin_x = 0

    def move(self):
        self.move_sin_x = sin(self.y) * 3
        self.x += round(self.move_sin_x)
        if self.y < self.window_height:
            self.y += self.y_speed
        else:
            self.y = -2 * self.radius

    def draw_line(self, start_point_x, start_point_y, end_point_x,
                  end_point_y):
        pygame.draw.line(self.surface, self.color,
                         (start_point_x, start_point_y),
                         (end_point_x, end_point_y))

    def draw(self):
        """
            cause some lazy ass didt't get a correct mathematic formula we get
            some aproximatelly coeficient — delta
        """
        delta = (self.radius * 2) // 3
        lines = [[self.x - self.radius, self.y, self.x + self.radius, self.y],
                 [self.x, self.y - self.radius, self.x, self.y + self.radius],
                 [self.x - delta, self.y - delta,
                  self.x + delta, self.y + delta],
                 [self.x + delta, self.y - delta,
                  self.x - delta, self.y + delta]]
        for index in range(len(lines)):
            self.draw_line(*lines[index])
