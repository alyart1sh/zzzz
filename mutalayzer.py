import requests

base_url = "https://mutalyzer.nl/api/normalize/"
variant = input("Введите вариант мутации : ")
url = base_url + variant + "?sequence=" + variant + "&only_variants=false"

response = requests.get(url)

if response.status_code == 200:

    data = response.json()
    reference_sequence = data["protein"]["reference"]
    predicted_sequence = data["protein"]["predicted"]
    description = data["protein"]["description"].replace(":", "_").replace(".", "_")


    with open("reference_sequence_" + description + ".fasta", "w") as f:
        f.write(">Reference sequence\n")
        f.write(reference_sequence)

    with open("predicted_sequence_" + description + ".fasta", "w") as f:
        f.write(">Predicted sequence\n")
        f.write(predicted_sequence)

    with open("combined_sequences_" + description + ".fasta", "w") as f:
        f.write(">Reference sequence\n")
        f.write(reference_sequence)
        f.write("\n>Predicted sequence\n")
        f.write(predicted_sequence)

    print("Последовательности успешно загружены.")
else:
    print("Ошибка при загрузке последовательностей. Код состояния:", response.status_code)
