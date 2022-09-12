import BowlingGame
import WindowGui
import PySimpleGUI as sg

def StartGame():
    """
    Starts a bowling game in GUI.
    """
    bowlingGame = BowlingGame.BowlingGame()
    pyGUI = WindowGui.PyGui()

    window = pyGUI.SetupWindow()
    tableWidget = window['-TABLE-']
   
    row = [[],[]]
    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Exit'):
            break
        elif event == 'Add':
            score = values['-SCORE-']

            if not bowlingGame.ValidateRoll(score):
                continue
            bowlingGame.RollBall(bowlingGame.rolls, row, score)

            pyGUI.UpdateTable(tableWidget, row, score, bowlingGame.frameScore)
        elif event == 'Reset':
            pyGUI.ResetTable(tableWidget)
            row = [[], []]
            bowlingGame.ResetGame()

StartGame()