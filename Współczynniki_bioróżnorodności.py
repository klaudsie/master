import os
import traceback
import subprocess
import tkvalidate
from tkinter import messagebox
from tkinter import *
from PIL import ImageTk, Image
import pylab
import tkinter as tk
from tkinter.ttk import *
from tkinter.filedialog import askopenfilename
import pandas as pd
import csv
import math
from tkinter.filedialog import asksaveasfile
import Pmw
from shapely.geometry import Point, Polygon
from geopandas import GeoDataFrame
import geopandas as gpd
import numpy as np
import ast

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, 
NavigationToolbar2Tk)
import matplotlib.pyplot as plt
from collections import Counter


#Przełącznik - umożliwia on przechodzenia do następnego okna.
class x(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.Przelacznik(Menu)

    def Przelacznik(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()

class Menu(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="Obliczanie wskaźników bioróżnorodności",font=('Times', 25)).pack(side="top")
        #Załadowanie zdjęcia
        self.photo = ImageTk.PhotoImage(Image.open("b1.png"))
        zdjecie = Label(image = self.photo)
        zdjecie.pack()
        zdjecie.place(x=100, y=100)

 

        button1=tk.Button(self, text="Przejdź dalej, aby wczytać dane", font=("Times", 15),
                  command=lambda: master.Przelacznik(WczytanieDanych)).pack(ipadx=10, ipady=10, side="bottom")
                                #W tym miejscu oznajmiam do której klasy przechodze

class WczytanieDanych(tk.Frame):
    def __init__(self, master):
        root.geometry("700x250")
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self)
        tk.Label(self, text="Wczytywanie danych",font=('Times', 25)).pack(side="top", pady=10)
    
        def wczytanie(event=None):
            plik=askopenfilename(filetypes = (("CSV Files","*.csv"),))
            #Możliwe jest wybranie pliku tylko CSV
            label1 = tk.Label(self, text="Wczytany plik: ", font=("Times",15), bg="white", fg="black")
            label2 = tk.Label(self, text= plik, font=("Times", 15),bg="white", fg="black")
            t=tk.Button(self, text="Przejdź dalej, aby wybrać obszar", font=("Times", 15), 
                      command=lambda: master.Przelacznik(WyborObszaru))
            #Możliwość przejścia dalej, do następnej klasy jest możliwe dopiero po
            #wczytaniu danych 
            t1=tk.Button(self, text="Wczytaj nowy plik", font=("Times",15),
                         command=lambda:master.Przelacznik(WczytanieDanych))
            #W razie wybrania złego pliku, użytkownik posiada możliwość, aby
            #wczytać go ponownie. Naciśnięcie "wczytaj nowy plik", powoduje, że
            #"Przełącznik" kieruje nas ponownie do klasy "WczytanieDanych".
            #Takie rozwiązanie może działać w nieskończoność. Ilość pomyłek
            #w wybraniu pliku jest nieograniczona
            WczytanieDanych.df=pd.read_csv(plik) #wczytanie pliku csv
            #print(WczytanieDanych.df)
        
            label1.pack(ipadx=2,ipady=2)
            label2.pack(ipadx=2,ipady=2)
            t.pack(side="right",ipadx=10,ipady=10, expand=True, pady=10)
            t1.pack(side="left",ipadx=10,ipady=10, expand=True, pady=10)

        

        tk.Button(self, text="Otwórz plik",font=("Times",15), command=wczytanie).pack(pady=10,ipadx=10,ipady=10, expand=True)
        
        
                                 
class WyborObszaru(tk.Frame):
    def __init__(self, master):
        root.geometry("700x200")
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self)
        tk.Label(self, text="Dla jakiego obszaru zamierzasz obliczyć bioróżnorodność?",font=('Times', 25)).pack(side="top", pady=10)

