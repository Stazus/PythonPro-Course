height = int(input('What is your height in cm?: '))

if height < 120:
    print("You can't enter")
elif height < 160:
    is_parent_present = input('Are you with your parents?: ')
    if is_parent_present == 'yes':
        print('You can come in')
    else:
        print("You can't come in")
else:
    print('You can come in')