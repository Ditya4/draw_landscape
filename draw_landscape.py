import pygame


class House:

    def __init__(self, x, y, width, height, color, surface):
        """
            x, y are the coords of the left bottom corner of the house wall
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.surface = surface
        self.walls_height = (self.height * 2) // 3
        self.roof_height = self.height // 3
        self.wall_points = None

    def draw_walls(self):
        wall_points = (self.x, self.y - self.walls_height,
                       self.x + self.width, self.y)
        pygame.draw.rect(self.surface, self.color, wall_points)

    def draw_roof(self):
        pass

    def draw_window(self):
        pass

    def draw_house(self):
        # self.wall_points = ((self.x, self.y),
        self.draw_walls()
        self.draw_roof()
        self.draw_window()


class Tree:

    def __init__(self, x, y, lower_segment_width, lower_segment_height,
                 surface, color="green"):
        """
            x, y are the coords of the left bottom of the tree trunk
        """
        self.x = x
        self.y = y
        self.width = lower_segment_width
        self.height = lower_segment_height
        self.surface = surface
        self.color = color


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
            a sun and right bottom point of the stick with lenght @lenght
        """
        shadow_first_point = (self.x, self.y)
        shadow_second_point = (self.x + self.width, self.y)
        shadow_third_point_x = ((self.x + self.width - sun.x) + self.x +\
                                 self.width)
        shadow_third_point_y = (self.y - sun.y) + self.y
        shadow_fourth_point_x = (self.x - sun.x) + self.x
        shadow_fourth_point_y = (self.y - sun.y) + self.y
        shadow_fourth_point = (shadow_fourth_point_x, shadow_fourth_point_y)
        shadow_third_point = (shadow_third_point_x, shadow_third_point_y)
        shadow_points = (shadow_first_point, shadow_second_point,
                         shadow_third_point, shadow_fourth_point)
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

    def move(self):
        self.x += self.x_speed
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


def main():
    pygame.init()
    window_width = 500
    window_height = 600
    sun_x = 20
    sun_y = 140
    sun_radius = 20
    sun_color = "yellow"
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
    house_x = 100
    house_y = 200
    house_width = 90
    house_height = 80
    house_color = "orange"

    points = (snow_first_point, snow_second_point, snow_third_point,
              snow_fourth_point)
    run = True
    clock = pygame.time.Clock()
    pygame.display.set_caption("Sun")
    win = pygame.display.set_mode((window_width, window_height))
    sun = Sun(sun_x, sun_y, sun_radius, sun_x_speed, sun_y_speed, win,
              sun_color)
    stick = Stick(stick_x, stick_y, stick_width, stick_height, win,
                  stick_color)
    house = House(house_x, house_y, house_width, house_height, house_color, win)

    while run:
        clock.tick(10)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        bg_draw(win, "white", points)
        sun.move()
        sun.draw()
        stick.draw()
        stick.draw_shadow(sun, stick_shadow_length)
        house.draw_house()
        pygame.display.update()
    pygame.quit()


if __name__ == "__main__":
    main()
