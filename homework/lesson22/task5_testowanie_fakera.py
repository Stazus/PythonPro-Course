from faker import Faker

# polskie dane
fake = Faker("pl_PL")

print("10 losowych imion i nazwisk:\n")

for i in range(10):
    print(f"{i+1}. {fake.name()}")

print("\n10 losowych zdań:\n")

for i in range(10):
    print(f"{i+1}. {fake.sentence()}")
