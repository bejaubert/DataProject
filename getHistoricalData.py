import yfinance as yf
import pandas as pd
from datetime import datetime
import openpyxl 

class CAC40HistoricalData:
    def __init__(self, ticker_symbol="^FCHI"):
        self.ticker_symbol = ticker_symbol

    def fetch_data(self):
        # Crée un objet Ticker pour le CAC 40
        cac40 = yf.Ticker(self.ticker_symbol)
        # Récupère toutes les données historiques disponibles
        data = cac40.history(period="max")
        # Assurez-vous que l'index est sans timezone pour éviter les problèmes lors de l'exportation vers Excel
        data.index = data.index.tz_localize(None)
        return data

    def save_to_excel(self, filename="CAC40_Historical_Data.xlsx"):
        data = self.fetch_data()
        # Obtient la date actuelle
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # Ajoute une colonne 'date_modification' avec la date actuelle pour chaque ligne
        data['date_modification'] = current_date
        data.to_excel(filename)
        print(f"Les données historiques du CAC 40 ont été sauvegardées dans {filename}, avec la date de modification.")

# Utilisation de la classe
if __name__ == "__main__":
    cac40_data = CAC40HistoricalData()
    cac40_data.save_to_excel()