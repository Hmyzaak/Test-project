import matplotlib.pyplot as plt
import pandas as pd
import os
from datetime import datetime

class Visualizer:
    """
    Třída pro vizualizaci dat.
    Poskytuje metody pro tvorbu různých typů grafů a jejich ukládání do souborů.
    """

    def __init__(self, output_dir: str = "output/reports"):
        """
        Inicializuje Visualizer s výstupním adresářem pro ukládání grafů.

        :param output_dir: Adresář pro ukládání vygenerovaných grafů (výchozí: "output/reports").
        """
        self.output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), output_dir)
        os.makedirs(self.output_dir, exist_ok=True)

    def _generate_file_name(self, base_name: str) -> str:
        """
        Vygeneruje název souboru s časovou značkou.

        :param base_name: Základní název souboru.
        :return: Název souboru s časovou značkou a příponou PNG.
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{base_name}_{timestamp}.png"

    def plot_monthly_expenses(self, monthly_expenses: pd.DataFrame):
        """
        Vytvoří a uloží sloupcový graf měsíčních výdajů.

        :param monthly_expenses: DataFrame s měsíčními výdaji (obsahuje sloupce "Month" a "Měsíční výdaje").
        """
        plt.figure(figsize=(10, 6))
        plt.bar(monthly_expenses["Month"].astype(str), monthly_expenses["Měsíční výdaje"], color="skyblue")
        plt.title("Měsíční výdaje", fontsize=16)
        plt.xlabel("Měsíc", fontsize=12)
        plt.ylabel("Výdaje (Kč)", fontsize=12)
        plt.xticks(rotation=45)
        plt.tight_layout()
        file_name = self._generate_file_name("monthly_expenses")
        file_path = os.path.join(self.output_dir, file_name)
        plt.savefig(file_path)
        plt.close()
        print(f"Graf měsíčních výdajů byl uložen do {file_path}.")

    def plot_category_distribution(self, category_analysis: pd.DataFrame):
        """
        Vytvoří a uloží koláčový graf rozdělení výdajů podle kategorií.

        :param category_analysis: DataFrame s kategoriemi a jejich výdaji (obsahuje sloupce "Kategorie" a "Celkové výdaje").
        """
        plt.figure(figsize=(8, 8))
        plt.pie(category_analysis["Celkové výdaje"], labels=category_analysis["Kategorie"],
                autopct="%1.1f%%", startangle=90, colors=plt.cm.Paired.colors)
        plt.title("Rozložení výdajů podle kategorií", fontsize=16)
        plt.tight_layout()
        file_name = self._generate_file_name("category_distribution")
        file_path = os.path.join(self.output_dir, file_name)
        plt.savefig(file_path)
        plt.close()
        print(f"Koláčový graf výdajů podle kategorií byl uložen do {file_path}.")

    def plot_top_items(self, top_items: pd.DataFrame):
        """
        Vytvoří a uloží sloupcový graf nejčastěji nakupovaných položek.

        :param top_items: DataFrame s nejčastějšími položkami (obsahuje sloupce "Položka" a "Celkový počet").
        """
        plt.figure(figsize=(10, 6))
        plt.bar(top_items["Položka"], top_items["Celkový počet"], color="lightgreen")
        plt.title("Top položky podle množství", fontsize=16)
        plt.xlabel("Položka", fontsize=12)
        plt.ylabel("Počet", fontsize=12)
        plt.xticks(rotation=45)
        plt.tight_layout()
        file_name = self._generate_file_name("top_items")
        file_path = os.path.join(self.output_dir, file_name)
        plt.savefig(file_path)
        plt.close()
        print(f"Graf nejčastěji nakupovaných položek byl uložen do {file_path}.")

# Příklad použití
if __name__ == "__main__":
    from data_loader import DataLoader
    from analyzer import Analyzer

    # Načtení a validace dat
    file_path = "nakupy.csv"  # Konkrétní název souboru (uložen ve složce data)
    loader = DataLoader(file_path)

    try:
        data = loader.load_data()
        validated_data = loader.validate_data(data)

        # Analýza dat
        analyzer = Analyzer(validated_data)
        monthly_expenses = analyzer.calculate_monthly_expenses()
        category_analysis = analyzer.analyze_categories()
        top_items = analyzer.get_top_items(n=5)

        # Vizualizace dat
        visualizer = Visualizer()
        visualizer.plot_monthly_expenses(monthly_expenses)
        visualizer.plot_category_distribution(category_analysis)
        visualizer.plot_top_items(top_items)

    except Exception as e:
        print(f"Chyba: {e}")
