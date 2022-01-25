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

import start

# required initialization step
pygame.init()

# set up game clock
game_clock = pygame.time.Clock()

WINDOW_SIZE = (500, 800)
window = pygame.display.set_mode(WINDOW_SIZE)

def main() -> None:
    # initial state
    cur_screen = start.Start(window)
    window.fill(colors.BACKGROUND_COLOR)
    latest_score = 0
    fps = 2

    while True:
        # handle user input
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                cur_screen.handle_click(event.pos)
            elif event.type == pygame.KEYDOWN:
                cur_screen.handle_key(event.key)

        # react to user input & run background processes
        cur_screen.update()

        # handle reactions to last update
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

            elif event == screen.SPEED_UP:
                fps += 1
            elif event == screen.RESET_SPEED:
                fps = 2

        # draw final result
        cur_screen.draw()

        # update screen & tick clock
        pygame.display.update()
        game_clock.tick(fps)


if __name__ == '__main__':
    main()
