import PySimpleGUI as sg

class PyGui:
    def SetupWindow(self):
        """
        Sets up windows GUI with tables, inputs, and buttons for playing a bowling game.
        """
        headings = [str(i+1) for i in range(10)]
        table = [[sg.Table(values=[[]],
                        headings=headings,
                        max_col_width=20,
                        auto_size_columns=False,
                        justification='right',
                        num_rows=2,
                        key='-TABLE-',
                        row_height=35)]]
        input = [[sg.Text('Score: '), 
                    sg.Input(key='-SCORE-', do_not_clear=False), 
                    sg.Button('Add'), 
                    sg.Text('Reset: '), 
                    sg.Button('Reset'), 
                    sg.Text('Exit: '), 
                    sg.Button('Exit')]]
        return sg.Window('Bowling Game', table+input)

    def UpdateTable(self, tableWidget, row, numPins, frameScore):
        """
        Updates a single row for the bowling game. 
        *Note: PySimpleGUI doesn't allow for cherry-picking and updating a single row, so we update a list of scores to do so.
        """
        row[0][-1] += numPins
        row[1] = frameScore
        tableWidget.update(values=row)

    def ResetTable(self, tableWidget):
        """
        Resets the bowling game table to a base state.
        """
        tableWidget.update([''], select_rows=[0])

