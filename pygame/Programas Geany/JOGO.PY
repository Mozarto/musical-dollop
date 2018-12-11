import pygame
import random
import math
import time
import json

pygame.init()

timer = time.time()

infoObject = pygame.display.Info()
Swidth, Sheight = infoObject.current_w, infoObject.current_h

win = 0

run = True

pontos_brutos = 0

i_fases = 1
myfont_fases = pygame.font.SysFont('Impact', 80)
speed_booster = 1
i_fases2 = 0
pisca = 0

a_re = 0
angle2 = 0

clock = pygame.time.Clock()

va1, va2 = pygame.image.load('../Imagens/vaca.png'), pygame.image.load('../Imagens/vaca2.png') 

#mouse##################################################################
def mouse(Swidth):
	volante = pygame.image.load('../Imagens/volante.png')
	x, y = pygame.mouse.get_pos()
	pygame.mouse.set_visible( False )
	pos = x-16, y-16
	return volante, pos


#sons###################################################################

def sounds():
	pygame.mixer.init()
	acelerada = pygame.mixer.Sound('../Sons/acelerado.wav')
	acelerada.set_volume(0.3)
	batida = pygame.mixer.Sound('../Sons/somexplosao.wav')
	batida.set_volume(1.0)
	vaca_som = pygame.mixer.Sound('../Sons/SomVaca.wav')
	vaca_som.set_volume(1.0)
	moto_som = pygame.mixer.Sound('../Sons/SomMoto.wav')
	moto_som.set_volume(0.2)
	return acelerada, batida, vaca_som, moto_som
	
