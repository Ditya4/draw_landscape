import pygame


class Mushroom:

    def __init__(self, x, y, hat_width, hat_height, stalk_width, stalk_height,
                 surface, hat_color, stalk_color, mushroom_type):
        """
            x, y — are a left botoom corner of the mushroom's stalk
        """
        self.x = x
        self.y = y
        self.hat_width = hat_width
        self.hat_height = hat_height
        self.stalk_width = stalk_width
        self.stalk_height = stalk_height
        self.surface = surface
        self.hat_color = hat_color
        self.stalk_color = stalk_color
        self.muchroom_type = mushroom_type
        self.center_axis_x = self.x + self.stalk_width // 2

    def draw_stalk(self):
        mushroom_stalk_points = ((self.x, self.y),
                                 (self.x, self.y - self.stalk_height),
                                 (self.x + self.stalk_width, self.y -
                                  self.stalk_height),
                                 (self.x + self.stalk_width, self.y))
        pygame.draw.polygon(self.surface, self.stalk_color,
                            mushroom_stalk_points)

    def draw_hat(self):
        ellipse_points = ((self.x + self.stalk_width // 2 -
                           self.hat_width // 2,
                           self.y - self.stalk_height - self.hat_height,
                           self.hat_width, self.hat_height))
        pygame.draw.ellipse(self.surface, self.hat_color, ellipse_points)

    def draw_stalk_by_coordinates(self, left_bot, left_top, right_top,
                                  right_bot):
        stalk_points = (left_bot, left_top, right_top, right_bot)
        pygame.draw.polygon(self.surface, self.stalk_color, stalk_points)

    def calc_point(self, x, y, direction):
        coefficient = 3
        if direction == "left":
            x1 = x - self.stalk_width // coefficient
            y1 = y + self.stalk_width // coefficient
            x2 = x + self.stalk_width // coefficient
            y2 = y - self.stalk_width // coefficient
        else:
            x1 = x + self.stalk_width // coefficient
            y1 = y + self.stalk_width // coefficient
            x2 = x - self.stalk_width // coefficient
            y2 = y - self.stalk_width // coefficient
        return (x1, y1), (x2, y2)

    def calc_stalk(self, direction):
        """ Let's try to rotate about 45 degrees
            we have :self.x, self.y lets send it and direction(left of right)
            into function, which will return coords of 2 points wight a
            first for left turn: x -= width // 3 y += width // 3 i gues...
            return coords of x_top, y_top, for drawing an ellipce.
            in result points we swight 3 and 4 point cause of rect drawing
        """
        first_point, second_point = self.calc_point(self.x, self.y, direction)
        if direction == "left":
            x_top = self.x - self.stalk_height
            y_top = self.y - self.stalk_height
        else:
            x_top = self.x + self.stalk_height
            y_top = self.y - self.stalk_height
        third_point, fourth_point = self.calc_point(x_top, y_top, direction)
        stalk_coords = (first_point, second_point, fourth_point,
                        third_point)
        self.draw_stalk_by_coordinates(*stalk_coords)
        return (x_top, y_top), stalk_coords

    def draw_mushroom(self):
        if self.muchroom_type == "single":
            self.draw_stalk()
            self.draw_hat()
        else:
            top_point_for_left_ellipce, stalk_coordinates = self.calc_stalk("left")
            self.draw_stalk_by_coordinates(*stalk_coordinates)
            top_point_for_right_ellipce, stalk_coordinates = self.calc_stalk("right")
            self.draw_stalk_by_coordinates(*stalk_coordinates)
            
