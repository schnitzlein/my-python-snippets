import pandas as pd

file_name = "mein_Dateiname.xlsx"

xl_file = pd.ExcelFile(file_name)

dfs = {sheet_name: xl_file.parse(sheet_name) for sheet_name in xl_file.sheet_names}
#print(dfs)

print(dfs['Tabellenblatt1']['Essen'])