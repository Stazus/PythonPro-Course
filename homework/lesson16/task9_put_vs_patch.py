# Zasób znajdujący się na serwerze:

# {
#     "name": "Katarzyna",
#     "email": "k.nowak@example.com",
#     "city": "Warszawa"
# }

# PUT - zastępuje cały zasób

put_request_body = {
    "name": "Kasia",
    "email": "k.nowak@example.com",
    "city": "Warszawa"
}

# PATCH - aktualizuje tylko wskazane pola

patch_request_body = {
    "name": "Kasia"
}

print("PUT:")
print(put_request_body)

print("\nPATCH:")
print(patch_request_body)

# Wyjaśnienie:
#
# PUT wymaga przesłania całego zasobu, nawet jeśli zmienia się tylko jedno pole.
#
# PATCH przesyła wyłącznie pola, które mają zostać zmienione.
#
# PATCH jest bardziej oszczędny pod względem ilości przesyłanych danych,
# ponieważ nie trzeba wysyłać całego obiektu.