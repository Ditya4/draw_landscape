import pygame


class Mushroom:

    def __init__(self, x, y, hat_width, hat_height, stalk_width, stalk_height,
                 surface, hat_color, stalk_color, mushroom_type):
        """
            x, y — are a botoom middle point of the mushroom's stalk
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

    def draw_stalk_by_coordinates(self, left_bot, left_top, right_top,
                                  right_bot):
        stalk_points = (left_bot, left_top, right_top, right_bot)
        pygame.draw.polygon(self.surface, self.stalk_color, stalk_points)

    def calc_point(self, x, y, direction):
        """ x, y is a top middle point of the stalk
            x1, y1 is gonna be coords of left point,
            x2, y2 - right point
        """
        coefficient = 3
        if direction == "left":
            x1 = x - self.stalk_width // coefficient
            y1 = y + self.stalk_width // coefficient
            x2 = x + self.stalk_width // coefficient
            y2 = y - self.stalk_width // coefficient
        elif direction == "right":
            x1 = x - self.stalk_width // coefficient
            y1 = y - self.stalk_width // coefficient
            x2 = x + self.stalk_width // coefficient
            y2 = y + self.stalk_width // coefficient
        elif direction == "top":
            x1 = x - self.stalk_width // 2
            y1 = y
            x2 = x + self.stalk_width // 2
            y2 = y
        return (x1, y1), (x2, y2)

    def calc_stalk(self, direction):
        """ Let's try to rotate about 45 degrees
            we have :self.x, self.y lets send it and direction(left of right)
            into function, which will return coords of 2 points wight a
            first for left turn: x -= width // 3 y += width // 3 i gues...
            return coords of x_top, y_top, for drawing an ellipce.
            in result points we switht 3 and 4 point cause of rect drawing
        """
        first_point, second_point = self.calc_point(self.x, self.y, direction)
        if direction == "left":
            x_top = self.x - self.stalk_height
            y_top = self.y - self.stalk_height
        elif direction == "right":
            x_top = self.x + self.stalk_height
            y_top = self.y - self.stalk_height
        elif direction == "top":
            x_top = self.x
            y_top = self.y - self.stalk_height
        third_point, fourth_point = self.calc_point(x_top, y_top, direction)
        stalk_coords = (first_point, second_point, fourth_point,
                        third_point)
        self.draw_stalk_by_coordinates(*stalk_coords)
        return (x_top, y_top), stalk_coords

    def draw_ellipse_angle(self, surface, color, rect, angle, width=0):
        target_rect = pygame.Rect(rect)
        shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
        pygame.draw.ellipse(shape_surf, color,
                            (0, 0, *target_rect.size), width)
        rotated_surf = pygame.transform.rotate(shape_surf, angle)
        surface.blit(rotated_surf,
                     rotated_surf.get_rect(center=target_rect.center))

    def calc_oval(self, x, y, direction):
        x1 = x - self.hat_width // 2
        if direction == "top":
            y1 = y - self.hat_height
        else:
            y1 = y - self.hat_height // 2
        return (x1, y1)

    def draw_mushroom(self):
        if self.muchroom_type == "single":
            oval_center_bottom_point, stalk_coordinates = (
                                            self.calc_stalk("top"))
            self.draw_stalk_by_coordinates(*stalk_coordinates)
            oval_left_top_point = self.calc_oval(*oval_center_bottom_point,
                                                 "top")
            self.draw_ellipse_angle(self.surface, self.hat_color,
                                    [*oval_left_top_point, self.hat_width,
                                     self.hat_height], 0)
        else:
            oval_center_bottom_point, stalk_coordinates = (
                                        self.calc_stalk("left"))
            self.draw_stalk_by_coordinates(*stalk_coordinates)
            oval_left_top_point = self.calc_oval(*oval_center_bottom_point,
                                                 "left")
            self.draw_ellipse_angle(self.surface, self.hat_color,
                                    [*oval_left_top_point, self.hat_width,
                                     self.hat_height], 45)

            oval_center_bottom_point, stalk_coordinates = (
                                        self.calc_stalk("right"))
            self.draw_stalk_by_coordinates(*stalk_coordinates)
            oval_left_top_point = self.calc_oval(*oval_center_bottom_point,
                                                 "right")
            self.draw_ellipse_angle(self.surface, self.hat_color,
                                    [*oval_left_top_point, self.hat_width,
                                     self.hat_height], -45)
