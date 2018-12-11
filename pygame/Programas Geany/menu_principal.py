import pygame
import random
from JOGO import *
from menu_comandos import *

pygame.init()

pygame.font.init()

infoObject = pygame.display.Info()
Swidth, Sheight = infoObject.current_w, infoObject.current_h

win = pygame.display.set_mode((Swidth, Sheight))
pygame.display.set_mode((Swidth, Sheight),pygame.FULLSCREEN)

timer = time.time()

run2 = True

clock = pygame.time.Clock()

i_se = False


#Text###################################################################
class option:
	height = 40
	def __init__(self, x, y, w, s, bc):
		self.x = x
		self.y = y
		self.width = w
		self.surface = s
		self.bc = bc
	
	def se(self):
		global i_se, i_se2
		click = False
		x, y = pygame.mouse.get_pos()
		press, a, b = pygame.mouse.get_pressed()
		if (x >  self.x) and (x < self.x + self.width) and (y >  self.y) and (y <  self.y + option.height):
			if press == 0:
				self.bc = True
				click = False
				if i_se == True:
					i_se = False
					click = True
			if  press == 1:				
				i_se = True
				self.bc = True
				
		else:
			self.bc = False
		return click
		
	def draw(self):
		if self.bc == True:
			pygame.draw.rect(win, (220, 100, 0),(self.x - (self.width/10),  self.y, self.width, option.height))		
		win.blit(self.surface,(self.x, self.y))
		

myfont_titulos = pygame.font.SysFont('Impact', 50)
myfont_options = pygame.font.SysFont('Impact', 30)
myfont_pontos = pygame.font.SysFont('Impact', 90)

Creditos = option(Swidth/2 - 285, Sheight/2 - 235, 0, myfont_options.render('Mozart Cotrim e Marcelo Flach apresentam:', False, (220, 0, 0)), False)
Creditos2 = option(Swidth/2 - 283, Sheight/2 - 233, 0, myfont_options.render('Mozart Cotrim e Marcelo Flach apresentam:', False, (220, 100, 0)), False)

Titulo_1 = option(Swidth/2 - 150, Sheight/2 - 200, 0, myfont_titulos.render('Gotta Go Fast', False, (220, 0, 0)), False)
Titulo_2 = option(Swidth/2 - 145, Sheight/2 - 195, 0, myfont_titulos.render('Gotta Go Fast', False, (220, 100, 0)), False)

jogar = option(Swidth/2 - 40, Sheight/2 + 50, 80, myfont_options.render('Jogar', False, (200, 0, 0)), False)

C = option(Swidth/2 - 80, Sheight/2 + 150, 160, myfont_options.render('Comandos', False, (200, 0, 0)), False)

op = 'ON'
OP_on = option(Swidth/2 + 75, Sheight/2 + 100, 40, myfont_options.render(str(op), False, (200,0,0)), False)
OP = option(Swidth/2 - 150, Sheight/2 + 100, 250, myfont_options.render('Contoles de Som', False, (200,0,0)), False)

def pontos():
	try:
		arquivo = open('pontos.json', 'r')
		pontuações = json.load(arquivo)
		arquivo.close()
	except:
		pontuações = [{'Melhores Pontuações': '---', 'Pontuação Atual': '---'}]
	MP_numero = option(Swidth/2 - 260, Sheight/2 -100, 325, myfont_pontos.render(str(pontuações[0]['Melhor Pontuação']), False, (200, 0, 0)), False)
	MP_numero_2 = option(Swidth/2 - 265, Sheight/2 -105, 325, myfont_pontos.render(str(pontuações[0]['Melhor Pontuação']), False, (200, 100, 0)), False)
	
	AP_numero = option(Swidth/2 + 45, Sheight/2 -100, 325, myfont_pontos.render(str(pontuações[0]['Pontuação Atual']), False, (200, 0, 0)), False)
	AP_numero_2 = option(Swidth/2 + 40, Sheight/2 -105, 325, myfont_pontos.render(str(pontuações[0]['Pontuação Atual']), False, (200, 100, 0)), False)
	return MP_numero, MP_numero_2, AP_numero, AP_numero_2

MP = option(Swidth/2 - 270, Sheight/2 - 130, 325, myfont_options.render('Melhor Pontuação', False, (200, 0, 0)), False)
MP_2 = option(Swidth/2 - 268, Sheight/2 - 128, 325, myfont_options.render('Melhor Pontuação', False, (200, 100, 0)), False)

AP = option(Swidth/2 + 30, Sheight/2 - 130, 325, myfont_options.render('Pontuação Atual', False, (200, 0, 0)), False)
AP_2 = option(Swidth/2 + 32, Sheight/2 - 128, 325, myfont_options.render('Pontuação Atual', False, (200, 100, 0)), False)

