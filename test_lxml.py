import pandas as pd
import lxml

url = "https://www.basketball-reference.com/leagues/NBA_2023_per_game.html"
html = pd.read_html(url, header=0)
df = html[0]
print(df.head())