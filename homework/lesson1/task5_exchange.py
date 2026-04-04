amount_pln = float(input('Amount in PLN to convert USD: ')) # podaj kwotę złotówek do przeliczenia na dolary
exchange_rate = 4.0 # kurs wymiany
amount_usd = amount_pln / exchange_rate # przeliczenie złotówek na dolary

print(f'Amount in USD: {amount_usd}')
