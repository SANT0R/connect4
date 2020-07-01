# Gerekli kütüphaneler

import numpy as np
import pygame
import sys
import math
import os
import random
from pygame.locals import *


#Muzik ve img dosyalarını dahil etmek için local dosya pathlari

filepath = os.path.abspath(__file__)
filedir = os.path.dirname(filepath)

music_path = os.path.join(filedir, "music/arka_plan_music.mp3")

efekt_path = os.path.join(filedir, "music/Efekt/Efekt")

img_path = os.path.join(filedir, "img/arka_plan_resim.png")


#Oyun tahtasinin satir ve sutun değişken atamalari

SATIR_SAYISI=6
SUTUN_SAYISI=7

#Projede kullanilan RGB renk atamalari

SIYAH=(0,0,0)
MAVI=(0,0,255)
KIRMIZI=(255,0,0)
BORDO=(128,0,0)
SARI=(255,255,0)

#Oyunda turu belirlemede kullanilacak degiskenler

OYUNCU1=0
OYUNCU2=1
AI=1

BOS=0
OYUNCU1_TASI=1
OYUNCU2_TASI=2
AI_TASI=2

#Oyun tahtasinin ve taslarin boyutlarini belirleyen atamalar

PENCERE_BOYU=4
KARE_BOYUT = 100
YARICAP = int(KARE_BOYUT/2-5)
genislik = SUTUN_SAYISI*KARE_BOYUT
yukseklik = (SATIR_SAYISI+1)*KARE_BOYUT
boyut = (genislik,yukseklik)

#pygame modulunu kullanmak için yapilan ayarlamalar

pygame.init()
ekran = pygame.display.set_mode(boyut)
pygame.display.set_caption("CONNECT 4")
pygame.display.update()


#Oyundaki yazilarin fontu

myfont = pygame.font.SysFont("monospace", 60, bold=True, italic=True)


#Oyun alaninin olusturulmasi

def oyun_alanı():
	tahta=np.zeros((SATIR_SAYISI,SUTUN_SAYISI))
	return tahta


#Oyun alanindaki bos yerlerin kontrolu

def yer_bosmu(tahta,sutun):
	return tahta[5][sutun]==0


#Tasin en alttaki bos satira aktarimi

def siradaki_bos_satir(tahta,sutun):
	for i in range(SATIR_SAYISI):
		if tahta[i][sutun]==0:
			return i


#Oyunu konsolda gorsel olarak yazdirma

def tahta_yaz(tahta):
	print(np.flip(tahta,0))


#Oyun alani taranarak kazanma koşullarinin olusup olusmadiginin testi

def kazandinmi(tahta, tas):
	#dikey kazanma koşullari
	for c in range(SUTUN_SAYISI-3):
		for r in range(SATIR_SAYISI):
			if tahta[r][c] == tas and tahta[r][c+1] == tas and tahta[r][c+2] == tas and tahta[r][c+3] == tas:
				return True

	 #yatay kazanma koşullari
	for c in range(SUTUN_SAYISI):
		for r in range(SATIR_SAYISI-3):
			if tahta[r][c] == tas and tahta[r+1][c] == tas and tahta[r+2][c] == tas and tahta[r+3][c] == tas:
				return True

	#capraz kazanma koşullari
	for c in range(SUTUN_SAYISI-3):
		for r in range(SATIR_SAYISI-3):
			if tahta[r][c] == tas and tahta[r+1][c+1] == tas and tahta[r+2][c+2] == tas and tahta[r+3][c+3] == tas:
				return True

	#capraz kazanma koşullari
	for c in range(SUTUN_SAYISI-3):
		for r in range(3, SATIR_SAYISI):
			if tahta[r][c] == tas and tahta[r-1][c+1] == tas and tahta[r-2][c+2] == tas and tahta[r-3][c+3] == tas:
				return True


#Oyun alanının gorsel olarak açilir pencereye aktarilmasi

