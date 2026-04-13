waga = float(input("Podaj swoją wagę w kilogramach: "))
wzrost = float(input("Podaj swój wzrost w metrach: "))

bmi = waga / (wzrost * wzrost)

print(f"Twoje BMI wynosi: {bmi:.2f}") # .2f - formatowanie liczby zmiennoprzecinkowej (float) do dwóch miejsc po przecinku