number_one = float(input('Type the first number: '))
number_two = float(input('Type the second number: '))
operator = input('type operator (+, -, *, /): ')

if operator == '+':
    result = number_one + number_two
    print(result)
    
elif operator == '-':
    result = number_one - number_two
    print(result)
    
elif operator == '*':
    result = number_one * number_two
    print(result)
    
elif operator == '/':
    if number_two == 0:
        print("Don't divide by 0!")
    else:
        result = number_one / number_two
        print(result)
        
else:
    print('Something else')