MP_numero, MP_numero_2, AP_numero, AP_numero_2 = pontos()

class Contrario:
	
	vel = 0
			
	def __init__(self, x, y, height, width, color, hitbox):
		self.x = x
		self.y = y
		self.height = height
		self.width = width 			
		self.color = color
		self.hitbox = hitbox 				
				
	def velocidade(self):
		self.vel = (Swidth/2) * (Swidth/200000)
		self.x -= self.vel		
		
		
	def eotl(self):
		if self.x + (self.width*2) < 0:
			self.x += Swidth + ((Swidth/8)*2)
		
	def impri(self):
		pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))		

height_faixas = Sheight/150
width_faixas = (Swidth/10)		

faixa_1_1 = Contrario(300,  (((Sheight/5)+((Sheight/5)*3)/4)-(height_faixas/2))   , height_faixas, width_faixas, (255, 255, 255),0)
faixa_1_2 = Contrario(((Swidth/10)*2.5)+300,  (((Sheight/5)+((Sheight/5)*3)/4)-(height_faixas/2))   ,  height_faixas, width_faixas, (255, 255, 255),0)
faixa_1_3 = Contrario(((Swidth/10)*5)+300,  (((Sheight/5)+((Sheight/5)*3)/4)-(height_faixas/2))   ,  height_faixas, width_faixas, (255, 255, 255),0)
faixa_1_4 = Contrario(((Swidth/10)*7.5)+300,  (((Sheight/5)+((Sheight/5)*3)/4)-(height_faixas/2))   ,  height_faixas, width_faixas, (255, 255, 255),0)
faixa_1_5 = Contrario((-(Swidth/10)*2.5)+300,  (((Sheight/5)+((Sheight/5)*3)/4)-(height_faixas/2))   ,  height_faixas, width_faixas, (255, 255, 255),0)###
faixa_1_6 = Contrario((-(Swidth/10)*5)+300,  (((Sheight/5)+((Sheight/5)*3)/4)-(height_faixas/2))   ,  height_faixas, width_faixas, (255, 255, 255),0)###

faixa_2_1 = Contrario(150,  (((Sheight/5)+(((Sheight/5)*3)/4)*2)-(height_faixas/2))   , height_faixas, width_faixas, (255, 255, 255),0)
faixa_2_2 = Contrario(((Swidth/10)*2.5)+150,  (((Sheight/5)+(((Sheight/5)*3)/4)*2)-(height_faixas/2))   , height_faixas, width_faixas, (255, 255, 255),0)
faixa_2_3 = Contrario(((Swidth/10)*5)+150,  (((Sheight/5)+(((Sheight/5)*3)/4)*2)-(height_faixas/2))   , height_faixas, width_faixas, (255, 255, 255),0)
faixa_2_4 = Contrario(((Swidth/10)*7.5)+150,  (((Sheight/5)+(((Sheight/5)*3)/4)*2)-(height_faixas/2))   , height_faixas, width_faixas, (255, 255, 255),0)
faixa_2_5 = Contrario((-(Swidth/10)*2.5)+150,  (((Sheight/5)+(((Sheight/5)*3)/4)*2)-(height_faixas/2))   , height_faixas, width_faixas, (255, 255, 255),0)###
faixa_2_6 = Contrario((-(Swidth/10)*5)+150,  (((Sheight/5)+(((Sheight/5)*3)/4)*2)-(height_faixas/2))   ,  height_faixas, width_faixas, (255, 255, 255),0)###

faixa_3_1 = Contrario(0,  (((Sheight/5)+(((Sheight/5)*3)/4)*3)-(height_faixas/2))   , height_faixas, width_faixas, (255, 255, 255),0)
faixa_3_2 = Contrario(((Swidth/10)*2.5), (((Sheight/5)+(((Sheight/5)*3)/4)*3)-(height_faixas/2))   ,  height_faixas, width_faixas, (255, 255, 255),0)
faixa_3_3 = Contrario(((Swidth/10)*5), (((Sheight/5)+(((Sheight/5)*3)/4)*3)-(height_faixas/2))   ,  height_faixas, width_faixas, (255, 255, 255),0)
faixa_3_4 = Contrario(((Swidth/10)*7.5), (((Sheight/5)+(((Sheight/5)*3)/4)*3)-(height_faixas/2))   ,  height_faixas, width_faixas, (255, 255, 255),0)
faixa_3_5 = Contrario((-(Swidth/10)*2.5), (((Sheight/5)+(((Sheight/5)*3)/4)*3)-(height_faixas/2))   ,  height_faixas, width_faixas, (255, 255, 255),0)###
faixa_3_6 = Contrario((-(Swidth/10)*5),  (((Sheight/5)+(((Sheight/5)*3)/4)*3)-(height_faixas/2))   ,  height_faixas, width_faixas, (255, 255, 255),0)###