def tahta_ciz(tahta):
	for c in range(SUTUN_SAYISI):
		for r in range(SATIR_SAYISI):
			pygame.draw.rect(ekran, MAVI, (c*KARE_BOYUT, r*KARE_BOYUT+KARE_BOYUT, KARE_BOYUT, KARE_BOYUT))
			pygame.draw.circle(ekran, SIYAH, (int(c*KARE_BOYUT+KARE_BOYUT/2), int(r*KARE_BOYUT+KARE_BOYUT+KARE_BOYUT/2)), YARICAP)

	for c in range(SUTUN_SAYISI):
		for r in range(SATIR_SAYISI):		
			if tahta[r][c] == OYUNCU1_TASI:
				pygame.draw.circle(ekran, KIRMIZI, (int(c*KARE_BOYUT+KARE_BOYUT/2), yukseklik-int(r*KARE_BOYUT+KARE_BOYUT/2)), YARICAP)
			elif tahta[r][c] == AI_TASI: 
				pygame.draw.circle(ekran, SARI, (int(c*KARE_BOYUT+KARE_BOYUT/2), yukseklik-int(r*KARE_BOYUT+KARE_BOYUT/2)), YARICAP)
	pygame.display.update()


#Oyuncunun sectigi sutuna tasın yerlestirilmesi

def tasi_birak(tahta,satir,sutun,tas):
	tahta[satir][sutun]=tas
	tahta_ciz(tahta)


#Yapay zekanin olasi hamleleri hesaplamasi icin geceici tas birakimi

def gecici_tasi_birak(tahta,satir,sutun,tas):
	tahta[satir][sutun]=tas


#Yapay zekanin yapabilecegi hamleler arasinda en iyisini secebilmesi icin puanlama sistemi

def puanlama(pencere,tas):
	k_tas = OYUNCU1_TASI
	if tas == OYUNCU1_TASI:
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


#Yapay zekanin tahtayi ve o anki durumu gozlemleyerek ilerisi icin yapabilecegi en iyi hamleyi hesaplamasi

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


# Yapay zekanin oynaya bilecegi bos yerlerin bulunmasi

def bos_bul(tahta):
	bos_yerler = []
	for col in range (SUTUN_SAYISI):
		if yer_bosmu(tahta,col):
			bos_yerler.append(col)

	return bos_yerler


#Yapay zekanin en iyi hamlesini bulmasi icin bos yerleri karsilastirmasi

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


#Oyunun bitip bitmediginin kontrolu

def oyun_sonu_mu(tahta):
	return kazandinmi(tahta,OYUNCU1_TASI) or kazandinmi(tahta,AI_TASI) or len(bos_bul(tahta)) == 0 


#Yapay zekanin tahtayi gozlemleyerek yapacagi hamleye karar vermesi icin min-max algoritmasi

def minimax(tahta, derinlik, alpha, beta, maximazingplayer):
	bos_yerler = bos_bul(tahta)
	terminal_dugum = oyun_sonu_mu(tahta)
	
	#Yapılacak hamle kalmadıysa
	if derinlik == 0 or terminal_dugum:
		if terminal_dugum:
			if kazandinmi(tahta,AI_TASI):
				return (None,1000000000000000000000)
			elif kazandinmi(tahta,OYUNCU1_TASI):
				
				return (None,-1000000000000000000)
			else: #Yapılacak hamle kalmadı
				return (None,0)
		else: #Derinlik sıfır
			return (None,gozlem(tahta,AI_TASI))
	
	#Rakibin o anki durumu ve maximum yapabilecegi hamlelerin karsılastırılması
	if maximazingplayer:
		deger = -math.inf
		sutun = random.choice(bos_yerler)
		for col in bos_yerler:
			row = siradaki_bos_satir(tahta,col)
			gecici = tahta.copy()
			gecici_tasi_birak(gecici,row,col,AI_TASI)
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
			gecici_tasi_birak(gecici,row,col,OYUNCU1_TASI)
			yeni_skor = minimax(gecici,derinlik-1, alpha, beta, True)[1]
			if yeni_skor < deger:
				deger = yeni_skor
				sutun = col
			
			beta = min(beta, deger)
			if alpha >=beta:
				break

		return sutun,deger


