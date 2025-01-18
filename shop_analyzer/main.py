from src.data_loader import DataLoader
from src.analyzer import Analyzer
from src.visualizer import Visualizer
import sys

def main(file_name: str):
    """
    Hlavní funkce aplikace Shop Analyzer.

    :param file_name: Název CSV souboru s daty (soubor musí být uložen ve složce 'data').
    """
    print("\n--- Shop Analyzer ---\n")
    try:
        # Načtení a validace dat
        print("Načítání dat...")
        loader = DataLoader(file_name)
        data = loader.load_data()
        validated_data = loader.validate_data(data)
        print("Data úspěšně načtena a validována.\n")

        # Analýza dat
        print("Provádění analýzy dat...")
        analyzer = Analyzer(validated_data)
        monthly_expenses = analyzer.calculate_monthly_expenses()
        category_analysis = analyzer.analyze_categories()
        top_items = analyzer.get_top_items(n=5)
        print("Analýza úspěšně dokončena.\n")

        # Vizualizace dat
        print("Generování grafů...")
        visualizer = Visualizer()
        visualizer.plot_monthly_expenses(monthly_expenses)
        visualizer.plot_category_distribution(category_analysis)
        visualizer.plot_top_items(top_items)
        print("Grafy byly úspěšně vygenerovány a uloženy.\n")

    except FileNotFoundError:
        print(f"Chyba: Soubor s názvem '{file_name}' nebyl nalezen.")
    except ValueError as e:
        print(f"Chyba: {e}")
    except Exception as e:
        print(f"Neočekávaná chyba: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Použití: python main.py <název_souboru.csv>")
    else:
        file_path = sys.argv[1]
        main(file_path)
