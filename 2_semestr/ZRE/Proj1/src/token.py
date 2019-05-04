

class Token(object):
    def __init__(self, value):
        self.value = value
        self.passedNumbers = []

    def AddPassedNumber(self, number):
        self.passedNumbers.append(number)