##        suwak = Combobox(self,)
##        suwak['values']= ("Dla całego kraju", "Dla wybranego obszaru")
##        #suwak.grid(column=0, row=0)
##        suwak.pack(pady=10)
        
        suwak=Combobox(self, values=("Dla całego kraju", "Dla wybranego obszaru"), width=27)
        suwak.current(0) #Ustawiam wartość domyślną dla suwaka 
        suwak.pack(pady=10)

        
        def wybor(event=None):
            if suwak.get()=="Dla całego kraju":
                #messagebox.showinfo("Wybór", "Dla całego kraju")
                WyborObszaru.wybor=suwak.get()
                #Tworze nową zmienną-WyborObszaru.wybor. Do tej zmiennej przypisuje
                #wartość get() z comboboxa (mojego suwaka). Umożliwia to "dostanie się"
                #do tej zmiennej w klasie Wyniki. Tam stworzyłam warunek, który
                #na podstawie wyboru użytkownika oblicza bioróżnorodność dla całego
                #kraju lub dla wybranego obszaru
            elif suwak.get()=="Dla wybranego obszaru":
                #messagebox.showinfo("Wybór", "Dla wybranego obszaru")
                WyborObszaru.wybor=suwak.get()
       
            tk.Button(self, text="Przejdź dalej, aby wybrać gatunki", font=("Times", 15),
                command=lambda: master.Przelacznik(Wspolczynniki)).pack(ipadx=10,ipady=10,side=tk.BOTTOM, expand=True, pady=10)
        tk.Button(self, text="Zatwierdź", font=("Times",15), command=wybor).pack(ipadx=10,ipady=10)
        
            
        

                

    

class Wspolczynniki(tk.Frame):
     def __init__(self, master):
        root.geometry("700x200")
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self)
        tk.Label(self, text="Liczba gatunków",font=('Times', 25)).pack(side="top", pady=10)
    
        label_1 = tk.Label(self, text="Dla ilu gatunków chcesz obliczyć bioróżnorodność? ", bg="white", fg="black")
        #Pmw.EntryField pozwala na konfiguracje entry. Uzytkownik ma mozliwosc wpisania
        #wyłącznie liczby z danego, ustalonego zakresu. Wpisywanie liter, liczb po przecinku,
        #wartości ujemnych jest zablokowane 
        Wspolczynniki.gatunek1=Pmw.EntryField(self,labelpos=W,validate = {'validator' : 'numeric',
                'min' : 2, 'max' : 100, 'minstrict' : 2}, value=2, errorbackground="white")
        label_1.pack(pady=10)
        Wspolczynniki.gatunek1.pack()
            
        #zmienna gatunek1 posłuży mi do pętli - wykona ją tyle razy, ile użytkownik zadeklarował gatunków 

          
        t2=tk.Button(self, text="Przejdź dalej, aby wybrać gatunki", font=("Times", 15),
                  command=lambda: master.Przelacznik(Gatunki))


        t2.pack(ipadx=10,ipady=10, expand=True, pady=10)

