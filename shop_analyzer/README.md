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