import pygame
import random
import math

pygame.init()

pygame.font.init()

infoObject = pygame.display.Info()
Swidth, Sheight = infoObject.current_w, infoObject.current_h

win = pygame.display.set_mode((Swidth, Sheight))
pygame.display.set_mode((Swidth, Sheight),pygame.FULLSCREEN)

run2 = True

angle2 = 0

clock = pygame.time.Clock()

try:
	pygame.mixer.init()
except:
	op = 'OFF'
	
turbo_print = 0

myfont_esc = pygame.font.SysFont('Impact', 50)
myfont_mouse = pygame.font.SysFont('Impact', 30)
myfont_turbo = pygame.font.SysFont('Impact', 90)

esc = myfont_esc.render("Pressione 'esc' para sair", False, (220, 0, 0))
esc2 = myfont_esc.render("Pressione 'esc' para sair", False, (220, 100, 0))
mouse = myfont_mouse.render('O carro seguirá o mouse, aperte o botão esquerdo para ir mais rápido', False, (220, 0, 0))
mouse2 = myfont_mouse.render('O carro seguirá o mouse, aperte o botão esquerdo para ir mais rápido', False, (220, 100, 0))
turbo = myfont_turbo.render('Turbo', False, (220, 0, 0))
turbo2 = myfont_turbo.render('Turbo', False, (220, 100, 0))
pause = myfont_mouse.render('Para pausar pressione "p" e para despausar pressione "esc"', False, (220, 0, 0))
pause2 = myfont_mouse.render('Para pausar pressione "p" e para despausar pressione "esc"', False, (220, 100, 0))

volante = pygame.image.load('../Imagens/volante.png')

def sounds():
	pygame.mixer.init()
	acelerada = pygame.mixer.Sound('../Sons/acelerado.wav')
	acelerada.set_volume(0.5)
	batida = pygame.mixer.Sound('../Sons/SomBatida.wav')
	
	return acelerada, batida

def mouse_function(Swidth):
	x, y = pygame.mouse.get_pos()
	pygame.mouse.set_visible( False )
	pos = x-16, y-16
	return pos

class Contrario:
	
	vel = 0
			
	def __init__(self, x, y, height, width, color, hitbox):
		self.x = x
		self.y = y
		self.height = height
		self.width = width 			
		self.color = color
		self.hitbox = hitbox 				
				
	def velocidade(self, sons, op):
		(x, y) = pygame.mouse.get_pos()
		self.vel = -(x-(Swidth/2)) * (Swidth/75000)
		press = pygame.mouse.get_pressed()
		if (x >= (Swidth/2) and x < (Swidth/2 + Swidth/3)) or (press[0] == 0 and x > (Swidth/2 + Swidth/3)):
			self.x += self.vel			
			if op == 'ON':
				sons[0].fadeout(500)			
		elif x >= (Swidth/2 + Swidth/3) and press[0] == 1:
			if op == 'ON':
				sons[0].play(fade_ms=200)
			self.vel = -(x-(Swidth/2)) * (Swidth/50000)
			self.x += self.vel						
		
	def eotl(self):
		if self.x + (self.width*2) < 0:
			self.x += Swidth + ((Swidth/8)*2)
		
	def impri(self):
		pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
				

height_faixas = Sheight/150
width_faixas = (Swidth/10)		

faixa_1_1 = Contrario(200,  (((Sheight/5)+((Sheight/5)*3)/4)-(height_faixas/2))   , height_faixas, width_faixas, (255, 255, 255),0)
faixa_1_2 = Contrario(((Swidth/10)*2.5)+200,  (((Sheight/5)+((Sheight/5)*3)/4)-(height_faixas/2))   ,  height_faixas, width_faixas, (255, 255, 255),0)
faixa_1_3 = Contrario(((Swidth/10)*5)+200,  (((Sheight/5)+((Sheight/5)*3)/4)-(height_faixas/2))   ,  height_faixas, width_faixas, (255, 255, 255),0)
faixa_1_4 = Contrario(((Swidth/10)*7.5)+200,  (((Sheight/5)+((Sheight/5)*3)/4)-(height_faixas/2))   ,  height_faixas, width_faixas, (255, 255, 255),0)
faixa_1_5 = Contrario((-(Swidth/10)*2.5)+200,  (((Sheight/5)+((Sheight/5)*3)/4)-(height_faixas/2))   ,  height_faixas, width_faixas, (255, 255, 255),0)###
faixa_1_6 = Contrario((-(Swidth/10)*5)+200,  (((Sheight/5)+((Sheight/5)*3)/4)-(height_faixas/2))   ,  height_faixas, width_faixas, (255, 255, 255),0)###

