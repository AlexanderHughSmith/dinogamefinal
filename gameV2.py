import pygame
import time
import random
from PIL import Image

pygame.init()

#Board Display
display_width = 800
display_height = 400
gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Dino Run')

#Define colors
white = (255,255,255)

#score
score = 0
highscore = 0
myfont = pygame.font.SysFont('Comic Sans MS', 25)
gofont = pygame.font.SysFont('Comic Sans MS', 85)

#Load images
Dinoimg = pygame.image.load(r'/home/alexander/Desktop/Programming/HackYSU/DinoGame/Images/dino.png')
Cactusimg = pygame.image.load(r'/home/alexander/Desktop/Programming/HackYSU/DinoGame/Images/cactus.png')
Fdinoimg = pygame.image.load(r'/home/alexander/Desktop/Programming/HackYSU/DinoGame/Images/flyingdino.png')

clock = pygame.time.Clock()

#Dinosaur Class
class dino(object):
	def __init__(self,x,y,width,height):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.isJump = False
		self.jumpCount = 10

		"""           (x cord,y cord, right, down"""
		self.hitbox = (self.x, self.y, 58, 64)

	#Displays the Dino
	def draw(self, win,img):
		gameDisplay.blit(img, (self.x, self.y))
		#pygame.draw.rect(gameDisplay,(255,0,0),self.hitbox,2) Hit Detection Box

	#Moves the hitbox with the dino
	def moveHitbox(self,y_change):
		self.hitbox = (self.x, y_change, 52, 64)

	#Y position of ducking dino
	def duck(self):
		self.y = 370

	#Y position of standing dino
	def unduck(self):
		self.y = 336

#Cactus class
class catcus(object):
	def __init__(self,x,y,width,height):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		"""           (x cord,y cord, right, down"""
		self.hitbox = (self.x+6, self.y, 52, 64)

	#Displays the Cactus
	def draw(self, win,img):
		gameDisplay.blit(img, (self.x, self.y))
		
	#Moves the cactus Right to Left, keeps the hitbox coordinates while it is moving, and resets the cactus when moved off the screen
	def move(self,x_change):
		self.x += x_change
		self.hitbox = (self.x+6, self.y, 52, 64)
		if self.x <= -64:
			self.x = 800 + random.randint(1,400)

#Pterodactyl Class
class fdino(object):
	def __init__(self,x,y,width,height):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		"""           (x cord,y cord, to the right, down"""
		self.hitbox = (self.x+6, self.y, 52, 64)

	#Displays the Pterodactyl
	def draw(self, win,img):
		gameDisplay.blit(img, (self.x, self.y))
		
	#Moves the Pterodactyl right to left, keeps the hitbox coordinates while it is moving, and resets the cactus when moved off the screen
	def move(self,x_change):
		self.x += x_change
		self.hitbox = (self.x+6, self.y, 52, 64)
		if self.x < -64:
			self.x = 800 + random.randint(1,400)
			print(self.x)


#create dinosaur
dinosaur = dino(250,336,64,64)

#create cactus
cactus_x = 800
cactus_y = 336
cactus_x_change = 0
cactus = catcus(cactus_x,cactus_y,64,64)

#create Pterodactyl
flyingdino_x = 1200
flyingdino_y = 290
flyingdino_x_change = 0
flyingdino = fdino(flyingdino_x,flyingdino_y,64,64)

#Game runs until run == False
run = True
playing = True
#Updates game window constantly
def redrawGameWindow(screen,img1,img2,img3):
	screen.blit(textsurface,(630,0))
	screen.blit(textsurfacehs,(630,20))
	dinosaur.draw(screen,img1)
	cactus.draw(screen,img2)
	flyingdino.draw(screen,img3)
	pygame.display.update()

while playing:
	#GAMEPLAY
	while run:
		#Game speed / Score increment
		clock.tick(36)
		score += 1


		#screenshot



		rect = pygame.Rect(0,0,500,400)
		sub = gameDisplay.subsurface(rect)
		pygame.image.save(sub,"screenshot_image7_100px.jpeg")
		sc = pygame.image.load("screenshot_image7_100px.jpeg")
		pil_string_image = pygame.image.tostring(sc,"RGBA",False)
		pilimg = Image.frombytes("RGBA",(500,400),pil_string_image)

		#print(pilimg)

		
		

		#
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
		
		#Prints score in top right of screen
		textsurface = myfont.render("Score: "+str(score), False, (0, 0, 0))
		textsurfacehs = myfont.render("High Score: "+str(highscore), False, (0, 0, 0))
		
		#Keypressed Events
		pressed = pygame.key.get_pressed()

		#scoring
		if highscore <= score:
			highscore = score+1

		#If the dinosaur is not jumping, and the dinosaur is at base level(336) then the dinosaur can jump //To Prevent ducking before hitting the ground
		if not(dinosaur.isJump):
			if pressed[pygame.K_SPACE] and dinosaur.y == 336:
				dinosaur.isJump = True

		#Jumping Bellcurve
		else:
			if dinosaur.jumpCount >= -10:
				neg = 1
				if dinosaur.jumpCount < 0:
					neg = -1
				dinosaur.y -= (dinosaur.jumpCount ** 2) * .4 * neg
				dinosaur.jumpCount -= 1
				dinosaur.moveHitbox(dinosaur.y)
			else:
				dinosaur.jumpCount = 10
				dinosaur.isJump = False

		#Ducking, if the down key is pressed, the dino is at base level, and the space bar is not pressed, then duck
		if pressed[pygame.K_DOWN] and dinosaur.y == 336 and not pressed[pygame.K_SPACE]:
			dinosaur.duck()
			dinosaur.moveHitbox(370)

		#After releasing the down key, immediately puts the dino back to base level
		elif event.type == pygame.KEYUP:
			if event.key == pygame.K_DOWN:
				dinosaur.unduck()
				dinosaur.moveHitbox(336)

		#Cactus speed
		cactus_x_change = -9
		cactus_x += cactus_x_change

		#flyingdino speed
		flyingdino_x_change = -9
		flyingdino_x += flyingdino_x_change

		#Hit Detection

		#Cactus hit detection
		if dinosaur.x+62 >= cactus.x and dinosaur.x+4<= cactus.x+50 and dinosaur.y+57 >= cactus.y+5:
			run = False
			pygame.time.delay(100)
		#flyingdino hit detection
		if dinosaur.x+59 >= flyingdino.x and dinosaur.x<= flyingdino.x+54 and dinosaur.y <= flyingdino.y+64 and dinosaur.y+64>=flyingdino.y :
			run = False
			pygame.time.delay(100)
		
		gameDisplay.fill(white)
		cactus.move(cactus_x_change)
		flyingdino.move(flyingdino_x_change)
		redrawGameWindow(gameDisplay,Dinoimg,Cactusimg,Fdinoimg)
	clock.tick(36)
	gameDisplay.fill(white)
	gotext = gofont.render("Game Over", False, (0, 0, 0))
	playagaintext= myfont.render("Press Enter to play again", False,(0,0,0))
	gameDisplay.blit(gotext,(250,150))
	gameDisplay.blit(playagaintext,(310,225))

	pygame.display.update()
	pressed = pygame.key.get_pressed()
	for event in pygame.event.get():
			if event.type == pygame.QUIT:
				playing = False
			if pressed[pygame.K_RETURN]:
				run = True
				if score > highscore:
					highscore = score
				score = 0
				cactus.x = 1400
				flyingdino.x = 900
pygame.quit()
quit()