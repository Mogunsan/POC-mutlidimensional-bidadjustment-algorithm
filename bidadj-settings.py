import pandas as pd
from pathlib import Path
#This file just generates the settings for xiter.py
mod_path = Path(__file__).parent
csv_path = 'data.csv'

raw_data = [(float(input("Total Conversions: "))),(float(input("Total Cost: "))),(float(input("Phone Conversion Percentage: "))/100),(float(input("Tablet Conversion Percentage: "))/100),(float(input("Desktop Conversion Percentage: "))/100),(float(input("Germany Conversion Percentage: "))/100),(float(input("Netherlands Conversion Percentage: "))/100),(float(input("Phone Cost Percentage: "))/100),(float(input("Tablet Cost Percentage: "))/100),(float(input("Desktop Cost Percentage: "))/100),(float(input("Germany Cost Percentage: "))/100),(float(input("Netherlands Cost Percentage: "))/100),float(input("Iterationstep: ")),int(input("Interations: ")),int(input("Iterationstartingpoint: "))]

df = pd.DataFrame(raw_data)
df.to_csv((mod_path / csv_path).resolve(),mode = 'w' , index = False, encoding='utf-8')
print(df)
print("Done")

# Normally used values in order
# 1234
# 223
# 31
# 7
# 62
# 98
# 2
# 42
# 9
# 49
# 95
# 5