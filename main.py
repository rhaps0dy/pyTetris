import pygame.display, pygame.image, pygame.font, pygame.time
import pygame.mixer, pygame.event
from math import fabs as abs, sin, cos
from pygame.locals import *
from sys import exit
from random import randint
import codecs

#Constants
UPLEFTPIXEL = (29, -70)
BOARD_Y = 15
BOARD_X = 9
START_X = 4
START_Y = 2
GRID_JUMP = 41

pygame.init()

#data containers
boardyx = [ ]
NonPieceBlocks = [ ]

for y in range(BOARD_Y+1):
	boardyx.append([ ])
	for x in range(BOARD_X+1):
		boardyx[y].append(0)
		
		
#pygame stuff, ya know...
windowSurface = pygame.display.set_mode((800, 600), 0)
ICON = pygame.image.load('Media/Images/tetris.ico')
pygame.display.set_icon(ICON)

background = pygame.image.load('Media/Images/Fondo5.png').convert_alpha()
prev_background = 5

MMENU = pygame.image.load('Media/Images/menu.png').convert_alpha()
BULLET = pygame.image.load('Media/Images/Bloc_indi_s.png').convert_alpha()
HISCORES = pygame.image.load('Media/Images/hiscores.png').convert_alpha()

color ={"1":(0xd7, 0x00, 0x00), "2":(0x73, 0x9d, 0x1d), "3":(0xff, 0x00, 0x00),
	"4":(0xff, 0x00, 0x00), "5":(0x73, 0x9d, 0x1d), "6":(0x06, 0x00, 0xff),
	"7":(0x00, 0x00, 0x00), "8":(0xff, 0xff, 0xff)}  

colorLletres = color["5"]

atariFont = pygame.font.Font("Fonts/AtariSmallBold.ttf", 36)

scorePos = (580, 390)
levelPos = (601, 473)
mutePos = (741, 523)

RALT_ENTER = KMOD_RALT|K_RETURN
LALT_ENTER = KMOD_LALT|K_RETURN

posicionsMenu = ((319, 268), (466, 268), (231, 347), (553, 347), (526, 420), (269, 420), (247, 497), (539, 497))
clock = pygame.time.Clock()

hiscoresNamePos = (93, 83)
hiscoresScorePos = (694, 83)
hiscoresNumPos = (42, 83)
hiscoresTenX = 24
hiscoresYLeap = 45
hiscoresHighlightH = 42
hiscoresHighlightColor = (0x0d, 0xcf, 0xe0)

controls = {"TurnCW":K_UP, "muteToggle":ord('o'), "Fullscreen":ord('f'),
	"Left":K_LEFT, "Right":K_RIGHT, "Enter":K_RETURN,
	"Accelerate":K_DOWN, "menuUp": K_UP, "menuDown":K_DOWN, "Down":K_SPACE, "Quit": K_ESCAPE, 'Pause':ord('p')}
#controls = {}
#file = open("controls", "r")
#for line in file.readlines():
#		ln = line.split()
		
#file.close()

keyMap = {"TurnCW":0, "TurnCCW":0, "Left":0, "Right":0, "Accelerate":0, "Down":0, "Backspace":0}

global boardyx, NonPieceBlocks
boardyx = [ ]
NonPieceBlocks = [ ]

def surt():
	pygame.quit()
	exit()

def reset():
	del boardyx
	del NonPieceBlocks
	global boardyx, NonPieceBlocks
	boardyx = [ ]
	NonPieceBlocks = [ ]
	
	for y in range(BOARD_Y+1):
		boardyx.append([ ])
		for x in range(BOARD_X+1):
			boardyx[y].append(0)
			
pygame.display.set_caption('Tetris 2D')

		

