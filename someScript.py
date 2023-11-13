import random

from db.models import User, Kandidaten, Stimmzettel, Stimmkreis
from db.session import get_db
import pandas as pd

parteien = ['CSU',
            'GRÜNE',
            'FREIE WÄHLER',
            'AfD',
            'SPD',
            'FDP',
            'DIE LINKE',
            'BP',
            'ÖDP',
            'Die PARTEI',
            'Tierschutzpartei',
            'V-Partei³',
            'PdH',
            'dieBasis',
            'Volt',
            'PIRATEN',
            'DIE FRANKEN',
            'LKR',
            'mut',
            'Gesundheitsforschung']

path = "C:/Users/daydo/Downloads/08_10_2023_Landtagswahl_2023_Stimmkreise_Bayern.csv"


def create_kandidaten():
    # Reading the CSV file
    df = pd.read_csv(path, encoding='latin1', sep=';')
    df = pd.DataFrame(df)
    df = df.rename(columns={'Parteiname': 'Parteiname.0'})

    for key in df.keys():
        print(key)
    kandidaten = []
    for index, row in df.iterrows():
        print(row['Name der Regionaleinheit'], end=", ")
        for partei, indexx in zip(parteien, range(len(parteien))):
            try:
                if row['Bewerber ' + partei] != '-':
                    print(f"{partei}: = {row['Bewerber ' + partei]}", end=", ")
                    kandidat: Kandidaten = Kandidaten(Vorname=row['Bewerber ' + partei].split(', ')[1],
                                                      Nachname=row['Bewerber ' + partei].split(', ')[0],
                                                      ParteiID=indexx + 1,
                                                      StimmkreisId=row['Schlüsselnummer'],
                                                      )
                    kandidaten.append(kandidat)

            except Exception:
                pass
        print()
    for kandidat in kandidaten:
        print(kandidat.Vorname)
    with get_db() as db:
        db.add_all(kandidaten)
        db.commit()


def get_kandidaten(stimmkreis_id, partei_id) -> Kandidaten:
    with get_db() as db:
        return db.query(Kandidaten).filter(
            Kandidaten.StimmkreisId == stimmkreis_id, Kandidaten.ParteiID == partei_id).one()


def get_kandidaten_id_random_from_the_wahlkreis(stimmkreis_id, partei_id) -> Kandidaten:
    with get_db() as db:
        wahlkreis_id = db.query(Stimmkreis).filter(Stimmkreis.StimmkreisId == stimmkreis_id).one().WahlkreisId
        kandidaten = db.query(Kandidaten).join(Stimmkreis).filter(
            Stimmkreis.WahlkreisId == wahlkreis_id, Kandidaten.ParteiID == partei_id).all()
        return random.choice(kandidaten)


def generate_stimmzettel_for_stimmkreis(stimmkreis_id: int):
    # Reading the CSV file
    df = pd.read_csv(path, encoding='latin1', sep=';')
    df = pd.DataFrame(df)
    df = df.rename(columns={'Parteiname': 'Parteiname.0'})

    # for key in df.keys():
    #     print(key)
    stimmzettel: list[Stimmzettel] = []
    for index, row in df.iterrows():
        if row['Schlüsselnummer'] == stimmkreis_id:
            stimmzettel = [Stimmzettel() for i in range(int(row['Wähler']))]
            erstimme_index = 0
            zweitstimme_index = 0
            for partei, indexx in zip(parteien, range(len(parteien))):
                try:

                    # generate erststimmen
                    if row['Bewerber ' + partei] != '-':
                        kandidate_id_from_the_stimmkreis = get_kandidaten(stimmkreis_id, indexx + 1).KandidatID
                        print(type(row[f'Erststimmen {partei} 2023']))
                        print(row[f'Erststimmen {partei} 2023'])
                        print('-')

                        for j in range(int(row[f'Erststimmen {partei} 2023'])):
                            stimmzettel[erstimme_index + j].Erstestimme = kandidate_id_from_the_stimmkreis
                        erstimme_index += int(row[f'Erststimmen {partei} 2023'])

                    # generate zweitstimmen
                    kandidate_id_from_the_wahlkreis = get_kandidaten_id_random_from_the_wahlkreis(stimmkreis_id,
                                                                                                  indexx + 1).KandidatID

                    for j in range(int(row[f'Zweitstimmen {partei} 2023'])):
                        stimmzettel[zweitstimme_index + j].Zweitstimme = kandidate_id_from_the_wahlkreis
                    zweitstimme_index += int(row[f'Zweitstimmen {partei} 2023'])
                except Exception:
                    pass
            print(len(stimmzettel))
            with get_db() as db:
                for stz in stimmzettel:
                    stz.Jahr = 2023
                db.add_all(stimmzettel)
                db.commit()


# create_kandidaten():

generate_stimmzettel_for_stimmkreis(131)
