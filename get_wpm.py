import math
import json
import os
import datetime
import PySimpleGUI as sg
from statistics import mean

# TODO: Add an undo button
# TODO: Add the active user at the top of the app
# TODO: Add app settings(Username)


class AverageCalculator():

    #  Construction
    def __init__(self):
        """Will accept integer input from 0 to 299. The average of those
        numbers are calculated using math.ceil() and then displayed to the user.
        When the user quits the program, the values are automatically stored in
        the same directory as the file."""

        #  Module Imports and implementations
        self.os = os
        self.datetime = datetime
        self.get_mean = mean
        self.gui = sg

        #  Flags
        self.add_score_successful = 0

        #  Button Attributes
        self.button_add_score = 'Add Score'
        self.button_quit = 'Quit'
        self.button_clear = 'Clear Scores'
        self.button_save = 'Create User'
        self.button_load_user = 'Load User'
        self.size_button = 12, 1
        self.color_button = ('white', '#6C6C6C')

        #  Files and Path
        self.filename = 'peter.json'
        self.username = self._get_username()
        self.working_directory = os.getcwd()
        self.file_path = self.os.path.join(
            self.working_directory, self.filename)
        self.create_new_user = False
        self.settings = self._load_settings()

        #  Create a date to use as the key in the data dictionary
        self.now = self.datetime.datetime.now()
        self.date = self.now.strftime("%m %d %y")

        #  Initialize the data
        self.data = self._load_user()

        #  Set the average of the data
        self.current_average = self._get_average()

        #  UX Elements
        self.font = 'Helvetica'

        #  Text Elements
        self.greeting = f'Welcome back, {self.username}!'
        self.wpm_display = ('Average: ' + str(self.current_average) + ' WPM')

        #  App theme
        self.gui.theme('Dark')
        self.gui.theme_button_color(self.color_button)

        #  App Layout
        self.layout = [
            [self.gui.Text(
                self.greeting, size=(40, 1), justification='left', font=(self.font, 15), key='-USERNAME-')],
            [self.gui.Text(self.wpm_display,
                           size=(20, 1),
                           justification='left', font=(self.font, 25),
                           key='-AVERAGE-')
             ], [self.gui.Text('Add Scores:', font=(self.font, 15)),
                 self.gui.InputText(key='wpm', font=(self.font, 15)),
                 self.gui.Button(self.button_add_score, font=(self.font, 15),
                                 button_color=self.color_button)
                 ], [
                self.gui.Button(self.button_load_user,
                                size=(self.size_button), font=(self.font, 15)),
                self.gui.Button(self.button_save,
                                size=(self.size_button), font=(self.font, 15)),
            ], [
                self.gui.Button(self.button_clear, size=(self.size_button),
                                font=(self.font, 15)),
                self.gui.Button(self.button_quit, size=(self.size_button),
                                font=(self.font, 15))
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
                        self.add_score_successful = 1
                except Exception as e:
                    # Add a popup to indicate a non integer value
                    self.gui.popup(
                        f'Please enter only numbers from 0 to 300\n{e}')

            if event == self.button_save:
                #  !Must fix this
                self._create_user()

            if event == self.button_load_user:
                self._load_new_user()
                self.window['-USERNAME-'].update(
                    'Welcome back, ' + self._get_username() + '!')

            #  Clears the current scores
            if event == self.button_clear:
                self.gui.popup_ok_cancel(
                    'CAUTION\nThis will erase all scores!' +
                    '\nDo you wish to proceed?', keep_on_top=True, button_color=self.color_button)
                self._clear_scores()
            self.current_average = self._get_average()
            self.window['-AVERAGE-'].update('Average: ' +
                                            str(self.current_average) + ' WPM')
            # self._update_display_field('-AVERAGE-', self.wpm_display)
            # self._update_display_field('-USERNAME-', self.greeting)
        #  Close the window on exit of event loop
        self.window.close()

    def _load_settings(self):
        """Load the app setting"""
        try:
            with open('settings.json', 'r') as f:
                return json.load(f)
        except:
            with open('settings.json', 'w') as f:
                return {}

    def _save_settings(self):
        with open(self.settings, 'w') as f:
            json.dump(self.settngs, f)

    def _update_display_field(self, field_to_update, text_output):
        """Updates the average score display in the program"""
        self.window[field_to_update].update(text_output)

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

    def _get_username(self):
        """Extract the username from the file loaded"""
        return self.filename.split('.')[0].title()

    def _load_user(self):
        """Loads the .json saved file. If no file exists, creates an empty
        dictionary with key[date]/value[]"""
        try:
            with open(self.file_path, 'r') as f:
                data = json.load(f)
                if not data or self.create_new_user:
                    data = {}
                    data[self.date] = []
                    return data
                return data
        except Exception as e:
            data = {}
            data[self.date] = []
            return data

    def _load_new_user(self):

        try:
            self.file_path = self.gui.popup_get_file("Select the user's file", keep_on_top=True, font=(
                self.font, 15), button_color=(self.color_button))
            self.filename = self.file_path.split('/')[-1]
            with open(self.file_path, 'r') as f:
                self.data = json.load(f)
        except:
            pass

    def _save_file(self):

        #  Makes sure there is something new to write to the file
        if self.add_score_successful or self.create_new_user:
            print('File Saved')
            print(self.file_path)
            with open(self.file_path, 'w') as f:
                json.dump(self.data, f)
            self.add_score_successful = 0

    def _create_user(self):
        #!Needs work. Plenty
        # TODO: Get the directory from values, call the Create User method. Add a popup if successful or not
        filename = self.gui.popup_get_text('Enter Username', keep_on_top=True, font=(
            self.font, 15))
        if len(filename) > 35:
            self.gui.popup('Error\nThe username is too long', keep_on_top=True,
                           font=(self.font, 15), button_color=(self.color_button))
        else:
            try:
                # TODO: Check the current directory if a user already exists
                if any(not c.isalnum() for c in filename.strip().lower()):
                    sg.popup('Error\nNo special characters or spaces allowed', keep_on_top=True, font=(
                        self.font, 15), button_color=(self.color_button))
                else:
                    filename = filename.strip().lower()
                    self.file_path = os.path.join(
                        os.getcwd(), (filename + '.json'))
                    print(self.working_directory)
                    self.create_new_user = True
                    self.data = {}
                    self._save_file()
            except:
                pass

    def _clear_scores(self):
        """Clears the scores the user has entered"""
        self.data[self.date] = []
        self._save_file()

    def _plot_scores(self):
        """Plot the scores using matplotlib by date"""
        pass


if __name__ == '__main__':
    program = AverageCalculator()
    program.main()