#Arayuze yazi yazdirma fonksiyonu

def metin_yaz(msj,font,renk,ekran,x,y):
	obj = font.render(msj,1,renk)
	ekran.blit(obj,(x,y))
	

#Menu arayuzu

click = False

def menu():
	
	# Ana muzik yuklemesi
	pygame.mixer.music.load(music_path) 
	pygame.mixer.music.play(-1,0.0)
	
	while True:

		#Efekt ve arka plan resim yuklemesi
		efekt = efekt_path
		rand = random.randint(1,10)
		efekt += str(rand)+".wav"
		arka_plan_resim = pygame.image.load(img_path).convert()
		ekran.blit(arka_plan_resim, (0, 0))

		#Pygame ile oyuncu hareketlerinin alinmasi
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			
			if event.type == MOUSEBUTTONDOWN:
				if event.button == 1:
					click = True


		metin_yaz("CONNECT4", myfont, MAVI, ekran, 150, 10)

		#Mouse un anlik pozisyonu
		mouse_x , mouse_y = pygame.mouse.get_pos()

		#Butonlarin olusturulmasi
		buton1 = pygame.Rect(50,100,200,50)
		buton2 = pygame.Rect(50,200,200,50)
		buton3 = pygame.Rect(50,300,200,50)
		buton4 = pygame.Rect(10,500,50,50)
		buton5 = pygame.Rect(100,500,50,50)
		buton6 = pygame.Rect(200,500,50,50)
		buton7 = pygame.Rect(10,600,50,50)
		buton8 = pygame.Rect(100,600,50,50)
		buton9 = pygame.Rect(200,600,50,50)


		#Buton aksiyonlari ile oyun baslatilmasi
		if buton1.collidepoint(mouse_x, mouse_y):
			if click:
				pygame.mixer.music.load(efekt) 
				pygame.mixer.music.play(0,0.0)
				oyun(0)
				pygame.mixer.music.load(music_path) 
				pygame.mixer.music.play(-1,0.0)

		if buton2.collidepoint(mouse_x, mouse_y):
			if click:
				pygame.mixer.music.load(efekt) 
				pygame.mixer.music.play(0,0.0)
				oyun(1)
				pygame.mixer.music.load(music_path) 
				pygame.mixer.music.play(-1,0.0)
		
		if buton3.collidepoint(mouse_x, mouse_y):
			if click:
				pygame.mixer.music.load(efekt) 
				pygame.mixer.music.play(0,0.0)
				oyun(2)
				pygame.mixer.music.load(music_path) 
				pygame.mixer.music.play(-1,0.0)

		if buton4.collidepoint(mouse_x, mouse_y):
			if click:
				pygame.mixer.music.load(efekt) 
				pygame.mixer.music.play(0,0.0)
				oyun(3,1)
				pygame.mixer.music.load(music_path) 
				pygame.mixer.music.play(-1,0.0)

		if buton5.collidepoint(mouse_x, mouse_y):
			if click:
				pygame.mixer.music.load(efekt) 
				pygame.mixer.music.play(0,0.0)
				oyun(3,2)
				pygame.mixer.music.load(music_path) 
				pygame.mixer.music.play(-1,0.0)

		if buton6.collidepoint(mouse_x, mouse_y):
			if click:
				pygame.mixer.music.load(efekt) 
				pygame.mixer.music.play(0,0.0)
				oyun(3,3)
				pygame.mixer.music.load(music_path) 
				pygame.mixer.music.play(-1,0.0)

		if buton7.collidepoint(mouse_x, mouse_y):
			if click:
				pygame.mixer.music.load(efekt) 
				pygame.mixer.music.play(0,0.0)
				oyun(3,4)
				pygame.mixer.music.load(music_path) 
				pygame.mixer.music.play(-1,0.0)

		if buton8.collidepoint(mouse_x, mouse_y):
			if click:
				pygame.mixer.music.load(efekt) 
				pygame.mixer.music.play(0,0.0)
				oyun(3,5)
				pygame.mixer.music.load(music_path) 
				pygame.mixer.music.play(-1,0.0)

		if buton9.collidepoint(mouse_x, mouse_y):
			if click:
				pygame.mixer.music.load(efekt) 
				pygame.mixer.music.play(0,0.0)
				oyun(3,6)
				pygame.mixer.music.load(music_path) 
				pygame.mixer.music.play(-1,0.0)
		


		#Hareketli efektleri
		if 50 < mouse_x < 50+200 and 100 < mouse_y < 100+50:
			pygame.draw.rect(ekran,BORDO,buton1)
		else:
			pygame.draw.rect(ekran,KIRMIZI,buton1)
		
		metin_yaz("PVP",myfont,MAVI,ekran,55,90)

		if 50 < mouse_x < 50+200 and 200 < mouse_y < 200+50:
			pygame.draw.rect(ekran,BORDO,buton2)
		else:
			pygame.draw.rect(ekran,KIRMIZI,buton2)
		
		metin_yaz("BOT 1",myfont,MAVI,ekran,55,190)

		if 50 < mouse_x < 50+200 and 300 < mouse_y < 300+50:
			pygame.draw.rect(ekran,BORDO,buton3)
		else:
			pygame.draw.rect(ekran,KIRMIZI,buton3)
		
		metin_yaz("BOT 2",myfont,MAVI,ekran,55,290)
		

		metin_yaz("Yapay  ", myfont, SARI, ekran, 30, 350)
		metin_yaz("Zeka ", myfont, SARI, ekran, 30, 420)


		if 10 < mouse_x < 10+50 and 500 < mouse_y < 500+50:
			pygame.draw.rect(ekran,BORDO,buton4)
		else:
			pygame.draw.rect(ekran,KIRMIZI,buton4)
		
		metin_yaz("1",myfont,MAVI,ekran,5,490)

		if 100 < mouse_x < 100+50 and 500 < mouse_y < 500+50:
			pygame.draw.rect(ekran,BORDO,buton5)
		else:
			pygame.draw.rect(ekran,KIRMIZI,buton5)
		
		metin_yaz("2",myfont,MAVI,ekran,105,490)

		if 200 < mouse_x < 200 + 50 and 500 < mouse_y < 500+50:
			pygame.draw.rect(ekran,BORDO,buton6)
		else:
			pygame.draw.rect(ekran,KIRMIZI,buton6)
		
		metin_yaz("3",myfont,MAVI,ekran,205,490)

		if 10 < mouse_x < 10+50 and 600 < mouse_y < 600+50:
			pygame.draw.rect(ekran,BORDO,buton7)
		else:
			pygame.draw.rect(ekran,KIRMIZI,buton7)
		
		metin_yaz("4",myfont,MAVI,ekran,5,590)

		if 100 < mouse_x < 100+50 and 600 < mouse_y < 600+50:
			pygame.draw.rect(ekran,BORDO,buton8)
		else:
			pygame.draw.rect(ekran,KIRMIZI,buton8)
		
		metin_yaz("5",myfont,MAVI,ekran,105,590)

		if 200 < mouse_x < 200+50 and 600 < mouse_y < 600+50:
			pygame.draw.rect(ekran,BORDO,buton9)
		else:
			pygame.draw.rect(ekran,KIRMIZI,buton9)
		
		metin_yaz("6",myfont,MAVI,ekran,205,590)
		
		click = False

		#Ekran update i
		pygame.display.update()


