from tkinter import Canvas, simpledialog, Button, filedialog, Tk

class Vrchol():
    def __init__(self, nx, ny, cisloVrchola):
        self.x = nx
        self.y = ny
        self.komponentaID = -1
        self.oznaceny = False
        self.cisloVrchola = cisloVrchola

class Graf():
    def __init__(self, can):
        self.vrcholy = []
        self.hrany = []
        self.r = 20
        self.pocetKomponent = -1
        self.can = can
        self.colors = ['blue','red', 'black','green','purple', 'cyan', 'pink', 'darkgreen', 'darkgrey', 'darkblue' ]
    
    def vytvor_vrchol(self, x, y):
        '''
        vytvori novy vrchol na zadanych suradniciach
        Parametre: x,y - suradnice noveho vrcholu
        '''
        
        self.vrcholy.append(Vrchol(x, y, len(self.vrcholy)))
        for i in range(len(self.hrany)):
            self.hrany[i].append(-1)
        self.hrany.append([-1 for i in range(len(self.hrany)+1)])
        
    def kresli_graf(self, vymazat_canvas = True):
        '''
        zobrazi graf v Canvas
        Parametre:
            can - pointer na Canvas, v ktorom sa bude graf kreslit
            vymazat_canvas - predvolene True. Hodnota True znamena, ze sa pred vykreslenim grafu vymazu vsetky objekty v Canvas        
        '''
        cv = 0
        if vymazat_canvas:
            self.can.delete('all')
        
        for cv1 in range(len(self.hrany)):
            for cv2 in range(cv1+1, len(self.hrany)):
                if self.hrany[cv1][cv2] != -1:
                    self.can.create_line(self.vrcholy[cv1].x, self.vrcholy[cv1].y, self.vrcholy[cv2].x, self.vrcholy[cv2].y, fill=self.colors[self.vrcholy[cv1].komponentaID])
                    sx = (self.vrcholy[cv1].x + self.vrcholy[cv2].x) // 2
                    sy = (self.vrcholy[cv1].y + self.vrcholy[cv2].y) // 2
                    self.can.create_text(sx, sy, text = self.hrany[cv1][cv2])
                
            
        for vrchol in self.vrcholy:
            cv += 1
            if vrchol.oznaceny:
                farba = "red"
            else:
                farba = ""
            can.create_oval(vrchol.x - self.r, vrchol.y - self.r, vrchol.x + self.r, vrchol.y + self.r, fill=farba, outline=self.colors[vrchol.komponentaID])
            can.create_text(vrchol.x, vrchol.y, text = cv-1)
    
    def daj_cislo_vrcholu(self, x, y):
        '''
        vrati cislo vrcholu na zadanych suradniciach. Vrati -1, ak sa na zadanych suradniciach ziadny vrchol nenachadza
        Parametre: x,y - suradnice, kde sa hlada vrchol
        '''
        for cv, vrchol in enumerate(self.vrcholy):
            sx, sy = vrchol.x, vrchol.y
            if (sx - x) ** 2 + (sy - y) ** 2 < self.r **2:
                return cv
        return -1
    
    def oznac_vrchol(self, cv, oznacit = True):
        '''
        nastavi vrcholu atribut oznaceny.
        Parametre:
            cv - cislo vrcholu
            oznacit - hodnotu, ktoru nastavi atributu oznaceny. V pripade, ze tento parameter bude vynechany, nastavi sa hodnota True
        '''
        self.vrcholy[cv].oznaceny = oznacit
    
    def pridaj_hranu(self, cv1, cv2, cena):
        '''
        prida do grafu hranu
        Parametre:
            cv1, cv2 - cisla vrcholov, ktore hrana spaja
            cena - cena hrany
        '''
        self.hrany[cv1][cv2] = cena
        self.hrany[cv2][cv1] = cena
    
    def daj_cislo_oznaceneho_vrcholu(self):
        '''
        vrati cislo oznaceneho vrcholu. V pripade, ze ziadny vrchol nie je oznaceny, vrati -1
        '''
        cv = -1
        for vrchol in self.vrcholy:
            cv += 1
            if vrchol.oznaceny:
                return cv
        return -1
    def uloz_do_suboru(self, cesta='graf.txt'):
        '''
        ulozi graf do suboru vo formate:
        1. riadok - pocet vrcholov grafu
        n - riadkov (kazdy obsahuje n-cisel) - tabulka susednosti (cien hran)
        n - riadkov suradnic (dve cele cisla) vrcholov grafu
        Parametre:
            cesta - cesta k suboru, do ktoreho sa graf ulozi. V pripade, ze cesta nie je zadana, graf sa ulozi do suboru graf.txt v priecinku, kde je program spusteny
        '''
        
        with open(cesta,'w') as f:
            print(len(self.vrcholy),file = f)
            for riadok in self.hrany:
                print(' '.join(list(map(str,riadok))), file=f)
            for vrchol in self.vrcholy:
                print(vrchol.x, vrchol.y, file=f)

    def nacitaj_zo_suboru(self, cesta='graf.txt'):
        #du - nacitat graf zo suboru
        '''
        nacita graf zo suboru
        cesta - cesta ku grafu , defaultna graf.txt
        '''
        self.vrcholy = []
        self.hrany = []
        with open(cesta) as file:
            pocet = int(file.readline())
            for i in range(pocet):
                riadok = [int(x) for x in file.readline().replace('\n', '').split()]
                self.hrany.append(riadok)

            for i in range(pocet):
                vrchol = [int(x) for x in file.readline().replace('\n', '').split()]
                self.vrcholy.append(Vrchol(vrchol[0], vrchol[1], len(self.vrcholy)))

    def vymaz(self):
        self.vrcholy = []
        self.hrany = []
        self.kresli_graf()

    def walk(self, vrchol, komponentaID, predchadzajuci=None):     
        vrchol.komponentaID = komponentaID
        if vrchol.navstiveny:
            return
        else:
            vrchol.navstiveny = True
            for index, hrana in enumerate(self.hrany[vrchol.cisloVrchola]):
                if hrana != -1:
                    if self.vrcholy[index].komponentaID == komponentaID and self.vrcholy[index]!=predchadzajuci:
                        self.cyklus = True
                    self.walk(self.vrcholy[index], komponentaID, vrchol)

    def najdi_KS(self):
        self.cyklus = False
        for vrchol in self.vrcholy:
            vrchol.komponentaID = -1
            vrchol.navstiveny = False
        komponentaID = 0
        for vrchol in self.vrcholy:
            if vrchol.navstiveny:
                continue
            else:
                self.walk(vrchol, komponentaID)
                komponentaID+=1
        
        
        # vrati pocet komponent, nastavi komponenty do vrcholov
        self.pocetKomponent = komponentaID
        return komponentaID 

    def je_suvisly(self):
        self.najdi_KS()
        print(self.pocetKomponent)
        if self.pocetKomponent > 1:
            return False
        else: 
            return True

    def min_kostra(self):
        hr = []
        for vrchol in self.vrcholy:
            vrchol.vKostre = False
        for cv1, riadok in enumerate(self.hrany): 
            for cv2, hodnota in enumerate(riadok):
                if hodnota !=-1 and cv1 < cv2:
                    hr.append((cv1, cv2, hodnota))
                    print((cv1, cv2, hodnota))
        hr.sort(key=lambda x: x[2])
        kostra = []
        self.hrany = [[-1 for i in range(len(self.hrany))] for x in range(len(self.hrany))]

        for cv1, cv2, hodnota in hr: 
            v1, v2 = self.vrcholy[cv1], self.vrcholy[cv2]
            if not(v1.vKostre) or not(v2.vKostre):
                v1.vKostre, v2.vKostre = True, True
                self.hrany[cv1][cv2] = hodnota
                self.hrany[cv2][cv1] = hodnota
                kostra.append((cv1,cv2, hodnota))

        return kostra

    def ma_cyklus(self):
        self.najdi_KS()
        return self.cyklus
                  
    def vypisKS(self):
        self.najdi_KS()
        for vrchol in self.vrcholy:
            print("vrchol", vrchol.cisloVrchola, "patri do komponenty", vrchol.komponentaID)
        print("pocet komponent je", self.pocetKomponent)
        self.kresli_graf()
    
    def vypisSuvisly(self):
        print("Je suvisly", self.je_suvisly())
        self.kresli_graf()

    def vypisMinKostra(self):
        print(self.min_kostra())
        self.kresli_graf()

    def vypisCyklus(self):
        print("Cyklus v grafe", self.ma_cyklus())



    
      


            
    