class MainMenu:
	def hiscores(self, score = -1):
		#Coses d'escriptura
		letterList = range(ord('b'), ord('d')+1) + range(ord('f'), ord('h')+1) + range(ord('j'), ord('n')+1) 
		letterList += range(ord('p'), ord('t')+1) + range(ord('v'), ord('z')+1)
		mayus = False
		altGr = False
		accents = {"obert":False, "tancat":False, "circumflex":False, "dieresi":False}
		def revisaAccents():
			res = False
			if accents["obert"]:
				self.hiscoreList[self.scoreIndex][1] += u"`"
				accents["obert"] = False
				res = True
			if accents["tancat"]:
				self.hiscoreList[self.scoreIndex][1] += u"´"
				accents["tancat"] = False
				res = True
			if accents["circumflex"]:
				self.hiscoreList[self.scoreIndex][1] += u"^"
				accents["circumflex"] = False
				res = True
			if accents["dieresi"]:
				self.hiscoreList[self.scoreIndex][1] += u"¨"
				accents["dieresi"] = False
				res = True
			return res
		self.posCursor = 0
		
		file = codecs.open("hiscores", "r", encoding='utf-8')
		self.hiscoreList = []
		for line in file.readlines():
			#print line[:4], "i", line[5:-1]
			self.hiscoreList.append([line[:4], line[5:-1]])
		file.close()
		self.hiscoreList.sort()
		
		isWriting = False
		self.scoreIndex = -1;
		if score > int(self.hiscoreList[0][0]):
			self.hiscoreList[0] = [str(score), u""]
			isWriting = True
			scoreString = ""
			if int(self.hiscoreList[0][0]) <= 9:
				self.hiscoreList[0][0] = scoreString = "000"+self.hiscoreList[0][0]
			elif int(self.hiscoreList[0][0]) <= 99:
				self.hiscoreList[0][0] = scoreString = "00"+self.hiscoreList[0][0]
			elif int(self.hiscoreList[0][0]) <= 999:
				self.hiscoreList[0][0] = scoreString = "0"+self.hiscoreList[0][0]
			else:
				scoreString = self.hiscoreList[0][0]
			self.hiscoreList.sort()
			self.hiscoreList.reverse()
			for i in range(10):
				if self.hiscoreList[i] == [scoreString, u""]:
					self.scoreIndex = i
					break
		else:
			self.hiscoreList.sort()
			self.hiscoreList.reverse()
		self.hiscoreSurfaceList = []
		
		def redibuixa():
				windowSurface.blit(background, (0, 0))
				windowSurface.blit(HISCORES, (0, 0))
				for i in range(10):
					if self.scoreIndex != -1 and i==self.scoreIndex:
						rect = pygame.Rect(0, hiscoresScorePos[1]+hiscoresYLeap*i, windowSurface.get_width(), hiscoresHighlightH)
						windowSurface.fill(hiscoresHighlightColor, rect)
					surf1 = atariFont.render(self.hiscoreList[i][0], False, (0xff, 0x00, 0x00))
					surf2 = atariFont.render(self.hiscoreList[i][1], False, (0xff, 0x00, 0x00))
					surf3 = atariFont.render(str(i+1)+".", False, (0xff, 0x00, 0x00))
					windowSurface.blit(surf1, (hiscoresScorePos[0], hiscoresScorePos[1]+hiscoresYLeap*i))
					windowSurface.blit(surf2, (hiscoresNamePos[0], hiscoresNamePos[1]+hiscoresYLeap*i))
					if i==9:
						windowSurface.blit(surf3, (hiscoresTenX, hiscoresNumPos[1]+hiscoresYLeap*i))
					else:
						windowSurface.blit(surf3, (hiscoresNumPos[0], hiscoresNumPos[1]+hiscoresYLeap*i))
				
				windowSurface.blit(BULLET, (247, 554))
				windowSurface.blit(BULLET, (539, 554))
				pygame.display.flip()
				
		redibuixa()
		wantMenu = True
		mayus = False
		altGr = False
		esborrar = 0
		while isWriting:
			clock.tick(30)
			if len(self.hiscoreList[self.scoreIndex][1]) > 32:
				self.hiscoreList[self.scoreIndex][1] = self.hiscoreList[self.scoreIndex][1][:32]
			if keyMap["Backspace"] == 1:
				esborrar += 1
				if esborrar > 10:
					self.hiscoreList[self.scoreIndex][1] = self.hiscoreList[self.scoreIndex][1][:-1]
			redibuixa()
			eventList = pygame.event.get()
			for event in eventList:
				if event.type == QUIT:
					surt()
				if event.type == KEYDOWN:
					if event.key == K_LSHIFT or event.key == K_RSHIFT:
						mayus = True
						
					elif event.key == 306 or event.key == 307:
						altGr = True
					
					elif event.key == ord('a'):
						if mayus:
							if accents["obert"]:
								accents["obert"] = False
								self.hiscoreList[self.scoreIndex][1] += u"À"
							elif accents["tancat"]:
								accents["tancat"] = False
								self.hiscoreList[self.scoreIndex][1] += u"Á"
							elif accents["circumflex"]:
								accents["circumflex"] = False
								self.hiscoreList[self.scoreIndex][1] += u"Â"
							elif accents["dieresi"]:
								accents["dieresi"] = False
								self.hiscoreList[self.scoreIndex][1] += u"Ä"
							else: self.hiscoreList[self.scoreIndex][1] += u"A"
						else:
							if accents["obert"]:
								accents["obert"] = False
								self.hiscoreList[self.scoreIndex][1] += u"à"
							elif accents["tancat"]:
								accents["tancat"] = False
								self.hiscoreList[self.scoreIndex][1] += u"á"
							elif accents["circumflex"]:
								accents["circumflex"] = False
								self.hiscoreList[self.scoreIndex][1] += u"â"
							elif accents["dieresi"]:
								accents["dieresi"] = False
								self.hiscoreList[self.scoreIndex][1] += u"ä"
							else: self.hiscoreList[self.scoreIndex][1] += u"a"
							
					elif event.key == ord('e'):
						if mayus:
							if accents["obert"]:
								accents["obert"] = False
								self.hiscoreList[self.scoreIndex][1] += u"È"
							elif accents["tancat"]:
								accents["tancat"] = False
								self.hiscoreList[self.scoreIndex][1] += u"É"
							elif accents["circumflex"]:
								accents["circumflex"] = False
								self.hiscoreList[self.scoreIndex][1] += u"Ê"
							elif accents["dieresi"]:
								accents["dieresi"] = False
								self.hiscoreList[self.scoreIndex][1] += u"Ë"
							else: self.hiscoreList[self.scoreIndex][1] += u"E"
						else:
							if accents["obert"]:
								accents["obert"] = False
								self.hiscoreList[self.scoreIndex][1] += u"è"
							elif accents["tancat"]:
								accents["tancat"] = False
								self.hiscoreList[self.scoreIndex][1] += u"é"
							elif accents["circumflex"]:
								accents["circumflex"] = False
								self.hiscoreList[self.scoreIndex][1] += u"ê"
							elif accents["dieresi"]:
								accents["dieresi"] = False
								self.hiscoreList[self.scoreIndex][1] += u"ë"
							else: self.hiscoreList[self.scoreIndex][1] += u"e"
					elif event.key == ord('i'):
						if mayus:
							if accents["obert"]:
								accents["obert"] = False
								self.hiscoreList[self.scoreIndex][1] += u"Ì"
							elif accents["tancat"]:
								accents["tancat"] = False
								self.hiscoreList[self.scoreIndex][1] += u"Í"
							elif accents["circumflex"]:
								accents["circumflex"] = False
								self.hiscoreList[self.scoreIndex][1] += u"Î"
							elif accents["dieresi"]:
								accents["dieresi"] = False
								self.hiscoreList[self.scoreIndex][1] += u"Ï"
							else: self.hiscoreList[self.scoreIndex][1] += u"I"
						else:
							if accents["obert"]:
								accents["obert"] = False
								self.hiscoreList[self.scoreIndex][1] += u"ì"
							elif accents["tancat"]:
								accents["tancat"] = False
								self.hiscoreList[self.scoreIndex][1] += u"í"
							elif accents["circumflex"]:
								accents["circumflex"] = False
								self.hiscoreList[self.scoreIndex][1] += u"î"
							elif accents["dieresi"]:
								accents["dieresi"] = False
								self.hiscoreList[self.scoreIndex][1] += u"ï"
							else: self.hiscoreList[self.scoreIndex][1] += u"i"
					elif event.key == ord('o'):
						if mayus:
							if accents["obert"]:
								accents["obert"] = False
								self.hiscoreList[self.scoreIndex][1] += u"Ò"
							elif accents["tancat"]:
								accents["tancat"] = False
								self.hiscoreList[self.scoreIndex][1] += u"Ó"
							elif accents["circumflex"]:
								accents["circumflex"] = False
								self.hiscoreList[self.scoreIndex][1] += u"Ô"
							elif accents["dieresi"]:
								accents["dieresi"] = False
								self.hiscoreList[self.scoreIndex][1] += u"Ö"
							else: self.hiscoreList[self.scoreIndex][1] += u"O"
						else:
							if accents["obert"]:
								accents["obert"] = False
								self.hiscoreList[self.scoreIndex][1] += u"ò"
							elif accents["tancat"]:
								accents["tancat"] = False
								self.hiscoreList[self.scoreIndex][1] += u"ó"
							elif accents["circumflex"]:
								accents["circumflex"] = False
								self.hiscoreList[self.scoreIndex][1] += u"ô"
							elif accents["dieresi"]:
								accents["dieresi"] = False
								self.hiscoreList[self.scoreIndex][1] += u"ö"
							else: self.hiscoreList[self.scoreIndex][1] += u"o"
					elif event.key == ord('u'):
						if mayus:
							if accents["obert"]:
								accents["obert"] = False
								self.hiscoreList[self.scoreIndex][1] += u"Ú"
							elif accents["tancat"]:
								accents["tancat"] = False
								self.hiscoreList[self.scoreIndex][1] += u"Ù"
							elif accents["circumflex"]:
								accents["circumflex"] = False
								self.hiscoreList[self.scoreIndex][1] += u"Û"
							elif accents["dieresi"]:
								accents["dieresi"] = False
								self.hiscoreList[self.scoreIndex][1] += u"Ü"
							else: self.hiscoreList[self.scoreIndex][1] += u"U"
						else:
							if accents["obert"]:
								accents["obert"] = False
								self.hiscoreList[self.scoreIndex][1] += u"ù"
							elif accents["tancat"]:
								accents["tancat"] = False
								self.hiscoreList[self.scoreIndex][1] += u"ú"
							elif accents["circumflex"]:
								accents["circumflex"] = False
								self.hiscoreList[self.scoreIndex][1] += u"û"
							elif accents["dieresi"]:
								accents["dieresi"] = False
								self.hiscoreList[self.scoreIndex][1] += u"ü"
							else: self.hiscoreList[self.scoreIndex][1] += u"u"
					
					elif event.key in letterList:
						revisaAccents()
						if mayus: self.hiscoreList[self.scoreIndex][1] += chr(event.key).upper()
						else: self.hiscoreList[self.scoreIndex][1] += chr(event.key)
					
					elif event.key == 44: #coma
						revisaAccents()
						if mayus: self.hiscoreList[self.scoreIndex][1] += u";"
						else: self.hiscoreList[self.scoreIndex][1] += u","
						
					elif event.key == 46: #punt
						revisaAccents()
						if mayus: self.hiscoreList[self.scoreIndex][1] += u":"
						else: self.hiscoreList[self.scoreIndex][1] += u"."
						
					elif event.key == 47: #guio
						revisaAccents()
						if mayus: self.hiscoreList[self.scoreIndex][1] += u"_"
						else: self.hiscoreList[self.scoreIndex][1] += u"-"
						
					elif event.key == 32: #espai
						if not revisaAccents():
							self.hiscoreList[self.scoreIndex][1] += u" "
						
					elif event.key == 48: #0
						revisaAccents()
						if mayus: self.hiscoreList[self.scoreIndex][1] += u"="
						else: self.hiscoreList[self.scoreIndex][1] += u"0"
						
					elif event.key == 49: #1
						revisaAccents()
						if mayus: self.hiscoreList[self.scoreIndex][1] += u"!"
						elif altGr: self.hiscoreList[self.scoreIndex][1] += u"|"
						else: self.hiscoreList[self.scoreIndex][1] += u"1"
						
					elif event.key == 50: #2
						revisaAccents()
						if mayus: self.hiscoreList[self.scoreIndex][1] += u'"'
						elif altGr: self.hiscoreList[self.scoreIndex][1] += u"@"
						else: self.hiscoreList[self.scoreIndex][1] += u"2"
						
					elif event.key == 51: #3
						revisaAccents()
						if mayus: self.hiscoreList[self.scoreIndex][1] += u"."
						elif altGr: self.hiscoreList[self.scoreIndex][1] += u"#"
						else: self.hiscoreList[self.scoreIndex][1] += u"3"
						
					elif event.key == 52: #4
						revisaAccents()
						if mayus: self.hiscoreList[self.scoreIndex][1] += u"$"
						elif altGr: self.hiscoreList[self.scoreIndex][1] += u"~"
						else: self.hiscoreList[self.scoreIndex][1] += u"4"
						
					elif event.key == 53: #5
						revisaAccents()
						if mayus: self.hiscoreList[self.scoreIndex][1] += u"%"
						elif altGr: self.hiscoreList[self.scoreIndex][1] += u"€"
						else: self.hiscoreList[self.scoreIndex][1] += u"5"
						
					elif event.key == 54: #6
						revisaAccents()
						if mayus: self.hiscoreList[self.scoreIndex][1] += u"&"
						elif altGr: self.hiscoreList[self.scoreIndex][1] += u"¬"
						else: self.hiscoreList[self.scoreIndex][1] += u"6"
						
					elif event.key == 55: #7
						revisaAccents()
						if mayus: self.hiscoreList[self.scoreIndex][1] += u"/"
						else: self.hiscoreList[self.scoreIndex][1] += u"7"
						
					elif event.key == 56: #8
						revisaAccents()
						if mayus: self.hiscoreList[self.scoreIndex][1] += u"("
						else: self.hiscoreList[self.scoreIndex][1] += u"8"
						
					elif event.key == 57: #9
						revisaAccents()
						if mayus: self.hiscoreList[self.scoreIndex][1] += u")"
						else: self.hiscoreList[self.scoreIndex][1] += u"9"
						
					elif event.key == 59: #enya
						revisaAccents()
						if mayus: self.hiscoreList[self.scoreIndex][1] += u"Ñ"
						else: self.hiscoreList[self.scoreIndex][1] += u"ñ"

					elif event.key == 61: #!invers
						revisaAccents()
						if mayus: self.hiscoreList[self.scoreIndex][1] += u"?"
						else: self.hiscoreList[self.scoreIndex][1] += u"¡"
					elif event.key == 45: #'
						revisaAccents()
						if mayus: self.hiscoreList[self.scoreIndex][1] += u"?"
						else:self.hiscoreList[self.scoreIndex][1] += u"'"

					elif event.key == 96: #º
						revisaAccents()
						if mayus: self.hiscoreList[self.scoreIndex][1] += u"ª"
						elif altGr: self.hiscoreList[self.scoreIndex][1] += u"\\"
						else: self.hiscoreList[self.scoreIndex][1] += u"º"

					elif event.key == 91: #`
						if mayus:
							if revisaAccents():
								self.hiscoreList[self.scoreIndex][1] += u"^"
							else:
								accents["circumflex"] = True
						elif altGr: self.hiscoreList[self.scoreIndex][1] += u"["
						else:
							if revisaAccents():
								self.hiscoreList[self.scoreIndex][1] += u"`"
							else:
								accents["obert"] = True

					elif event.key == 92: #ç
						revisaAccents()
						if mayus: self.hiscoreList[self.scoreIndex][1] += u"Ç"
						elif altGr: self.hiscoreList[self.scoreIndex][1] += u"}"
						else: self.hiscoreList[self.scoreIndex][1] += u"ç"
						
					elif event.key == 93: #+
						revisaAccents()
						if mayus: self.hiscoreList[self.scoreIndex][1] += u"*"
						elif altGr: self.hiscoreList[self.scoreIndex][1] += u"]"
						else: self.hiscoreList[self.scoreIndex][1] += u"+"
						
					elif event.key == 39: #´
						if mayus:
							if revisaAccents():
								self.hiscoreList[self.scoreIndex][1] += u"¨"
							else:
								accents["dieresi"] = True
							
						elif altGr: self.hiscoreList[self.scoreIndex][1] += u"{"
						else:
							if revisaAccents():
								self.hiscoreList[self.scoreIndex][1] += u"´"
							else:
								accents["tancat"] = True
						
					elif event.key == 8: #backspace
						self.hiscoreList[self.scoreIndex][1] = self.hiscoreList[self.scoreIndex][1][:-1]
						keyMap["Backspace"] = 1
					
					elif event.key == K_RETURN or event.key == K_ESCAPE:
						isWriting = False
					else: pass
					
				if event.type == KEYUP: 
					if event.key == K_LSHIFT or event.key == K_RSHIFT:
						mayus = False
					elif event.key == 306 or event.key == 307:
						altGr = False
					elif event.key == 8: #backspace
						keyMap["Backspace"] = 0
						esborrar = 0
		redibuixa()

		file = codecs.open("hiscores", "w", encoding='utf-8')
		for a in self.hiscoreList:
			file.write(unicode(str(a[0]))+u' '+unicode(a[1])+u'\n')
		file.close()
		
		while wantMenu:
			clock.tick(30)
			eventList = pygame.event.get()
			for event in eventList:
				if event.type == QUIT:
					surt()
				if event.type == KEYDOWN:
					if event.key == controls['Quit'] or event.key==controls["Enter"]:
						wantMenu = False
						break
					elif event.key == 8: #backspace
						esborrar = 0
						keyMap["Backspace"] = 1
		self.dibuixa()
		
	def dibuixa(self):
		self.posCursor = 0
		def redibuixa():
			windowSurface.blit(background, (0, 0))
			windowSurface.blit(MMENU, (0, 0))
			windowSurface.blit(BULLET, posicionsMenu[self.posCursor])
			windowSurface.blit(BULLET, posicionsMenu[self.posCursor+1])
			pygame.display.flip()
		redibuixa()
		#entra main loop
		wantMenu = True
		while wantMenu:
			clock.tick(30)
			eventList = pygame.event.get()
			for event in eventList:
				if event.type == QUIT:
					surt()
				if event.type == KEYDOWN:
					if event.key == controls['Quit']:
						surt()
				
					if event.key == controls['menuDown']:
						self.posCursor += 2
						if self.posCursor > 7: self.posCursor = 0
						redibuixa()
						
					if event.key == controls['menuUp']:
						self.posCursor -= 2
						if self.posCursor < 0: self.posCursor = 6
						redibuixa()
					if event.key == controls["Enter"]:
						if self.posCursor == 0:
							wantMenu = False
							reset()
						if self.posCursor == 2:
							self.hiscores()
						if self.posCursor == 6:
							surt()

