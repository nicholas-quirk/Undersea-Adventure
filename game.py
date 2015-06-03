#os used for platform independence: pygame includes game modules: menu to include menu.py
import os, pygame, random, sys, menu
from pygame.locals import *
from sys import exit

#Make the game platform independent.
main_dir = os.path.split(os.path.abspath(__file__))[0]
image_dir = os.path.join(main_dir, 'image')
sound_dir = os.path.join(main_dir, 'sound')
data_dir = os.path.join(main_dir, 'data')

#const images
background_image_filename = 'underwater_background.png'
mouse_image_filename = 'fish.png'
hotdog_image = 'hotdog.png'
lives_image = 'heart.png'
death_animation_image = 'explosion.png'
life_animation_image = 'sparkles.png'

#const sounds
death_sound = 'humiliation.mp3'
life_sound = 'fanfare.wav'
level_0_sound = 'rampage.wav'
level_1_sound = 'dominating.wav'
level_2_sound = 'unstoppable.wav'
level_3_sound = 'wickedsick.wav'
level_4_sound = 'holyshit.wav'

#Hotdog object will fall from the top to bottom, the user must dodge them to survive.
class Hotdog(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_path = os.path.join(image_dir, hotdog_image)
        self.image = pygame.image.load(self.image_path)
        self.rect = self.image.get_rect()
        self.rate = random.randint(10, 50) #Initialize an object to fall at a random speed.
        self.pos = (random.randint(0,1024), 0) #Initialize an object to fall from a random position.
        self.collided = False #This boolean will ensure the user doesn't loose multiple lives from one collision.

    #Refreshes the object as it falls. If it falls off screen, a new random speed and position is assigned.
    def update(self, canvas, score):
        self.pos = (self.pos[0], self.pos[1] + int(self.rate))
        if self.pos[1] > 640: #If the hotdog falls off screen.
            self.rate = random.randint(score, 50)  #New random speed.
            self.pos = (random.randint(0,1024), 0) #New random position.
            self.collided = False
        self.rect = pygame.Rect(self.pos,(self.rect[2], self.rect[3]))
        canvas.blit(self.image, self.rect)

#User will control the cursor by dodging object.
class Cursor(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_path = os.path.join(image_dir, mouse_image_filename)
        self.image = pygame.image.load(self.image_path).convert_alpha()
        self.lives = 10 #Default amount of live the user starts with.
        self.rect = self.image.get_rect()

    def update(self,canvas):
        self.x, self.y = pygame.mouse.get_pos()
        self.rect = pygame.Rect(self.x,self.y,self.rect[2], self.rect[3])
        canvas.blit(self.image, self.rect)

#Displays the tallying score as the users plays the game.
#If the user beats the high score than the new high score will be written to the high score file.
class Score(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.x = 0
        self.font = pygame.font.Font(None, 60)
        self.text = self.font.render(str(self.x), 1, (10, 10, 10))
        self.text_file_path = os.path.join(data_dir, 'high_score.txt')

    def update(self, canvas):
        self.x += .5 #Increment the score 0.5 for every clock tick.
        self.y = int(self.x)
        self.text = self.font.render("Score: " + str(self.y), 1, (255, 0, 0))
        self.textpos =     self.text.get_rect(center = (500, 20))
        canvas.blit(self.text, self.textpos)

    def highScore(self):
        self.f = open(self.text_file_path, 'r') #Read high score file
        self.currentHigh = self.f.read()
        self.currentHigh = int(self.currentHigh)
        self.f.close()

        if(self.y > self.currentHigh): #If previous high score is lower than current, write the new high score to the file.
            self.f = open(self.text_file_path, 'w')
            self.f.write(str(self.y))
            self.f.close()

#Opens the high score file and displays the current high score for the player to try and beat.
class HighScoreDisplay(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.text_file_path = os.path.join(data_dir, 'high_score.txt')
        self.f = open(self.text_file_path, 'r+')
        self.currentHigh = self.f.readline()
        self.font = pygame.font.Font(None, 60)

    def update(self, canvas):
        self.text = self.font.render("Hi: " + str(self.currentHigh), 1, (255, 255, 255))
        self.textpos =     self.text.get_rect(center = (900, 20))
        canvas.blit(self.text, self.textpos)

#Displays the current lives the user has. Updates as the user looses and gains lives.
class LivesDisplay(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.x = 0
        self.font = pygame.font.Font(None, 60)
        self.text = self.font.render(str(self.x), 1, (10, 10, 10))

    def update(self, canvas, lives):
        self.x = lives
        self.text = self.font.render("Lives: " + str(self.x), 1, (255, 255, 0))
        self.textpos =     self.text.get_rect(center = (100, 20))
        canvas.blit(self.text, self.textpos)

#Lives sprite offers a way for the user to gain a live, implementation is very similar to class Hotdog.
class Lives(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_path = os.path.join(image_dir, lives_image)
        self.image = pygame.image.load(self.image_path)
        self.rect = self.image.get_rect()
        self.rate = random.randint(20, 40)
        self.pos = (random.randint(0,1024), 0)
        self.collided = False

    def update(self,canvas):
        self.pos = (self.pos[0] ,self.pos[1] + int(self.rate))
        if self.pos[1] > 2048:
            self.pos = (random.randint(0,1024), 0)
            self.rate = (random.randint(20,40))
            self.collided = False
        self.rect = pygame.Rect(self.pos,(self.rect[2], self.rect[3]))
        canvas.blit(self.image, self.rect)

#Blits a new image for the cursor. The current implemention is to invert the fishes colors which is just
#a seperate .png file. Also, plays a sound when the cursor and hotdog objects collide.
class DeathAnimation(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_path = os.path.join(image_dir, death_animation_image)
        self.image = pygame.image.load(self.image_path)
        self.rect = self.image.get_rect()
        self.sound_path = os.path.join(sound_dir, death_sound)
        self.sound = pygame.mixer.Sound(self.sound_path) #Plays a sound when hit.

    def update(self, canvas):
        self.sound.play(0,0,0)
        self.x, self.y = pygame.mouse.get_pos()
        self.rect = pygame.Rect(self.x,self.y,self.rect[2], self.rect[3])
        canvas.blit(self.image, self.rect)

#Implementation is very similar to the DeathAnimation class. A different image and sound is implemented when
#a life is collected.
class LifeAnimation(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_path = os.path.join(image_dir, life_animation_image)
        self.image = pygame.image.load(self.image_path)
        self.rect = self.image.get_rect()
        self.sound_path = os.path.join(sound_dir, life_sound)
        self.sound = pygame.mixer.Sound(self.sound_path)

    def update(self, canvas):
        self.sound.play(0,0,0)
        self.x, self.y = pygame.mouse.get_pos()
        self.rect = pygame.Rect(self.x,self.y,self.rect[2], self.rect[3])
        canvas.blit(self.image, self.rect)

#Level system is base on the current score. For every 100 points, the level of the game increases.
class Level():

    #Initialize the sounds that will play with the next level is reached.
    def __init__(self):
        self.sound_0_path = os.path.join(sound_dir, level_0_sound)
        self.sound_0 = pygame.mixer.Sound(self.sound_0_path)
        self.sound_1_path = os.path.join(sound_dir, level_1_sound)
        self.sound_1 = pygame.mixer.Sound(self.sound_1_path)
        self.sound_2_path = os.path.join(sound_dir, level_2_sound)
        self.sound_2 = pygame.mixer.Sound(self.sound_2_path)
        self.sound_3_path = os.path.join(sound_dir, level_3_sound)
        self.sound_3 = pygame.mixer.Sound(self.sound_3_path)
        self.sound_4_path = os.path.join(sound_dir, level_4_sound)
        self.sound_4 = pygame.mixer.Sound(self.sound_4_path)

    #When a score increments by 100, the range at which the objects fall shortens. This leads the the objects all falling faster.
    def select(self, score):
        if score <= 100: return 15 #Level 0
        if score == 101:
            self.sound_0.play(0,0,0)
            return 21
        if score >= 102 and score <= 200: return 21 #Level 1
        if score == 201:
            self.sound_1.play(0,0,0)
            return 28
        if score >= 202 and score <= 300: return 28 #Level 2
        if score == 301:
            self.sound_2.play(0,0,0)
            return 35
        if score >= 302 and score <= 400: return 35 #Level 3
        if score == 401:
            self.sound_3.play(0,0,0)
            return 42
        if score >= 402 and score <= 500: return 42 #Level 4
        if score == 501: #Level 5
            self.sound_4.play(0,0,0)
            return 49
        else: return 49

def main():
    #Initialize all imported pygame modules.
    pygame.init()
    #Clock object used to control the fps.
    clock = pygame.time.Clock()

    #Display in fullscreen. Widescreen support. Will resize if necessary.
    screen = pygame.display.set_mode((1024, 640), pygame.FULLSCREEN, 32)
    background_path = os.path.join(image_dir, background_image_filename)
    #background = pygame.Surface(screen.get_size())
    background = pygame.image.load(background_path).convert()

    #Title of the game window if not in fullscreen.
    pygame.display.set_caption("Watch Out!")

    #Only the cursor sprite will display, not the mouse cursor.
    pygame.mouse.set_visible(False)

    #Initialize object sprites.
    cursor = Cursor()
    lives = Lives()
    hotdog1 = Hotdog()
    hotdog2 = Hotdog()
    hotdog3 = Hotdog()
    hotdog4 = Hotdog()
    hotdog5 = Hotdog()
    hotdog6 = Hotdog()
    hotdogs = [hotdog1, hotdog2, hotdog3, hotdog4, hotdog5, hotdog6] #Hotdog sprite list, easier to handle with iteration

    #Initialize display sprites.
    score = Score()
    livesDisplay = LivesDisplay()
    highScoreDisplay = HighScoreDisplay()

    #Animation objects.
    deathAnimation = DeathAnimation()
    lifeAnimation = LifeAnimation()

    #Sprite grouping.
    sprites = pygame.sprite.RenderPlain(score, cursor, lives, highScoreDisplay)
    spritesHotdogs = pygame.sprite.RenderPlain(hotdogs)
    deathSprite = pygame.sprite.RenderPlain(deathAnimation)
    lifeSprite = pygame.sprite.RenderPlain(lifeAnimation)

    #Initialize level class.
    level = Level()

    Run = True
    while Run:
        #Determines if an event occurs.
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                Run = False

        #Display background and call update function for sprite classes.
        screen.blit(background, (0,0))
        livesDisplay.update(screen, cursor.lives)
        sprites.update(screen)
        spritesHotdogs.update(screen, level.select(score.y))

        #Ensure that a hotdog doesn't take away multiple lives from one hit.
        if cursor.lives >= 1:
            for hotdog in hotdogs: #Iterate through hotdog sprite list.
                if pygame.sprite.collide_rect(hotdog, cursor) and hotdog.collided == False:
                    cursor.lives -= 1
                    hotdog.collided = True #When true, a hotdog cannot subtract from user lives.
                    deathSprite.update(screen)

            #Addes a life on collision, and ensure that more lives are not added for a single collision.
            if pygame.sprite.collide_rect(lives, cursor) and lives.collided == False:
                cursor.lives += 1
                lives.collided = True
                lifeSprite.update(screen)

        #User has run out of lives.
        else:
            Run = False
            score.highScore() #Call high score class
            menu.main() #Go back to menu screen.

        pygame.display.flip()
        clock.tick(15) #Clock set to 15ms, don't want to stress the CPU.


if __name__ == '__main__':
    main()
    pygame.quit()