class Contrario:
	
	(x, y) = pygame.mouse.get_pos()
	vel = -(x-(Swidth/2)) * 0.05	
	vaca_vel = 3
	vaca_start = 0
	oldpos_vaca = 0	
	
	def __init__(self, x, y, height, width, color, hitbox):
		self.x = x
		self.y = y
		self.height = height
		self.width = width 			
		self.color = color
		self.hitbox = hitbox 	
				
	def velocidade(self, contrarios, sons, op, pontos, carro, blit):
		global i_fases, speed_booster, i_fases2
		(x, y) = pygame.mouse.get_pos()
		if i_fases > i_fases2:
			speed_booster = speed_booster * 1.05
			self.pontos1 = pontos
			i_fases2 = i_fases
		self.vel = (-(x-(Swidth/2)) * (Swidth/75000)) * speed_booster
		if carro.y < (Sheight/5) or carro.y > (Sheight/5*4):
			self.vel = self.vel * 0.6
		if self.height == 40:
			self.vel = self.vel * 0.5
		press = pygame.mouse.get_pressed()
		if (x >= (Swidth/2) and x < (Swidth/2 + Swidth/3)) or (press[0] == 0 and x > (Swidth/2 + Swidth/3)):
			self.x += self.vel			
			global pontos_brutos		
			pontos_brutos += 1/len(contrarios)*(-self.vel/10)			
			if op == 'ON':
				sons[0].set_volume(0.25)			
				sons[0].play(fade_ms=200)
		elif x >= (Swidth/2 + Swidth/3) and press[0] == 1:
			if op == 'ON':
				sons[0].set_volume(0.5)
			self.vel = (-(x-(Swidth/2)) * (Swidth/50000)) * speed_booster
			if carro.y < (Sheight/5) or carro.y > (Sheight/5*4):
				self.vel = self.vel * 0.6
			if self.height == 40:
				self.vel = self.vel * 0.5
			self.x += self.vel			
			pontos_brutos += 1.5/len(contrarios)*(-self.vel/10)
					
	def re(self, contrarios, carro):
		x, y = pygame.mouse.get_pos()
		self.vel = -(x-(Swidth/4)) * (Swidth/200000)
		global a_re
		if x <= (Swidth/4) and a_re/len(contrarios) <= Swidth/8:
			self.x += self.vel	
			a_re += self.vel
		elif a_re/len(contrarios) >= Swidth/8 and x > Swidth/2 + Swidth/3:
			a_re = 0
						
	def eotl(self):
		if self.x + (self.width*2) < 0:
			self.x += Swidth + ((Swidth/8)*2)
	
	def random_place(self):		
		if self.x < (0 - (self.width*3)):
			self.y = random.randrange(int(Sheight/5),int((Sheight/5) + ((Sheight/5)*3) - self.height), 1)
			self.x = random.randrange(Swidth, 7500, 1)
	
	def random_place_ar(self):
		a = random.randrange(1,3,1)
		if self.x < (0 - (self.width*3)) and a == 2:
			self.y = Sheight/5 - self.height
			self.x = random.randrange(Swidth, 4000, 1)
		elif self.x < (0 - (self.width*3)) and a == 1:
			self.y = int((Sheight/5)*4)
			self.x = random.randrange(Swidth, 4000, 1)
					
	def random_place_vaca(self):
		if self.x < (0 - (self.width*3)):
			self.y = random.randrange(int(Sheight/5),int((Sheight/5) + ((Sheight/5)*3) - self.height), 1)
			self.x = random.randrange(Swidth, 12000, 1)
			while  self.x < self.oldpos_vaca + 100 and self.x > self.oldpos_vaca-100:
				self.x = random.randrange(Swidth, 12000, 1)
			self.oldpos_vaca = self.x
	
	def random_place_moto(self):
		if self.x < (0 - (self.width*3)):
			self.y = random.randrange(int(Sheight/5),int((Sheight/5) + ((Sheight/5)*3) - self.height), 1)
			self.x = random.randrange(Swidth, 6000, 1)
			while  self.x < self.oldpos_vaca + 100 and self.x > self.oldpos_vaca - 100:
				self.x = random.randrange(Swidth, 6000, 1)
			self.oldpos_vaca = self.x
			
	def motoca(self, carro, sons, op):
		if self.x < Swidth + 20 and self.x > Swidth - 20 and op == "ON":
			sons[3].play(fade_ms=200)
		if carro.y > self.y:
			self.y += int(carro.vel * 0.5)
		elif carro.y < self.y:
			self.y -= int(carro.vel * 0.5)
		
	def move_vaca(self, va_img, blit, sons, op):
		if self.x < Swidth + 10 and self.x > Swidth - 10 and op == "ON":
			sons[2].play(fade_ms=200)
		if Contrario.vaca_start == 0:
			Contrario.vaca_start = 1			
		elif Contrario.vaca_start == 1:
			Contrario.vaca_start = 0
		self.y = self.y + self.vaca_vel
		if self.y < int(Sheight/5):
			self.vaca_vel = 3
			va_img = va2
		elif self.y > int((Sheight/5) + ((Sheight/5)*3) - self.height):
			self.vaca_vel = -3
			va_img = va1
		if self.vaca_vel == -3:
			va_img = va1
		elif self.vaca_vel == 3:
			va_img = va2
				
		if Contrario.vaca_start == 1:
			blit[7] = va_img
		if Contrario.vaca_start == 0:
			blit[9] = va_img
		
		return blit

	def impri(self):
		pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
		
	def hit(self, enemy, run):
		if self.hitbox[1] > enemy.hitbox[0] and self.hitbox[1] < enemy.hitbox[1]:
			if (self.hitbox[2] < enemy.hitbox[3] and self.hitbox[2] > enemy.hitbox[2]) or (self.hitbox[3] > enemy.hitbox[2] and self.hitbox[3] < enemy.hitbox[3]):
				run = False							
		elif  self.hitbox[0] < enemy.hitbox[1] and self.hitbox[0] > enemy.hitbox[0]:
			if (self.hitbox[2] < enemy.hitbox[3] and self.hitbox[2] > enemy.hitbox[2]) or (self.hitbox[3] > enemy.hitbox[2] and self.hitbox[3] < enemy.hitbox[3]):
				run = False
		return run
		
	def update(self):
		self.hitbox = (int(self.x + (self.width/5)), int(self.x + self.width - (self.width/5)), int(self.y + (self.height/5)), int(self.y + self.height - (self.height/5)))
		
		
