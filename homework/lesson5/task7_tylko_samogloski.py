zdanie = input("Podaj zdanie: ")

print("Samogłoski w podanym zdaniu: ")

for litera in zdanie:
    if litera.lower() not in "aeiouy": # Jeski to nie spółgłoska, pomiń
        continue
    print(litera)
        