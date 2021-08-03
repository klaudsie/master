Plik Aplikacja należy rozpakować odpowiednim narzędziem. 

Nazwa programu: Współczynniki_bioróżnorodności.py
Niezbędne pakiety do prawidłowego działania programu są zestawione poniżej. Część z nich to wbudowane moduły standardowej biblioteki Pythona, natomiast niektóre należy zainstalować poleceniem \textit{pip install} [nazwa_modułu] w wierszu poleceń. 

1. os - standardowa biblioteka pythona
2. traceback -  standardowa biblioteka pythona
3.  subprocess - standardowa biblioteka pythona
4. tkvalidate - pip install tkvalidate 
5. pylab - pylab jest częścią matplotlib
6. tkinter - standardowa biblioteka pythona
7. pandas - pip install pandas 
8. csv - standardowa biblioteka pythona
9. math - standardowa biblioteka pythona
10. Pmw - pip install Pmw
11. numpy - pip install numpy 
12. ast - standardowa biblioteka pythona
13. shapely.geometry - pip install Shapely 
14. PIL - pip install Pillow
15. collections - standardowa biblioteka pythona 
16.  matplotlib - pip install matplotlib
17. geopandas - pip install geopandas (dla systemu macOS),  https://geoffboeing.com/2014/09/using-geopandas-windows/ (dla systemu Windows należy postępować zgodnie z instrukcjami z powyższej strony)

Do budowania aplikacji wykorzystano język Python w wersji 3.8.


Eksport pliku:

Dane, na których pracuje program eksportowane są ze strony iNaturalist. 
Pierwszym krokiem jest stworzenie zapytania. Zapytanie to nie powinno zwracać więcej niż 200 000 wyników. 

Kolejnym etapem jest wybranie kolumn, które będą eksportowane. Kluczowe, dla prawidłowego działania programu, jest pobranie następujących kolumn: latitude, longitude, common_name. Długość i szerokość geograficzna(longitude, latitude) dostępne są w kategorii Geo, natomiast nazwa gatunku (common_name) w kategorii Takson. Zdecydowana większość zmiennych jest domyślnie wybrana do eksportu. Należy zatem usunąć niepotrzebne kolumny, a pozostawić wyżej wymienione. Ostatnim działaniem jest wyeksportowanie danych. Proces ten trwa dłużej, gdy wybranych obserwacji jest wiele.