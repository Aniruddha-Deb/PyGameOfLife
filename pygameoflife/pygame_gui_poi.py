import pygame
import pygame_gui

def run():
    pygame.init()

    win_surf = pygame.display.set_mode((800, 600))

    background = pygame.Surface((800, 600))
    background.fill(pygame.Color('black'))

    clock = pygame.time.Clock()
    is_running = True

    nticks = 0
    while is_running:
        time_delta = clock.tick(60)/1000
        nticks += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
            
        nticks %= 60
        if nticks == 0:
            print("1 sec elapsed")
        pygame.display.update()

run()