#Inimigos###############################################################

#faixas##############################

def faixas_0():
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

	faixas = [faixa_1_1 ,faixa_1_2, faixa_1_3, faixa_1_4, faixa_1_5, faixa_1_6, faixa_2_1, faixa_2_2, faixa_2_3, faixa_2_4, faixa_2_5, faixa_2_6, faixa_3_1, faixa_3_2, faixa_3_3, faixa_3_4, faixa_3_5, faixa_3_6]
	return faixas
	
#Inimigos##########################

def inimigos_0(faixas):
	buraco = Contrario(-500 , -500,  100, 100, (0,0,0), (0,0,0,0))
	buraco_2 = Contrario(-500 , -500,  100, 100, (0,0,0),(0,0,0,0))
	buraco_3 = Contrario(-500 , -500,  100, 100, (0,0,0),(0,0,0,0))
	arvore_1 = Contrario(-500, -500, 220, 220, (0,0,0), (0,0,0,0))
	arvore_2 = Contrario(-500, -500, 220, 220, (0,0,0), (0,0,0,0))
	arvore_3 = Contrario(-500, -500, 220, 220, (0,0,0), (0,0,0,0))
	arvore_4 = Contrario(-500, -500, 220, 220, (0,0,0), (0,0,0,0))
	vaca_1 = Contrario(-500, -500, 128, 40, (0,0,0), (0,0,0,0))
	vaca_2 = Contrario(-500, -500, 128, 40, (0,0,0), (0,0,0,0))
	moto = Contrario(-500, -500, 40, 100, (0,0,0), (0,0,0,0))
	contrarios = []	
	
	for i in faixas:
		contrarios.append(i)
	
	
	va_img = va1
	Bu_Img_1 = pygame.image.load('../Imagens/Buraco1.png')
	Bu_Img_2 = pygame.image.load('../Imagens/Buraco2.png')
	Bu_Img_3 = pygame.image.load('../Imagens/Buraco3.png')
	Ar_Img = pygame.image.load('../Imagens/Arvore.png')	
	Mo_Img = pygame.image.load('../Imagens/moto.png')
	
	blit = [buraco, Bu_Img_1, buraco_2, Bu_Img_2, buraco_3, Bu_Img_3, vaca_1, va_img, vaca_2, va_img, moto, Mo_Img, arvore_1, Ar_Img, arvore_2, Ar_Img, arvore_3, Ar_Img, arvore_4, Ar_Img]
	
	random_enemies = [buraco, buraco_2, buraco_3, arvore_1, arvore_2, arvore_3, arvore_4, vaca_1, vaca_2, moto]
	
	for i in random_enemies:
		contrarios.append(i)
			
	enemies_hit = random_enemies
	
	return contrarios, random_enemies, enemies_hit, blit, va_img

########################################################################
	
#Carro##################################################################
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
		if self.y < (Sheight/5) or self.y > (Sheight/5*4):
			self.vel = self.vel * 0.6
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
		
	def update(self):
		self.hitbox = (self.x - self.width/2, self.x + self.width/2, self.y - self.height/2, self.y + self.height/2)
				
def carro_0():
	carro = Carro(((Swidth/8)),((Sheight/2)), 128, 64, (0,0,0,0), pygame.image.load('../Imagens/carríneo.png'))
	carro_vel = 0
	return carro

#################################	

def fase(pontos):
	global i_fases, myfont_fases, pisca
	pisca += 1
	if pisca > 60:
		pisca = 0
	if pontos > (i_fases-1) * 60 and pontos < (i_fases-1) * 60 + 15 and pisca > 30:
		fase_surface = myfont_fases.render('Fase ' + str(i_fases), False, (200,0,0))
		fase_surface2 = myfont_fases.render('Fase ' + str(i_fases), False, (200,100,0))
		win.blit(fase_surface2, (Swidth/2 - 110 + 5, Sheight/5 * 4 + 5))
		win.blit(fase_surface, (Swidth/2 - 110, Sheight/5 * 4))
	elif pontos > (i_fases-1) * 60 + 15:
		i_fases += 1

