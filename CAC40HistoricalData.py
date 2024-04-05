import os
import yfinance as yf
from datetime import datetime
import pandas as pd

class CAC40HistoricalData:
    """
    Récupère et sauvegarde les données historiques pour une liste de symboles boursiers du CAC 40.

    Attributes:
        tickers_list (list): Liste des symboles boursiers à traiter.
        save_path (str): Chemin du dossier de sauvegarde des fichiers CSV.
    """

    def __init__(self, tickers_list, save_path="."):
        """
        Initialise la classe avec une liste de symboles boursiers et un chemin de sauvegarde.
        
        Args:
            tickers_list (list): Liste des symboles boursiers à récupérer.
            save_path (str): Chemin du dossier où les fichiers CSV seront sauvegardés.
        """
        self.tickers_list = tickers_list
        self.save_path = save_path

    def fetch_data(self, ticker_symbol):
        """
        Récupère les données historiques pour un symbole boursier donné et les renverse pour avoir la date la plus récente en premier.
        
        Args:
            ticker_symbol (str): Le symbole boursier à traiter.
            
        Returns:
            pandas.DataFrame: Un DataFrame contenant les données historiques, triées par date décroissante.
        """
        ticker = yf.Ticker(ticker_symbol)
        data = ticker.history(period="max")
        data.index = data.index.tz_localize(None)
        # Inversion de l'ordre des lignes pour avoir la date la plus récente en premier
        return data


    def save_to_csv(self, data, ticker_symbol):
        """
        Sauvegarde les données dans un fichier CSV, nommé après le symbole boursier.
        
        Args:
            data (pandas.DataFrame): Les données à sauvegarder.
            ticker_symbol (str): Le symbole boursier utilisé pour nommer le fichier.
        """
        filename = f"{ticker_symbol}_Historical_Data.csv"
        filepath = os.path.join(self.save_path, filename)
        data.to_csv(filepath)
        print(f"Saved historical data for {ticker_symbol} in {filepath}")

    def process_and_save_all(self):
        """
        Traite et sauvegarde les données historiques pour tous les symboles boursiers dans la liste.
        """
        for ticker_symbol in self.tickers_list:
            data = self.fetch_data(ticker_symbol)
            self.save_to_csv(data, ticker_symbol)

# Utilisation de la classe
if __name__ == "__main__":
    # Liste des symboles boursiers pour le CAC 40
    tickers = ['AI.PA','AIR.PA','ALO.PA','MT.AS','CS.PA','BNP.PA','EN.PA','CAP.PA','CA.PA','ACA.PA',
               'BN.PA','DSY.PA','EDEN.PA','ENGI.PA','EL.PA','ERF.PA','RMS.PA','KER.PA','OR.PA','LR.PA',
               'MC.PA','ML.PA','ORA.PA','RI.PA','PUB.PA','RNO.PA','SAF.PA','SGO.PA',
               'SAN.PA', 'SU.PA', 'GLE.PA', 'STLAP.PA', 'STMPA.PA', 'TEP.PA', 'HO.PA', 'TTE.PA', 'URW.PA', 'VIE.PA',
               'DG.PA', 'WLN.PA'
               ] 

    # Chemin de sauvegarde (par exemple, "./data")
    save_directory = "./financial_data_lake"
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    cac40_data = CAC40HistoricalData(tickers_list=tickers, save_path=save_directory)
    cac40_data.process_and_save_all()
