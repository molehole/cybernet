

from terminal.models import Etykieta
import csv

with open('scripts/import_file.csv', 'r') as f:
    spamdata = csv.reader(f, delimiter=';')
    for row in spamdata:
        Etykieta.objects.create(nr = row[0], ta = row[1], tura = row[2],  pozycja = row[3], data = row[4], elementy=row[5], element=row[6])
