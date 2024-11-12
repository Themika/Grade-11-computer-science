def sales(amount):
    dict = {
        10000: "Superstar Salesperson",
        5000: "Regular Salesperson",   
    }
    if amount >= 10000:
        return dict[10000]
    elif amount >= 5000:
        return dict[5000]
    else:
        return "Improving Salesperson"