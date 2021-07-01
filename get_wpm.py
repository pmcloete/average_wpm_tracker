import math
import json
import os
import datetime
import PySimpleGUI as sg
from statistics import mean


class AverageCalculator():

    #  Construction
    def __init__(self):
        """Will accept integer input from 0 to 299. The average of those 
        numbers are calculated using math.ceil() and then displayed to the user.
        When the user quits the program, the values are automatically stored in
        the same directory as the file."""
        #  Button Attributes
        self.button_add_score = 'Add Score'
        self.button_quit = 'Quit'
        self.button_clear = 'Clear Scores'
        self.button_create_backup = 'Create Backup'
        self.button_load_backup = 'Load Backup'
        self.size_button = 12, 1
        self.color_button = '#6C6C6C'

        #  Default Filename
        self.filename = 'words_per_minute.json'

        #  UX Elements
        self.font = 'Helvetica'

        #  Module Imports and implementations
        self.os = os
        self.datetime = datetime
        self.get_mean = mean
        self.gui = sg

        #  App theme
        self.theme = self.gui.theme('Dark')

        #  Create a date to use as the key in the data dictionary
        self.now = self.datetime.datetime.now()
        self.date = self.now.strftime("%m %d %y")

        #  Initialize the data
        self.data = self._load_file()

        #  Set the average of the data
        self.current_average = self._get_average()

        #  App Layout
        self.layout = [
            [self.gui.Text('Average: ' + (str(self.current_average) + ' WPM'),
                           size=(20, 1),
                           justification='left', font=(self.font, 25),
                           key='-AVERAGE-')
             ], [self.gui.Text('Add Scores:', font=(self.font, 15)),
                 self.gui.InputText(key='wpm', font=(self.font, 15)),
                 self.gui.Button(self.button_add_score, font=(self.font, 15),
                                 button_color=self.color_button)
                 ], [
                self.gui.Button(self.button_create_backup,
                                size=(self.size_button), font=(self.font, 15),
                                button_color=self.color_button),
                self.gui.Button(self.button_load_backup,
                                size=(self.size_button), font=(self.font, 15),
                                button_color=self.color_button),
            ], [
                self.gui.Button(self.button_clear, size=(self.size_button),
                                font=(self.font, 15),
                                button_color=self.color_button),
                self.gui.Button(self.button_quit, size=(self.size_button),
                                font=(self.font, 15),
                                button_color=self.color_button)
            ], [
                self.gui.Text('© Peter Inc. 2021', pad=(6, 2), font=(
                    self.font, 10), justification='left')
            ]
        ]

        #  Create the App window
        self.window = self.gui.Window('Average WPM Calculator', self.layout,
                                      return_keyboard_events=True)

    def main(self):
        """A program to store arbitrary values and return the average"""

        while True:
            event, values = self.window.read()
            #  Program quit
            if event == self.gui.WIN_CLOSED or event == self.button_quit:
                #  Save the data in the current directory
                #  TODO: Change this to save at file location as per where
                #        the program is being run from.
                self._save_file()
                break

            #  The user added a new score
            if event == self.button_add_score:
                try:
                    #  Must be integers in a valid range
                    if int(values['wpm']) > 0 and int(values['wpm']) < 300:
                        self.data[self.date].append(int(values['wpm']))
                    pass
                except Exception as e:
                    # Add a popup to indicate a non integer value
                    self.gui.popup(
                        f'Please enter only numbers from 0 to 300\n{e}')

            #  Clears the current scores
            if event == self.button_clear:
                self.gui.popup_ok_cancel(
                    'CAUTION\nThis will erase all scores!' +
                    '\nDo you wish to proceed?', button_color=self.color_button)
                self._clear_scores()
            self._update_scores()
        #  Close the window on exit of event loop
        self.window.close()

    def _update_scores(self):
        """Updates the average score display in the program"""
        self.window['-AVERAGE-'].update('Average: ' +
                                        str(self._get_average()) + ' WPM')

    def _get_average(self, contents={}):
        """Returns the average of all the values in the list"""
        summed = []
        try:
            #  TODO: Must be tested on a different date to ensure that the
            #        average is correctly calculated over multiple days
            for key in self.data.keys():
                summed.extend(self.data[key])
            return math.ceil(self.get_mean(summed))  # No decimal places
        except Exception as e:
            return 0

    def _load_file(self):
        """Loads the .json saved file. If no file exists, creates an empty
        dictionary with key[date]/value[]"""
        try:
            with open(self.filename, 'r') as f:
                data = json.load(f)
                if not data:
                    data = {}
                    data[self.date] = []
                    return data
                return data
        except Exception as e:
            data = {}
            data[self.date] = []
            return data

    def _save_file(self, path=''):
        os.chdir('/Users/peter/Library/Mobile Documents/com~apple~CloudDocs/' +
                 'PythonMain/projects/pysimplegui_average_wpm')
        #  Save the contents in .json format and quit
        with open(self.filename, 'w') as f:
            json.dump(self.data, f)

    def _clear_scores(self):
        self.data[self.date] = []
        with open(self.filename, 'w') as f:
            json.dump(self.data, f)

    def _plot_scores(self):
        """Plot the scores using matplotlib by date"""
        pass


if __name__ == '__main__':
    program = AverageCalculator()
    program.main()
