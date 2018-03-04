import pygame

class AntStepVar:
    def __init__(self, minValue, maxValue, startValue=1):
        self.value = startValue
        self.min = minValue
        self.max = maxValue

    def UpdateValue(self, shouldIncrease, step=1):
        if shouldIncrease:
            self.value += step
        else:
            self.value -= step

        if self.value > self.max:
            self.value = self.min
        elif self.value < self.min:
            self.value = self.max

    def GetValue(self):
        return self.value
        