import re

examples = [
    ("Barbora Krejcikova y Elena Rybakina", ['Barbora Krejcikova', 'Elena Rybakina']),
    ("¡PAOLINI ES FINALISTA! Jasmine Paolini con Donna Vekic", ['Jasmine Paolini', 'Donna Vekic']),
    ("WIMBLEDON: Barbora Krejcikova se corona como CAMPEONA tras derrotar a Jasmine Paolini", ['Barbora Krejcikova', 'Jasmine Paolini']),
]


for example in examples:
    """
    Recognize person1 and person2 in a string. Where each person has a name and a surname. Both beggining with a capital letter.
    Exaples:
    - WIMBLEDON: Barbora Krejcikova se corona como CAMPEONA tras derrotar a Jasmine Paolini" -> ['Barbora Krejcikova', 'Jasmine Paolini']
    - "¡PAOLINI ES FINALISTA! Jasmine Paolini con Donna Vekic" -> ['Jasmine Paolini', 'Donna Vekic']
    - "Barbora Krejcikova y Elena Rybakina" -> ['Barbora Krejcikova', 'Elena Rybakina']
    """
    nameAndSurname = r'([A-Z][a-z]+ [A-Z][a-z]+)'
    # match nameAndSurname followed by anything and then nameAndSurname
    pattern = rf'{nameAndSurname}.*{nameAndSurname}'
    match = re.search(pattern, example[0])

    if match:
        name1 = match.group(1)
        name2 = match.group(2)

        print([match.group(i) for i in range(1, 3)])
        assert [name1, name2] == example[1], f"Expected: {example[1]}, got: {name1}, {name2}"
    else:
        print("No match")

