import csv

try:
    with open('students.csv', 'r',encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader) #pierwszy wiersz to nazwy kolumn
        print(f"nagłówki: {header}")
        print("_"*70)
        for row in reader:
            name = row[0]
            surname = row[1]
            points = int(row[2])

            print(f"Student: {name} {surname} -> punkty: {points}")
            print("_"*40)

except FileNotFoundError:
    print("Nie znaleziono pliku")
except ValueError:
    print("błąd konwersji danych")
