import pandas as pd

datas ={
"name": ["Ajay", "Balaji", "Shiva"],
"marks": [80, 78, 56],
"age": [21, 23, 22]
}

df =pd.DataFrame(datas)
df["marks"] = df.loc["marks"]>60
print(df["marks"])
