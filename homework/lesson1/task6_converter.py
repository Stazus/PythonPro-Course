number_dec = int(input('Type decinal number: '))
number_bin = bin(number_dec) # Ob - informacja, że liczba jest w systemie binarnym, funkcja wbudowana bin() informuje w jakim systemie liczbowym jest zapisana liczba
number_hex = hex(number_dec) #Ox - prefix informujący, że liczba jest w systemie szesnastkowym

print(f'Binary: {number_bin}')

print(f'Hexadecimal: {number_hex} ')
