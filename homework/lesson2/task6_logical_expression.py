driving_license = input("Do you have a driving license? (yes/no): ")

age = int(input("How old are you?: "))

can_he_drive = (age >= 18) and (driving_license.lower() == "yes")

print(can_he_drive)