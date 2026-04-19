for i in range(1, 6):
    for j in range(1, 6): # Pętla wewnętrzna działa w całości dla kazdego pojedynczegi i (i=1: j=1,2,3,4,5 itd)
        wynik = i * j
        print(f"{i} * {j} = {wynik}")
    print()