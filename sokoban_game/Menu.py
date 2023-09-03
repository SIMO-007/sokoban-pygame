import pygame
import pygame_menu
import os
from pygame_menu.examples import create_example_window
import sokoban

# Constants and global variables
ABOUT = ['''Created by: 
Mohammed Fathi & Tarek Nakkouch 
**ingame press r to reset game
& esc to return**''']


LEVELS = [""]
FPS = 60
WINDOW_SIZE = (680, 480)
sourceFileDir = os.path.dirname(os.path.abspath(__file__))
background = pygame.image.load(os.path.join(sourceFileDir,'images/background.jpg'))


def change_lvl(value, level) :
    LEVELS[0] = level   



def play_function(level, f):
   
    level = level[0]
    if level == '':
        level = '1'
        
    # global variables
    global main_menu
    global clock
    
    i = sokoban.startgame(int(level))
    
    if i == False:
        
        main_menu.enable()
        events = pygame.event.get()
        if main_menu.is_enabled():
            main_menu.update(events)
    
        while True:
            
            clock.tick(FPS) # execute loop 60 times per sec for every user

            # User events
            events = pygame.event.get()
            for e in events:
                if e.type == pygame.QUIT:
                    exit()
                elif e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE:
                        main_menu.enable()

                        # Quit this function, then skip to loop of main-menu 
                        return
            # Pass events to main_menu
            if main_menu.is_enabled():
                main_menu.update(events)



def main_background() : 
    #Function used by menus, draw on background while menu is active.
    global surface
    surface.fill((0,153,153))


def return_lvl(v,l):
    return l


def start_menu():

    # -------------------------------------------------------------------------
    # Global variables
    # -------------------------------------------------------------------------
    global clock
    global main_menu
    global surface

    # -------------------------------------------------------------------------
    # Create window
    # -------------------------------------------------------------------------
    surface = create_example_window('SOKOBAN GAME', WINDOW_SIZE)
    clock = pygame.time.Clock()

    # -------------------------------------------------------------------------
    # Create menus: Play Menu
    # -------------------------------------------------------------------------
    submenu_theme = pygame_menu.themes.THEME_SOLARIZED
    play_menu = pygame_menu.Menu(
        height=WINDOW_SIZE[1] * 0.7,
        title='Play Menu',
        width=WINDOW_SIZE[0] * 0.75,
        theme=submenu_theme,
    )

    
    submenu_theme.widget_font_size = 32
    play_submenu = pygame_menu.Menu(
        height=WINDOW_SIZE[1] * 0.5,
        theme=submenu_theme,
        title='Submenu',
        width=WINDOW_SIZE[0] * 0.7
    )
    
    play_submenu.add.button('Return to main menu', pygame_menu.events.RESET)

    play_menu.add.button('Start',  # When pressing return -> play(DIFFICULTY[0], font)
                         play_function,
                         LEVELS,
                         pygame.font.Font(pygame_menu.font.FONT_FRANCHISE, 30))
    play_menu.add.selector('Select level ',
                           [('1 ', '1'),
                            ('2 ', '2'),
                            ('3', '3'),
                            ('4', '4'),
                            ('5', '5'),
                            ('6', '6'),
                            ('7', '7'),
                            ('8', '8'),
                            ('9', '9'),
                            ('10', '10'),],
                           onchange=change_lvl,
                           selector_id='select_level')
    
    play_menu.add.button('Return to main menu', pygame_menu.events.BACK)

    # -------------------------------------------------------------------------
    # Create menus:About
    # -------------------------------------------------------------------------
    about_theme = pygame_menu.themes.THEME_SOLARIZED
    about_theme.widget_margin = (0, 0)

    about_menu = pygame_menu.Menu(
        height=WINDOW_SIZE[1] * 0.6,
        theme=about_theme,
        title='About',
        width=WINDOW_SIZE[0] * 0.6
    )

    for m in ABOUT:
        about_menu.add.label(m, align=pygame_menu.locals.ALIGN_LEFT, font_size=20)
    about_menu.add.vertical_margin(30)
    about_menu.add.button('Return to menu', pygame_menu.events.BACK)

    # -------------------------------------------------------------------------
    # Create menus: Main
    # -------------------------------------------------------------------------
    main_theme = pygame_menu.themes.THEME_SOLARIZED

    main_menu = pygame_menu.Menu(
        height=WINDOW_SIZE[1] * 0.6,
        theme=main_theme,
        title='Main Menu',
        width=WINDOW_SIZE[0] * 0.6
    )

    main_menu.add.button('Play', play_menu)
    main_menu.add.button('About', about_menu)
    main_menu.add.button('Quit', pygame_menu.events.EXIT)

    # -------------------------------------------------------------------------
    # Main loop
    # -------------------------------------------------------------------------
    while True:

        clock.tick(FPS)

        # Paint background
        main_background()

        # User events
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()

        # Main menu
        if main_menu.is_enabled():
            main_menu.mainloop(surface, main_background, fps_limit=FPS)