#Oyun arayuzu

def oyun(seviye,derinlik=1):
	#Oyun tahtasi olusturma
	tahta = oyun_alanı()
	tahta_ciz(tahta)
	#tahta_yaz(tahta)

	#Ilk atamalar
	oyun_sonu = False
	tur=random.randint(OYUNCU1,AI)

	#Oyun dongusu
	while not oyun_sonu:

		#Oyun efektlerinin yuklenmesi
		efekt1 = efekt_path
		rand = random.randint(1,10)
		efekt1 += str(rand)+".wav"

		# Oyuncu 1 Girisi
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()

			if event.type == pygame.MOUSEMOTION:
				pygame.draw.rect(ekran, SIYAH, (0,0, genislik, KARE_BOYUT))
				posx = event.pos[0]
				if tur == OYUNCU1 and not oyun_sonu:
					pygame.draw.circle(ekran, KIRMIZI, (posx, int(KARE_BOYUT/2)), YARICAP)
				if seviye == 0 and not tur == OYUNCU1 and not oyun_sonu:
					pygame.draw.circle(ekran, SARI, (posx, int(KARE_BOYUT/2)), YARICAP)
				

			if event.type == pygame.MOUSEBUTTONDOWN:
				pygame.draw.rect(ekran, SIYAH, (0,0, genislik, KARE_BOYUT))
				if tur == OYUNCU1 and not oyun_sonu:

					posx = event.pos[0]
					col = int(math.floor(posx/KARE_BOYUT))

					if yer_bosmu(tahta, col):
						row = siradaki_bos_satir(tahta, col)
						tasi_birak(tahta, row, col, OYUNCU1_TASI)
		
						pygame.mixer.music.load(efekt1) 
						pygame.mixer.music.play(0,0.0)

						if kazandinmi(tahta, OYUNCU1_TASI):
							metin_yaz("Oyuncu1 Kazandı!!   ",myfont,KIRMIZI,ekran,40,10)
							oyun_sonu = True
					tur += 1
					tur %= 2
					
				
				# Oyuncu 2 Girisi
				elif seviye == 0 and not tur == OYUNCU1 and not oyun_sonu:

					posx = event.pos[0]
					col = int(math.floor(posx/KARE_BOYUT))

					if yer_bosmu(tahta, col):
						row = siradaki_bos_satir(tahta, col)
						tasi_birak(tahta, row, col, OYUNCU2_TASI)
						
						
						pygame.mixer.music.load(efekt1) 
						pygame.mixer.music.play(0,0.0)

						if kazandinmi(tahta, OYUNCU2_TASI):
							metin_yaz("Oyuncu2 Kazandı!!   ",myfont,SARI,ekran,40,10)
							oyun_sonu = True
					tur += 1
					tur %= 2

		# Bot Girisleri
		if not seviye ==0:

			if tur == AI and not oyun_sonu:
				
				#Bot1 girisi
				if seviye == 1:
					pygame.time.wait(2000)
					col = random.randint(0,SUTUN_SAYISI-1)
					
				#Bot2 girisi
				elif seviye == 2:
					pygame.time.wait(2000)
					col = en_iyi_hamle(tahta,AI_TASI)
				
				#Yapay zeka girisi
				elif seviye == 3:
					col,minimax_skor = minimax(tahta, derinlik, -math.inf , math.inf , True)

				#Bot hamle belirlemesi
				if yer_bosmu(tahta, col):
					row = siradaki_bos_satir(tahta, col)
					tasi_birak(tahta, row, col, AI_TASI)

					efekt1 = efekt_path
					rand = random.randint(1,10)
					efekt1 += str(rand)+".wav"
					pygame.mixer.music.load(efekt1) 
					pygame.mixer.music.play(0,0.0)

					if kazandinmi(tahta, AI_TASI):
						metin_yaz("AI Kazandı!!   ",myfont,SARI,ekran,40,10)
						oyun_sonu = True
				tur += 1
				tur %= 2

		#Oyun sonu kontrolu
		if bos_bul(tahta) == [] and not oyun_sonu:
			msj = myfont.render("BERABERE!!", 1, MAVI)
			ekran.blit(msj, (40,10))
			oyun_sonu = True
		
		
		#tahta_yaz(tahta)
		tahta_ciz(tahta)
		

		if oyun_sonu:
			pygame.time.wait(3000)


#Menu cagirimi
menu()