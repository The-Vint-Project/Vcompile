def isEven(number):

    #generate list of even numbers
    evenNumbers=[]
    for i in range((number)):
        evenNumbers.append(i*2)
j
    if number in evenNumbers:
        return True
    else:
        return False

print(isEven(100))