import csv
import pandas as pd
import numpy as np
import re

file_path = r"C:\Users\emirh\PycharmProjects\RealEstimate\data_2019_01_13_2.csv"
file_path_new = file_path.split('.')[0] + "_cleaned" + ".csv"


csv_file = open(file_path, 'r', encoding='utf-8')
df = pd.read_csv(csv_file)
# broj soba
df['Broj soba'] = df['Broj soba'].str.replace("Garsonjera","1").replace("Petosoban i više", 5).str.extract('(\d+)', expand=False)
# broj kvadrata
kvadrata_stanovi_regex = r'(((?<=cc)|(?<=cc\s)|(?<=cca)|(?<=cca\s)|(?<=\~)|(?<=cca)|(?<=oko\s)|(?<=oko))|(?<=^))((\d{2,3})|(\d{2,3},\d{1,2})|(\d{2,6}\.\d{1,2}))((?=\s?\+)|(?=\s?kv)|(?=$)|(?=\s?\()|(?=\s?mÂ²)|(?=\s?qm)|(?=\s?m2)|(?=\s?m$))'
kvadrata_zemljista_regex = r'(((?<=cc)|(?<=cc\s)|(?<=cca)|(?<=cca\s)|(?<=\~)|(?<=cca)|(?<=oko\s)|(?<=oko))|(?<=^))((\d{2,6})|(\d{2,6},\d{1,2})|(\d{2,6}\.\d{1,3})|(\d{1,3}\s?du[n,l]um\w*))((?=\s?\+)|(?=\s?kv)|(?=$)|(?=\s?\()|(?=\s?mÂ²)|(?=\s?qm)|(?=\s?m2)|(?=\s?m$)|(?=\s?metara))'
for i in df.index:
    if df.at[i, 'Kategorija'] != 'Zemljišta' and df.at[i, 'Kategorija'] != 'Poslovni prostori':
        try:
            df.at[i, 'Kvadrata'] = re.search(kvadrata_stanovi_regex, str(df.at[i, 'Kvadrata']), re.IGNORECASE).group(0)
        except AttributeError:
            df.at[i, 'Kvadrata'] = np.nan
    if df.at[i, 'Kategorija'] == 'Zemljišta' or df.at[i, 'Kategorija'] == 'Poslovni prostori':
        try:
            df.at[i, 'Kvadrata'] = re.search(kvadrata_zemljista_regex, str(df.at[i, 'Kvadrata']), re.IGNORECASE).group(0)
            if 'du' in str(df.at[i, 'Kvadrata']):
                df.at[i, 'Kvadrata'] = int(re.search(r"^\d{1,3}", "100 Dunuma", re.IGNORECASE).group(0)) * 1000
        except AttributeError:
            df.at[i, 'Kvadrata'] = np.nan
    if re.search(',\d{3}', str(df.at[i, 'Kvadrata'])):
        df.at[i, 'Kvadrata'] = float(str(df.at[i, 'Kvadrata']).replace(',', '').strip())
    else:
        df.at[i, 'Kvadrata'] = float(str(df.at[i, 'Kvadrata']).replace(',','').strip())
# cijena
df['Cijena'] = df['Cijena'].replace('Po dogovoru', np.nan)
# for i in df.index:
    # if df.at[i, 'Vrsta oglasa'] == 'Prodaja' and df.at[i, 'Kategorija'] != 'Garaže':

