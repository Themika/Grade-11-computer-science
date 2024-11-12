def sum_numbers(inputs):
    total = 0
    for i in range(len(inputs)):
        total += inputs[i]
    return total

def mean(inputs):
    total = sum(inputs)
    return total/len(inputs)
def median(inputs):
    inputs.sort()
    n = len(inputs)
    if n%2 == 0:
        return (inputs[n//2-1] + inputs[n//2])/2
    else:
        return inputs[n//2]
def mode(inputs):
    inputs.sort()
    n = len(inputs)
    max_count = 0
    mode = inputs[0]
    count = 1
    for i in range(1, n):
        if inputs[i] == inputs[i-1]:
            count += 1
        else:
            if count > max_count:
                max_count = count
                mode = inputs[i-1]
            count = 1
    if count > max_count:
        mode = inputs[n-1]
    return mode
