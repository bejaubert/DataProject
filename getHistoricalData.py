import yfinance as yf
from datetime import datetime
import pandas as pd

class StockHistoricalData:
    def __init__(self, ticker_symbol="TTE.PA"):  # symbole boursier de Total ou peu importe
        self.ticker_symbol = ticker_symbol

    def fetch_data(self):
        # Crée un objet Ticker pour l'action spécifiée
        stock = yf.Ticker(self.ticker_symbol)
        # Récupère toutes les données historiques disponibles
        data = stock.history(period="max")
        # S'assurer que l'index est sans timezone pour éviter les problèmes lors de l'exportation vers Excel
        data.index = data.index.tz_localize(None)
        return data

    def save_to_excel(self, filename="Total_Historical_Data.xlsx"):  # Modifier ici le nom du fichier par défaut
        data = self.fetch_data()
        # Formattez les dates dans un format lisible ('YYYY-MM-DD') avant de sauvegarder
        data.index = data.index.strftime("%Y-%m-%d") # corrige le problème de date en visualisant l'excel
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data['date_modification'] = current_date
        data.to_excel(filename)
        print(f"Les données historiques de l'action Total ont été sauvegardées dans {filename}, avec la date de modification.")

# Utilisation de la classe
if __name__ == "__main__":
    stock_data = StockHistoricalData()
    stock_data.save_to_excel()
