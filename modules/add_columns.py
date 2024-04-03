import pandas as pd
import sys


def aggiungi_colonne_vuote(path_tsv, nuove_colonne):
    # Leggi il file TSV
    df = pd.read_csv(path_tsv, sep="\t")

    # Aggiungi colonne vuote per ogni stringa nella lista
    for colonna in nuove_colonne:
        df[colonna] = ""

    # Salva il DataFrame aggiornato nello stesso file TSV
    df.to_csv(path_tsv, sep="\t", index=False)


# Esempio di utilizzo
if __name__ == "__main__":
    path_file = sys.argv[1]
    nuove_colonne = input(
        "Inserisci le stringhe separate da virgole per le nuove colonne: "
    ).split(",")

    aggiungi_colonne_vuote(path_file, nuove_colonne)
    print("Colonne vuote aggiunte con successo.")