class MovingBlock2D:
	x = 0
	y = 0
	parent = None
	globX = 0
	globY = 0
	surface = None
	def __init__(self, loc, parent, color):
		self.x, self.y = loc
		self.parent = parent
		self.globX = self.x + self.parent.x
		self.globY = self.y + self.parent.y
		
		self.surface = pygame.image.load("Media/Images/Bloc_"+color+".png")
		
	def move(self, x, y):
		self.x, self.y = x, y
		self.globX = self.x + self.parent.x
		self.globY = self.y + self.parent.y
	
	def update(self):
		surfX = self.globX*GRID_JUMP + UPLEFTPIXEL[0]
		surfY = self.globY*GRID_JUMP + UPLEFTPIXEL[1]
		windowSurface.blit(self.surface, (surfX, surfY))
		
	def carve(block):
		NonPieceBlocks.append(Block2D(block.globX,
			block.globY, block.surface))
		boardyx[int(block.globY)][int(block.globX)] = 1
		
class Block2D:
	globX = 0
	globY = 0
	surface = None
	def __init__(self, x, y, surf):
		self.globX, self.globY = int(x), int(y)
		boardyx[self.globY][self.globX] = 1
		self.surface = surf
	
	def baixa(self, linies):
		#~ print self.globX, self.globY
		boardyx[self.globY][self.globX] = 0
		self.globY += linies
		#~ print self.globX, self.globY
		boardyx[self.globY][self.globX] = 1
		
	def update(self):
		surfX = self.globX*GRID_JUMP + UPLEFTPIXEL[0]
		surfY = self.globY*GRID_JUMP + UPLEFTPIXEL[1]
		windowSurface.blit(self.surface, (surfX, surfY))
		boardyx[self.globY][self.globX] = 1
		
		
