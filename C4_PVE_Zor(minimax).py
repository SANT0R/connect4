import numpy as np
import pygame
import sys
import math
import random

SATIR_SAYISI=6
SUTUN_SAYISI=7

SIYAH=(0,0,0)
MAVI=(0,0,255)
KIRMIZI=(255,0,0)
SARI=(255,255,0)

OYUNCU=0
AI=1

OYUNCU_TASI=1
AI_TASI=2

PENCERE_BOYU=4
BOS=0

def oyun_alanı():
    tahta=np.zeros((SATIR_SAYISI,SUTUN_SAYISI))
    return tahta

def tasi_birak(tahta,satir,sutun,tas):
    tahta[satir][sutun]=tas

def yer_bosmu(tahta,sutun):
    #secilen sutun bosmu
    return tahta[5][sutun]==0

def siradaki_bos_satir(tahta,sutun):
    #tası secilen stunun en alt bos satirina ekle
    for i in range(SATIR_SAYISI):
        if tahta[i][sutun]==0:
            return i

def tahta_yaz(tahta):
    print(np.flip(tahta,0))

def kazandinmi(tahta, tas):
	#dikey kazanma koşulları
	for c in range(SUTUN_SAYISI-3):
		for r in range(SATIR_SAYISI):
			if tahta[r][c] == tas and tahta[r][c+1] == tas and tahta[r][c+2] == tas and tahta[r][c+3] == tas:
				return True

	 #yatay kazanma koşulları
	for c in range(SUTUN_SAYISI):
		for r in range(SATIR_SAYISI-3):
			if tahta[r][c] == tas and tahta[r+1][c] == tas and tahta[r+2][c] == tas and tahta[r+3][c] == tas:
				return True

	#capraz kazanma koşulları
	for c in range(SUTUN_SAYISI-3):
		for r in range(SATIR_SAYISI-3):
			if tahta[r][c] == tas and tahta[r+1][c+1] == tas and tahta[r+2][c+2] == tas and tahta[r+3][c+3] == tas:
				return True

	#capraz kazanma koşulları
	for c in range(SUTUN_SAYISI-3):
		for r in range(3, SATIR_SAYISI):
			if tahta[r][c] == tas and tahta[r-1][c+1] == tas and tahta[r-2][c+2] == tas and tahta[r-3][c+3] == tas:
				return True

def tahta_ciz(tahta):
	for c in range(SUTUN_SAYISI):
		for r in range(SATIR_SAYISI):
			pygame.draw.rect(ekran, MAVI, (c*KARE_BOYUT, r*KARE_BOYUT+KARE_BOYUT, KARE_BOYUT, KARE_BOYUT))
			pygame.draw.circle(ekran, SIYAH, (int(c*KARE_BOYUT+KARE_BOYUT/2), int(r*KARE_BOYUT+KARE_BOYUT+KARE_BOYUT/2)), YARICAP)

	for c in range(SUTUN_SAYISI):
		for r in range(SATIR_SAYISI):		
			if tahta[r][c] == OYUNCU_TASI:
				pygame.draw.circle(ekran, KIRMIZI, (int(c*KARE_BOYUT+KARE_BOYUT/2), yukseklik-int(r*KARE_BOYUT+KARE_BOYUT/2)), YARICAP)
			elif tahta[r][c] == AI_TASI: 
				pygame.draw.circle(ekran, SARI, (int(c*KARE_BOYUT+KARE_BOYUT/2), yukseklik-int(r*KARE_BOYUT+KARE_BOYUT/2)), YARICAP)
	pygame.display.update()

def puanlama(pencere,tas):
	k_tas = OYUNCU_TASI
	if tas == OYUNCU_TASI:
		k_tas = AI_TASI
	skor=0
	if pencere.count(tas) == 4:
		skor += 100
	elif pencere.count(tas) == 3 and pencere.count(BOS) == 1:
		skor += 5
	elif pencere.count(tas) == 2 and pencere.count(BOS) == 2:
		skor += 2
	if pencere.count(k_tas) == 3 and pencere.count(BOS) == 1:
		skor -= 4

	return skor