class Gatunki(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, root)
        root.geometry("750x550")
        #od root odchodzi main_frame. Od main_frame odchodzi druga, my_canvas również odchodzi od main_frame
        #od my_canvas odchodzi trzecia, na którym buduję pętle 
        #main_frame=Frame(root)
        main_frame = tk.Frame(root, background="white")
        main_frame.pack(fill=BOTH, expand=1)
        #main_frame.config(width=500, height= 500)
        #fill=BOTH = wypełnia przestrzeń od lewej do prawej i od gory do dolu
        #druga=Frame(main_frame)
        druga=tk.Frame(main_frame)
        druga.pack(fill=X, side=BOTTOM)
        #side_LEFT, fill=X

        my_canvas=Canvas(main_frame, width=1000, height=500)
        my_canvas.pack( fill=BOTH, expand=0)#0
        my_canvas.place(relx=0.5, rely=0.5, anchor=CENTER)


        y_scrollbar=tk.Scrollbar(main_frame, orient=VERTICAL, comman=my_canvas.yview)
        y_scrollbar.pack(side=RIGHT, fill=Y)


        my_canvas.configure(yscrollcommand=y_scrollbar.set)


        my_canvas.bind("<Configure>",lambda e: my_canvas.config(scrollregion= my_canvas.bbox(ALL))) 

        trzecia=tk.Frame(my_canvas,width=1000, height=1000, bg="white")
        my_canvas.create_window((0,0),window= trzecia, anchor="n")
        my_canvas.place(relx=0.5, rely=0.5, anchor=CENTER)
        tk.Label(trzecia, text="Podaj nazwy gatunków, dla których chcesz obliczyć bioróżnorodność.",font=('Times', 25)).pack(side="top", pady=15)

 
        n=0
        Gatunki.lista=[]
        if not Wspolczynniki.gatunek1.get():
            Gatunki.lgat=2
        else:
            Gatunki.lgat=int(Wspolczynniki.gatunek1.get()) #z klasy Wspolczynniki poobieram zmienna gatunek 1
        Gatunki.names = WczytanieDanych.df.common_name.tolist()
        #a=tuple(names)
        #Usunięcie tych samych nazw gatunków:
        nowa = []
        for i in Gatunki.names:
            if i not in nowa:
                nowa.append(i)
        
        #przekonwertowanie listy na tuple (daje to mozliwosc "wrzucenia" tuple do comboboxa)
        a=tuple(nowa)
        for i in range(Gatunki.lgat):
            n=n+1
            tk.Label(trzecia, text=n).pack()
            gatunek11=Combobox(trzecia, values=a, width=25)
            #tk.label_11.pack(pady=10)
            gatunek11.pack()
            Gatunki.lista.append(gatunek11)
        
            
            
            #Gatunki.nazwy_gatunkow=Gatunki.gatunek11.get()
            

        def ZatwierdzWyczysc(event):
            #my_canvas.delete("all")
            #for widget in main_frame.winfo_children():
                #widget.destroy()
            main_frame.pack_forget()
            trzecia.pack_forget()
            root.geometry("400x200")
            
            tk.Button(self, text="Przejdź dalej, aby zobaczyć wyniki", font=("Times", 15),
                command=lambda: master.Przelacznik(Wyniki)).pack(ipadx=10,ipady=10,side=tk.BOTTOM, expand=True,  pady=60)

            
            #Przenoszę przycisk przejścia dalej tutaj, ponieważ należy zmusić użytkownika, aby poprzez
            #przycisk "zatwierdz wyniki" wyczyścił okno main_frame.
            #W przeciwnym razie w klasie "Wyniki" wyświetla nam się okno utworzone w poprzedniej klasie
            
            
        #Button(trzecia,..), ponieważ przycisk "Zatwierdz wyniki" obejmuje w tym wypadku scrollbar
        #i możliwość wybrania tego przycisku wystepuje na samym dole okna
        button_1 = Button(trzecia, text="Zatwierdź wyniki")
        button_1.bind("<Button-1>", ZatwierdzWyczysc)
        button_1.pack(fill=X, pady=10)

      