def desenho(Swidth, faixas, carro, blit, pontos_surface, pontos_surface_2, pontos):
	win.fill((138, 230, 100))
	
	#Cenário##########
	pygame.draw.rect(win,(138, 239, 106), (0, (((Sheight/5)*1)-50), Swidth, (((Sheight/5)*3)+100))) 
	pygame.draw.rect(win,(95, 70, 55), (0, (((Sheight/5)*1)-15), Swidth, (((Sheight/5)*3)+30)))
	pygame.draw.rect(win, (13, 13, 13), (0, (((Sheight/5)*1)-5), Swidth, (((Sheight/5)*3)+10))) 
	pygame.draw.rect(win, (115, 107, 95), (0, ((Sheight/5)*1), Swidth, ((Sheight/5)*3))) 
	
	for i in faixas:
		Contrario.impri(i)
	
	for i in range(len(blit)-8):
		if i % 2 == 0:
			if blit[i].x + blit[i].width > 0 and blit[i].x < Swidth: 
				win.blit(blit[i+1], (int(blit[i].x), int(blit[i].y)))
			
	#Carro############
	carro_segue, pos = Carro.seguir(carro)
	win.blit(carro_segue, pos)
	
	for i in range(8, len(blit), 1):
		if i % 2 == 0:
			if blit[i].x + blit[i].width > 0 and blit[i].x < Swidth: 
				win.blit(blit[i+1], (int(blit[i].x), int(blit[i].y)))	
	
	volante, pos = mouse(Swidth)
	win.blit(volante, pos)
	
	#Pontos############
	win.blit(pontos_surface_2,(7, 2))
	win.blit(pontos_surface,(5, 0))
	
	fase(pontos)
		
			
	pygame.display.update()
	

def sair(run, event):	
	if event.type == pygame.QUIT:
		run = False
	elif event.type == pygame.KEYDOWN:
		if event.key == pygame.K_ESCAPE:
			run = False
	return run

def pause(event, pause_botao):	
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
			
	return pause_botao

def pontuation():
	actual_time = time.time() - timer
	myfont_pontos = pygame.font.SysFont('Impact', 30)
	pontos = int((pontos_brutos-(actual_time*8))/40)
	pontos_surface = myfont_pontos.render('Pontuação:' + str(pontos), False, (220, 0, 0))
	pontos_surface_2 = myfont_pontos.render('Pontuação:' + str(int(pontos)), False, (220, 100, 0))
	return pontos_surface, pontos_surface_2, pontos

def json_function(pontos):
	try:
		arquivo = open('pontos.json', 'r')
		pontuações = json.load(arquivo)
		arquivo.close()
	except:
		pontuações = [{'Melhor Pontuação':str(pontos), 'Pontuação Atual':str(pontos)}]
	if len(pontuações) > 0:
		if int(pontuações[0]['Melhor Pontuação']) < int(pontos):
			pontuações[0]['Melhor Pontuação'] = str(pontos)
		pontuações[0]['Pontuação Atual'] = str(pontos)
	arquivo = open('pontos.json', 'w')
	json.dump(pontuações, arquivo)
	arquivo.close() 
	
