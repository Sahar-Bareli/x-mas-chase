import pygame
from pygame.locals import *
import time


names =["Ore", "Danielle", "Ljuba", "Tamir", "Dekel", "Trans", "Ella", "Daniel"]

price = 50000


class Line:
    def __init__(self, x, speed, width, lifetime, fade_speed):
        self.__x = x
        self.__pos = x
        self.__speed = speed
        self.__width = width
        self.__lifetime = lifetime
        self.__age = 0
        self.__fade_speed = fade_speed

    def draw(self, screen):
        if self.__age >= self.__lifetime:
            return
        width, height = pygame.display.get_surface().get_size()
        self.__surface = pygame.Surface((self.__width, height))
        self.__surface.fill((255, 255, 255))
        alpha = int(255 - ((self.__age - self.__lifetime / 2) / (self.__lifetime / 2) * 255**(1/self.__fade_speed))**self.__fade_speed)
        print(alpha)
        self.__surface.set_alpha(alpha)
        screen.blit(self.__surface, (self.__pos, 0))
        self.__pos += self.__speed
        self.__age += 1


def AAfilledRoundedRect(surface, rect, color, radius=0.4):

    """
    AAfilledRoundedRect(surface,rect,color,radius=0.4)

    surface : destination
    rect    : rectangle
    color   : rgb or rgba
    radius  : 0 <= radius <= 1
    """

    rect         = Rect(rect)
    color        = Color(*color)
    alpha        = color.a
    color.a      = 0
    pos          = rect.topleft
    rect.topleft = 0,0
    rectangle    = pygame.Surface(rect.size,SRCALPHA)

    circle       = pygame.Surface([min(rect.size)*3]*2,SRCALPHA)
    pygame.draw.ellipse(circle,(0,0,0),circle.get_rect(),0)
    circle       = pygame.transform.smoothscale(circle,[int(min(rect.size)*radius)]*2)

    radius              = rectangle.blit(circle,(0,0))
    radius.bottomright  = rect.bottomright
    rectangle.blit(circle,radius)
    radius.topright     = rect.topright
    rectangle.blit(circle,radius)
    radius.bottomleft   = rect.bottomleft
    rectangle.blit(circle,radius)

    rectangle.fill((0,0,0),rect.inflate(-radius.w,0))
    rectangle.fill((0,0,0),rect.inflate(0,-radius.h))

    rectangle.fill(color,special_flags=BLEND_RGBA_MAX)
    rectangle.fill((255,255,255,alpha),special_flags=BLEND_RGBA_MIN)

    return surface.blit(rectangle,pos)


def main():
    pygame.init()

    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

    width, height = pygame.display.get_surface().get_size()

    line = Line(70, 3, 3, 50, 4)

    play = True
    while play:
        screen.fill((0, 0, 255))

        line.draw(screen)

        for name in names:
            rect_width = width / 10
            rect_height = height / 10
            rect_left = names.index(name) * (0.9 * width - rect_width) / (len(names) - 1) + width * 0.05
            rect_top = height / 7
            rect = pygame.Rect(1 , 1, rect_width, rect_height)
            surface = pygame.Surface((rect_width + 2, rect_height + 2), pygame.SRCALPHA)
            surface = surface.convert_alpha()
            AAfilledRoundedRect(surface, rect, (255, 0, 0))
            name_font_size = int(rect_height / 2)
            font = pygame.font.SysFont("arial", name_font_size)
            text_width, text_height = font.size(name)
            label = font.render(name, 1, (255, 255, 255))
            surface.blit(label, ((int(rect_width + 2 - text_width) / 2), (int(rect_height + 2 - text_height) / 2)))
            screen.blit(surface, (rect_left, rect_top))

        font = pygame.font.SysFont("arial", name_font_size * 3)
        text_width, text_height = font.size(str(price))
        label = font.render(str(price), 1, (255, 255, 255))
        screen.blit(label, ((width - text_width) / 2, height / 2))

        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    play = False

        pygame.display.update()

        time.sleep(1 / 500)


if __name__ == "__main__":
    main()