def gozlem(tahta,tas):
	skor=0

	#Merkez sutun gözlemi
	merkez_dizin = [int(i) for i in list(tahta[:, SUTUN_SAYISI//2])]
	merkez_sayac = merkez_dizin.count(tas)
	skor += merkez_sayac * 3

	#Yatay gözlem
	for r in range(SATIR_SAYISI):
		satir_dizisi=[int(i)for i in list(tahta[r,:])]
		for c in range(SUTUN_SAYISI-3):
			pencere = satir_dizisi[c:c+PENCERE_BOYU]
			skor+=puanlama(pencere,tas)
	
	#Dikey gözlem
	for c in range(SUTUN_SAYISI):
		sutun_dizisi=[int(i)for i in list(tahta[:,c])]
		for c in range(SATIR_SAYISI-3):
			pencere = sutun_dizisi[r:r+PENCERE_BOYU]
			skor+=puanlama(pencere,tas)
	
	#Çapraz gözlem
	for r in range(SATIR_SAYISI-3):
		for c in range(SUTUN_SAYISI-3):
			pencere = [tahta[r+i][c+i] for i in range(PENCERE_BOYU)]
			skor+=puanlama(pencere,tas)
	
	for r in range(SATIR_SAYISI-3):
		for c in range(SUTUN_SAYISI-3):
			pencere = [tahta[r+3-i][c-i] for i in range(PENCERE_BOYU)]
			if pencere.count(tas) == 4:
				skor +=100
			elif pencere.count(tas) == 3 and pencere.count(BOS)==1:
				skor+=10
	
	return skor

def bos_bul(tahta):
	bos_yerler = []
	for col in range (SUTUN_SAYISI):
		if yer_bosmu(tahta,col):
			bos_yerler.append(col)
	return bos_yerler

def en_iyi_hamle(tahta,tas):
	bos_yerler=bos_bul(tahta)
	en_iyi_skor =-10000
	en_iyi_sutun =random.choice(bos_yerler)
	for col in bos_yerler:
		row = siradaki_bos_satir(tahta,col)
		gecici_tahta = tahta.copy()
		tasi_birak(gecici_tahta,row,col,tas)
		skor = gozlem(gecici_tahta,tas)
		if skor > en_iyi_skor:
			en_iyi_skor = skor
			en_iyi_sutun = col
			
	return en_iyi_sutun


def terminal_mi(tahta):
	return kazandinmi(tahta,OYUNCU_TASI) or kazandinmi(tahta,AI_TASI) or len(bos_bul(tahta)) == 0 


def minimax(tahta, derinlik, alpha, beta, maximazingplayer):
	bos_yerler = bos_bul(tahta)
	terminal_dugum = terminal_mi(tahta)
	
	if derinlik == 0 or terminal_dugum:
		if terminal_dugum:
			if kazandinmi(tahta,AI_TASI):
				return (None,1000000000000000000000)
			elif kazandinmi(tahta,OYUNCU_TASI):
				
				return (None,-1000000000000000000)
			else: #Yapılacak hamle kalmadı
				return (None,0)
		else: #Derinlik sıfır
			return (None,gozlem(tahta,AI_TASI))
	
	if maximazingplayer:
		deger = -math.inf
		sutun = random.choice(bos_yerler)
		for col in bos_yerler:
			row = siradaki_bos_satir(tahta,col)
			gecici = tahta.copy()
			tasi_birak(gecici,row,col,AI_TASI)
			yeni_skor = minimax(gecici,derinlik-1, alpha, beta, False)[1]
			if yeni_skor > deger:
				deger = yeni_skor
				sutun = col
			
			alpha = max(alpha, deger)
			if alpha >=beta:
				break

		return sutun,deger
	else:	#Minimazing
		deger = math.inf
		sutun = random.choice(bos_yerler)
		for col in bos_yerler:
			row = siradaki_bos_satir(tahta,col)
			gecici = tahta.copy()
			tasi_birak(gecici,row,col,OYUNCU_TASI)
			yeni_skor = minimax(gecici,derinlik-1, alpha, beta, True)[1]
			if yeni_skor < deger:
				deger = yeni_skor
				sutun = col
			
			beta = min(beta, deger)
			if alpha >=beta:
				break

		return sutun,deger







tahta= oyun_alanı()
oyun_sonu=False
tur=random.randint(OYUNCU,AI)

pygame.init()

KARE_BOYUT=100

genislik=SUTUN_SAYISI*KARE_BOYUT
yukseklik=(SATIR_SAYISI+1)*KARE_BOYUT
boyut=(genislik,yukseklik)

ekran=pygame.display.set_mode(boyut)


YARICAP=int(KARE_BOYUT/2-5)




tahta_ciz(tahta)
tahta_yaz(tahta)

pygame.display.update()

myfont = pygame.font.SysFont("monospace", 60, bold=True, italic=True)

while not oyun_sonu:

	# Oyuncu 1 Girisi
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

		if event.type == pygame.MOUSEMOTION:
			pygame.draw.rect(ekran, SIYAH, (0,0, genislik, KARE_BOYUT))
			posx = event.pos[0]
			if tur == OYUNCU:
				pygame.draw.circle(ekran, KIRMIZI, (posx, int(KARE_BOYUT/2)), YARICAP)
			

		if event.type == pygame.MOUSEBUTTONDOWN:
			pygame.draw.rect(ekran, SIYAH, (0,0, genislik, KARE_BOYUT))
			#print(event.pos)
			if tur == OYUNCU:
				posx = event.pos[0]
				col = int(math.floor(posx/KARE_BOYUT))

				if yer_bosmu(tahta, col):
					row = siradaki_bos_satir(tahta, col)
					tasi_birak(tahta, row, col, 1)

					if kazandinmi(tahta, OYUNCU_TASI):
						msj = myfont.render("Oyuncu Kazandı!!   ", 1, KIRMIZI)
						ekran.blit(msj, (40,10))
						oyun_sonu = True

					tur += 1
					tur = tur % 2
					
					tahta_yaz(tahta)
					tahta_ciz(tahta)

	# AI Girisi
	if tur==AI and not oyun_sonu:

		#col = random.randint(0,SUTUN_SAYISI-1)
		#col = en_iyi_hamle(tahta,AI_TASI)
		col,minimax_skor = minimax(tahta, 6, -math.inf , math.inf , True)

		if yer_bosmu(tahta, col):
			#pygame.time.wait(500)
			row = siradaki_bos_satir(tahta, col)
			tasi_birak(tahta, row, col, AI_TASI)

			if kazandinmi(tahta, AI_TASI):
				msj = myfont.render("AI Kazandı!!", 1, SARI)
				ekran.blit(msj, (40,10))
				oyun_sonu = True

		tur += 1
		tur = tur % 2

 
		tahta_yaz(tahta)
		tahta_ciz(tahta)

	if oyun_sonu:
		pygame.time.wait(3000)
