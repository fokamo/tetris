"""main.py - for handling the high-level logic

For external use:
- .main() function to run the game
"""

import pygame
import sys

import colors
import end
import game
import screen

# required initialization step
import start

pygame.init()

# set up game clock
FPS = 2
game_clock = pygame.time.Clock()


WINDOW_SIZE = (400, 800)
window = pygame.display.set_mode(WINDOW_SIZE)


def main() -> None:
    cur_screen = start.Start(window)
    window.fill(colors.BACKGROUND_COLOR)
    latest_score = 0

    while True:
        print('click')
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                print('mousedown')
                cur_screen.handle_click(event.pos)

            elif event.type == pygame.KEYDOWN:
                print('keydown')
                cur_screen.handle_key(event.key)

        cur_screen.update()

        for event in cur_screen.get_events():
            if event == screen.EXIT_GAME:
                pygame.quit()
                sys.exit()

            elif event in screen.CHANGE_SCREEN:
                if isinstance(cur_screen, game.Game):
                    latest_score = cur_screen.get_score()

                if event == screen.END_SCREEN:
                    cur_screen = end.End(window, latest_score)
                elif event == screen.GAME_SCREEN:
                    cur_screen = game.Game(window)
                window.fill(colors.BACKGROUND_COLOR)

        cur_screen.draw()

        # update screen & tick clock
        pygame.display.update()
        game_clock.tick(FPS)


if __name__ == '__main__':
    main()
"""

if __name__ == '__main__':
    while True:
        print('click')
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                print('keydown')
        game_clock.tick(FPS)
"""
