import requests as r
from Bio import SeqIO
from io import StringIO

ID=input()

Url="http://www.uniprot.org/uniprot/"
currentUrl=Url+ID+".fasta"
response = r.post(currentUrl)
cData=''.join(response.text)
Seq=StringIO(cData)
pSeq=list(SeqIO.parse(Seq,'fasta'))

with open(f'{ID}.fasta', 'wb') as file:
    file.write(response.content)
