# ShopAnalyzer

**ShopAnalyzer** je jednoduchá aplikace pro analýzu nákupů domácnosti. Umožňuje načítat data o nákupech z CSV souborů, provádět jejich analýzu a generovat přehledné vizualizace.

---

## Funkcionalita

1. **Načítání a validace dat**  
   Načítání dat z CSV souboru a ověření jejich správnosti.  
   - Ověření chybějících hodnot.  
   - Validace formátu dat.  

2. **Analýza dat**  
   - Výpočet měsíčních výdajů.  
   - Identifikace nejčastěji nakupovaných položek.  
   - Rozbor výdajů podle kategorií.  

3. **Vizualizace dat**  
   - Časové grafy měsíčních výdajů.  
   - Koláčové grafy rozložení výdajů podle kategorií.  
   - Sloupcové grafy nejčastěji nakupovaných položek.  

---

## Požadavky

- Python 3.9+
- Pandas
- NumPy
- Matplotlib

---

## Další kapitola

Instalace

Klonujte nebo stáhněte tento repozitář.

Ujistěte se, že máte nainstalovaný Python (verze 3.8 nebo novější).

Nainstalujte požadované balíčky:

pip install -r requirements.txt

Použití

Spusťte aplikaci pomocí příkazové řádky:

python main.py <název_souboru.csv>

Například:

python main.py nakupy.csv

Struktura projektu

data_loader.py: Modul pro načítání a validaci dat.

analyzer.py: Modul pro analýzu dat.

visualizer.py: Modul pro vizualizaci dat.

main.py: Hlavní spouštěcí skript propojující všechny komponenty.

output/reports: Složka pro ukládání vygenerovaných grafů.

Zamýšlená rozšíření

Uživatelské rozhraní:

Implementace webového nebo desktopového uživatelského rozhraní pro snadnější interakci s aplikací.

Načítání dat z obrázků účtenek:

Integrace OCR technologie pro extrakci dat přímo z naskenovaných účtenek.



Aplikace byla vytvořena jako ukázkový projekt pro procvičení práce s Pythonem, datovou analýzou a vizualizací.


shop_analyzer/
├── data/
│   └── nakupy.csv             # Zdroj dat (nákupy z účtenek)
├── output/
│   └── reports/               # Výstupy (grafy, analýzy)
├── src/
│   ├── __init__.py            # Inicializace modulu
│   ├── data_loader.py         # Třída pro načítání a validaci dat
│   ├── analyzer.py            # Analytické funkce a logika
│   ├── visualizer.py          # Vizualizace dat (grafy)
│   └── utils.py               # Pomocné funkce
├── tests/
│   └── test_analyzer.py       # Testy pro analytické funkce
│   └── test_data_loader.py    # Testy pro načítání dat
├── main.py                    # Hlavní spouštěcí skript
├── requirements.txt           # Závislosti projektu
└── README.md                  # Dokumentace