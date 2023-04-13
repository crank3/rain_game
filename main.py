import keyboard
import pygame
import random as rand
import math
import time as t


# CONSTANTS
WIDTH = 1800
HEIGHT = 1000
screen = pygame.display.set_mode((WIDTH, HEIGHT))

WIDTH_healthbar = (WIDTH/2)-10
HEIGHT_healthbar = 20

fps = 200


# FUNCTIONS

def spawn_player(color):
    player_size = 20
    player = pygame.Surface((20, 20))
    player_rect = player.get_rect()
    player.fill(color)
    player_rect.update(((WIDTH / 2) - player_size, HEIGHT / 1.5), (player_size, player_size))
    health = 1
    return [player, player_rect, color, health]


def player_move(player_n, pos, delta_x, delta_y):
    # player = an element of p, which contains the surface and the rect of the playe

    pos[0] += delta_x
    pos[1] += delta_y
    player_n[1].update((pos[0], pos[1]), (20, 20))


def spawn_rain():
    rain_width = 20
    rain_height = 40
    rain = pygame.Surface((rain_width, rain_height))
    rain_rect = rain.get_rect()
    rain_rect.update((rand.randint(0, WIDTH-rain_width), 0), (rain_width, rain_height))

    rain.fill(rand.choice([pygame.Color(255, 0, 0, 255),
                           pygame.Color(0, 255, 0, 255),
                           pygame.Color(0, 0, 255, 255),
                           pygame.Color(255, 255, 0, 255),
                           pygame.Color(0, 255, 255, 255),
                           pygame.Color(255, 0, 255, 255)]))

    return [rain, rain_rect]


def healthbar(color, left, top):
    bar_width = WIDTH_healthbar
    bar_height = HEIGHT_healthbar
    bar = pygame.Surface((bar_width, bar_height))
    bar_rect = bar.get_rect()
    bar.fill(color)
    bar_rect.update((left, top), (bar_width, bar_height))
    return [bar, bar_rect]








playing = True
if __name__ == '__main__':

    # Rain
    all_rain = []


    # Players
    p = [spawn_player('white'), spawn_player('white')]
    # p[0][0] = player1,     p[0][1] = player1_rect
    # p[1][0] = player2,     p[1][1] = player2_rect
    p1_pos = [float(p[0][1][0]), float(p[0][1][1])]
    p2_pos = [float(p[1][1][0]), float(p[1][1][1])]

    # Healthbars
    p[0].append(healthbar(p[0][2], 10,  HEIGHT - 50))
    p[1].append(healthbar(p[1][2], WIDTH/2, HEIGHT - 50))







    rain_freq = 1  # rain / second
    rain_speed = 4

    time = 0
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++ GAME LOOP
    while playing:
        t.sleep(1/fps)

        if keyboard.is_pressed('esc'):
            quit()


        # Player Movement
        p1_speed = 5
        # if screen.get_rect().contains(p[0][1]):
        if (keyboard.is_pressed('w')+keyboard.is_pressed('s')+keyboard.is_pressed('a')+keyboard.is_pressed('d')) >= 2:
            p1_speed = p1_speed / math.sqrt(2)
        if keyboard.is_pressed('w'):
            player_move(p[0], p1_pos, 0, -p1_speed)
        if keyboard.is_pressed('s'):
            player_move(p[0], p1_pos, 0, p1_speed)
        if keyboard.is_pressed('a'):
            player_move(p[0], p1_pos, -p1_speed, 0)
        if keyboard.is_pressed('d'):
            player_move(p[0], p1_pos, p1_speed, 0)
        p[0][1].clamp_ip(screen.get_rect())

        p2_speed = 5
        if (keyboard.is_pressed('up')+keyboard.is_pressed('down')+keyboard.is_pressed('left')+keyboard.is_pressed('right')) >= 2:
            p2_speed = p2_speed / math.sqrt(2)
        if keyboard.is_pressed('up'):
            player_move(p[1], p2_pos, 0, -p2_speed)
        if keyboard.is_pressed('down'):
            player_move(p[1], p2_pos, 0, p2_speed)
        if keyboard.is_pressed('left'):
            player_move(p[1], p2_pos, -p2_speed, 0)
        if keyboard.is_pressed('right'):
            player_move(p[1], p2_pos, p2_speed, 0)
        p[1][1].clamp_ip(screen.get_rect())

        for player in p:  # increases player health if white
            if (player[2] == 'white') and ((time % (200//5)) == 0) and (player[3] < 100):
                player[3] += 1






        # Rain Stuff
        if (time % (200//rain_freq)) == 0:
            all_rain.append(spawn_rain())
            all_rain.append(spawn_rain())
            all_rain.append(spawn_rain())
        for rain in all_rain:
            rain[1] = rain[1].move(0, rain_speed)

            # Rain+Player Collision
            for player in p:
                if rain[1].colliderect(player[1]):
                    if player[2] != rain[0].get_at((0, 0)):
                        player[2] = rain[0].get_at((0, 0))
                        player[3] -= 10
                    else:
                        player[3] += 5
                    all_rain.remove(rain)

        if ((time % 300) == 0) and (rain_freq < 200):
            rain_freq += 1
        if (time % 2000) == 0:
            rain_speed += 1



        # Update Healthbars
        for player in p:
            left = player[4][1][0]
            top = player[4][1][1]
            bar_width = player[4][1][2]
            bar_height = player[4][1][3]

            new_width = WIDTH_healthbar * (player[3]/100)

            if new_width <= 0:
                print('game over :O')
                exit()

            player[4][0] = pygame.Surface((new_width, bar_height))
            player[4][1].update((left, top), (new_width, bar_height))





        # End Stuff
        time += 1
        # print(time)
        screen.fill('black')

        # Blitting
        for player in p:
            player[4][0].fill(player[2])
            screen.blit(player[4][0], player[4][1])

            player[0].fill(player[2])
            screen.blit(player[0], player[1])

        for rain in all_rain:
            screen.blit(rain[0], rain[1])


        # Seriously the end
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False


