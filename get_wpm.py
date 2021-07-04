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
        self.button_create_user = 'Create User'
        self.button_load_user = 'Load User'
        self.size_button = 12, 1
        self.color_button = ('white', '#6C6C6C')

        #  Files and Path
        self.filename = ''
        self.working_directory = os.getcwd()
        self.file_path = self.os.path.join(
            self.working_directory, self.filename)
        self.create_new_user = False
        self.setting_file_path = os.path.join(os.getcwd(), 'settings.json')

        #  Create a date to use as the key in the data dictionary
        self.now = self.datetime.datetime.now()
        self.date = self.now.strftime("%m %d %y")

        #  Initialize the data
        self.data = self._load_user()
        self.settings = self._load_settings()
        self.username = self._get_username()

        #  Set the average of the data
        self.current_average = self._get_average()

        #  UX Elements
        self.font = 'Helvetica'

        #  Text Elements
        self.greeting = f'Hi, {self.username}!'
        self.wpm_display = ('Average: ' + str(self.current_average) + ' WPM')

        #  App theme
        self.gui.theme('Dark')
        self.gui.theme_button_color(self.color_button)

    def main(self):
        """A program to store arbitrary values and return the average"""
        self._initialize()
        #  App Layout
        self.layout = [
            [self.gui.Text(
                (f'Hi, {self.username.title()}'), size=(40, 1), justification='left', font=(self.font, 15), key='-USERNAME-')],
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
                self.gui.Button(self.button_create_user,
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
        while True:
            event, values = self.window.read()
            #  Program quit
            if event == self.gui.WIN_CLOSED or event == self.button_quit:
                #  Save the data in the current directory
                #  TODO: Change this to save at file location as per where
                #        the program is being run from.
                self._save_file()
                # self.settings['last_user'] = self.username
                # self.settings['file_path'] = self.file_path
                self._save_settings()
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
                    print(e)
                    self.gui.popup(
                        f'Please enter only numbers from 0 to 300\n{e}')

            if event == self.button_create_user:
                self._create_user()
                #  Update the username when a new user is loaded
                self.window['-USERNAME-'].update(
                    'Welcome back, ' + self._get_username() + '!')

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

        #  Close the window on exit of event loop
        self.window.close()

    def _initialize(self):
        """Initializes files and settings if the program is run for the
        first time"""

        try:
            if self.settings['first_load']:
                username = self.gui.popup_get_text(
                    'Average WPM Calculator\nPlease enter your name')
                self.settings['username'] = username
                self.settings['last_user'] = username
                self.username = self.settings['username'].strip(
                ).lower()
                self.filename = self.settings['username']
                self.file_path = self.os.path.join(
                    self.os.getcwd(), (self.username + '.json'))
                self._save_file()
                self.settings['first_load'] = False
                self.settings['file_path'] = self.file_path
                self._save_settings()
            else:
                self.username = self.settings['username']
        except Exception as e:
            quit()

    def _load_settings(self):
        """Load the app setting. Will init an empty settings file on the first
        run of the program"""
        try:
            with open('settings.json', 'r') as f:
                return json.load(f)
        except:
            with open('settings.json', 'w') as f:
                return {'first_load': True, 'username': '', 'last_user': '',
                        'file_path': ''}

    def _save_settings(self):
        """Save the settings file"""
        with open(self.setting_file_path, 'w') as f:
            json.dump(self.settings, f)

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
        """Returns the username from the settings file"""
        return self.settings['username'].title()

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
        """Loads a different user"""
        try:
            self.file_path = self.gui.popup_get_file("Select the user's file", keep_on_top=True, font=(
                self.font, 15), button_color=(self.color_button))
            if self.file_path is None:
                pass
            else:
                self.filename = self.file_path.split('/')[-1]
                self.settings['last_user'] = self.filename.split('.')[0]
                self.settings['username'] = self.settings['last_user']
                self.settings['file_path'] = self.file_path
                with open(self.file_path, 'r') as f:
                    self.data = json.load(f)
        except Exception as e:
            print(e)

    def _save_file(self):
        """Saves a users file to disk"""
        #  Makes sure there is something new to write to the file
        if self.add_score_successful or self.create_new_user or self.settings['first_load']:
            print('File Saved')
            print(self.file_path)
            with open(self.file_path, 'w') as f:
                json.dump(self.data, f)
            self.add_score_successful = 0

    def _create_user(self):
        """Creates a new user to use the program"""
        username = self.gui.popup_get_text('Enter Username', keep_on_top=True, font=(
            self.font, 15))
        if len(username) > 35:
            self.gui.popup('Error\nThe username is too long', keep_on_top=True,
                           font=(self.font, 15), button_color=(self.color_button))
        else:
            try:
                # TODO: Check the current directory if a user already exists
                if any(not c.isalnum() for c in username.strip().lower()):
                    sg.popup('Error\nNo special characters or spaces allowed', keep_on_top=True, font=(
                        self.font, 15), button_color=(self.color_button))
                else:
                    username = username.strip().lower()
                    self.file_path = os.path.join(
                        os.getcwd(), (username + '.json'))
                    print(self.working_directory)
                    self.create_new_user = True
                    self.settings['username'] = username
                    self.settings['last_user'] = username
                    self.data = self._load_user()
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
