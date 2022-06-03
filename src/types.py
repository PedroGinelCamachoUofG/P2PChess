


def checkNumber(coordinates):
    if (coordinates[0] > 9) or (coordinates[1] > 9) or (coordinates[0] < 1) or (coordinates[1] < 1):
        return False
    else:
        return True

def diagonal(coordinates):
        condition = True
        output = []
        copy = coordinates
        while condition:
            coordinates[0] = coordinates[0] + 1
            coordinates[1] = coordinates[1] + 1
            if checkNumber(coordinates):
                output.append(coordinates)
                print(output)
            else:
                condition = False
        for num in range(0,9):
            coordinates[0] = coordinates[0] - 1
            coordinates[1] = coordinates[1] - 1
            if checkNumber(coordinates):
                output.append(coordinates)
            else:
                break
        return output

def test(gay):
    d = []
    for num in range(0,10):
        gay[1] = gay[1] + 1
        if checkNumber(gay):
            d.append(gay)
    return d

print(test([1,3]))