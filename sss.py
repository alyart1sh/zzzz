import requests as r
from Bio import SeqIO
from io import StringIO
import argparse
from typing import Union, BinaryIO

def save_sequence(UI: str, content: Union[bytes, BinaryIO]) -> None:
    with open(f'{UI}.fasta', 'wb') as file:
        file.write(content)

Url = "http://www.uniprot.org/uniprot/"
def request_save(UI):
    currentUrl = Url + UI + ".fasta"
    response = r.post(currentUrl)
    if response.status_code == 200:
        cData = ''.join(response.text)
        Seq = StringIO(cData)
        pSeq = list(SeqIO.parse(Seq, 'fasta'))
        save_sequence(UI, response.content)
    else:
        return

def main(UI=None):
    if UI is None:
        UI = input("Введите ID: ")
    request_save(UI)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Загрузка последовательности белка ID и сохранение её в файле формата FASTA")
    parser.add_argument("-id", "--UI", type=str, help="UniProt ID для загрузки.", required=True)
    args = parser.parse_args()

    if args.UI:
        main(args.UI)
    else:
        main()

