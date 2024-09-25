def get_positive_integer(prompt):
    while True:
        try:
            value = int(input(prompt))
            if value >= 0:
                return value
            else:
                print("ERROR: Enter a positive integer value.")
        except ValueError:
            print("ERROR: Enter a valid positive integer.")