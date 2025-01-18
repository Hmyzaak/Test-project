import csv
import random
import os
from datetime import datetime, timedelta


# Funkce pro generování náhodného data v požadovaném rozsahu měsíců
def generate_date(start_date, months_range):
    # Vytvoří náhodný měsíc v rámci zadaného rozsahu
    delta = timedelta(days=random.randint(0, months_range * 30))
    return start_date - delta


# Funkce pro generování položky a kategorie
def generate_item(category):
    items = items = {
        "Potraviny": ["chleba", "banány", "rajčata", "mléko", "jogurt", "plísňový sýr", "káva", "těstoviny", "rýže", "mrkev", "máslo", "uzený sýr", "vejce", "kukuřice"],
        "Drogerie": ["deodorant", "šampon", "toaletní papír", "holící žiletky", "mycí gel", "zubní pasta", "kosmetické tampony", "prací prášek", "ústní voda", "krém na ruce"],
        "Zábava": ["dárky", "vstupné na koncert", "vstupné do kina", "předplatné časopisu", "deskovky", "hudební nástroje", "vstupné do zoo", "knížky", "hračky"],
        "Elektro": ["sluchátka", "USB kabel", "nabíječka", "powerbanka", "světelný zdroj", "televize", "mobilní telefon", "počítačová myš", "klávesnice", "elektrický zubní kartáček"],
        "Oblečení": ["tričko", "džíny", "svetr", "ponožky", "boty", "kapsáče", "mikina", "šaty", "kabela", "kravata"],
        "Sport a fitness": ["běžecké boty", "joggingové kalhoty", "posilovací činky", "cvičební podložka", "kolo", "sportovní láhev", "fitness náramek", "proteinový prášek", "tenisová raketa", "basketbalový míč"],
        "Zahrada a DIY": ["zahradní hadice", "zahradní nářadí", "květiny", "hnojivo", "pletivo", "rýč", "zahradní lopata", "gril", "lopatka na sázení", "zahradní židle"],
        "Cestování": ["cestovní kufr", "cestovní taška", "lístek na vlak", "lístek na let", "mapy", "fotoaparát", "cestovní polštář", "sluneční brýle", "opalovací krém", "plavky"],
        "Domácí potřeby": ["čisticí prostředky", "vysavač", "televize", "mikrovlnná trouba", "kávovar", "pračka", "lednice", "žehlička", "lampa", "osušky"],
        "Kancelářské potřeby": ["tiskárna", "papíry", "tužky", "sešívačka", "závěsy na okna", "kalkulačka", "desky na dokumenty", "obálky", "lepící páska", "nástěnné hodiny"]
    }
    item = random.choice(items.get(category, []))
    return item


# Hlavní skript pro generování CSV souboru
def generate_csv():
    # Dotazy na uživatele
    num_records = int(input("Zadejte počet záznamů, které chcete generovat: "))
    months_range = int(
        input("Zadejte rozsah měsíců, který chcete zahrnout (např. 12 pro leden 2024 až prosinec 2024): "))
    num_categories = int(input("Zadejte počet kategorií, které chcete přiřazovat (1-10): "))

    # Výběr kategorií
    categories = ["Potraviny", "Drogerie", "Zábava", "Elektro", "Oblečení", "Sport a fitness", "Zahrada a DIY",
                  "Cestování", "Domácí potřeby", "Kancelářské potřeby"]
    selected_categories = random.sample(categories, num_categories)

    # Stanovení počátečního data
    start_date = datetime(2024, 12, 31)  # Začátek období (leden 2024)

    # Cesta k nové složce pro uložení souboru
    folder_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'test')

    # Pokud složka neexistuje, vytvoříme ji
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Cesta pro CSV soubor
    file_path = os.path.join(folder_path, 'nakupy-test.csv')

    # Vytvoření CSV souboru
    with open(file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        # Zápis hlavičky do souboru
        writer.writerow(["Datum", "Položka", "Kategorie", "Množství", "Cena za jednotku", "Celková cena"])

        # Generování záznamů
        for _ in range(num_records):
            category = random.choice(selected_categories)
            item = generate_item(category)
            quantity = random.randint(1, 5)
            unit_price = round(random.uniform(50, 500), 2)
            total_price = round(quantity * unit_price, 2)

            # Generování náhodného data v rámci zadaného rozsahu měsíců
            date = generate_date(start_date, months_range).strftime("%d.%m.%Y")

            # Zápis záznamu
            writer.writerow([date, item, category, quantity, unit_price, total_price])

    print(f"CSV soubor byl úspěšně vygenerován do složky: {file_path}")


# Spuštění generování
generate_csv()