faixass = [faixa_1_1 ,faixa_1_2, faixa_1_3, faixa_1_4, faixa_1_5, faixa_1_6, faixa_2_1, faixa_2_2, faixa_2_3, faixa_2_4, faixa_2_5, faixa_2_6, faixa_3_1, faixa_3_2, faixa_3_3, faixa_3_4, faixa_3_5, faixa_3_6]

def desenho():
	win.fill((118, 250, 108))

	#Cenário##########
	pygame.draw.rect(win,(180, 230, 87), (0, (((Sheight/5)*1)-50), Swidth, (((Sheight/5)*3)+100))) 
	pygame.draw.rect(win,(95, 70, 55), (0, (((Sheight/5)*1)-15), Swidth, (((Sheight/5)*3)+30)))
	pygame.draw.rect(win, (13, 13, 13), (0, (((Sheight/5)*1)-5), Swidth, (((Sheight/5)*3)+10))) 
	pygame.draw.rect(win, (115, 107, 95), (0, ((Sheight/5)*1), Swidth, ((Sheight/5)*3))) 
	
	for i in faixass:
		Contrario.impri(i)
		
	win.blit(Creditos2.surface,(Creditos2.x, Creditos2.y))	
	win.blit(Creditos.surface,(Creditos.x, Creditos.y))	
	win.blit(Titulo_2.surface,(Titulo_2.x, Titulo_2.y))
	win.blit(Titulo_1.surface,(Titulo_1.x, Titulo_1.y))
	win.blit(OP.surface,(OP.x, OP.y))
	win.blit(MP_2.surface, (MP_2.x, MP_2.y))
	win.blit(MP.surface, (MP.x, MP.y))
	win.blit(AP_2.surface, (AP_2.x, AP_2.y))
	win.blit(AP.surface, (AP.x, AP.y))
	win.blit(MP_numero.surface, (MP_numero.x, MP_numero.y))
	win.blit(MP_numero_2.surface, (MP_numero_2.x, MP_numero_2.y))
	win.blit(AP_numero.surface, (AP_numero.x, AP_numero.y))
	win.blit(AP_numero_2.surface, (AP_numero_2.x, AP_numero_2.y))
	lista_options = [jogar, C, OP_on]
	for i in lista_options:
		option.draw(i)
	
	pygame.display.update()

def escolha():
	global op
	
	click = option.se(jogar)
	if click == True:
		init_menu(op, win)
		pygame.mouse.set_visible( True )	
		global MP_numero, MP_numero_2, AP_numero, AP_numero_2
		MP_numero, MP_numero_2, AP_numero, AP_numero_2 = pontos()
						
	click = option.se(OP_on)
	if click == True:
		if op == 'ON':
			op = 'OFF'
			music(op)			
		elif op == 'OFF':
			op  = 'ON'
			music(op)			
	click = option.se(C)
	if click == True:
		loop_comandos(win)
		pygame.mouse.set_visible( True )
		music(op)
	return op

def sair2(run2):	
	if event.type == pygame.QUIT:
		run2 = False
	elif event.type == pygame.KEYDOWN:
		if event.key == pygame.K_ESCAPE:
			run2 = False
	return run2

def music(op):	
	if op == 'ON':
		pygame.mixer.init()
		pygame.mixer.music.load('../Sons/TokyoDrift.mp3')
		pygame.mixer.music.set_volume(0.5)
		pygame.mixer.music.play(-1)
	elif op == 'OFF':
		pygame.mixer.quit()

try:
	if op == 'ON':
		music(op)	
except:
	op = 'OFF'

while run2:
		
	clock.tick(60)
	
	for event in pygame.event.get():
		run2 = sair2(run2)
		
	for i in faixass:
		Contrario.velocidade(i)
		Contrario.eotl(i)
	
	op = escolha()	
		
	if op == 'ON':
		OP_on = option(Swidth/2 + 75, Sheight/2 + 100, 40, myfont_options.render(str(op), False, (200,0,0)), OP_on.bc)
	elif op == 'OFF':
		OP_on = option(Swidth/2 + 75, Sheight/2 + 100, 50, myfont_options.render(str(op), False, (200,0,0)), OP_on.bc)
		
		
	desenho()
	
pygame.mixer.quit()	


