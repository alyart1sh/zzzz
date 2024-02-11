import requests as r
from Bio import SeqIO
from io import StringIO
import argparse

def save_sequence(ID, content):
    with open(f'{ID}.fasta', 'wb') as file:
        file.write(content)

def request_save(ID):
    Url = "http://www.uniprot.org/uniprot/"
    currentUrl = Url + ID + ".fasta"
    response = r.post(currentUrl)
    if response.status_code == 200:
        cData = ''.join(response.text)
        Seq = StringIO(cData)
        pSeq = list(SeqIO.parse(Seq, 'fasta'))
        save_sequence(ID, response.content)
    else:
        print("Ошибка при запросе. Информации по такому ID нет в базе данных.")

def main(ID=None):
    if ID is None:
        ID = input("Введите ID: ")
    request_save(ID)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Загрузка последовательности белка ID и сохранение её в файле формата FASTA")
    parser.add_argument("-id", "--ID", type=str, help="UniProt ID для загрузки.")
    args = parser.parse_args()

    if args.ID:
        main(args.ID)
    else:
        main()

