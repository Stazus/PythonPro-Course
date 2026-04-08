name = input("What's your name?: ")

while True:
    try:
        age = int(input("How old are you?: "))
        break
    except ValueError:
        print("Age must be a number! Please try again.")
        
city = input("What city do you live in?: ")

print(f"So, your name is {name}, you are {age} years old and you live in {city}.")