class TetrisPiece:
	x = 0
	y = 0
	blocks = []
	blocksXYlist = []
	position = 0
	#classe pare per a totes les peces
	
	def __init__(self, x, y, colour):
		#~ print 'init tetrispiece'
		self.y, self.x = y, x
		self.blocks = []
		block = MovingBlock2D(self.blocksXYlist[0][0], self, colour)
		self.blocks.append(block)
		block = MovingBlock2D(self.blocksXYlist[0][1], self, colour)
		self.blocks.append(block)
		block = MovingBlock2D(self.blocksXYlist[0][2], self, colour)
		self.blocks.append(block)
		block = MovingBlock2D(self.blocksXYlist[0][3], self, colour)
		self.blocks.append(block)
	
	def move(self, locx, locy, ignoreCollision = 0):
		if not ignoreCollision:
			for block in self.blocks:
				if block.x + self.x + locx > BOARD_X or block.x + self.x + locx < 0: return 0
				if block.y + self.y + locy > BOARD_Y: return 0
				if boardyx[int(block.y + self.y + locy)][int(block.x + self.x + locx)] == 1: return 0
		self.x += locx
		self.y += locy
		for block in self.blocks:
			block.move(block.x, block.y)
		return 1
		
	def move_to(self, x, y):
		self.x = x
		self.y = y
		for block in self.blocks:
			block.move(block.x, block.y)
		return 1
			
	def turn_cw(self):
		blocksXY = None
		Xoffset = 0
		
		self.position += 1
		if self.position > len(self.blocksXYlist)-1:
			self.position = 0
		blocksXY = self.blocksXYlist[self.position]
		for block in self.blocks:
			if blocksXY[self.blocks.index(block)][0] + self.x > BOARD_X:
				xoffs = -(blocksXY[self.blocks.index(block)][0] + self.x - BOARD_X)
				if xoffs < Xoffset: Xoffset = xoffs
				continue
			if blocksXY[self.blocks.index(block)][0] + self.x < 0:
				xoffs = abs(blocksXY[self.blocks.index(block)][0] + self.x)
				if xoffs > Xoffset: Xoffset = xoffs
				continue
			if blocksXY[self.blocks.index(block)][1] + self.y > BOARD_Y: return 0
			if boardyx[int(blocksXY[self.blocks.index(block)][1] + self.y)][int(blocksXY[self.blocks.index(block)][0] + self.x)] == 1: return 0
				
		for block in self.blocks:
			x, y = blocksXY[self.blocks.index(block)]
			block.move(x, y)
		if self.move(Xoffset, 0, ignoreCollision = False) == 0:
			self.position -=1
			if self.position < 0:
				self.position = len(self.blocksXYlist)-1
			blocksXY = self.blocksXYlist[self.position]
			for block in self.blocks:
				x, y = blocksXY[self.blocks.index(block)]
				block.move(x, y)
		return 1
		
	def update(self):
		for block in self.blocks:
			block.update()
			
	def carve(self):
		for block in self.blocks:
			block.carve()
			
