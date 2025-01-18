import pandas as pd


class Analyzer:
    """
    Třída pro analýzu dat načtených z CSV souboru.
    Poskytuje metody pro výpočet statistických a analytických hodnot.
    """

    def __init__(self, data: pd.DataFrame):
        """
        Inicializuje Analyzer s validovaným DataFrame.

        :param data: Validovaný DataFrame obsahující data k analýze.
        """
        self.data = data

    def calculate_monthly_expenses(self) -> pd.DataFrame:
        """
        Spočítá celkové měsíční výdaje.

        :return: DataFrame s měsíčními výdaji (měsíc a celkové výdaje).
        """
        self.data["Month"] = self.data["Datum"].dt.to_period("M")
        monthly_expenses = (self.data.groupby("Month")
                            ["Celková cena"].sum()
                            .reset_index()
                            .rename(columns={"Celková cena": "Měsíční výdaje"}))
        print("Měsíční výdaje byly vypočítány.")
        return monthly_expenses

    def get_top_items(self, n: int = 5) -> pd.DataFrame:
        """
        Získá nejčastěji nakupované položky.

        :param n: Počet nejčastějších položek (výchozí 5).
        :return: DataFrame s názvy položek a počtem jejich výskytů.
        """
        top_items = (self.data.groupby("Položka")
                     ["Množství"].sum()
                     .sort_values(ascending=False)
                     .head(n)
                     .reset_index()
                     .rename(columns={"Množství": "Celkový počet"}))
        print(f"Top {n} položek bylo identifikováno.")
        return top_items

    def analyze_categories(self) -> pd.DataFrame:
        """
        Analyzuje rozložení výdajů podle kategorií.

        :return: DataFrame s kategoriemi a jejich celkovými výdaji.
        """
        category_analysis = (self.data.groupby("Kategorie")
                              ["Celková cena"].sum()
                              .reset_index()
                              .rename(columns={"Celková cena": "Celkové výdaje"}))
        print("Výdaje podle kategorií byly analyzovány.")
        return category_analysis

# Příklad použití
if __name__ == "__main__":
    from data_loader import DataLoader  # Import DataLoader z předchozího kódu

    # Načtení a validace dat
    file_path = "nakupy.csv"  # Konkrétní název souboru (uložen ve složce data)
    loader = DataLoader(file_path)

    try:
        data = loader.load_data()
        validated_data = loader.validate_data(data)

        # Analýza dat
        analyzer = Analyzer(validated_data)

        monthly_expenses = analyzer.calculate_monthly_expenses()
        print(monthly_expenses)

        top_items = analyzer.get_top_items(n=5)
        print(top_items)

        category_analysis = analyzer.analyze_categories()
        print(category_analysis)

    except Exception as e:
        print(f"Chyba: {e}")
