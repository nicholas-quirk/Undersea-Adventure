import pygame, os, game, sys
from pygame.locals import *
from math import sin

#os.path will ensure that the program runs on any platform.
main_dir = os.path.split(os.path.abspath(__file__))[0]
image_dir = os.path.join(main_dir, 'image') #Specify paths for the images used.
sound_dir = os.path.join(main_dir, 'sound') #Specify paths for the sounds used.

#Make the cursor a sprite, which will be used for collision detection.
class Cursor(pygame.sprite.Sprite):

    #init functions are used to initialize class variables.
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_path = os.path.join(image_dir, 'hotdog.png')
        self.image = pygame.image.load(self.image_path).convert_alpha()
        self.rect = self.image.get_rect() #pygame module uses rectangles for collision detection of sprites

    #update functions are used to refresh the screen when actions are taken by the user.
    def update(self,canvas):
        self.x, self.y = pygame.mouse.get_pos() #Return the mouse position.
        self.rect = pygame.Rect(self.x,self.y,self.rect[2], self.rect[3]) #Return the rectangles dimensions.
        canvas.blit(self.image, self.rect) #blit is a function displays the sprite on the screen

#This class is made into a sprite for the menu, it will start the game.
class StartDisplay(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_path = os.path.join(image_dir, 'start.png')
        self.image = pygame.image.load(self.image_path)
        self.rect = self.image.get_rect()

    def update(self, canvas):
        self.x, self.y = canvas.get_size()
        self.pos = (self.x/2 - self.rect.width/2, self.y/2) #Center the text on the screen
        self.rect = pygame.Rect(self.pos, (self.rect[2], self.rect[3]))
        canvas.blit(self.image, self.rect)

#This class is made into a sprite for the menu, it will exit the game.
class ExitDisplay(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_path = os.path.join(image_dir, 'exit.png')
        self.image = pygame.image.load(self.image_path)
        self.rect = self.image.get_rect()

    def update(self, canvas):
        self.x, self.y = canvas.get_size()
        self.pos = (self.x/2 - self.rect.width/2, self.y/2 + 100)
        self.rect = pygame.Rect(self.pos,(self.rect[2], self.rect[3]))
        canvas.blit(self.image, self.rect)

def main():

    #initialize and setup screen
    pygame.init()
    clock = pygame.time.Clock()

    #Fullscreen if capable, will default to 1024, 640 if fullscreen fails.
    screen = pygame.display.set_mode((1024, 640), pygame.FULLSCREEN, 32)

    #load image and quadruple
    background_path = os.path.join(image_dir, 'menu.bmp')
    bitmap = pygame.image.load(background_path)
    anim = 0.0

    #Load and play intro sound byte
    intro_sound = os.path.join(sound_dir, 'intro.wav')
    pygame.mixer.music.load(intro_sound)
    pygame.mixer.music.play(0, 0.0)
    pygame.mouse.set_visible(False)

    #Initialize sprites.
    startDisplay = StartDisplay()
    exitDisplay = ExitDisplay()
    cursor = Cursor()

    #Create sprite group.
    sprites = pygame.sprite.RenderPlain(startDisplay, exitDisplay, cursor)

    #mainloop
    xblocks = range(0, 1024, 20)
    yblocks = range(0, 640, 20)

    Run = True
    while Run:

        #This loop give the background the liquid appearance.
        anim = anim + 0.2
        for x in xblocks:
            xpos = (x + (sin(anim + x * .01) * 15)) + 20 #Sin functions are used to manipulate the pixels.
            for y in yblocks:
                ypos = (y + (sin(anim + y * .01) * 15)) + 20
                screen.blit(bitmap, (x, y), (xpos, ypos, 20, 20)) #Update the screen after the pixels have been changed.

        #Event loop that determine if an event has happened.
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                sys.exit() #Run = False #Quit with ESC key
            if event.type == MOUSEBUTTONDOWN:
                if pygame.sprite.collide_rect(cursor, startDisplay):
                    game.main() #Start game if clicked.
                if pygame.sprite.collide_rect(cursor, exitDisplay):
                    sys.exit() #Run = False #Exit game if clicked.

        sprites.update(screen) #Calls the update functions for all sprites in the sprite group.
        pygame.display.flip() #Update the contents of the entire display.

if __name__ == '__main__':
    main()