class BeamPiece(TetrisPiece):
	def __init__(self, x, y, colour = 'blau'):
		self.blocksXYlist = [((-1,0),(0,0),(1,0),(2,0)), ((0,-1), (0,0), (0,1), (0,2))]	
		TetrisPiece.__init__(self, x, y, colour)
		
class SquarePiece(TetrisPiece):
	def __init__(self, x, y, colour = 'verd'):
		self.blocksXYlist = [((0,0),(0,1),(1,0),(1,1))]	
		TetrisPiece.__init__(self, x, y, colour)
	def turn_cw(self): pass
		
class LPiece(TetrisPiece):
	def __init__(self, x, y, colour = 'taronja'):
		self.blocksXYlist = [((-1,0),(0,0),(1,0),(1,-1)), ((0,-2),(0,-1),(0,0),(1,0)),
			((-1,0),(-1,-1),(0,-1),(1,-1)), ((0,-2),(1,-2),(1,-1),(1,0))]	
		TetrisPiece.__init__(self, x, y, colour)
		
class MirrorLPiece(TetrisPiece):
	def __init__(self, x, y, colour = 'indi'):
		self.blocksXYlist = [((-1,-1),(-1,0),(0,0),(1,0)), ((0,-2),(0,-1),(0,0),(1,-2)),
			((-1,-1),(0,-1),(1,-1),(1,0)), ((1,-2),(1,-1),(1,0),(0,0))]	
		TetrisPiece.__init__(self, x, y, colour)
		
