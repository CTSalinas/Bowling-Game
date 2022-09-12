import PySimpleGUI as sg

class Util:
    valid = ['x', 'X', '/', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    validX = ['x', 'X']

    def CalculateFrameScore(self):
        """
        Uses rolls to calculate previous frames (due to a strike or spare) and current frames.
        """
        lenRolls = len(self.rolls)-1
        currFrame = self.GetFrame(lenRolls)

        self.CheckSpecialRoll(currFrame)
        if self.CompleteSpecialRoll(currFrame):
            return

        if self.strikeQueue or self.spareQueue:
            return

        self.FinalizeFrameScore(currFrame)

    def CheckBonus(self, row):
        """
        Check to see if we have bonus rolls for the last frame of a bowling game.
        """
        if len(self.rolls) % 2 == 0 and not self.bonus:
                row[0].append([])
        if self.bonus == True or len(self.rolls) == 18:
                self.bonus = True
                return True
        return False

    def FinalizeFrameScore(self, currFrame):
        """
        Finishes the frame score for the current frame being checked.
        """
        lenRolls = len(self.rolls)-1
        if lenRolls % 2 == 0 and currFrame > 0:
            self.frameScore[currFrame] = self.GetPins(self.rolls, lenRolls) + self.frameScore[currFrame-1]
        elif lenRolls % 2 == 0:
            self.frameScore[currFrame] = self.GetPins(self.rolls, lenRolls)
        elif lenRolls % 2 == 1:
            self.frameScore[currFrame] += self.GetPins(self.rolls, lenRolls)

    def GetFrame(self, lenRolls):
        """
        Gets or creates a frame to be used for calculating.
        """
        if lenRolls % 2 == 0:
            self.frameScore.append('Calculating...')
        return len(self.frameScore)-1

    def GetPins(self, rolls, index):
        """
        Returns a certain (0-10) amount of pins based off of valid input.
        """
        if rolls[index] in Util.validX:
            return 10
        elif rolls[index] == '/':
            return 10-int(rolls[-2])
        else:
            return int(rolls[index])

    def ValidateRoll(self, val):
        """
        Validates rolls based on player input.
        TODO: Research PySimpleGUI on how the GUI package handles exceptions. Exceptions are preferred here!
        TODO: Move 'Game Over' logic to a separate method for cleanliness.
        """
        if val not in Util.valid:
            sg.Print("Incorrect input for pins. Valid input is x, /, and numbers 0-9.")
            return False

        if self.bonus:
            if (len(self.bonusRolls) == 0 or self.bonusRolls[-1] in Util.validX or self.bonusRolls[-1] == '/')  and val == '/':
                sg.Print("Spare isn't possible on the first roll and you can't roll a spare after a strike or spare. Try again.")
                return False
            if len(self.bonusRolls) > 0 and self.bonusRolls[-1].isnumeric() and val == 'x':
                sg.Print("Strike isn't possible after a knocking down 0-9 pins.")
                return False
            if len(self.bonusRolls) > 0 and val != '/' and val not in Util.validX and (self.bonusRolls[-1].isnumeric() == True) and (self.GetPins(self.bonusRolls, -1) + int(val) > 9):
                sg.Print("Invalid amount of pins. Remaining amount of pins must be up to 9 or be a spare.")
                return False
            if len(self.bonusRolls) == 2 and 'x' not in self.bonusRolls and 'X' not in self.bonusRolls and '/' not in self.bonusRolls:
                sg.Print("No bonus rolls were earned. Game over! Press restart to play a new game.")
                return False
            if len(self.bonusRolls) >= 3:
                sg.Print("No bonus rolls left. Game over! Press restart to play a new game.")
                return False
        else:
            if len(self.rolls) % 2 == 0 and val == '/':
                sg.Print("Spare isn't possible on the first roll. Try again.")
                return False
            if len(self.rolls) % 2 == 1 and val in Util.validX:
                sg.Print("Strike isn't possible on the second roll. Try again.")
                return False
            if len(self.rolls) % 2 == 1 and len(self.rolls) > 0 and val != '/' and (int(self.rolls[-1]) + int(val) > 9):
                sg.Print("Invalid amount of pins. Remaining amount of pins must be up to 9 or be a spare.")
                return False
        return True