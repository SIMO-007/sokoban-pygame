import pygame
import sys
import os

import time
from numpy import around


FPS=60
pygame.init()

clock = pygame.time.Clock()
sourceFileDir = os.path.dirname(os.path.abspath(__file__))
background = pygame.image.load(os.path.join(sourceFileDir,'images/background.jpg'))

wall = pygame.image.load(os.path.join(sourceFileDir,'images/wall.png'))
wall = pygame.transform.scale(wall,(50,50))

box = pygame.image.load(os.path.join(sourceFileDir,'images/box.png'))
box = pygame.transform.scale(box,(50,50))

man = pygame.image.load(os.path.join(sourceFileDir,'images/megaman.png'))
man = pygame.transform.scale(man,(50,50))

star = pygame.image.load(os.path.join(sourceFileDir,'images/str.png'))
star = pygame.transform.scale(star,(30,30))


class Game :
    def __init__(self,file,level):

        f = open(file,'r')

        self.matrix = []
        matrix = self.matrix
        level_found = False


        for l in f :
            if not level_found:
                if l.strip() == 'Level '+str(level):
                    level_found = True
            else :
                row = []
                if l.strip() != '':
                    for c in l : 
                        if c == "\n": continue
                        else : row.append(c)
                    matrix.append(row)   
                else : break
        
        self.stars = self.get_stars()

    def size(self):
        x = 0
        y = len(self.matrix)
        for row in self.matrix:
            if len(row) > x:
                x = len(row)
        return (x * 50, y * 50)
    
    def print_matrix(self):
        for x in self.matrix:
            for y in x:
                print(y,end='')
            print('')

    def get_matrix(self):
        return self.matrix


    def get_obj(self,x,y):
        return self.matrix[y][x]
    
    def set_obj(self,x,y,obj):
        self.matrix[y][x] = obj

    def get_hero(self):
        x = 0
        y = 0
        for row in self.matrix:
            for pos in row:
                if pos in ['@']:
                    return (x,y)
                else:
                    x += 1
            y += 1
            x = 0
    
    def can_move(self,x,y):
        return self.get_obj(self.get_hero()[0]+x,self.get_hero()[1]+y) not in ['#','$']

    def next_obj(self,x,y):
        return self.get_obj(self.get_hero()[0]+x,self.get_hero()[1]+y)
    
    def can_push(self,x,y):
        return (self.next_obj(x,y) in ['$'] and self.next_obj(x+x,y+y) in [' ','.'])
    
    def get_stars(self):
        stars = []
        x=0
        y=0
        for l in self.matrix :
            for c in l:
                if c == ".": 
                    stars.append((x,y))
                x+=1
            y+=1
            x=0
        return stars

    def get_boxs(self):
        boxes = []
        x=0
        y=0
        for l in self.matrix :
            for c in l:
                if c == "$": 
                    boxes.append((x,y))
                x+=1
            y+=1
            x=0
        return boxes
    
    def is_comp(self):
        bxs = self.get_boxs()

        for b in bxs:
            if b not in self.stars :
                return False
        return True

    def move_box(self,x,y,a,b):
        current_box = self.get_obj(x,y)
        future_box = self.get_obj(x+a,y+b)
        if current_box == '$' and future_box == ' ':
            self.set_obj(x+a,y+b,'$')
            #self.set_obj(x,y,' ')
    
    def move_hero(self,x,y):
        current_pos = self.get_hero()
        next_obj = self.next_obj(x,y)
        #next_box = self.next_obj(2*x,2*y)

        if self.can_move(x,y):

            if next_obj == ' ' and current_pos not in self.stars:

                self.set_obj(current_pos[0],current_pos[1],' ')
                self.set_obj(current_pos[0]+x,current_pos[1]+y,'@')

            elif next_obj == ' ' and current_pos in self.stars:

                self.set_obj(current_pos[0],current_pos[1],'.')
                self.set_obj(current_pos[0]+x,current_pos[1]+y,'@')

            elif next_obj == '.' and current_pos in self.stars:

                self.set_obj(current_pos[0],current_pos[1],'.')
                self.set_obj(current_pos[0]+x,current_pos[1]+y,'@')

            elif next_obj == '.' and current_pos not in self.stars:

                self.set_obj(current_pos[0],current_pos[1],' ')
                self.set_obj(current_pos[0]+x,current_pos[1]+y,'@')

        elif self.can_push(x,y):
        
            self.set_obj(current_pos[0]+x,current_pos[1]+y,'@')
            self.set_obj(current_pos[0],current_pos[1],' ')
            self.set_obj(current_pos[0]+2*x,current_pos[1]+2*y,'$')
        
        for c in self.stars:
            if self.matrix[c[1]][c[0]] == ' ':
                self.matrix[c[1]][c[0]] = '.'
        
        self.is_comp()

