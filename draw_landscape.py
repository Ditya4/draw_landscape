import pygame
from random import randint


class House:

    def __init__(self, x, y, width, height, walls_color, roof_color,
                 window_color, surface):
        """
            x, y are the coords of the left bottom corner of the house wall
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.walls_color = walls_color
        self.roof_color = roof_color
        self.window_color = window_color
        self.surface = surface
        self.walls_height = (self.height * 2) // 3
        self.roof_height = self.height // 3

    def draw_walls(self):
        wall_points = ((self.x, self.y - self.walls_height),
                       (self.x + self.width, self.y - self.walls_height),
                       (self.x + self.width, self.y),
                       (self.x, self.y))
        pygame.draw.polygon(self.surface, self.walls_color, wall_points)
        # draw_points(wall_points, self.surface)

    def draw_roof(self):
        roof_points = ((self.x, self.y - self.walls_height),
                       (self.x + self.width, self.y - self.walls_height),
                       (self.x + self.width // 2,
                        self.y - self.walls_height - self.roof_height))
        pygame.draw.polygon(self.surface, self.roof_color, roof_points)
        # draw_points(roof_points, self.surface)

    def draw_window(self):
        left_bottom_window_point = (self.x + self.width // 3,
                                    self.y - self.walls_height // 3)
        left_top_window_point = (self.x + self.width // 3,
                                 self.y - (self.walls_height // 3) * 2)
        right_top_window_point = (self.x + (self.width // 3) * 2,
                                  self.y - (self.walls_height // 3) * 2)
        right_bottom_wondow_point = (self.x + (self.width // 3) * 2,
                                     self.y - self.walls_height // 3)

        window_points = (left_bottom_window_point, left_top_window_point,
                         right_top_window_point, right_bottom_wondow_point)
        pygame.draw.polygon(self.surface, self.window_color, window_points)
        # draw_points(window_points, self.surface)

    def draw_shadow_walls(self, sun, lenght):
        """
            left bottom and right bottom points of the wall are used for shadow
            polygone and left top and right top will be send into
            :create_shadow_point(point, sun) functoin
            FIXME :length for a while didn't implimented.
            self.x, y are the coords of the left bottom corner
            of the house wall
        """
        first_point = (self.x, self.y)
        second_point = create_shadow_point((self.x, self.y -
                                            self.walls_height), sun)
        third_point = create_shadow_point(
            (self.x + self.width // 2, self.y - self.walls_height +
             self.roof_height), sun)
        fourth_point = create_shadow_point((self.x + self.width, self.y -
                                           self.walls_height), sun)
        fiveth_point = (self.x + self.width, self.y)
        house_shadow_points = (first_point, second_point, third_point,
                               fourth_point, fiveth_point)
        roof_shadow_points = (first_point, fourth_point, third_point,
                              fiveth_point)
        pygame.draw.polygon(self.surface, "black", house_shadow_points)
        pygame.draw.polygon(self.surface, "black", roof_shadow_points)
        # draw_points(house_shadow_points, self.surface)

    def draw_house(self):
        self.draw_walls()
        self.draw_roof()
        self.draw_window()


class Tree:

    def __init__(self, x, y, lower_segment_width, lower_segment_height,
                 trunk_width, trunk_height, crown_size, surface,
                 trunk_color="brown", crown_color="green"):
        """
            x, y are the coords of the left bottom of the tree trunk
        """
        self.x = x
        self.y = y
        self.width = lower_segment_width
        self.height = lower_segment_height
        self.trunk_width = trunk_width
        self.trunk_height = trunk_height
        self.crown_size = crown_size
        self.surface = surface
        self.trunk_color = trunk_color
        self.crown_color = crown_color
        self.center_axis_x = self.x + self.trunk_width // 2

    def draw_tree_trunk(self):
        tree_trunk_points = ((self.x, self.y),
                             (self.x, self.y - self.trunk_height),
                             (self.x + self.trunk_width, self.y -
                              self.trunk_height),
                             (self.x + self.trunk_width, self.y))
        pygame.draw.polygon(self.surface, self.trunk_color, tree_trunk_points)

    def draw_tree_crone(self, i):
        """
            we have center and first segment height and width, so
            go just draw a triangle, and decrease some height within
            every calls of this medhod
        """
        lower_center_x = self.center_axis_x
        lower_center_y = self.y - self.trunk_height - (self.height - 7) * i

        crown_points = ((lower_center_x - self.width // 2, lower_center_y),
                        (lower_center_x + self.width // 2, lower_center_y),
                        (lower_center_x, lower_center_y - self.height))
        pygame.draw.polygon(self.surface, self.crown_color, crown_points)
        draw_points(crown_points, self.surface)

    def draw_tree(self):
        self.draw_tree_trunk()
        for i in range(0, self.crown_size):
            self.draw_tree_crone(i)


class Stick:

    def __init__(self, x, y, width, height, surface, color):
        """
            x and y are coords of left bottom of the stick
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.surface = surface
        self.color = color

    def draw(self):
        points = ((self.x, self.y), (self.x, self.y - self.height),
                  (self.x + self.width, self.y - self.height),
                  (self.x + self.width, self.y))
        pygame.draw.polygon(self.surface, self.color, points)

    def draw_shadow(self, sun, lenght):
        """
            first and second shadow polygone points are left and right bottom
            points of stick
            third point is the proection on the same line as from center of
            a sun and right bottom point of the stick with some scale
            FIXME :length for a while didn't implimented.
        """
        shadow_first_point = (self.x, self.y)
        shadow_second_point = (self.x + self.width, self.y)
        shadow_third_point_function = create_shadow_point((self.x + self.width,
                                                           self.y), sun)
        shadow_fourth_point_function = create_shadow_point((self.x, self.y),
                                                           sun)
        shadow_points = (shadow_first_point, shadow_second_point,
                         shadow_third_point_function,
                         shadow_fourth_point_function)
        pygame.draw.polygon(self.surface, "black", shadow_points)


