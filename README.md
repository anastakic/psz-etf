# Pronalazenje skrivenog znanja - projektni zadatak jun/jul 2021. godine

## Zadatak 1: Prikupljanje podataka

### Skripte:
- task_1_data_collecting.py
- task_1_database_connection.py

Za realizaciju prikupljanja web podataka sa url <https://www.nekretnine.rs/> korišćena je bs4 biblioteka. 
Podaci se čuvaju u real_estate bazi podataka na MySQL serveru.

## Zadatak 2: Analiza podataka

### Skripte:
- task_2_data_analysis.py

Analiza podataka predstavlja izvršavanje određenih upita nad bazom i njihovo čuvanje u .csv fajlovima u poddirektorijumu task_2_analysis, 
sledećim redom:

### A) Broj nekretnina za prodaju/iznajmljivanje
- A_count_by_type_offer.csv
### B) Broj nekretnina za prodaju u svakom od gradova
- B_count_offers_by_city.csv
### C) Broj uknjiženih/neuknjiženih
- C_count_offers_by_type_apartment.csv
- C_count_offers_by_type_house.csv
### D) Trideset najskupljih stanova/kuća
- D_top_30_most_expensive_apartments.csv
- D_top_30_most_expensive_houses.csv
### E) Prvih sto najvećih stanova/kuća
- E_top_100_biggest_apartments.csv
- E_top_100_biggest_houses.csv
### F) Izgrađeni 2020. godine za prodaju/iznajmljivanje po ceni opadajuće
- F_built_in_2020_sell.csv
- F_built_in_2020_rent.csv
### G) Top trideset sa najvećim brojem soba/kvadraturom/površinom zemljišta
- G_offers_by_total_rooms.csv
- G_offers_by_size_apartments.csv
- G_offers_by_land_area_size.csv
    
## Zadatak 3: Vizuelizacija podataka

### Skripte:
- task_3_data_visualization.py

Vizualizacija podataka predstavlja izvršavanje određenih upita nad bazom i njihov grafički prikaz sačuvan u .png formatu u 
poddirektorijumu task_3_visualization, sledećim redom:

### A) Deset delova Beograda sa najviše nekretnina
- A_top_10_parts_of_Belgrade.png
### B) Stanovi prema kvadraturi
- B_offers_by_apartment_size.png
### C) Izgrađene nekretnine po dekadama
- C_offers_by_build_year.png
- C_offers_by_real_estate_state.png
### D) Nekretnine za prodaju/iznajmljivanje u pet gradova sa najviše nekretnina
- D_top_5_cities_ratio.png
### E) Nekretnine za prodaju/iznajmljivanje po ceni
- E_offers_number_by_price.png
### F) Nekretnine za prodaju sa parkingom u Beogradu
- F_real_estate_in_Belgrade_with_parking.png

## Zadatak 4: Implementacija regresije

### Skripte:
- task_4_regression.py
- task_4_linear_regression_gradient_descent.py
- task_4_distance_calculation.pu
- task_4_gui_app.py

Ovaj zadatak obuhvata realizaciju višestruke linearne regresije koja koristi gradijentni spust za obučavanje modela. 
Nezavisne ulazne promenljive su udaljenost mesta nekretnine od centra grada, veličina nekretnine, godina izgradnje, 
broj soba i sprat na kom se nekretnina nalazi, dok je izlazni parametar cena same nekretnine. 
Ulazni parametni prosleđuju se kroz gui aplikaciju, koja je zajednička za zadatke 4 i 5.
Prilikom obučavanja modela koriste se normalizovani podatke zbog mogućnosti pojave overflow-a prilikom računana.
Sve metode linearne regresije su realizovane, bez korišćenja python biblioteka namenjih za ovaj tip rada.


## Zadatak 5: Implementacija klasifikacije

### Skripte:
- task_5_kNN
- task_4_distance_calculation.pu
- task_4_gui_app.py

Kao algoritam klasifikacije u ovom zadatku modelovan je algoritam K-najbližih suseda. Pokretanje ovog zadatka, 
kao i prethodnog, realizuje se pokretanjem gui aplikacije, gde se kroz formu unose određeni podaci, opciono se
može promeniti vrednost parametra K, i odabrati metrika za račun udaljenosti. Rezultat klasifikacije raspoređuje 
nekretninu u jednu od pet klasa:
* klasa 1:   cena manja od 49 999 €
* klasa 2:   cena izmedju 50 000 € i 99 999 €
* klasa 3:   cena izmedju 100 000 € i 149 999 €
* klasa 4:   cena izmedju 150 000 € i 199 999 €
* klasa 5:   cena veća od 200 000 €



