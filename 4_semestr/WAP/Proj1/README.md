# Ants

### Základní zadání
Cieľom projektu je implementovať hru Mravenci:
https://www.instaluj.cz/mravenci
http://panda38.sweb.cz/software.html

- možnost vytvářet hry po síti (případně hrát 'proti počítači', jehož  přístup ke hře můžeme případně vytvořit)
- hra by byla hratelná pomocí webového GUI
- vytvořili bychom API pro programátory pro možnost hrát přes vlastní  modul / reinforcement learning stroj...
- backend bude zaznamenávat dokončené hry do DB a poskytne možnost  stažení dat pro analýzu / strojové učení

Dokumentácia bude obsahovať popis implementovaného API a ukážky použitia.

Na implementáciu je možné použiť ľubovolnú webovú technológiu a jazyk, t.j. Javascript s nejakým frameworkom (Angular, React, Ember, Vue, ...) (alebo aj bez), jazyky prekladané do Javascriptu (Typescript, Clojurescript, Elm, Purescript, ...) alebo technológie prekladané do WebAssembly.
Dokumentácia bude obsahovať odôvodnenie výberu technológie (chcem ci jazyk X vyskúšať je valídny ale nie dostatočný dôvod - skúsiť rozpísať čo Vás na danej technológii zaujalo) ako aj spätné zhodnotenie výberu technológie a práce s ňou (framework X bol dobrá voľba pretože feature Y nám výrazne zjednodušila implementáciu, technológia Z bola náročná na naučenie a pri práci na projekte sme nepocítili žiadne benefity...).

#### Všeobecné dodatky k zadání
Do WISu je třeba odevzdat zdrojové texty, soubory nutné pro sestavení projektu, dokumentaci v elektronické podobě a provést demonstraci cvičícímu.
Při odevzdání projektu vícečlenného týmu je nutné přesně popsat přínos jednotlivých členů týmu na řešení projektu.

V dokumentaci je vhodné vysvětlit výběr implementačních technologií.

Odevzdání projektu bude probíhat elektronicky a bude doplněno povinnou demonstrací výsledků v termínech vypsaných cvičícími v posledních dvou týdnech semestru.
Do IS se odevzdávají dva soubory, jeden *.zip s pouze zdrojovými soubory a jeden *.pdf soubor s dokumentací.
Odevzdávejte pouze Vámi vytvořené soubory, na převzaté knihovny se odkazujte v dokumentaci s příslušným popisem jejich začlenění do Vašeho projektu.

Prezentace a demonstrace je povinná a je možná až po elektronickém odevzdání.
Na termín prezentace se musí týmy registrovat. Při demonstraci se zaměřte především na to, čeho jste chtěli v projektu dosáhnout a co se vám povedlo.
Výhodou jsou známé plány v budoucím využití projektu.

Do technické zprávy (na rozdíl od prezentace) uveďte vše, co se týká vypracování projektu, jeho implementace a testování.
Dokumentujte informační zdroje, ze kterých bylo čerpáno při řešení, vlastní myšlenky a přínos. Nepopisujte všeobecně známé věci a triviality.
Podrobně vyjmenujte použité knihovny ve Vašem řešení a postup při jejich kompilaci s Vaší implementací.

Ve všech případech definujte vzhled všech zobrazovaných částí ve zvláštním externím stylovém předpise CSS (případně preprocesorem CSS)
opatřeném komentáři tak, aby uživatel mohl přizpůsobit vzhled řešení svým potřebám (zejména použité barvy, písmo, velikosti).

Použití hotových knihoven, frameworků nebo jejich částí je povoleno za předpokladu, že odevzdaný projekt obsahuje podstatnou část původního kódu.
Drobné úpravy cizích projektů nelze považovat za obhajitelný projekt.

#### Kompatibilita
Zvolené zadání implementujte tak, aby byl kód plně funkční nejméně v prohlížečích Firefox a Chrome v aktuálních verzích.

### Jak funguje hra Mravenci
Cílem hry je zničit hrad protihráče anebo postavit svůj hrad vysoký 100 a více jednotek.
Každý hráč má 3 typy surovin, které může používat - cihly, zbraně a krystaly. Všechny suroviny hráči narůstají vždy na začátku kola podle toho, kolik má pracovníků v dané oblasti (stavitelů, vojáků a mágů)
Hráč má v ruce 8 karet a každé kolo buď zahraje jednu kartu anebo některou zahodí. Zahraná / zahozená karta je na konci kola nahrazena novou z balíčku.

Karty ve hře:

| jméno karty | efekt | cena |
| ------ | ------ | ------ |
| Zeď | hradba +3 |  1x cihla |
| Základy | hrad +2 | 1x cihla  |
| Věž | hrad +5 | 5x cihla |
| Obrana | hradba +6 | 3x cihla |
| Hradba | hradba +22 | 12x cihla |
| Škola | stavitelé +1 | 8x cihla |
| Rezervy | hrad +8, hradba -4 | 3x cihla  |
| Povoz | hrad +8, hrad soupeře -4 | 10x cihla |
| Pevnost | hrad +20 | 18x cihla |
| Babylon | hrad +32 | 39x cihla |

| jméno karty | efekt | cena |
| ------ | ------ | ------ |
| Četa | útok 6 | 4x zbraň |
| Jezdec | útok 4 | 2x zbraň |
| Nábor | vojáci +1 | 8x zbraň |
| Rytíř | útok 3 | 2x zbraň |
| Sabotér | zásoby soupeře -4 | 12x zbraň |
| Smrtka | útok 32 | 28x zbraň |
| Střelec | útok 2 | 1x zbraň |
| SWAT | hrad soupeře -10 | 18x zbraň |
| Zloděj | převod zásob soupeře 5 | 15x zbraň |
| Zteč | útok 12 | 10x zbraň |

| jméno karty | efekt | cena |
| ------ | ------ | ------ |
| Čaroděj | mágové +1 | 8x krystal |
| Čaruj cihly | cihly +8 | 4x krystal |
| Čaruj zbraně | zbraně +8 | 4x krystal |
| Čaruj krystaly | krystaly +8 | 4x krystal |
| Drak | útok 25 | 21x krystal |
| Kletba | vše +1, vše soupeře -1 | 25x krystal |
| Skřítci | hrad +22 | 22x krystal |
| Znič cihly | cihly soupeře -8 | 4x krystal |
| Znič zbraně | zbraně soupeře -8 |4x krystal  |
| Znič krystaly | krystaly soupeře -8  | 4x krystal |


### Implementace
###
