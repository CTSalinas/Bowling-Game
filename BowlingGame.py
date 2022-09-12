from collections import deque
import BowlingUtil
import FrameUtil

class BowlingGame(BowlingUtil.Util, FrameUtil.Util):
    """
    Class for playing a single bowling game.
    """
    def __init__(self):
        self.frameScore = []
        self.rolls = []
        self.bonus = False
        self.bonusRolls = []
        self.strikeQueue = deque()
        self.spareQueue = deque()

    def ResetGame(self):
        """
        Resets the state of the bowling game to a base state.
        """
        self.frameScore = []
        self.rolls = []
        self.bonus = False
        self.bonusRolls = []
        self.strikeQueue = deque()
        self.spareQueue = deque()

    def RollBall(self, rolls, row, numPins):
        """
        Rolls a single ball for the bowling game.
        """
        if self.CheckBonus(row):
            self.bonusRolls.append(numPins)
        rolls.append(numPins)
        self.AddStrikeBonusRolls(numPins)
        self.CalculateFrameScore()
