
"""File allows for easy access to the way ants
move"""

import pygame
import CustomMath

class AntStepVar:
    """Varible class that allows for min/max clamping and string converstion"""
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
        self.value = CustomMath.Clamp(self.value,self.min,self.max)

    def UpdateByString(self, stringValue):
        """Update the value with the given string"""
        if stringValue.isdigit():
            self.value = int(stringValue)
        elif len(stringValue) > 0 and stringValue[0] == "-":
            self.value = self.min
        else:
            self.value = self.startValue
        self.value = CustomMath.Clamp(self.value,self.min,self.max)

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
        """Returns the min value the varible can have"""
        return self.min
        
    def GetMax(self):
        """Returns the max value the varible can have"""
        return self.max
        
class AntStepGroup():
    """A group of antStepVars that allow for quicker access to group functions"""

    def __init__(self,minValue,maxValue):
        self.up = AntStepVar(minValue,maxValue)
        self.down = AntStepVar(minValue,maxValue)
        self.right = AntStepVar(minValue,maxValue)
        self.left = AntStepVar(minValue,maxValue)

    def SetMaxValue(self, value):
        """Sets all the antstepvar max values to the new value entered"""
        self.up.SetMaxValue(value)
        self.down.SetMaxValue(value)
        self.right.SetMaxValue(value)
        self.left.SetMaxValue(value)
        
    def GetGroup(self):
        """Returns the AntstepVar objects of the ant group object"""
        return [self.up, self.down, self.right, self.left]

    def GetGroupValues(self):
        """Returns all the values of the right, left, up, down ant step varibles"""
        return [x.GetValue() for x in self.GetGroup()]