faixa_2_1 = Contrario(100,  (((Sheight/5)+(((Sheight/5)*3)/4)*2)-(height_faixas/2))   , height_faixas, width_faixas, (255, 255, 255),0)
faixa_2_2 = Contrario(((Swidth/10)*2.5)+100,  (((Sheight/5)+(((Sheight/5)*3)/4)*2)-(height_faixas/2))   , height_faixas, width_faixas, (255, 255, 255),0)
faixa_2_3 = Contrario(((Swidth/10)*5)+100,  (((Sheight/5)+(((Sheight/5)*3)/4)*2)-(height_faixas/2))   , height_faixas, width_faixas, (255, 255, 255),0)
faixa_2_4 = Contrario(((Swidth/10)*7.5)+100,  (((Sheight/5)+(((Sheight/5)*3)/4)*2)-(height_faixas/2))   , height_faixas, width_faixas, (255, 255, 255),0)
faixa_2_5 = Contrario((-(Swidth/10)*2.5)+100,  (((Sheight/5)+(((Sheight/5)*3)/4)*2)-(height_faixas/2))   , height_faixas, width_faixas, (255, 255, 255),0)###
faixa_2_6 = Contrario((-(Swidth/10)*5)+100,  (((Sheight/5)+(((Sheight/5)*3)/4)*2)-(height_faixas/2))   ,  height_faixas, width_faixas, (255, 255, 255),0)###

faixa_3_1 = Contrario(0,  (((Sheight/5)+(((Sheight/5)*3)/4)*3)-(height_faixas/2))   , height_faixas, width_faixas, (255, 255, 255),0)
faixa_3_2 = Contrario(((Swidth/10)*2.5), (((Sheight/5)+(((Sheight/5)*3)/4)*3)-(height_faixas/2))   ,  height_faixas, width_faixas, (255, 255, 255),0)
faixa_3_3 = Contrario(((Swidth/10)*5), (((Sheight/5)+(((Sheight/5)*3)/4)*3)-(height_faixas/2))   ,  height_faixas, width_faixas, (255, 255, 255),0)
faixa_3_4 = Contrario(((Swidth/10)*7.5), (((Sheight/5)+(((Sheight/5)*3)/4)*3)-(height_faixas/2))   ,  height_faixas, width_faixas, (255, 255, 255),0)
faixa_3_5 = Contrario((-(Swidth/10)*2.5), (((Sheight/5)+(((Sheight/5)*3)/4)*3)-(height_faixas/2))   ,  height_faixas, width_faixas, (255, 255, 255),0)###
faixa_3_6 = Contrario((-(Swidth/10)*5),  (((Sheight/5)+(((Sheight/5)*3)/4)*3)-(height_faixas/2))   ,  height_faixas, width_faixas, (255, 255, 255),0)###

faixass = [faixa_1_1 ,faixa_1_2, faixa_1_3, faixa_1_4, faixa_1_5, faixa_1_6, faixa_2_1, faixa_2_2, faixa_2_3, faixa_2_4, faixa_2_5, faixa_2_6, faixa_3_1, faixa_3_2, faixa_3_3, faixa_3_4, faixa_3_5, faixa_3_6]

class Carro:
	
	vel = 0
		
	def __init__(self, x, y, w, h, hit, i):
		self.x = x
		self.y = y
		self.width = w
		self.height = h		
		self.hitbox = hit
		self.imagem = i
		
	def mover_carro(self):
		x, y = pygame.mouse.get_pos()
		press = pygame.mouse.get_pressed()
		self.vel = (x-(Swidth/2)) / (Sheight/6)
		if self.vel > 0 and press[0] == 0:
			self.vel = self.vel
		elif self.vel > 0 and press[0] == 1:
			self.vel = self.vel*1.5
		else:
			self.vel = 0
		if y > (self.y):
			self.y += self.vel		
		if y < (self.y):
			self.y -= self.vel
		global carro_vel
		carro_vel = self.vel		
			
	def seguir(self):
		position = pygame.mouse.get_pos()
		angle = math.atan2(position[1] - self.y, position[0] - self.x)
		global angle2
		if angle2 < angle:
			angle2 += self.vel/1000
			if angle2 > angle:
				angle2 = angle
		elif angle2 > angle:
			angle2 -= self.vel/1000
			if angle2 < angle:
				angle2 = angle
		playerrot = pygame.transform.rotate(self.imagem, 360-angle2*57.29)
		playerpos = (self.x-playerrot.get_rect().width/2, self.y-playerrot.get_rect().height/2)
		return playerrot, playerpos
		

