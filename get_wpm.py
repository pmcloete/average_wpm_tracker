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
        self.button_save = 'Save File'
        self.button_load_file = 'Load File'
        self.size_button = 12, 1
        self.color_button = '#6C6C6C'

        #  Default Filename
        self.filename = 'words_per_minute.json'
        self.file_extension = '.json'
        self.current_path = os.getcwd()
        self.backup_path = ''
        self.backup_used = True

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
                self.gui.Button(self.button_load_file,
                                size=(self.size_button), font=(self.font, 15),
                                button_color=self.color_button),
                self.gui.Button(self.button_save,
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
                except Exception as e:
                    # Add a popup to indicate a non integer value
                    self.gui.popup(
                        f'Please enter only numbers from 0 to 300\n{e}')

            if event == self.button_save:
                #  !Must fix this
                self._save_backup()

            if event == self.button_load_file:
                self._load_backup()

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
            with open(self.os.path.join(self.current_path,self.filename), 'r') as f:
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

    def _load_backup(self):
        self.backup_used = True
        self.backup_path = self.gui.popup_get_file("Select a file to upload",font=(self.font, 15), button_color=self.color_button)
        # self.filename = filepath.split('/')[-1]
        with open(self.backup_path, 'r') as f:
            self.data = json.load(f)


    def _save_file(self):
        #  Save the contents in .json format and quit
        if not self.backup_used:
            with open(self.os.path.join(self.current_path, self.filename), 'w') as f:
                json.dump(self.data, f)
        else:
            with open(self.backup_path, 'w') as f:
                json.dump(self.data, f)
            self.backup_used = True


    def _save_backup(self):
        #!Needs work. Plenty
        # TODO: Get the directory from values, call the save file method. Add a popup if successful or not
        filename = self.gui.popup_get_text('Enter the filename')
        if any(not c.isalnum() for c in filename):
            sg.popup_error('No special characters allowed')
        else:
            self.backup_path = os.path.join(os.getcwd(),(filename + '.json'))
            print(self.backup_path)
            self._save_file()


    def _clear_scores(self):
        self.data[self.date] = []
        self.current_path = os.getcwd()
        self._save_file()

    def _plot_scores(self):
        """Plot the scores using matplotlib by date"""
        pass


if __name__ == '__main__':
    program = AverageCalculator()
    program.main()