class TPiece(TetrisPiece):
	def __init__(self, x, y, colour = 'lila'):
		self.blocksXYlist = [((0,0),(0,-1),(1,0),(-1,0)), ((0,0), (0,-1), (0,1), (1,0)),
			((-1,0),(0,0),(1,0),(0,1)), ((-1,0),(0,0),(0,-1),(0,1))]	
		TetrisPiece.__init__(self, x, y, colour)
		
class SPiece(TetrisPiece):
	def __init__(self, x, y, colour = 'roig'):
		self.blocksXYlist = [((0,-1),(0,0),(1,0),(1,1)), ((-1,1), (0,0), (0,1), (1,0))]
		TetrisPiece.__init__(self, x, y, colour)
		
class ZPiece(TetrisPiece):
	def __init__(self, x, y, colour = 'groc'):
		self.blocksXYlist = [((0,-1),(0,0),(-1,0),(-1,1)), ((-1,0), (0,0), (0,1), (1,1))]	
		TetrisPiece.__init__(self, x, y, colour)

def nova_peca(rand):
	if rand == 0: peca = BeamPiece(START_X, START_Y)
	if rand == 1: peca = MirrorLPiece(START_X, START_Y)
	if rand == 2: peca = SquarePiece(START_X, START_Y)
	if rand == 3: peca = LPiece(START_X, START_Y)
	if rand == 4: peca = TPiece(START_X, START_Y)
	if rand == 5: peca = SPiece(START_X, START_Y)
	if rand == 6: peca = ZPiece(START_X, START_Y)
	return peca
