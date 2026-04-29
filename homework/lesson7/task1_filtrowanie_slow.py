slowa = ["jabłko", "banan", "kiwi", "gruszka", "truskawka"]

dlugie_slowa = [s for s in slowa if len(s) > 5]

print("Słowa zawierające więcej niz 5 liter: ", dlugie_slowa)