def print_game(matrix,screen,stars):
    screen.blit(background,(0,0))
    x = 0
    y = 0

    for row in matrix:
        for char in row:
            if char == '#': #wall
                screen.blit(wall,(x,y))
            elif char == '@': #worker on floor
                screen.blit(man,(x,y))
            elif char == '.': #dock
                screen.blit(star,(x,y))
            elif char == '$': #box
                screen.blit(box,(x,y))    
            x += 50
        x = 0
        y += 50


def time_conversion(s):
    min, s = divmod(s, 60)
    hours, min = divmod(min, 60)
    return (hours,min,s)




def completed_game(screen,n,s):
    
    t = time_conversion(s)
    
    X = 650
    Y = 500
    display_surface = pygame.display.set_mode((X, Y))
    screen.blit(background,(0,0))
    font = pygame.font.Font('freesansbold.ttf',22)
    font1 = pygame.font.Font('freesansbold.ttf',28)
    
    # create a text surface object,
    # on which text is drawn on it.
    text = font1.render("LEVEL COMPLETED !!",True,(255,255,255))
    time = font.render(f"{t[0]} hours {t[1]} minutes {t[2]} seconds ",True,(255,255,255))
    moves = font.render(f"NB of moves : {n}",True,(255,255,255))
    esc = font.render("press esc to go back",True,(255,255,255))
    # create a rectangular object for the
    # text surface object
    textRect = text.get_rect()
    timeRect = time.get_rect()
    movesRect = moves.get_rect()
    escRect = esc.get_rect()

    # set the center of the rectangular object.
    textRect.center = (300,100)
    timeRect.center = (200,300)
    movesRect.center = (500,300)
    escRect.center = (300,450)

        # copying the text surface object
        # to the display surface object
        # at the center coordinate.
    display_surface.blit(text, textRect)
    display_surface.blit(time, timeRect)   
    display_surface.blit(moves, movesRect)
    display_surface.blit(esc, escRect)
    # iterate over the list of Event objects
    # that was returned by pygame.event.get() method.
    for event in pygame.event.get():     
        if event.type == pygame.QUIT:
            quit()

        elif event.type == pygame.K_ESCAPE:
            break
        
        # Draws the surface object to the screen.
        pygame.display.update()
            


def startgame(x):
    g = Game(sourceFileDir + '/levels.coffee',x)
    screen = pygame.display.set_mode(g.size())

    n=0
    t1 = time.perf_counter()
    while 1:
        clock.tick(FPS)
        esc = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                
                if event.key == pygame.K_UP: g.move_hero(0,-1); n += 1
                elif event.key == pygame.K_DOWN: g.move_hero(0,1) ; n += 1
                elif event.key == pygame.K_LEFT: g.move_hero(-1,0); n += 1
                elif event.key == pygame.K_RIGHT: g.move_hero(1,0); n += 1
                elif event.key == pygame.K_r : g = Game(sourceFileDir + '/levels.coffee',x) 
                elif event.key == pygame.K_ESCAPE : esc = True
                elif event.key == pygame.K_q: sys.exit(0)

        if esc :
            screen = pygame.display.set_mode((680, 480))
            return False ,False
            

        print_game(g.get_matrix(),screen,g.get_stars())   
    
        pygame.display.update()

        if g.is_comp() == True:
            t2 = time.perf_counter()
            t = t2 - t1
            t = around(t,0)
            completed_game(screen,n,t)
            
            return False
        

    