def nova_peca_cua(rand):
	if rand == 0: peca = pygame.image.load("Media/Images/BeamPiece.png")
	if rand == 1: peca = pygame.image.load("Media/Images/MirrorLPiece.png")
	if rand == 2: peca = pygame.image.load("Media/Images/SquarePiece.png")
	if rand == 3: peca = pygame.image.load("Media/Images/LPiece.png")
	if rand == 4: peca = pygame.image.load("Media/Images/TPiece.png")
	if rand == 5: peca = pygame.image.load("Media/Images/SPiece.png")
	if rand == 6: peca = pygame.image.load("Media/Images/ZPiece.png")
	return (peca, rand)

def renderScore(score):
	if score <= 9:
		surf = atariFont.render("000"+str(score), False, colorLletres)
	elif score <= 99:
		surf = atariFont.render("00"+str(score), False, colorLletres)
	elif score <= 999:
		surf = atariFont.render("0"+str(score), False, colorLletres)
	else:
		surf = atariFont.render(str(score), False, colorLletres)
	return surf
		
def renderLevel(level):
	if level <= 9:
		surf = atariFont.render("0"+str(level), False, colorLletres)
	else:
		surf = atariFont.render(str(level), False, colorLletres)
	return surf
		
############################## FI DE DEFINICIONS #############################=3

pauseImage = pygame.image.load("Media/Images/pause_guai.png")
gameoverImage = pygame.image.load("Media/Images/Game_Over.png")
muteImage = pygame.image.load("Media/Images/mute.png")

pauseSound = pygame.mixer.Sound('Media/Music/pause.ogg')
unpauseSound = pygame.mixer.Sound('Media/Music/unpause.ogg')
pygame.mixer.music.load('Media/Music/MusicaTetris2.ogg')
muteSound = False
pygame.mixer.music.play(-1, 0.0)

fullscreen = False

mm = MainMenu()

