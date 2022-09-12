import unittest
from BowlingGame import BowlingGame

class GameTest(unittest.TestCase):

    def setUp(self) -> None:
        self.testBowlingGame = BowlingGame()

    def _RollMany(self, pins, num):
        for i in range(num):
            self._RollOne(pins)
    
    def _RollOne(self, pins):
        self.testBowlingGame.RollBall(self.testBowlingGame.rolls, [[], []], pins)
            
    def test_GutterGame(self):
        self._RollMany('0', 20)
        self.assertEqual(0, self.testBowlingGame.frameScore[9])

    def test_AllStrike(self):
        self._RollMany('x', 12)
        self.assertEqual(300, self.testBowlingGame.frameScore[9])
    
    def test_OneStrike(self):
        self._RollOne('x')
        self._RollOne('1')
        self._RollOne('1')
        self._RollMany('0', 16)
        self.assertEqual(14, self.testBowlingGame.frameScore[9])

    def test_OneSpare(self):
        self._RollOne('1')
        self._RollOne('/')
        self._RollOne('1')
        self._RollMany('0', 17)
        self.assertEqual(12, self.testBowlingGame.frameScore[9])

    def test_RegularGame(self):
        rolls = [8, 1, 6, 2, 7, 1, 3, 5, 2, 6, 8, 0, 5, 1, 7, 1, 9, 0, 1, 1]
        for roll in rolls:
            self._RollOne(str(roll))
        self.assertEqual(74, self.testBowlingGame.frameScore[9])

if __name__ == '__main__':
    unittest.main()