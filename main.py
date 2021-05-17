import nltk
import pandas
import re
from sklearn.metrics import precision_score

# reading excel sheets
CodingDrugs = "CodingDrugs.csv"
BNFNames = "BNFNames.xlsx"
Drug_Drug = "drug-drug.csv"
Drug_Capture = "drug-drug.csv"
field = ['Term']
field2 = ['Drug Names']

# Read from the csv
codingDrugs = pandas.read_csv(CodingDrugs, skipinitialspace=True, usecols=field)
# Read from the BNF Nice database
bnfNames = pandas.read_excel(BNFNames, sheet_name="Sheet1", usecols=field2)
# Read from drug-drug csv
Drug_Drug = pandas.read_csv(Drug_Drug, skipinitialspace=True)

# Single name and Multi-Name Lists
multiNameList = []
tempList = []
newList = []
singleNameList = []

# Filling Medical Corpus
# Getting from BNF Drug names
for numList, drug_names in bnfNames.iterrows():
    # Separating single and multi-words according to the symbols and white spaces
    # Symbols: ' ',',','-','/'
    if ' ' in drug_names[0] \
            or ',' in drug_names[0] or '-' in drug_names[0]:
        multiNameList.append(drug_names[0])
    else:
        singleNameList.append(drug_names[0])

# Getting from Drug-Capture file
for name in Drug_Drug:
    if name not in multiNameList and name not in singleNameList and "Unnamed: 0" not in name:
        if ' ' in name or ',' in name or '-' in name:
            multiNameList.append(name)
        else:
            singleNameList.append(name)

# Split the names in Multi-word list
for drug in multiNameList:
    if ' ' in drug:
        tempList.append(str(drug).split(' '))
    elif '/' in drug:
        tempList.append(str(drug).split('/'))
    elif ',' in drug:
        tempList.append(str(drug).split(','))

# Arrange each into each individual elements
for drug in tempList:
    for sName in drug:
        newList.append(sName)
        # print(drug)


# Tokeninzed each drug names
single_tokenized_sents = [nltk.word_tokenize(i) for i in singleNameList]

multi_tokenized_sents = [nltk.sent_tokenize(i) for i in multiNameList]

newList_tokenized_sents = [nltk.sent_tokenize(i) for i in newList]


# for thing in multi_tokenized_sents:
#     print(thing)
# *****************************************************************************************************************************

singleCount = 0
multipleCount = 0

for index, term in codingDrugs.iterrows():
    for multiName in multi_tokenized_sents:
        if multiName[0].lower() in term[0].lower()\
                and re.search(r'\b%s\b' % multiName[0].lower(), term[0].lower()):

            # extractedNames.add(multiName[0])
            # extractedNames.add(str(index + 1))
            print("Terms: " + term[0])
            print("Extracted Multi-Name: " + multiName[0])
            print("Index row: " + str(index + 1))
            print("\n")
            multipleCount += 1

    for singleName in single_tokenized_sents:
        if singleName[0].lower() in term[0].lower() \
                and re.search(r'\b%s\b' % singleName[0].lower(), term[0].lower()) \
                and singleName[0].lower() not in [j[0].lower() for j in newList_tokenized_sents]:

            # extractedNames.add(singleName[0])
            # extractedNames.add(str(index + 1))

            print("Terms: " + term[0])
            print("Extracted Single Name: " + singleName[0])
            print("Index row: " + str(index + 1))
            print("\n")
            singleCount += 1

print("Single word count: " + str(singleCount))
print("Multi word count: " + str(multipleCount))

