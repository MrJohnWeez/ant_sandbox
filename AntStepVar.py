import pygame

class AntStepVar:
    def __init__(self, minValue, maxValue, startValue=1):
        """Class for incrementing a varible for an ant step"""
        self.value = startValue
        self.min = minValue
        self.max = maxValue
        self.startValue = startValue
    def SetMaxValue(self,value):
        self.max = value

    def UpdateValue(self, shouldIncrease, step=1):
        """Increment the value by the step value up or down"""
        if shouldIncrease:
            self.value += step
        else:
            self.value -= step

        if self.value > self.max:
            self.value = self.min
        elif self.value < self.min:
            self.value = self.max
    def UpdateByString(self, stringValue):
        """Update the value with the given string"""
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
        """Return value of class"""
        return self.value
    
    def SetValue(self, value):
        """Set value of class given an int"""
        self.value = value

    def GetDefault(self):
        """Return the defult starting value for the class"""
        return self.startValue

    def Reset(self):
        """Set the value of class to defualt starting value"""
        self.value = self.startValue

    def GetMin(self):
        return self.min
    def GetMax(self):
        return self.max
        
class AntStepGroup():
    def __init__(self,minValue,maxValue):
        self.up = AntStepVar(minValue,maxValue)
        self.down = AntStepVar(minValue,maxValue)
        self.right = AntStepVar(minValue,maxValue)
        self.left = AntStepVar(minValue,maxValue)
    def SetMaxValue(self, value):
        self.up.SetMaxValue(value)
        self.down.SetMaxValue(value)
        self.right.SetMaxValue(value)
        self.left.SetMaxValue(value)
        
    def GetGroup(self):
        return [self.up, self.down, self.right, self.left]

    def GetGroupValues(self):
        return [x.GetValue() for x in self.GetGroup()]