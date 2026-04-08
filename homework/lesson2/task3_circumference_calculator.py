while True: # Loop to load correct length
    try:
        length = float(input("Type the length of the rectangle: "))
        break
    except ValueError:
        print("Please enter a valid number for the length. Please try again.")
        
while True: # Loop to load correct width
    try:
        width = float(input("Type the width of the rectangle: "))
        break
    except ValueError:
        print("Please enter a valid number for the width. Please try again.")
        
perimeter_of_a_rectangle = 2 * (length + width)

print(f"The perimeter of the rectangle is: {perimeter_of_a_rectangle}")