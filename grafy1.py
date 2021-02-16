from tkinter import Canvas, Tk, simpledialog, Entry, Frame, Label, OptionMenu, StringVar, Button



class Settings():
    def __init__(self):
        self.hodnoteneHrany = True
        self.width=600
        self.height = 600

settings = Settings()


class Node():
    def __init__(self, x, y, num):
        self.pos = [x, y]
        self.number = num
        self.visited = False
        self.komponenta = -1


class Graf():
    def __init__(self, can, hodnoteneHrany):
        self.cyklus = False
        self.colors = ["red", "blue", "green", "purple", "cyan", "orange", "brown", "darkgreen", "black"]
        self.vrcholy = []
        self.hrany = []
        self.r = 20
        self.selected = -1
        self.can = can
        self.hodnoteneHrany = hodnoteneHrany

    def klik(self, event):
        # print("klik")
        for vrchol in self.vrcholy:
            if (((event.x - vrchol.pos[0]) ** 2 + (event.y - vrchol.pos[1]) ** 2) ** (1 / 2)) < self.r:
                # selectovanie
                if self.selected == -1:
                    self.selected = self.vrcholy.index(vrchol)
                    # print("klik selected", self.selected)
                    return
                else:
                    self.pridajHranu(self.selected, self.vrcholy.index(vrchol))
                    # print("klik2")
                    return

        if self.selected != -1:
            self.pridajVrchol(event.x, event.y)
            self.pridajHranu(self.selected, len(self.vrcholy)-1)
        else:
            self.pridajVrchol(event.x, event.y)

    def vypisTabulku(self):

        print("////hodnoty hran \\\\\\\\\"")
        for vrchol in self.hrany:
            print(vrchol)
        print('.........')

    def vymazVsetko(self):
        self.vrcholy = []
        self.hrany = []
        self.selected = -1
        self.can.delete("all")
        self.Komponenty = {}

    def pridajVrchol(self, x, y):
        # print("pridaj vrchol")
        self.vrcholy.append(Node(x, y, len(self.vrcholy)))
        # self.vrcholy.append((x,y))
        for hrana in self.hrany:
            hrana.append(-1)
        self.hrany.append([-1 for i in range(len(self.hrany) + 1)])
        # self.nakresliVrchol(x,y)
        self.nakresliVsetko()
        # self.vypisTabulku()

    def nakresliVrchol(self, vrchol):
        x, y = vrchol.pos
        # print("nakresliVrchol")
        # print(vrchol.komponenta)
        self.can.create_oval(x - self.r/2, y - self.r/2, x + self.r/2, y + self.r/2, outline=self.colors[vrchol.komponenta])
        self.can.create_text(x, y, text=vrchol.number, fill=self.colors[vrchol.komponenta])

    def pridajHranu(self, vrchol1, vrchol2):
        if self.hodnoteneHrany:
            hodnotaHrany = simpledialog.askinteger("hodnota hrany", "kolko chces aby bola hodnota hrany")
        else:
            hodnotaHrany = 1

        self.hrany[vrchol1][vrchol2] = hodnotaHrany
        self.hrany[vrchol2][vrchol1] = hodnotaHrany
        # self.nakreslihranu((self.vrcholy[vrchol1], self.vrcholy[vrchol2]),hodnotaHrany)
        self.nakresliVsetko()
        self.selected = -1


    def nakreslihranu(self, vrcholy):
        # print(suradnice[0][0], suradnice[1][1])
        # x1,x2,y1,y2= suradnice[0][0],suradnice[1][0], suradnice[0][1], suradnice[1][1]
        vrchol1, vrchol2 = vrcholy
        x1, y1 = vrchol1.pos
        x2, y2 = vrchol2.pos
        sx, sy = (x1 + x2) // 2, (y1 + y2) // 2
        hodnota = self.hrany[vrchol1.number][vrchol2.number]
        self.can.create_line(x1, y1, x2, y2, fill=self.colors[vrchol1.komponenta])

        if self.hodnoteneHrany:
            self.can.create_text(sx, sy+10, text=hodnota, font="Georgia 20")

    def nakresliVsetko(self):
        # self.najdi_KS()
        self.can.delete("all")
        for vrchol in self.vrcholy:
            self.nakresliVrchol(vrchol)
        for vrcholIndex in range(len(self.hrany)):
            for vrchol2index in range(vrcholIndex, len(self.hrany)):
                if self.hrany[vrcholIndex][vrchol2index] != -1:
                    # self.nakreslihranu((self.vrcholy[vrcholIndex],self.vrcholy[vrchol2index]), self.hrany[vrcholIndex][vrchol2index])
                    self.nakreslihranu((self.vrcholy[vrcholIndex], self.vrcholy[vrchol2index]))

    def uloz(self, path="./graf.txt"):
        # print("ukladam")
        with open(path, 'w') as file:
            file.write(str(len(self.vrcholy))+'\n')
            for vrchol in self.hrany:
                for i in vrchol:
                    file.write(str(i) + " ")
                file.write('\n')
            for vrchol in self.vrcholy:
                file.write(str(vrchol.pos[0])+" "+str(vrchol.pos[1])+"\n")

    def nacitaj(self, path="./graf.txt"):
        self.vrcholy = []
        self.hrany = []
        with open(path) as file:
            pocet = int(file.readline())
            for i in range(pocet):
                a = [int(x) for x in file.readline().replace('\n', '').split()]
                # a = file.readline.split()
                self.hrany.append(a)
            for i in range(pocet):
                a = [int(x) for x in file.readline().replace('\n', '').split()]
                # print(a)
                # a = file.readline.split()
                self.vrcholy.append(Node(a[0], a[1], len(self.vrcholy)))

        # print("nacitany")
        # print(self.hrany)
        
        # print(self.ma_cyklus(), "cyklus")
        # print(self.je_suvisly(), "suvisly")
        # self.min_kostra()
        # print(self.vrcholy)
        self.nakresliVsetko()

    def prechadzaj(self, vrchol, idKomponenty, neprechadzajZnovu):
        # print("PRECHADZAM", vrchol.number, vrchol.visited)
        if not(vrchol.visited):
            vrchol.visited = True
            vrchol.komponenta = idKomponenty
            # print(vrchol.number, vrchol.komponenta)
            for dalsi in range(len(self.hrany[vrchol.number])):

                if self.hrany[vrchol.number][dalsi] != -1 and self.vrcholy[dalsi] != neprechadzajZnovu:
                    # print(self.hrany[vrchol.number], vrchol.number, dalsi)
                    self.prechadzaj(self.vrcholy[dalsi], idKomponenty, vrchol)
        else:
            self.cyklus = True

    def najdi_KS(self):
        for i in self.vrcholy:
            i.visited = False
        idKomponenty = 1
        self.Komponenty = {}
        for vrchol in self.vrcholy:
            if not(vrchol.visited):
                self.Komponenty[idKomponenty] = []
                self.prechadzaj(vrchol, idKomponenty, "")
                idKomponenty += 1
        for vrchol in self.vrcholy:
            self.Komponenty[vrchol.komponenta].append(vrchol)
        self.nakresliVsetko()
        return idKomponenty -1

    def je_suvisly(self):
        
        if self.najdi_KS() == 1:
            vysledok = True
        else:
            vysledok = False
        return vysledok

        # VYPISANIE KOMPONENTOV
        # for key in self.Komponenty:
        #     for vrchol in self.Komponenty[key]:
        #         print(vrchol.number, end = " ")
        #     print()
    def ma_cyklus(self):
        self.najdi_KS()
        return self.cyklus


    def min_kostra(self):  
        # print(self.hrany)      
        for vrchol in self.vrcholy:
            vrchol.stav = 0 #0 pre mimo| 1 pre sused| 2 vkostre|
            vrchol.hodnotaPridania = 9999999999
            vrchol.druhyKoniec = None
        selected = self.vrcholy[0]
        vrchol.stav = 1
        susedneVrcholy = [selected]
        selected.hodnotaPridania = 0
        Kostra = {'hrany':[], "hodnoty":[]}

        while(len(susedneVrcholy)> 0):
            selected = min(susedneVrcholy, key=lambda x: x.hodnotaPridania)
            susedneVrcholy.pop(susedneVrcholy.index(selected))
            selected.stav = 2
            if selected.druhyKoniec!=None:
                Kostra['hrany'].append((selected.number, selected.druhyKoniec.number))
                Kostra["hodnoty"].append(self.hrany[selected.number][selected.druhyKoniec.number])
            for cisloVrchola, hodnotaHrany in enumerate(self.hrany[selected.number]):                
                vedlajsiVrchol = self.vrcholy[cisloVrchola]
                if hodnotaHrany > 0:
                    if vedlajsiVrchol.stav < 2 and vedlajsiVrchol.hodnotaPridania > hodnotaHrany:
                        susedneVrcholy.append(vedlajsiVrchol)
                        vrchol.stav = 1
                        vedlajsiVrchol.hodnotaPridania = hodnotaHrany
                        vedlajsiVrchol.druhyKoniec = selected
            

        self.hrany=[[-1 for i in range(len(self.hrany))] for i in range(len(self.hrany))]
        for index, hrana in enumerate(Kostra["hrany"]):
                self.hrany[hrana[0]][hrana[1]] = Kostra["hodnoty"][index]
                self.hrany[hrana[1]][hrana[0]] = Kostra["hodnoty"][index]
        self.kostra = Kostra["hrany"]
        return self.kostra # vrati pole hran
            
    def vypis(self, what):
        if what == "suvisly":
            print("Je suvisly", self.je_suvisly())
        elif what == "komponenty":
            print("Pocet komponent v grafe", self.najdi_KS())
            for vrchol in self.vrcholy:
                print("Komponenta pre vrchol", vrchol.number, "je", vrchol.komponenta)    
        elif what=="cyklus":
            print("Graf ma cyklus", self.ma_cyklus())
        elif what =="kostra":
            print("Hrany v kostre", self.min_kostra())
        self.nakresliVsetko()
                

            
        # print(Kostra['hrany'])