def klik(event):
    '''
    udalost pri kliknuti lavym tlacidlom mysi do Canvas
    '''
    cv = graf.daj_cislo_vrcholu(event.x, event.y)
    cpv = graf.daj_cislo_oznaceneho_vrcholu()
    if cpv == -1:#prvy klik
        if cv == -1:#neklikol som na ziadny vrchol
            graf.vytvor_vrchol(event.x, event.y)
        else:
            graf.oznac_vrchol(cv)
    else:#druhy klik
        if cv == cpv:#druhy klik na ten isty vrchol ako prvy klik
            graf.oznac_vrchol(cv, False)
        elif cv == -1: #druhy klik na prazdne miesto (mimo vrcholov)
            return
        else:#idem robit hranu
            cena = simpledialog.askinteger('cena','Zadaj cenu hrany:')
            if cena != None:#zadal cenu hrany
                graf.pridaj_hranu(cv, cpv, cena)
            graf.oznac_vrchol(cpv,False)
    graf.kresli_graf(can)

def ulozgraf():
    '''
    zavola prislusnu metodu pre graf
    '''
    cesta = filedialog.asksaveasfilename(title='Ulozenie grafu')
    if cesta!='':
        graf.uloz_do_suboru(cesta)

def nacitajgraf():
    graf.nacitaj_zo_suboru()
    graf.kresli_graf(can)



root = Tk()

can = Canvas(root, width=800, height=600)
graf = Graf(can)
can.pack()
can.bind('<Button-1>',klik)
Button(text='Uloz',command=ulozgraf).pack()
Button(text='Nacitaj',command=nacitajgraf).pack()
Button(text='Najdi_KS',command=graf.vypisKS).pack()
Button(text='Je suvisly',command=graf.vypisSuvisly).pack()
Button(text='Min_kostra',command=graf.vypisMinKostra).pack()
Button(text='Cyklus',command=graf.vypisCyklus).pack()
Button(text='Vymaz',command=graf.vymaz).pack()

root.mainloop()