class Wyniki(tk.Frame):
    def __init__(self, master):
        root.geometry("700x550")
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self)
        tk.Label(self, text="Wyniki",font=('Times', 25)).pack(side="top", pady=10)

        if WyborObszaru.wybor=="Dla całego kraju":
        #zliczanie wszystkich gatunków
            Gatunki.k=[]
            N=0
            shannon_wiener=0
            simpson=0
            for i in Gatunki.lista:
                #print(i.get())
                #Gatunki.k=i.get().append
                #przez i.get() dostaję się do elementów zapisanych w liście w klasie "Gatunki"
                #gat_malalitera=(WczytanieDanych.df["common_name"]==i.get()).sum()
                #w pliku csv nazwy gatunków zapisane są niekonsekwetnie - raz wielką, a raz mała literą stąd użycie funkcji capitalize()
                gat_duzalitera=(WczytanieDanych.df["common_name"]==i.get().capitalize()).sum()
                gat_duzalitera11=(WczytanieDanych.df["common_name"]==i.get().lower()).sum()
                gat_lacznie=int(gat_duzalitera) + int(gat_duzalitera11)
                N=N+gat_lacznie
                #Gatunki.k+=i.get()
                #print(k)
        
        
            for i in Gatunki.lista:
                #gat_malalitera1=(WczytanieDanych.df["common_name"]==i.get()).sum()
                gat_duzalitera1=(WczytanieDanych.df["common_name"]==i.get().capitalize()).sum()

                gat_duzalitera11=(WczytanieDanych.df["common_name"]==i.get().lower()).sum()
            
                gat_lacznie1=int(gat_duzalitera1) + int(gat_duzalitera11)

                pi=gat_lacznie1/N
                #print(pi)
                #ln=math.log(pi,10)
                if pi==0:
                    continue
                ln=np.log(pi)
                shannon_wiener= shannon_wiener + (pi * ln)
                #print(shannon_wiener)
                #Wspolczynnik Simpsona - Polska
                simpson= simpson + (pi**2)
        elif WyborObszaru.wybor=="Dla wybranego obszaru":
            Gatunki.k=[]
            N=0
            shannon_wiener=0
            simpson=0
            #lista jest na zewnątrz w pliku tekstowym o nazwie "obszar.txt"
            try:
                obszar=open("obszar.txt","r")
                obszar1=obszar.read()
            
            #Ast pozwala a konwertowanie stringów, które mają być listą, na liste.
            #Przez użyciem ten funkcji sprawdziłam type(obszar1). Wynikiem było <class "str">
            #Aby funkcja Polygon działała prawidłowo, potrzebuje <class 'list'>
            #Jest to moźliwe przez wykorzystanie 'ast'
                obszar3=ast.literal_eval(obszar1)
                polygon=Polygon(obszar3)
                #print(polygon)
            except SyntaxError:
                messagebox.showinfo("Błąd", "Niepoprawnie dokonano zapisu długości i szerokości geograficznej w pliku 'obszar.txt'. Zdefiniuj obszar prawdiłowo i przeprowadź badanie ponowanie.")
                master.Przelacznik(WczytanieDanych)
                sys.exit(1) #Jeżeli zostanie napotkany błąd, to program nie wykonana
                #operacji zamieszonych poniżej. Bez wykorzystania sys.exit program "wrzuca"
                #użytkownika z powrotem do okna "Wczytaj wyniki", ale wykonuje to, co zapisane poniżej.
                #Takie rozwiązanie generowało błedy 

                
            WczytanieDanych.df["common_name"]=WczytanieDanych.df["common_name"].str.capitalize()
            dlong=WczytanieDanych.df["longitude"]
            dlat=WczytanieDanych.df["latitude"]
            dcn=WczytanieDanych.df["common_name"]
            ll=len(dlong)
            n1=0
        
            #Tworzę listę z wartościami z entry (nazwami gatunków)
            gatt=[]
            for i in Gatunki.lista:
                gatt.append(i.get())

            
##            for j in range(ll):
##                punkt1=Point(dlat[j], dlong[j])
##                for i in gatt:
##                
##                  #print(punkt1.within(polygon))
##                    if ((punkt1.within(polygon)==True) and (dcn[j]==i)):
##                        n=n+1
##                    else:
##                        n1=n1+1
            
            
            wybrane=[]
            n=0
            k=0
            nowe_lat=[]
            nowe_long=[]
            nowe_common_name=[]
            for j in range(ll):
                punkt1=Point(dlat[j], dlong[j])
                for i in gatt:
                #print(punkt1.within(polygon))
                    if ((punkt1.within(polygon)==True) and dcn[j]==i.capitalize()):
                        wybrane.append(i)
                        n=n+1 #Ilość WSZYSTKICH osobików. Wartość ta podstawiana jest do mianownika
                        nowe_lat.append(dlat[j]) #do nowych list przyposuje wartości z pętli. Pozwoli mi to na stworzenie nowej ramki danych
                        nowe_long.append(dlong[j]) #dla osobników zaobserowanych na wybranym obszarze
                        nowe_common_name.append(i)  #Takie rozwiązanie pozwoli na zamieszczenie tych konkretnych osobników na wyznaczonym obszarze
            
            Wyniki.NoweDane=pd.DataFrame(
                {"latitude": nowe_lat,
                 "longitude": nowe_long,
                 "common_name": nowe_common_name
                 })
            counter=Counter(wybrane)
            #print(counter)
            #Aby móc poprawnie podstawić wartość do licznika (ilość osobników danego gatunku)
            #to należy policzyć ilość tych samych osobników z listy. Do tego
            #posłuzyła mi funkcja 'count'. Nastepnie stworzyłam pętlę, która
            #pozwala mi "dostać się" do tego, co zapisane jest w zmiennej 'counter'
            for i in counter:
                licznik=counter[i]
                pi=licznik/n
                if pi==0:
                    continue
                ln=np.log(pi)
                shannon_wiener= shannon_wiener + (pi * ln)
                simpson= simpson + (pi**2)
            