class Gui():
    def __init__(self, root, settings):
        self.root = root
        self.settings = settings
        
        self.entry = Entry(root)
        self.canvas= Canvas(root, width=settings.width, height=settings.height, background='white')
        self.canvas.grid(row=0, column=1)
        self.stvar = StringVar()
        self.stvar.set("one")

        self.Graf1 = Graf(self.canvas, self.settings.hodnoteneHrany) 

        


        self.frame = Frame(self.root, width="150", height=600,  bg="#1e272e")
        self.frame.grid(row=0, column=0, sticky='nswe')
        self.frame.grid_propagate(0)
        # self.label1 = Label(self.frame, text="Figure").grid(row=0, column=0, sticky="nw")
        self.selectedText = StringVar()
        self.selectedText.set("None")
        self.label10 = Label(self.frame, bg="#1e272e", fg="white", text="Selected V: ").grid(row=1, column=0, sticky="we")
        self.label11 = Label(self.frame,bg="#1e272e", fg="white", width=10, textvariable=self.selectedText).grid(row=1, column=1, sticky="we",pady=20,)
        
        # self.option = OptionMenu(self.frame, self.stvar, "one", "two", "three").grid(row=1, column=1, sticky='nwe')
        self.UlozButton = Button(self.frame, text="Uloz Graf", bg="#05c46b", relief="flat", command=self.Graf1.uloz).grid(row=3, column=0,columnspan=2,  sticky="we")
        self.NacitajButton = Button(self.frame, text="Nacitaj Graf", bg="#05c46b", command=self.Graf1.nacitaj).grid(row=4, column=0, columnspan=2, sticky="we")
        self.NVymazButton = Button(self.frame, text="Vymaz graf", bg="#05c46b", command=self.Graf1.vymazVsetko).grid(row=5, column=0, columnspan=2, sticky="we")
        self.cyklusButton = Button(self.frame, text="Ma cyklus", bg="#05c46b", command=lambda: self.Graf1.vypis("cyklus")).grid(row=6, column=0, columnspan=2, sticky="we")
        self.KomponentyButton = Button(self.frame, text="Vyznac komponenty", bg="#05c46b", command=lambda:self.Graf1.vypis("komponenty")).grid(row=7, column=0, columnspan=2, sticky="we")
        self.JeSuvislyButton = Button(self.frame, text="Je Suvisly", bg="#05c46b", command=lambda:self.Graf1.vypis("suvisly")).grid(row=8, column=0, columnspan=2, sticky="we")
        self.MinKostraButton = Button(self.frame, text="Min_Kostra", bg="#05c46b", command=lambda:self.Graf1.vypis("kostra")).grid(row=9, column=0, columnspan=2, sticky="we")
        self.canvas.bind('<Button-1>', self.lclick)
  

    def lclick(self, event):
        # print(event)
        
        self.Graf1.klik(event)
        # print(self.Graf1.selected,"selected gui")
        self.selectedText.set("None" if self.Graf1.selected==-1 else str(self.Graf1.selected))



if __name__=='__main__':
    root = Tk()
    gui = Gui(root, settings)

    root.mainloop()

# spravit to tak aby sa to vykreslovalo naraz vzdy vsetko,




# print("pre pridanie bodu - L-click")
# print("pre ulozenie grafu - M-Click")
# print("pre nacitanie grafu zo suboru graf.txt, R-click")
# print("pri nacitani vypise ci je suvisly a azda ma cyklus")
# print("default je nastavena hodnota hrany na 1, ked sa nastavy hodnoteneHrany na True, tak bude hodnoteny")

