
"""
config.py

Configuration management for Space Explorer.

Copyright (C) 2002 David Boddie, Paul Boddie, Infukor

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import pygame
from pygame.locals import *
import os, string
import image

try:

    import pygame.mixer
    sound_status = 1

except ImportError:

    sound_status = 0



__version__ = "0.31"
__full_version__ = __version__ + " (21st March 2009)"



# Choices

def read_choices(choices_file):

    choices = {}

    line_number = 1
    while (1==1):
        choice = make_safe(choices_file.readline())

        if choice != '':
            at = choice.find(':')
            if at == -1:
                report_error('Syntax error in Choices file at line '+str(line_number)+'.', name)
                sys.exit(1)

            choices[choice[:at].strip()] = choice[at+1:].lstrip()
        else:
            break

        line_number = line_number + 1

    return choices


def write_choices(choices_file, choices_dict):

    # Write the choices as key : value where all the values are aligned
    # in a column using eight-space tabs.

    # Find the maximum length of any of the choice keys.
    maximum = 0

    for name in choices_dict.keys():

        maximum = max( maximum, len(name) )

    # Determine the number of tabs required to reach the values column
    value_tabs = int(maximum / 8) + ((maximum % 8) != 0)

    # Write the choices to a file

    for name in choices_dict.keys():

        # Determine the number of eight-space tabs required to
        # align the value field with the others.

        tabs_in_name = int( len(name) / 8)
        tabs_required = value_tabs - tabs_in_name

        line = string.expandtabs( name + ('\t'*tabs_required) + ': ' + \
            choices_dict[name], 8 )

        choices_file.write(line + '\n')


def make_safe(s):
    """string = make_safe(string)

    Remove control characters from a string."""

    s = string.expandtabs(s, 8)
    new = ''
    for i in s:
        if ord(i) > 31:
            new = new + i

    return new

class Configuration:

    # Note: aspect ratio is preserved for all pictures, so only the height
    # needs to be specified for each one.

    # Size of the screen
    screen_size = ( 440, 440 )

    # Font sizes
    title_size = 32
    subtitle_size = 16
    game_title_size = 20
    game_text_size = 16
    game_small_text_size = 12
    high_text_size = 20
    
    # Screen background colour
    background_colour = (0, 0, 0)
    
    # Star details
    number_of_star_colours = 12
    number_of_stars_per_colour = 8
    
    # Game title text
    game_title_text = "Space Explorer"
    
    # Game credits
    game_credits = \
    ( "",
      "",
      "(C) 1982, 2002 Infukor Corp.",
      "",
      "We own your games",
      "",
      "Not to be played outside Japan ;-)",
      "",
      "Released under the GNU General Public Licence, version 3"
    )

    # Hidden credits
    game_hidden_credits = \
    ( "",
      "",
      "",
      "Copyright (C) 2002",
      "David Boddie, Paul Boddie",
      "for www.infukor.com",
      "",
      "Version: " + __full_version__
    )

    # Game start prompt
    game_start_prompt = "Press fire to play"

    # Instructions
    instructions_main_text = "Your mission"
    instructions_aliens_text = "Destroy these:"
    instructions_rescue_text = "Rescue these:"

    # Launch text
    game_launch_text = "Select destination"

    # Destinations

    # Each tuple is of the form <name>, <RGB>, <level>
    game_launch_destinations = \
    (
        ("Training levels", (63, 191, 63), 1),
        ("Immediate action", (151, 151, 151), 3),
        ("Get ready", (151, 151, 0), 11),
        ("Starship commander", (151, 0, 0), 21),
        ("Super pilot", (191, 0, 0), 31)
    )

    # Default key controls
    key_move = K_a
    key_fire = K_s
    key_pause = K_p
    key_unpause = K_o
    key_hidden = K_h
    key_define_keys = K_k
    key_exit = K_ESCAPE

    # Default mouse controls
    mouse_move_button = 0   # left button
    mouse_fire_button = 2   # right button

    # Control definition text
    define_controls_text = "Define controls"

    define_controls_instruct = "Press key for"

    define_controls_messages = \
    {
        "Move starship": ("key_move", "mouse_move_button"),
        "Fire":          ("key_fire", "mouse_fire_button"),
        "Pause":         ("key_pause", None),
        "Unpause":         ("key_unpause", None)
    }
    
    define_controls_prompt = "Press a key"
    
    # Game level introduction text
    game_level_intro_text = "Wave %s"

    game_level_subtitle_text = \
    {
        "intro": "Pilot training",
        "formation": "Formation challenge",
        "free form": "Free form attack",
        "legacy": None,
        "generation": "Destroy generators",
        "rescue": "Rescue mission",
        "standard": None
    }

    game_level_subtitle_colour = \
    {
        "intro": (191, 191, 191),
        "generation": (127, 191, 191),
        "formation": (191, 191, 63),
        "free form": (191, 63, 63),
        "rescue": (127, 127, 191)
    }
    
    # Score and lives labels
    game_score_text = "Score"
    game_lives_text = "Lives"
    
    # Extra life texts
    game_recaptured_text = "Recaptured"
    game_extra_life_text = "In reserve"
    
    # Game over text
    game_over_text = "Game Over"

    # High score screen text
    game_high_text = "Enter your name"
    game_high_end_text = "End"
    game_high_del_text = "Del"
    
    # Starting URL
    #game_initial_url = "http://www.infukor.com/Games/Space%20Explorer/"
    game_initial_url = "file:///home/david/Private/WWW sites/david.boddie.org.uk/Pages/index.html"
    game_fallback_url = "docs/index.html"
    
    # High scores
    high_scores = []
    
    # Maximum name length (number of characters)
    high_name_max_length = 20
    
    # Maximum number of objects
    game_max_objects = 32

    # Frame rate of the display (Hz)
    framerate = 24
    
    # Number of updates per second
    updaterate = 24

    # Fade in time (seconds)
    fade_in_time = 1

    # Fading in speed (alpha per update)
    fade_in_speed = int( max(1, 255.0 / (fade_in_time * updaterate) ) )

    # Fade out time (seconds)
    fade_out_time = 1

    # Fading out speed (alpha per update)
    fade_out_speed = int( max(1, 255.0 / (fade_out_time * updaterate) ) )

    def __init__(self, directory):

        # Record the name of the directory which contains the configuration.    
        self.directory = directory
        
        # Store the status of the sound system using the global sound_status
        # constant.
        global sound_status
        
        if sound_status == 1:
        
            # Try to initialise the mixer at the required frequency.
            # [This should be in a try...except block but I don't know
            # which exception I should be checking for.]
            try:
            
                # Set the mixer frequency upon initialisation.
                pygame.mixer.init(11025)
            
            except pygame.error:
            
                sound_status = 0

        # Record the sound system status. This will be used by the
        # Resources class when it is instantiated.
        self.sound_status = sound_status
    
    def load_scores(self):
    
        try:
            lines = open(os.path.join(self.directory, "Scores"))

            self.high_scores = []

            for i in range(0, 10):

                # Put the score, name and last_location into the
                # list of high scores.
                line = lines.readline().rstrip()

                score, name, wave = line.split("\t")

                self.high_scores.append( (score, name, wave) )

            # Only allow ten scores.
            self.high_scores = self.high_scores[:10]

        except (IOError, ValueError):

            self.high_scores = []

            for i in range(10, 0, -1):
            
                if i % 2 == 0:
                    self.high_scores.append((str(i*10), "INFUKOR", i))
                else:
                    self.high_scores.append((str(i*10), "WWW.INFUKOR.COM", i))
    
    def save_scores(self):

        try:
            lines = open(os.path.join(self.directory, "Scores"), "w")

            # Write the scores, names and waves to the file.
            for line in self.high_scores:

                # Put the score, name and last_location onto a line.
                lines.write("\t".join(map(str, line)) + "\n")

            lines.close()

        except IOError:

            pass

    def load_controls(self):

        try:
            f = open(os.path.join(self.directory, "Controls"))
            controls = read_choices(f)
            f.close()

            for name, (key_text, button_text) in \
                self.define_controls_messages.items():

                # Replace the controls using entries from the file.
                try:
                    key_button = controls[name].split(",")

                    # Convert the items in the list to integers.
                    key_button = map(int, key_button)
                    
                    # Overwrite the key definition.
                    self.__dict__[key_text] = key_button[0]
                    
                    if len(key_button) > 1:

                        # Overwrite the mouse button definition.
                        self.__dict__[button_text] = key_button[1]

                except (KeyError, ValueError):

                    pass

        except IOError:

            pass

    def save_controls(self):

        try:
            f = open(os.path.join(self.directory, "Controls"), "w")

            # Write the control definitions to the file.
            for name, (key_text, button_text) in \
                self.define_controls_messages.items():
            
                # Write the name and control definitions in the form
                # name: key, button

                key_val = eval("self." + key_text)

                control_str = name + ":" + str(key_val)

                if button_text is not None:

                    button_val = eval("self." + button_text)
                    control_str = control_str + "," + str(button_val)

                f.write(control_str + "\n")

            f.close()

        except IOError:

            pass



class Resources:

    image_files = \
    [
        "starship.png", "fire.png",
        "istarship1.png", "istarship2.png", "istarship3.png",
        "istarship4.png",
        "gateway1.png", "gateway2.png", "gateway3.png",
        "gateway4.png", "gateway5.png", "gateway6.png",
        "alien1.png", "alien2.png", "alien3.png",
        "alien4.png", "alien5.png", "alien6.png",
        "explosion1.png", "explosion2.png", "explosion3.png",
        "explosion4.png",
        "infukor-logo.png", "infukor-title.png",
        "target1.png", "target2.png",
        "target3.png", "target4.png", "target5.png", "target6.png",
        "target7.png", "target8.png",
        "target9.png", "target10.png", "target11.png", "target12.png"
    ]
      
    image_names = \
    [
        "starship", "fire",
        "istarship1", "istarship2", "istarship3", "istarship4",
        "gateway1", "gateway2", "gateway3",
        "gateway4", "gateway5", "gateway6",
        "alien1", "alien2", "alien3",
        "alien4", "alien5", "alien6",
        "explosion1", "explosion2", "explosion3",
        "explosion4",
        "infukor logo", "infukor title",
        "target1", "target2",
        "target3", "target4", "target5", "target6",
        "target7", "target8",
        "target9", "target10", "target11", "target12"
    ]

    sample_defs = \
    {
        "capture": "capture.ogg",
        "explosion": "explosion.ogg",
        "hyperspace": "hyperspace.ogg",
        "laser": "laser.ogg",
        "recovered": "recovered.ogg",
        "title sound": "titlesound.ogg"
    }
            
    def __init__(self, directory, screen = None, sound = 0):
    
        # Load the images.
        
        self.images = image.Images(
            os.path.join(directory, "Pictures"),
            self.image_files, self.image_names,
            screen = screen
            )
        
        # Load the mouse cursor shape.
        self.cursors = image.Cursors(
            os.path.join(directory, "Pictures"),
            [ ("cross_cursor.xbm", "cross_mask.xbm") ],
            [ "cross" ]
            )
        
        # Store and check the sound system status.
        self.sound_status = sound_status
        
        #print "Sound:", ['off', 'on'][sound_status]
        
        # Set the number of channels to use.
        pygame.mixer.set_num_channels(8)
        
        if pygame.mixer.get_num_channels() == 0:
        
            self.sound_status = 0
        
        if self.sound_status == 1:
        
            # Load the sound samples.
            self.samples = {}
            
            for name, filename in self.sample_defs.items():
            
                # Initialise each sound and store it in the samples
                # dictionary.
                file = os.path.join(directory, "Sounds", filename)
                
                try:
                    sample = pygame.mixer.Sound(file)
                    self.samples[name] = sample
                
                except pygame.error:
                    
                    # Ensure that an entry for this name is created.
                    self.samples[name] = None