carro = Carro(((Swidth/8)),((Sheight/2)), 128, 64, (0,0,0,0), pygame.image.load('../Imagens/carríneo.png'))
carro_vel = 0

def desenho2(volante, pos):
	win.fill((118, 250, 108))	
	
	#Cenário##########
	pygame.draw.rect(win,(180, 230, 87), (0, (((Sheight/5)*1)-50), Swidth, (((Sheight/5)*3)+100))) 
	pygame.draw.rect(win,(95, 70, 55), (0, (((Sheight/5)*1)-15), Swidth, (((Sheight/5)*3)+30)))
	pygame.draw.rect(win, (13, 13, 13), (0, (((Sheight/5)*1)-5), Swidth, (((Sheight/5)*3)+10))) 
	pygame.draw.rect(win, (115, 107, 95), (0, ((Sheight/5)*1), Swidth, ((Sheight/5)*3))) 
	
	for i in faixass:
		Contrario.impri(i)
		
	win.blit(mouse2, (Swidth/100+2, Sheight/100+2))
	win.blit(mouse, (Swidth/100, Sheight/100))
	win.blit(esc2, ((Swidth/10)*6 + 3,(Sheight/10)*9 + 3))
	win.blit(esc, ((Swidth/10)*6 ,(Sheight/10)*9))
	win.blit(pause2, ((Swidth/100) + 2,(Sheight/10) + 2))
	win.blit(pause, ((Swidth/100) ,(Sheight/10)))
	press = pygame.mouse.get_pressed()
	if press[0] == 1:
		global turbo_print
		if turbo_print < 30:
			win.blit(turbo2,(Swidth/100 + 5, (Sheight/10) *8.5 + 5))
			win.blit(turbo,(Swidth/100, (Sheight/10) *8.5))
			turbo_print += 1
		if turbo_print > 29 and turbo_print < 61:
			turbo_print += 1
		if turbo_print == 60:
			turbo_print -= 60
	
	pos = mouse_function(Swidth)
	win.blit(volante, pos)
	
	carro_segue, pos = Carro.seguir(carro)
	win.blit(carro_segue, pos)
	
	pygame.display.update()
		

def sair(run2,event):	
	if event.type == pygame.QUIT:
		run2 = False
	elif event.type == pygame.KEYDOWN:
		if event.key == pygame.K_ESCAPE:
			run2 = False
	return run2

def pause_function(event, pause_botao):	
	if event.type == pygame.KEYDOWN:
		if event.key == pygame.K_p:
			pause_botao = True
			while pause_botao:
				clock.tick(3)
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						pause_botao = False
					elif event.type == pygame.KEYDOWN and not event.key == pygame.K_p:
						if event.key == pygame.K_ESCAPE:
							pause_botao = False
				myfont_pause = pygame.font.SysFont('Impact', 90)
				pause_1 = myfont_pause.render('Pause', False, (200, 0, 0))
				pause_2 = myfont_pause.render('Pause', False, (200, 100, 0))
				win.blit(pause_2, (Swidth/2 - 120 + 5, Sheight/2 - 75 + 5)) 
				win.blit(pause_1, ( Swidth/2 - 120, Sheight/2 - 75))
				pygame.display.update()

def loop_comandos(win2):
	sons = []
	try:
		if op == 'ON':
			a, b = sounds()
			sons.append(a)
			sons.append(b)
	except:
		op = 'OFF'
	pause_botao = False
	pos = mouse_function(Swidth)
	win = win2
	global run2
	run2 = True
	while run2:	
		clock.tick(60)
		for event in pygame.event.get():
			run2 = sair(run2, event)
			pause_botao = pause_function(event, pause_botao)
			
		for i in faixass:
			Contrario.velocidade(i, sons, op)
			Contrario.eotl(i)
		
		Carro.mover_carro(carro)
		
		desenho2(volante, pos)