def init_menu(op, win2):
	global win, timer, pontos_brutos, run, i_fases, i_fases2, speed_booster
	run_final = False
	count = -1
	i_fases = 1
	i_fases2 = 0
	speed_booster = 1
	win = win2
	timer = time.time()
	actual_time = time.time() - timer
	pontos_brutos = 0
	sons = []
	try:
		if op == 'ON':
			a, b, c, d = sounds()
			sons.append(a)
			sons.append(b)
			sons.append(c)
			sons.append(d)
	except:
		op = 'OFF'
	run = True
	faixas = faixas_0()
	contrarios, random_enemies, enemies_hit, blit, va_img = inimigos_0(faixas)
	carro = carro_0()
	Contrario.vaca_start = 0
	exp1, exp2, exp3, exp4, exp5 = pygame.image.load('../Imagens/explosao/explosão.gif'), pygame.image.load('../Imagens/explosao/explosão (1).gif'),pygame.image.load('../Imagens/explosao/explosão (2).gif'), pygame.image.load('../Imagens/explosao/explosão (3).gif'), pygame.image.load('../Imagens/explosao/explosão (4).gif')
	explosao = [exp1, exp2, exp3, exp4, exp5]
	pontos = loop(faixas, contrarios, random_enemies, enemies_hit, carro, blit, sons, op, va_img, explosao, run_final, count)
	json_function(pontos)
	

def loop(faixas, contrarios, random_enemies, enemies_hit, carro, blit, sons, op, va_img, explosao, run_final, count):
	global run
	pause_botao = False
	while run:
		pontos_surface, pontos_surface_2, pontos = pontuation()
		
		clock.tick(60)
	
		Carro.mover_carro(carro)
		Carro.update(carro)
	
		for event in pygame.event.get():
			run = sair(run, event)
			pause_botao = pause(event, pause_botao)
		
		for i in range(len(random_enemies)):
			if i < 3:
				Contrario.random_place(random_enemies[i])
			elif i < 7:
				Contrario.random_place_ar(random_enemies[i])
			elif i < 9 and i_fases > 2:
				Contrario.random_place_vaca(random_enemies[i])
				blit = Contrario.move_vaca(random_enemies[i], va_img, blit, sons, op)
			elif i == 9 and i_fases > 3:
				Contrario.random_place_moto(random_enemies[i])
				Contrario.motoca(random_enemies[i], carro, sons, op)	
		
		for i in contrarios:
			Contrario.velocidade(i, contrarios, sons, op, pontos, carro, blit)	
			Contrario.re(i, contrarios, carro)
		
		for i in faixas:
			Contrario.eotl(i)
			
		for i in enemies_hit:
			run = Contrario.hit(carro, i, run)
			Contrario.update(i)
		
		desenho(Swidth, faixas, carro, blit, pontos_surface, pontos_surface_2, pontos)
		try:
			if run == False:
				sons[0].play()
		except:
				asas = 0
		if run == False:
			run_final = True
			count = 0
			if op == 'ON':
				try:
					sons[0].fadeout(10)					
				except:
					asas = 0
		while run_final:
			try:
				sons[1].set_volume(1.0)
				sons[1].play(fade_ms=100)
			except:
				op = 'OFF'
			clock.tick(10)
			count += 1
			win.fill((138, 230, 100))
			#Cenário##########
			pygame.draw.rect(win,(138, 239, 106), (0, (((Sheight/5)*1)-50), Swidth, (((Sheight/5)*3)+100))) 
			pygame.draw.rect(win,(95, 70, 55), (0, (((Sheight/5)*1)-15), Swidth, (((Sheight/5)*3)+30)))
			pygame.draw.rect(win, (13, 13, 13), (0, (((Sheight/5)*1)-5), Swidth, (((Sheight/5)*3)+10))) 
			pygame.draw.rect(win, (115, 107, 95), (0, ((Sheight/5)*1), Swidth, ((Sheight/5)*3))) 
			for i in faixas:
				Contrario.impri(i)
			for i in range(len(blit)-8):
				if i % 2 == 0:
					if blit[i].x + blit[i].width > 0 and blit[i].x < Swidth: 
						win.blit(blit[i+1], (int(blit[i].x), int(blit[i].y)))
	
			
			for i in range(8, len(blit), 1):
				if i % 2 == 0:
					if blit[i].x + blit[i].width > 0 and blit[i].x < Swidth: 
						win.blit(blit[i+1], (int(blit[i].x), int(blit[i].y)))
						
			win.blit(explosao[count], (carro.x - 200, carro.y - 200))
			pygame.display.update()
			if count == 4:
				run_final = False
		
	return pontos



