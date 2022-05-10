#!/usr/bin/env python3

from fuzzywuzzy import fuzz, process
import pandas as pd
import os

print()
print("Welcome to the Standardizer")
print("")
print("This tool works ONLY with .xls files (for now)")
print()
print()

directory = os.getcwd()
print("This will be the directory where new file will be created:")
print(directory)
print()
print()

basepath = input("Drag and drop base_vgnames.csv here: ")
pricelist = input("Enter path to the pricelist (or drag and drop): ") # take path to the pricelist

base = pd.read_csv(basepath, header=0) # base for the standardizer - vg names from metacritic
pricelist = pd.read_excel(pricelist) # link path to the pandas
name_converter = pricelist.drop(['price', 'quantity', 'supplier'], axis=1)

threshold = 81 # score for game name change

mat1 = [] # empty list for ratio
mat2 = [] # empty list for game names
p = [] # empty list for checks

new_names = name_converter['product_name'].tolist()

# loop that replaces additional info (not relevant) from suppliers so it wont mess up ratio
for i in range(len(new_names)):
    new_names[i] = new_names[i].replace(' PC (Steam)', '')
    new_names[i] = new_names[i].replace(' PC (Origin)', '')
    new_names[i] = new_names[i].replace(' PC (Uplay)', '')
    new_names[i] = new_names[i].replace(' EU', '')
    new_names[i] = new_names[i].replace(' (EUROPE)', '')
    new_names[i] = new_names[i].replace(' (STEAM)', '')
    new_names[i] = new_names[i].replace(' (ROW)', '')
    new_names[i] = new_names[i].replace(' SCAN', '')
    new_names[i] = new_names[i].replace(' (EU)', '')
    new_names[i] = new_names[i].replace(' PC', '')
    new_names[i] = new_names[i].replace(' Standard', '')
        
# list1 = base['game_title'].to_list() # game names from base file to list


for i in new_names:
    mat1.append(process.extractOne(i, base['game_title'], scorer=fuzz.ratio)) # adding ratios to mat1 list
name_converter['matches'] = mat1 # adding ratios to converter

# checking rations based on set treshold
for i in range(len(name_converter['matches'])):
    if name_converter['matches'][i][1] >= threshold:
        p.append(name_converter['matches'][i][0])
    else:
        p.append(new_names[i])
        base.loc[-1] = new_names[i]
    mat2.append(','.join(p))
    p = []

pricelist['product_name'] = mat2

pricelist.to_excel('new_pricelist.xlsx', sheet_name='Pricelist', index=False)
base.to_csv('base_vgnames.csv', index=False)

close = input("press ENTER to close")