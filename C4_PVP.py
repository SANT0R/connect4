import numpy as np
import pygame
import sys
import math

SATIR_SAYISI=6
SUTUN_SAYISI=7

SIYAH=(0,0,0)
MAVI=(0,0,255)
KIRMIZI=(255,0,0)
SARI=(255,255,0)


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
			if tahta[r][c] == 1:
				pygame.draw.circle(ekran, KIRMIZI, (int(c*KARE_BOYUT+KARE_BOYUT/2), yukseklik-int(r*KARE_BOYUT+KARE_BOYUT/2)), YARICAP)
			elif tahta[r][c] == 2: 
				pygame.draw.circle(ekran, SARI, (int(c*KARE_BOYUT+KARE_BOYUT/2), yukseklik-int(r*KARE_BOYUT+KARE_BOYUT/2)), YARICAP)
	pygame.display.update()


tahta= oyun_alanı()
oyun_sonu=False
tur=0

pygame.init()

KARE_BOYUT=100

genislik=SUTUN_SAYISI*KARE_BOYUT
yukseklik=(SATIR_SAYISI+1)*KARE_BOYUT
boyut=(genislik,yukseklik)

ekran=pygame.display.set_mode(boyut)


YARICAP=int(KARE_BOYUT/2-5)




tahta_ciz(tahta)
#tahta_yaz(tahta)

pygame.display.update()

myfont = pygame.font.SysFont("monospace", 60, bold=True, italic=True)

while not oyun_sonu:

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

		if event.type == pygame.MOUSEMOTION:
			pygame.draw.rect(ekran, SIYAH, (0,0, genislik, KARE_BOYUT))
			posx = event.pos[0]
			if tur == 0:
				pygame.draw.circle(ekran, KIRMIZI, (posx, int(KARE_BOYUT/2)), YARICAP)
			else: 
				pygame.draw.circle(ekran, SARI, (posx, int(KARE_BOYUT/2)), YARICAP)
		pygame.display.update()

		if event.type == pygame.MOUSEBUTTONDOWN:
			pygame.draw.rect(ekran, SIYAH, (0,0, genislik, KARE_BOYUT))
			#print(event.pos)
			# Oyuncu 1 Girisi
			if tur == 0:
				posx = event.pos[0]
				col = int(math.floor(posx/KARE_BOYUT))

				if yer_bosmu(tahta, col):
					row = siradaki_bos_satir(tahta, col)
					tasi_birak(tahta, row, col, 1)

					if kazandinmi(tahta, 1):
						msj = myfont.render("Oyuncu 1 Kazandı!!   ", 1, KIRMIZI)
						ekran.blit(msj, (40,10))
						oyun_sonu = True


			# Oyuncu 2 Girisi
			else:
				posx = event.pos[0]
				col = int(math.floor(posx/KARE_BOYUT))

				if yer_bosmu(tahta, col):
					row = siradaki_bos_satir(tahta, col)
					tasi_birak(tahta, row, col, 2)

					if kazandinmi(tahta, 2):
						msj = myfont.render("Oyuncu 2 Kazandı!!", 1, SARI)
						ekran.blit(msj, (40,10))
						oyun_sonu = True

			tahta_yaz(tahta)
			tahta_ciz(tahta)

			tur += 1
			tur = tur % 2

			if oyun_sonu:
				pygame.time.wait(3000)