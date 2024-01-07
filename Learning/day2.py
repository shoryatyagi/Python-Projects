# Get input from the user
number = int(input("Enter a number: "))

# Check the category of the number and print the corresponding statement
if number < 0:
    print("The number is negative.")
elif number == 0:
    print("The number is zero.")
else:
    print("The number is positive.")
