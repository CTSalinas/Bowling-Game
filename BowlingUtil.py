class Util:
    def AddStrikeBonusRolls(self, numPins):
        """
        Since strikes have to wait for two rolls to be calculated, we add those new rolls to the queue.
        """
        for i in range(len(self.strikeQueue)):
            self.strikeQueue[i].append(numPins)

    def CalculateSpare(self, lenRolls, currFrame):
        """
        Calculates the frame score after a spare has occurred. 
        """
        spare = self.spareQueue.popleft()
        spareIndex, spareFrame = spare[0], spare[1]

        if spareFrame == 0:
            self.frameScore[spareFrame] = 10 + self.GetPins(self.rolls, spareIndex+1)
        else:
            self.frameScore[spareFrame] = self.frameScore[spareFrame-1] + 10 + self.GetPins(self.rolls, spareIndex+1)

        if not self.strikeQueue and not self.spareQueue:
            self.frameScore[currFrame] = self.frameScore[currFrame-1] + self.GetPins(self.rolls, lenRolls)

    def CalculateStrike(self, lenRolls, currFrame):
        """
        Calculates the frame score after a strike has occurred.
        """
        strike = self.strikeQueue.popleft()
        strikeFrame = strike[0]
        strikeFirstShot, strikeSecondShot = self.GetPins(strike, 1), self.GetPins(strike, 2)

        if strikeFrame == 0:
            self.frameScore[strikeFrame] = 10 + strikeFirstShot + strikeSecondShot
        else:
            self.frameScore[strikeFrame] = self.frameScore[strikeFrame-1] + 10 + strikeFirstShot + strikeSecondShot
        
        if not self.strikeQueue and not self.spareQueue:
            self.frameScore[currFrame] = self.frameScore[currFrame-1] + self.GetPins(self.rolls, lenRolls) + self.GetPins(self.rolls, lenRolls-1)

    def CheckSpecialRoll(self, currFrame):
        """
        Check if we have a valid "special" roll (strike, spare).
        """
        lenRolls = len(self.rolls)-1

        if self.IsStrike():
            self.frameScore[currFrame] = "Strike!"
            self.rolls.append('_')
            self.strikeQueue.append([currFrame])
        elif self.IsSpare():
            self.frameScore[currFrame] = "Spare!"
            self.spareQueue.append([lenRolls, currFrame])

    def CompleteSpecialRoll(self, currFrame):
        """
        Since special rolls require new rolls to occur, we check to see if a special roll is ready to be calculated.
        """
        lenRolls = len(self.rolls)-1
        if self.SpareIsReady(lenRolls):
            self.CalculateSpare(lenRolls, currFrame)
            return True
        if self.StrikeIsReady(lenRolls):
            self.CalculateStrike(lenRolls, currFrame)
            return True

    def IsSpare(self):
        """
        Check if the roll is a valid spare.
        """
        return self.rolls[-1] == '/' and len(self.rolls) % 2 == 0

    def IsStrike(self):
        """
        Check if the roll is a valid strike.
        """
        return self.rolls[-1].lower() == 'x' and len(self.rolls) % 2 == 1

    def SpareIsReady(self, lenRolls):
        """
        Check if the spare is ready to be calculated after 1 roll.
        """
        if not self.spareQueue:
            return False
        spare = self.spareQueue[0]
        spareIndex = spare[0]
        return lenRolls - spareIndex > 0

    def StrikeIsReady(self, lenRolls):
        """
        Check to see if the strike is ready to be calculated after 2 rolls.
        """
        if not self.strikeQueue:
            return False
        strike = self.strikeQueue[0]
        return len(strike) == 3