class Sun:

    def __init__(self, x, y, radius, x_speed, y_speed, surface, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.surface = surface
        self.color = color

    def move(self, window_width, sun_x, sun_y):
        if self.x < window_width + self.radius:
            self.x += self.x_speed
        else:
            self.x = sun_x
            self.y = sun_y
        self.y += self.y_speed

    def draw(self):
        pygame.draw.circle(self.surface, self.color, (self.x, self.y),
                           self.radius)


def bg_draw(surface, color, points):
    """
        Draw background into black color and white snow in front
    """
    surface.fill((0, 0, 0,))
    pygame.draw.polygon(surface, color, (points))


def draw_points(points, surface):
    for point in points:
        print(point)
        pygame.draw.circle(surface, "green", point, 2, 2)


def create_shadow_point(point, sun):
    point_x = point[0]
    point_y = point[1]
    result_x = (point_x - sun.x) + point_x
    result_y = (point_y - sun.y) + point_y
    return (result_x, result_y)


def main():
    window_width = 500
    window_height = 600
    sun_x = -25
    sun_y = 140
    sun_radius = 20
    sun_color = "VioletRed1"
    sun_x_speed = 5
    sun_y_speed = 1
    snow_first_point = (-3, 250)
    snow_second_point = (602, 350)
    snow_third_point = (602, 602)
    snow_fourth_point = (-3, 602)
    stick_x = 250
    stick_y = 350
    stick_width = 20
    stick_height = 90
    stick_color = "brown"
    stick_shadow_length = 50
    house_x = 120
    house_y = 330
    house_width = 60
    house_height = 80
    house_walls_color = "cyan"
    house_roof_color = "turquoise"
    house_window_color = "yellow"
    house_shadow_length = 50
    tree_x = 350
    tree_y = 550
    tree_lower_segment_width = 55
    tree_lower_segment_height = 20
    tree_trunk_width = 5
    tree_trunk_height = 10
    tree_trunk_color = "brown"
    tree_crown_colors = ("gold", "red", "orange", "purple", "dark violet", "firebrick1")
    tree_crown_color_index = 0
    tree_crown_size = 8
    trees = []
    points = (snow_first_point, snow_second_point, snow_third_point,
              snow_fourth_point)
    run = True

    pygame.init()
    clock = pygame.time.Clock()
    pygame.display.set_caption("Landscape")
    win = pygame.display.set_mode((window_width, window_height))
    sun = Sun(sun_x, sun_y, sun_radius, sun_x_speed, sun_y_speed, win,
              sun_color)
    stick = Stick(stick_x, stick_y, stick_width, stick_height, win,
                  stick_color)
    house = House(house_x, house_y, house_width, house_height,
                  house_walls_color, house_roof_color, house_window_color, win)

    for x in range(25):
        tree_crown_color_index = x % len(tree_crown_colors)
        trees.append(Tree(randint(tree_lower_segment_width // 2,
                                  window_width -
                                  tree_lower_segment_width // 2),
                          randint(350, window_height),
                          tree_lower_segment_width, tree_lower_segment_height,
                          tree_trunk_width, tree_trunk_height, tree_crown_size,
                          win, tree_trunk_color,
                          tree_crown_colors[tree_crown_color_index]))
    '''
    tree = Tree(tree_x, tree_y, tree_lower_segment_width,
                tree_lower_segment_height, tree_trunk_width, tree_trunk_height,
                tree_crown_size, win, tree_trunk_color, tree_crown_color)
    '''
    while run:
        clock.tick(10)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        bg_draw(win, "white", points)
        sun.move(window_width, sun_x, sun_y)
        sun.draw()
        stick.draw()
        stick.draw_shadow(sun, stick_shadow_length)
        house.draw_house()
        house.draw_shadow_walls(sun, house_shadow_length)
        for tree in trees:
            tree.draw_tree()
        pygame.display.update()
    pygame.quit()


if __name__ == "__main__":
    main()
