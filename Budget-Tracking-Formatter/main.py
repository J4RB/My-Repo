import csv

path = "/Users/Jacob/OneDrive/Dokumenter/Budget/Kontoudtog/MainKonto-26022021-10072023.csv"
types = {
    'Income': {
        'Løn og pension', 
        'Formueafkast', 
        'Øvrige indtægter'
    },
    'Expenses': {
        'Bolig',
        'Dagligvarer',                                                                   
        'Transport',
        'Tøj, sko og personlig pleje',                                                   
        'Fornøjelser og fritid',                                                         
        'Personforsikringer',
        'Anden gæld',                                                         
        'Øvrige udgifter'
    },
    'Savings': {
        'Pension, opsparing og investering'
        # 'Opsparing',
        # 'Værdipapirkøb',
        # 'Pension'
    }
}

with open(path, newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=';')
    next(reader)
    for row in reader:
        row = [i.strip() for i in row]
        row = [i for i in row if i]
        row = row[:len(row)-3]
        
        # Date
        row[0] = row[0].replace('.', '-')
        
        # Amount
        row[4] = row[4].replace('.', '')
        row[4] = float(row[4].replace(',', '.'))

        # Type
        if row[1] in types['Income']:
            row.insert(1, 'Income')
        elif row[1] in types['Expenses']:
            row.insert(1, 'Expenses')
        elif row[1] in types['Savings']:
            row.insert(1, 'Savings') 
            del row[2]
        elif row[1] == 'Ukategoriseret':
            if row[4] < 0:
                row.insert(1, 'Expenses')
            else:
                row.insert(1, '')
            row[2] = ''
            row[3] = ''
        elif row[1] == 'Opdelt':
            row.insert(1, '')
        else:
            raise Exception("Category, {} , not in types".format(row[1]))
        
        print(row)
        #print(', '.join(row))
