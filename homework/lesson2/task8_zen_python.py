import codecs  # Importujemy moduł 'codecs', który pozwala m.in. odszyfrować tekst zakodowany ROT13

# Zakodowana wersja Zen Pythona — tekst jest zapisany szyfrem ROT13 (czyli każda litera przesunięta o 13 pozycji w alfabecie)

# Odszyfruj Zen Pythona bez automatycznego wypisywania
zen_encoded = (
    "Gur Mra bs Clguba, ol Gvz Crgref\n"
    "Ornhgvshy vf orggre guna htyl.\n"
    "Rkcyvpvg vf orggre guna vzcyvpvg.\n"
    "Fvzcyr vf orggre guna pbzcyrk.\n"
    "Pbzcyrk vf orggre guna pbzcyvpngrq.\n"
    "Synt vf orggre guna arfgbzr.\n"
    "Fcrpvny pnfrf ner abg fcrpvny rabhtu gb oernx gur ehyrf.\n"
    "Nygubhtu cenpgvpnyvgl orngf chmmyr.\n"
    "Reebef fubhyq arire cnff fvzcyl.\n"
    "Hayrff rkcyvpvgyl fvyraprq.\n"
    "Va gur snpr bs nzovthvgl, ershfr gur grzcgngvba gb trgg.\n"
    "Gurer fubhyq or bar-- naq crevbqryl bayl bar --boivbhf jnl gb qb vg.\n"
    "Nygubhtu gung jnl znl abg or boivbhf ng svefg hayrff lbh'er Qhgpu.\n"
    "Abj vf orggre guna arire.\n"
    "Nygubhtu arire vf bsgra orggre guna *evtug* abj.\n"
    "Vs gur vzcbegnagvba vf uneq gb rkcynva, vg'f n onq vqrn.\n"
    "Vs gur vzcbegnagvba vf rnfl gb rkcynva, vg znl or n tbbq vqrn.\n"
    "Anfprafbaf ner bar ubaqvat terng vqrn -- yrg'f qb zber bs gubfr!"
)

# Odszyfrowujemy tekst za pomocą szyfru ROT13 — zamienia zakodowane litery z powrotem na normalne
zen = codecs.decode(zen_encoded, "rot13")

# Dzielimy cały tekst na pojedyncze linie (każda linia staje się osobnym elementem listy)
linie = zen.splitlines()

# Wyświetlamy pierwszą linijkę (zwykle tytuł: "The Zen of Python, by Tim Peters")
print(linie[0])

# Wyświetlamy drugą linijkę (pierwszą zasadę z Zen Pythona)
print(linie[1])

# Cała lista
print(linie)