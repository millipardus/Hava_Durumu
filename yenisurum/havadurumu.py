#!/usr/bin/env python
# -*- coding: cp1254 -*-

from Tkinter import *
from urllib import urlopen
from urllib import urlretrieve
from re import findall
from codecs import open as ac
from threading import Thread
from tkMessageBox import *
from subprocess import check_output
import os
from sqlite3 import connect

check_output("chcp 1254", shell=True)



class HavaDurumu(Tk):
    def __init__(self):
        self.acilis = 1
        Tk.__init__(self)
        self.insaEt()
        self.pencereAyarla(self, 244, 42, 0, 0)
        self.overrideredirect(1)
        self.lift()
        self.sicaklikCek()
        
    def sicaklikCek(self):
        kodlar = urlopen("http://mgm.gov.tr/tahmin/il-ve-ilceler.aspx").read()
        ifade='<em class="renkMin zemimeZ">(.*?&#176;C)</em>'
        ifade2='<em class="renkMax">(.*?&#176;C)</em>'

        son_ifade = '.*?<td id="sondrm" class="sond_zaman">(.*?)<br.*?>(.*?)</td>.*?'
        
        bul = findall(ifade, kodlar)
        bul2 = findall(ifade2, kodlar)
        son_bul = findall(son_ifade, kodlar)

        print son_bul
        
        if bul:
            sayisal_sicaklik = bul[0].replace("&#176;C", "").replace(',', '.')
        elif bul2:
            sayisal_sicaklik = bul2[0].replace("&#176;C", "").replace(',', '.')
    
        if bul:
            sicaklik = bul[0].replace("&#176;", u"°")
        elif bul2:
            sicaklik = bul2[0].replace("&#176;", u"°")
        self.hava_durumu["text"] = u"Sıcaklık: "+sicaklik
        self.sondurum["text"] = "Son güncelleme: "+son_bul[0][0]+" "+son_bul[0][1]
        
        if self.acilis and float(sayisal_sicaklik) > 38.0:
            showwarning(u"Uyarı !", u"Hava ısınıyor.")

        self.acilis+=1

        self.after(self.Cevir(1), self.sicaklikCek)
    
    def insaEt(self):
        self.hava_durumu = Label(self, text=u"")
        self.hava_durumu.pack()

        self.sondurum = Label(self, text=u"")
        self.sondurum.pack()
    
    def pencereAyarla(self, pencere, gen, yuk, d1, d2):
        #pencere.title(baslik)
        pencere.resizable(d1, d2)
        x = pencere.winfo_screenwidth() - gen
        y = 0
        
        pencere.geometry("%dx%d+%d+%d" %(gen, yuk,x, y))

    def Cevir(self, dk):
        return (dk*1000*60)
            
class Veritabani(object):
    def __init__(self):
        self.surumCek()
        if not 'surum_bilgisi.db' in os.listdir('.'):
            self.vt = connect("surum_bilgisi.db")
            self.im = self.vt.cursor()
            self.im.execute("CREATE TABLE surum (surumb)")
            self.im.execute("INSERT INTO surum VALUES (?)", (self.surum2,))
            self.vt.commit()
        else:
            self.vt = connect("surum_bilgisi.db")
            self.im = self.vt.cursor()
            self.im.execute("SELECT * FROM surum")
            self.surum = self.im.fetchall()[0][0]
            if self.surum != self.surum2:
                soru = askquestion(u"Güncelleme", u"Hava Durumu yazılımının yeni sürümü çıktı.\nSürüm: %s\nGüncellemek ister misiniz ?" %self.surum2)
                if soru == "yes":
                    self.im.execute("DROP TABLE surum")
                    self.im.execute("CREATE TABLE surum (surumb)")
                    self.im.execute("INSERT INTO surum VALUES (?)", (self.surum2,))
                    self.vt.commit()
                    
                    if sys.argv[0].endswith(".py"):
                        os.system("python guncelle.py %s" %sys.argv[0])
                    elif sys.argv[0].endswith(".exe"):
                        os.system("guncelle.exe %s" %sys.argv[0])
        
    def surumCek(self):
        oku = urlopen("https://raw.githubusercontent.com/millipardus/Hava_Durumu/master/surum.txt").read()
        global surum
        surum = float(oku)
        print surum
        self.calis = 0
        self.surum2 = surum
                    
if __name__ == "__main__":
    pencere = HavaDurumu()
    veritabani = Veritabani()
    pencere.mainloop()

    
        
        