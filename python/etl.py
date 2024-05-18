from datetime import datetime
import pandas as pd
import numpy as np
import sys


# tableau pour la récupération des erreurs
type_error = []

def check_legal_characters(df):
    # Vérification des caractères légaux pour la colonne 'Date'
    global type_error
    try:
        pd.to_datetime(df['Date'])
        print("'Date': OK")
    except ValueError:
        print("'Date': PAS OK")
        type_error += [f"'Date' format"]

    # Vérification des caractères légaux pour toutes les autres colonnes
    for column in df.columns:
        if column not in ('Date','date_modification'):
            if df[column].str.match(r'^-?\d*\.?\d*$').all():
                print(f"'{column}': OK")
            else:
                print(f"'{column}': PAS OK")
                type_error += [f"'{column}' format"]
# Utilisation de la fonction pour vérifier le dataframe


     
     
def recast_columns(df):
    # Recast de la colonne 'Date'
    df['Date'] = pd.to_datetime(df['Date'])

    # Recast des autres colonnes
    for column in df.columns:
        if column != 'Date':
            if column in ['Open', 'High', 'Low', 'Close']:
                df[column] = pd.to_numeric(df[column])
            elif column == 'Volume':
                df[column] = df[column].astype(int)
            elif column in ['Dividends', 'Stock Splits']:
                df[column] = df[column].astype(float)
            elif column == 'date_modification':
                df[column] = pd.to_datetime(df[column])
    return df
# Utilisation de la fonction pour recaster le dataframe

print('casting ok')

def filter_aberrant_values(df):
    # Initialiser un dataframe pour stocker les lignes non valides
    global type_error
    df_invalid = pd.DataFrame(columns=df.columns)

    # Filtrer les valeurs négatives dans les colonnes de prix
    price_columns = ['Open', 'High', 'Low', 'Close']
    invalid_price_rows = df[(df[price_columns] < 0).any(axis=1)]
    df_invalid = pd.concat([df_invalid, invalid_price_rows])
    df = df[~df.index.isin(invalid_price_rows.index)]

    # Filtrer les dates avant la création du CAC 40 (date de début : 31 décembre 1987)
    invalid_date_rows = df[df['Date'] < '1987-12-31']
    df_invalid = pd.concat([df_invalid, invalid_date_rows])
    df = df[~df.index.isin(invalid_date_rows.index)]

    # Filtrer les dates supérieures à la date actuelle
    current_date = np.datetime64(datetime.now().date())
    invalid_future_date_rows = df[df['Date'] > current_date]
    df_invalid = pd.concat([df_invalid, invalid_future_date_rows])
    df = df[~df.index.isin(invalid_future_date_rows.index)]

    # Autres filtres spécifiques aux données financières peuvent être ajoutés ici
    if invalid_date_rows.shape[0] > 0 or invalid_future_date_rows.shape[0] > 0:
        type_error += ['Date val']

    if invalid_price_rows.shape[0] > 0:
        type_error += ['Num val']
        
    return df, df_invalid

# Appliquer les filtres


# Importation temporaire du flux
df = pd.read_csv('ACA.PA_Historical_Data.csv')

# Selection de la ligne la plus récente 
df = df.iloc[-1].to_frame().T

# Cast en string pour éviter tous problèmes de formats
df = df.astype(str)



check_legal_characters(df)


if len(type_error) != 0:
     errors = ', '.join(type_error)
     df_unvalid = df
     df_unvalid['type_error'] = errors
     sys.exit()

df = recast_columns(df)

df, df_invalid = filter_aberrant_values(df)
if df_invalid.shape[0] == 0:
     errors = ', '.join(type_error)
     df_unvalid = df_invalid
     df_unvalid['type_error'] = errors
     sys.exit()