# Ask about height
height = int(input('Enter your height in cm: '))

# Ask if there is a guardian
guardian_input = input('Do you have a guardian? Yes/No: ')

# Change the answer to a Boolean value
has_guardian = guardian_input == 'Yes'

# Entry requirements:
# height of at least 120 cm and a guardian
# or height of at least 160 cm
access_granted = (height >= 120 and has_guardian) or (height >= 160)

print(access_granted)