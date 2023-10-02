import math
import pygame


class SpriteObject(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=(x, y))
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect.center = pygame.mouse.get_pos()


class Line(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((200, 200))
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect(center=(x, y))
        self.color = (255, 255, 0)
    def update(self):
        self.image.fill(0)
        pygame.draw.polygon(self.image, self.color, [[50, 50], [50, 100], [100, 100], [100, 50]])
        self.mask = pygame.mask.from_surface(self.image)

    def change_color(self, color):
        self.color = color




pygame.init()
window = pygame.display.set_mode((500, 500))
pygame.mouse.set_visible(False)
window.fill((0, 0, 0))
clock = pygame.time.Clock()

sprite_image = pygame.image.load('AirPlane.png').convert_alpha()
moving_object = SpriteObject(0, 0, sprite_image)
line_object = Line(*window.get_rect().center)
all_sprites = pygame.sprite.Group([moving_object, line_object])
red = 0
max_flag = False

run = True
while run:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    all_sprites.update()

    if pygame.sprite.collide_mask(moving_object, line_object):
        if max_flag != True:
            red = min(255, red + 10)
            print(red)
        else:
            red = max(0, red - 10)
            print(red)
        if red == 255:
            max_flag = True
        elif red == 0:
            max_flag = False

    else:
        red = 0

    line_object.change_color((255, 255, red))
    all_sprites.draw(window)
    pygame.display.flip()

pygame.quit()
exit()