##            for j in range(ll):
##                punkt1=Point(dlat[j], dlong[j])
##                for i in gatt:
##                #print(punkt1.within(polygon))
##                    if ((punkt1.within(polygon)==True) and dcn[j]==i.capitalize()):
##                        n1=n1+1
##                        #print("n1:", n1)
##                        pi=n1/n
##                        #print("pi", pi)
##                        ln=math.log(pi,10)
##                        shannon_wiener= shannon_wiener + (pi * ln)
##                        #print(shannon_wiener)
##                        #Wspolczynnik Simpsona - Polska
##                        simpson= simpson + (pi**2)

      

        def Zapisz(event=None):
            #a=shannon_wiener.get()
            #b=simpson.get()
            a=str(shannon_wiener)
            b=str(simpson)
            #NAleży zamienić float na str, ponieważ funkcja write nie obługuje float'ow
            plik=asksaveasfile(defaultextension=".txt")
            #dodałam "\n", ponieważ wyniki nakładały się na siebie - były nieczytalne
            plik.write("Wybrane gatunki: \n")
            Gatunki.k=[]
            for i in Gatunki.lista:
                #print(i.get())
                plik.write(i.get() + "\n")
            plik.write("\nWspółczynniki bioróżnorodności: \n" + "Współczynnik Shannona-Wienera wynosi: " + a + "\n")
            plik.write("Współczynnik Simpsona wynosi: " + b)
            if WyborObszaru.wybor=="Dla wybranego obszaru":
                plik.write("\n\nGatunki, które zaobserwowano na wybranym obszarze i na podstawie których dokonano analizy: \n")
                nowa11 = []
                for i in wybrane:
                    if i not in nowa11:
                        nowa11.append(i)
                #W pliku txt zapisywane są nazwy gatunków, które wystąpiły na badanym obszarze
                #Może zdarzyć się sytuacja, gdzie użytkownik wybrał 10 gatunków, a tylko 7 z nich
                #występowały na badanym obszarze. W takiej sytuacji dla 7 z tych gatunków obliczana jest
                #bioróżnorodność. Pozostałe 3 są pomijane       
                for g in nowa11:
                    #print(g)
                    plik.write(g + "\n")
                
                


        def Mapa(event=None):
            if WyborObszaru.wybor=="Dla całego kraju":
                for i in Gatunki.lista:
                    NoweDane = WczytanieDanych.df[0:0] #puste dane
                    #print("NoweDane",NoweDane.head())
                    #Zmieniam nazwy gatunkow na male litery, aby poprawnie wskazywalo  lokalizacje
                    WczytanieDanych.df['common_name'] = WczytanieDanych.df['common_name'].str.lower()
                    NoweDane=WczytanieDanych.df[WczytanieDanych.df["common_name"]==i.get().lower()]
                    #print("NoweDane:",NoweDane.head())
                
                    geometry = [Point(xy) for xy in zip(NoweDane['longitude'], NoweDane['latitude'])]
                    gdf = GeoDataFrame(NoweDane, geometry=geometry)
                
                    mapa= gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
                    gdf.plot(ax=mapa.boundary.plot(figsize=(10, 6)), marker='.', color='red', markersize=10);
                    plt.suptitle(i.get()) #Printowanie dla jakiego gatunku odnosi się dany plot 
                    plt.get_current_fig_manager().set_window_title(i.get())
                    plt.show()
            elif WyborObszaru.wybor=="Dla wybranego obszaru":
                for i in counter:
                    NoweDane=Wyniki.NoweDane[0:0]
                    Wyniki.NoweDane['common_name'] = Wyniki.NoweDane['common_name'].str.lower()
                    NoweDane=Wyniki.NoweDane[Wyniki.NoweDane["common_name"]==i.lower()]
                    geometry = [Point(xy) for xy in zip(NoweDane['longitude'], NoweDane['latitude'])]
                    gdf = GeoDataFrame(NoweDane, geometry=geometry)
                
                    mapa= gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
                    gdf.plot(ax=mapa.boundary.plot(figsize=(10, 6)), marker='.', color='red', markersize=10);
                    plt.suptitle(i) #Printowanie dla jakiego gatunku odnosi się dany plot 
                    #Zmiana nazwy okna
                    plt.get_current_fig_manager().set_window_title(i)
                    plt.show()

                
       
        label5 = tk.Label(self, text="Gatunki wybrane do badania: ", font=("Times",15), bg="white", fg="black")    
        label5.pack()
                    
        #Wyświetlanie w oknie 'wyniki' gatunki, które zostały uwzględnione w obliczeniach:
        if WyborObszaru.wybor=="Dla całego kraju":
            Gatunki.k=[]
            for i in Gatunki.lista:
                label6 = tk.Label(self, text= i.get(), font=("Times", 15),bg="white", fg="green")
                label6.pack()

        elif WyborObszaru.wybor=="Dla wybranego obszaru":
            nowa11 = []
            for i in wybrane:
                if i not in nowa11:
                    nowa11.append(i)
            for g in nowa11:
                label6 = tk.Label(self, text= g, font=("Times", 15),bg="white", fg="green")
                label6.pack()
            

                
      
        #round - zaokrąglenie wyników    
        shannon_wiener=round(-(shannon_wiener),3)
        simpson=round(simpson,3)
        label1 = tk.Label(self, text="Wskaźnik Shannona-Wienera wynosi: ", font=("Times",15), bg="white", fg="black")    
        label2 = tk.Label(self, text= shannon_wiener, font=("Times", 15),bg="white", fg="black")
        label1.pack()
        label2.pack()

        label3 = tk.Label(self, text="Wskaźnik Simpsona wynosi: ", font=("Times",15), bg="white", fg="black")    
        label4 = tk.Label(self, text= simpson, font=("Times", 15),bg="white", fg="black")
        label3.pack()
        label4.pack()

        

        t1=tk.Button(self, text="Powtórz badanie", font=("Times",15),
                         command=lambda:master.Przelacznik(WczytanieDanych))
        t2=tk.Button(self, text="Zapisz wyniki", font=("Times", 15), command=Zapisz)

        t3=tk.Button(self, text="Wygeneruj mapę z lokalizacją wybranych gatunków", font=("Times",15),
                     command=Mapa)
                         
        
        t1.pack(ipadx=10,ipady=10, expand=True, pady=10)
        t2.pack(ipadx=10,ipady=10, expand=True, pady=10)
        t3.pack(ipadx=10,ipady=10, expand=True, pady=10)

       
        #print("Wskaźnik Shannona-Wienera wynosi: ",shannon_wiener)
        #print("Wskaźnik Simpsona wynosi: ",simpson)
        #print("n",n)
        #print("n1", n1)



  
        
    

        
           


if __name__ == "__main__":
    root = x()
    root.title("Obliczanie wskaźników bioróżnordoności")
    root.geometry("{}x{}+{}+{}".format(700, 600, 600, 40)) 
    root.mainloop()
