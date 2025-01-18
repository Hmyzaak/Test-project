import pandas as pd
import os
import chardet

class DataLoader:
    """
    Třída pro načítání a validaci dat z CSV souborů.

    Funkcionalita:
    1. Dynamicky sestavuje cestu k souboru relativní k adresáři 'data'.
    2. Automaticky detekuje kódování CSV souboru.
    3. Načítá data do Pandas DataFrame s kontrolou integrity souboru.
    """

    def __init__(self, file_name: str):
        """
        Inicializuje DataLoader s názvem souboru.

        :param file_name: Název CSV souboru s daty (soubor musí být uložen ve složce 'data').
        """
        self.file_path = os.path.join(os.path.dirname(__file__), "../data", file_name)

    def detect_encoding(self) -> str:
        """
        Detekuje kódování CSV souboru.

        Pomocí knihovny chardet detekuje nejpravděpodobnější kódování souboru.
        Tato metoda je užitečná při práci se soubory s různým nebo neznámým kódováním.

        :return: Řetězec reprezentující detekované kódování (např. 'utf-8', 'windows-1250').
        """
        with open(self.file_path, 'rb') as f:
            result = chardet.detect(f.read())
        return result['encoding']

    def load_data(self) -> pd.DataFrame:
        """
        Při načítání:
        - Kontroluje existenci souboru.
        - Validuje obsah souboru (např. prázdné soubory nebo neplatné znaky).
        - Automaticky použije správné kódování pro dekódování textu.

        :return: Pandas DataFrame obsahující načtená data.
        :raises FileNotFoundError: Pokud soubor neexistuje na dané cestě.
        :raises ValueError: Pokud soubor obsahuje neplatné znaky pro detekované kódování nebo je prázdný.
        :raises pd.errors.EmptyDataError: Pokud je soubor prázdný.
        """
        encoding = self.detect_encoding()
        try:
            data = pd.read_csv(self.file_path, encoding=encoding)
            print(f"Data úspěšně načtena z {self.file_path} s kódováním: {encoding}")
            return data
        except FileNotFoundError:
            raise FileNotFoundError(f"Soubor '{self.file_path}' nebyl nalezen.")
        except UnicodeDecodeError:
            raise ValueError(f"Soubor '{self.file_path}' obsahuje neplatné znaky pro kódování {encoding}.")
        except pd.errors.EmptyDataError:
            raise ValueError(f"Soubor '{self.file_path}' je prázdný.")

    def validate_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Validuje integritu datového rámce.
        Kontroluje chybějící hodnoty a nesprávné datové typy.

        :param df: DataFrame, který má být validován.
        :return: Validovaný DataFrame.
        :raises ValueError: Pokud jsou v datech závažné chyby.
        """
        required_columns = ["Datum", "Položka", "Kategorie", "Množství", "Cena za jednotku", "Celková cena"]

        # Kontrola přítomnosti požadovaných sloupců
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise ValueError(f"Chybějící sloupce: {', '.join(missing_columns)}")

        # Kontrola na chybějící hodnoty
        if df.isnull().any().any():
            raise ValueError("Data obsahují chybějící hodnoty.")

        # Kontrola a konverze datového typu sloupce "Datum"
        if not pd.api.types.is_datetime64_any_dtype(df["Datum"]):
            try:
                # Pokus o konverzi s více formáty a preferencí DD.MM.YYYY
                df["Datum"] = pd.to_datetime(
                    df["Datum"],
                    format=None,  # Automatická detekce formátu
                    dayfirst=True,  # Upřednostnění formátu DD.MM.YYYY
                    errors="coerce"  # Nahrazení neplatných hodnot NaT
                )
                if df["Datum"].isna().any():
                    raise ValueError("Sloupec 'Datum' obsahuje neplatné hodnoty.")
            except Exception:
                raise ValueError("Sloupec 'Datum' neobsahuje validní datové hodnoty.")

        # Kontrola číselného typu ve sloupcích "Množství", "Cena za jednotku" a "Celková cena"
        numeric_columns = ["Množství", "Cena za jednotku", "Celková cena"]
        for col in numeric_columns:
            if not pd.api.types.is_numeric_dtype(df[col]):
                raise ValueError(f"Sloupec '{col}' musí obsahovat číselné hodnoty.")
        # Zamyslet se nad desetinnými čísly (formát '6.1' nebo '6,1' a zvážit zaokrouhlení na celá čísla pro dašlí výpočty)

        print("Data byla úspěšně validována.")
        return df


# Příklad použití
if __name__ == "__main__":
    file_path = "nakupy.csv"  # Konkrétní název souboru (uložen ve složce data)
    loader = DataLoader(file_path)

    try:
        data = loader.load_data()
        validated_data = loader.validate_data(data)
        print(validated_data.head())
    except Exception as e:
        print(f"Chyba: {e}")
