import pygame

class AntStepVar:
    def __init__(self, minValue, maxValue, startValue=1):
        self.value = startValue
        self.min = minValue
        self.max = maxValue
        self.startValue = startValue

    def UpdateValue(self, shouldIncrease, step=1):
        if shouldIncrease:
            self.value += step
        else:
            self.value -= step

        if self.value > self.max:
            self.value = self.min
        elif self.value < self.min:
            self.value = self.max
    def UpdateByString(self, stringValue):
        if stringValue.isdigit():
            self.value = int(stringValue)
        elif len(stringValue) > 0 and stringValue[0] == "-":
            self.value = self.min
        else:
            self.value = self.startValue
        
        if self.value > self.max:
            self.value = self.max
        elif self.value < self.min:
            self.value = self.min

    def GetValue(self):
        return self.value
        