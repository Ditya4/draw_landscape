import pygame
from random import randint, choice
import snowflake as sn
import mushroom as mushroom_module


class Cloud:

    def __init__(self, x, y, width, height, x_speed, y_speed, surface, color):
        """
            x, y are a coords of left top of the cloud rect, which is out
            of the ellipse figure
        """
        self.x = x
        self.cloud_x = x
        self.y = y
        self.cloud_y = y
        self.width = width
        self.height = height
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.surface = surface
        self.color = color

    def draw_cloud(self):
        pygame.draw.ellipse(self.surface, self.color,
                            (self.x, self.y, self.width, self.height))

    def move_cloud(self, window_width):
        if self.x <= window_width:
            self.x += self.x_speed
        else:
            self.x = self.cloud_x
            self.y = self.cloud_y
        self.y += self.y_speed



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

    def draw_shadow_house(self, sun):
        """
            left bottom and right bottom points of the wall are used for shadow
            polygone and left top and right top will be send into
            :create_shadow_point(point, sun) functoin
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

    def draw_shadow(self, sun):
        """
            first and second shadow polygone points are left and right bottom
            points of stick
            third point is the proection on the same line as from center of
            a sun and right bottom point of the stick with some scale
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
    surface.fill(("cyan"))
    pygame.draw.polygon(surface, color, (points))


def draw_points(points, surface):
    for point in points:
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
    right_horizont_y = 350
    left_horizont_y = 250
    snow_first_point = (-3, left_horizont_y)
    snow_second_point = (602, right_horizont_y)
    snow_third_point = (602, 602)
    snow_fourth_point = (-3, 602)
    stick_x = 250
    stick_y = 350
    stick_width = 20
    stick_height = 90
    stick_color = "brown"
    house_x = 320
    house_y = 380
    house_width = 60
    house_height = 80
    house_walls_color = "cyan"
    house_roof_color = "turquoise"
    house_window_color = "yellow"
    tree_lower_segment_width = 55
    tree_lower_segment_height = 20
    tree_trunk_width = 5
    tree_trunk_height = 10
    tree_trunk_color = "brown"
    tree_crown_colors = ("gold", "red", "orange", "purple", "dark violet",
                         "firebrick1")
    tree_crown_color_index = 0
    tree_crown_size = 4
    trees_count = 7
    trees = []
    # for symetry stalk_width and hat_width should be even numbers
    mushroom_hat_width = 30
    mushroom_hat_height = 10
    mushroom_stalk_width = 6
    mushroom_stalk_height = 16
    mushroom_hat_colors = ("red", "green")
    mushroom_stalk_color = "brown"
    mushroom_type = ("single", "double")
    mushrooms_count = 7
    mushrooms = []
    cloud_width = 100
    cloud_height = 25
    cloud_x_speed = 5
    cloud_y_speed = 1
    cloud_colors = ("white", "MistyRose2", "PaleGreen1")
    clouds_count = 15
    clouds = []
    snowflake_radius = 12
    snowflake_y_speed = 2
    snowflake_colors = ("red", "blue", "pink")
    snowflake_types = ("snowflake", "circle")
    snowflakes = []
    snowflakes_count = 40
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

    for number in range(trees_count):
        tree_crown_color_index = number % len(tree_crown_colors)
        trees.append(Tree(randint(tree_lower_segment_width // 2,
                                  window_width -
                                  tree_lower_segment_width // 2),
                          randint(right_horizont_y, window_height),
                          tree_lower_segment_width, tree_lower_segment_height,
                          tree_trunk_width, tree_trunk_height, tree_crown_size,
                          win, tree_trunk_color,
                          tree_crown_colors[tree_crown_color_index]))

    for number in range(mushrooms_count):
        mushroom_hat_color_index = number % len(mushroom_hat_colors)
        mushrooms.append(mushroom_module.Mushroom(randint(
                            mushroom_hat_width // 2,
                            window_width - mushroom_hat_width // 2),
                         randint(right_horizont_y, window_height),
                         mushroom_hat_width,
                         mushroom_hat_height, mushroom_stalk_width,
                         mushroom_stalk_height, win,
                         mushroom_hat_colors[mushroom_hat_color_index],
                         mushroom_stalk_color, choice(mushroom_type)))

    for number in range(clouds_count):
        cloud_color_index = number % len(cloud_colors)
        clouds.append(Cloud(randint(-window_width, -cloud_width),
                      randint(-left_horizont_y, left_horizont_y -
                              cloud_height * 6),
                      cloud_width, cloud_height, cloud_x_speed,
                      cloud_y_speed, win, cloud_colors[cloud_color_index]))

    for number in range(snowflakes_count):
        snowflake_color_index = number % len(snowflake_colors)
        snowflakes.append(sn.Snowflake(randint(snowflake_radius,
                                               window_width -
                                               snowflake_radius),
                                       randint(-300, window_height),
                                       snowflake_radius, win,
                                       snowflake_colors[snowflake_color_index],
                                       snowflake_y_speed, window_height,
                                       choice(snowflake_types)))

    while run:
        clock.tick(10)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        bg_draw(win, "white", points)

        sun.move(window_width, sun_x, sun_y)
        sun.draw()
        for cloud in clouds:
            cloud.move_cloud(window_width)
            cloud.draw_cloud()
        stick.draw()
        stick.draw_shadow(sun)
        house.draw_shadow_house(sun)
        house.draw_house()
        for tree in trees:
            tree.draw_tree()
        for mushroom in mushrooms:
            mushroom.draw_mushroom()
        for snowflake in snowflakes:
            snowflake.move()
            snowflake.draw()

        pygame.display.update()
    pygame.quit()


if __name__ == "__main__":
    main()