while True:
		
	#data containers

	fallTime = 21 #en frames
	frames = 0

	score = 0
	level = 1
	linesThisFrame = 0
	linesTotal = 0
	nextGoal = 10

			
	scoreSurface = renderScore(score)
	levelSurface = renderLevel(level)
			

	pecaActual = nova_peca(randint(0, 6))
	nextPieces = [nova_peca_cua(randint(0, 6)), nova_peca_cua(randint(0, 6)),
		nova_peca_cua(randint(0, 6)), nova_peca_cua(randint(0, 6))]
	#~ pecaActual = nova_peca(2)
	#~ nextPieces = [nova_peca_cua(2), nova_peca_cua(2),
		#~ nova_peca_cua(2), nova_peca_cua(2)]

	timesSetZero = 0
	gameOver = False
	sortir = False
	mm.dibuixa()
	while True:
		#framerate
		clock.tick(30)
		refScreen = False
		if not pecaActual:
			keyMap['Accelerate'] = 0
			pecaActual = nova_peca(nextPieces[0][1])
			del nextPieces[0]
			nextPieces.append(nova_peca_cua(randint(0, 6)))
			refScreen = True
			#~ nextPieces.append(nova_peca_cua(2))
			for block in pecaActual.blocks:
				if boardyx[block.globY][block.globX] == 1:
					gameOver = True
		
		eventList = pygame.event.get()
		for event in eventList:
			if event.type == QUIT:
					sortir = True	
			if event.type == KEYDOWN:
				if event.key == controls['Quit']:
					sortir = True	
				if event.key == controls['Pause']:
					if not muteSound: pygame.mixer.music.pause()
					windowSurface.blit(background, (0, 0))
					windowSurface.blit(pauseImage, (0, 0))
					pygame.display.flip()
					if not muteSound: pauseSound.play()
					continua = True
					while continua:
						clock.tick(10)
						for event in pygame.event.get():
							if event.type == QUIT:
								sortir = True
								continua = False

							if event.type == KEYDOWN:
								if event.key == controls['Quit']:			
									sortir = True
									continua = False
								if event.key == controls['Pause']:
									continua = False
									break
								
					if not muteSound:
						unpauseSound.play()
						pygame.time.wait(100)
						pygame.mixer.music.unpause()
				if event.key == controls['TurnCW']:
					keyMap["TurnCW"] = 1
				#~ if event.key == controls['TurnCCW']:
					#~ print '\n'
					#~ for i in boardyx:
						#~ print i
					#~ keyMap["TurnCCW"] = 1
				if event.key == controls['Left']:
					keyMap["Left"] = 1
				if event.key == controls['Right']:
					keyMap["Right"] = 1
				if event.key == controls['Accelerate']:
					keyMap["Accelerate"] = 1
				if event.key == controls['Down']:
					keyMap["Down"] = 1							
				if event.key == controls['Fullscreen']:
					if fullscreen:
						fullscreen = False
						pygame.display.set_mode((800, 600), 0)
						refScreen = True
					else:
						fullscreen = True
						pygame.display.set_mode((800, 600), pygame.FULLSCREEN)
						refScreen = True
					
			if event.type == KEYUP:
				if event.key == controls['TurnCW']:
					keyMap["TurnCW"] = 0
				if event.key == controls['Left']:
					timesSetZero = 0
					keyMap["Left"] = 0
				if event.key == controls['Right']:
					timesSetZero = 0
					keyMap["Right"] = 0
				if event.key == controls['Accelerate']:
					keyMap["Accelerate"] = 0
				if event.key == controls['Down']:
					keyMap["Down"] = 0
				if event.key == controls['muteToggle']:
					if muteSound:
						muteSound = False
						pygame.mixer.music.unpause()
						refScreen = True
					else:
						muteSound = True
						pygame.mixer.music.pause()
						refScreen = True

		if sortir: break				
		
		
		frames += 1
		if frames > fallTime:
			frames = 0
			refScreen = True
			if not pecaActual.move(0, 1):
				pecaActual.carve()
				pecaActual = None
				
				
		if keyMap['TurnCW'] == 1:
			if pecaActual: pecaActual.turn_cw()
			refScreen = True
			keyMap['TurnCW'] = 0
			
		if keyMap['Left'] == 1:
			if (timesSetZero > 7 or timesSetZero == 0) and pecaActual:
				pecaActual.move(-1, 0)
				refScreen = True
			timesSetZero += 1
		if keyMap['Right'] == 1:
			if (timesSetZero > 7 or timesSetZero == 0) and pecaActual:
				pecaActual.move(1, 0)
				refScreen = True
			timesSetZero += 1
			
		if keyMap['Accelerate'] == 1:
			frames = fallTime
		
			
		if keyMap['Down'] == 1:
			while pecaActual.move(0, 1): pass
			pecaActual.carve()
			pecaActual = None
			score += 1
			scoreSurface = renderScore(score)
			keyMap['Down'] = 0
			frames = 0
			refScreen = True
		
		suprY = []
		for y in boardyx[3:]:
			if y == [1,1,1,1,1,1,1,1,1,1]:
				ind = boardyx.index(y)
				boardyx[ind] = [0,0,0,0,0,0,0,0,0,0]
				suprY.append(ind)
				for block in NonPieceBlocks[:]:
					if block.globY == ind:
						del NonPieceBlocks[NonPieceBlocks.index(block)]
				
					
		linesThisFrame = len(suprY)
		for y in suprY:
			for block in NonPieceBlocks[:]:
				if block.globY < y:
					block.baixa(1)
		
		if linesThisFrame != 0:
			refScreen = True
			linesTotal += linesThisFrame		
			if linesThisFrame == 1:
				score += 10
			elif linesThisFrame == 2:
				score += 30
			elif linesThisFrame == 3:
				score += 65
			elif linesThisFrame == 4:
				score += 100
			scoreSurface = renderScore(score)
			if linesTotal >= nextGoal:
				nextGoal += 10
				if nextGoal == 220: gameOver = True #CONGRATULATIONS YOU WON
				level += 1
				fallTime = 21-level
				ranNum = prev_background
				while ranNum==prev_background:
					ranNum = randint(1, 8)
				background = pygame.image.load('Media/Images/Fondo%d.png'%(ranNum)).convert_alpha()
				prev_background = ranNum
				colorLletres = color[str(ranNum)]
				levelSurface = renderLevel(level)
				scoreSurface = renderScore(score)
		
		if refScreen:
			windowSurface.blit(background, (0, 0))
			
			if pecaActual: pecaActual.update()
			windowSurface.blit(nextPieces[0][0], (450, 62))
			windowSurface.blit(nextPieces[1][0], (626, 62))
			windowSurface.blit(nextPieces[2][0], (626, 197))
			windowSurface.blit(nextPieces[3][0], (450, 197))
			
			for block in NonPieceBlocks:
				block.update()
				
			windowSurface.blit(scoreSurface, scorePos)
			windowSurface.blit(levelSurface, (601, 473))
			if muteSound: windowSurface.blit(muteImage, mutePos)
			
			pygame.display.flip()
		#loop end
		if gameOver:
			windowSurface.blit(gameoverImage, (0, 0))
			pygame.display.flip()
			pygame.time.wait(2000)
			mm.hiscores(score)
			break