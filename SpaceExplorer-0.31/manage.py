
"""
manage.py

Screen/menu/game management for Space Explorer.

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

import gc, math

import gameobjects, keyboard, level, music
from events import *

# Game management objects ------------------------------------------------------

class GameManager:

    def __init__(self, parent):
    
        self.parent = parent
        self.config = parent.config
        self.resources = parent.resources
        
        # Tell the parent object that this is the manager object.
        self.parent.manager = self
        
        # Fading flag to determine whether objects should fade in or out.
        self.fading = "in"
        
        # Exiting flag
        self.exiting = 0
    
    def unlink(self):
    
        # Remove references to the parent and its objects.
        del self.parent
        del self.config
        del self.resources
    
    def render(self, screen):
    
        pass
    
    def update(self):
    
        pass
    
    def event_handler(self, event):
    
        return []
    
    def fade_objects(self, layers = None):
    
        self.fading = "out"
        
        if layers == None:
        
            layers = range(1, 4)
        
        for layer in layers:
        
            objects = self.parent.find_object(
                gameobjects.GameObject, layer, all = 1
                )
            
            # Fade out all the objects where possible.
            
            # The background objects should take longer to fade out
            # than the foreground objects.
            for object in objects:
            
                if hasattr(object, "fading"):
                
                    object.fading = "out"
    
    def grab_cursor(self):
    
        # Grab the mouse focus.
        pygame.event.set_grab(1)
        
        # Set the cursor shape.
        pygame.mouse.set_cursor(*self.resources.cursors["cross"])
    
    def release_cursor(self):
    
        # Release the mouse focus.
        pygame.event.set_grab(0)
        
        # Set the cursor shape.
        pygame.mouse.set_cursor(*pygame.cursors.arrow)



class TitleScreen(GameManager):

    def __init__(self, parent, phase = 0):

        GameManager.__init__(self, parent)
        
        # Frame number since the object was created.
        self.frame = 0
        
        # Phase number
        self.phase = phase
        self.item = 0
        
        # Frame numbers of important events.
        self.frames = (
            ( (0 * self.config.updaterate, self.add_blank_background),
              (0 * self.config.updaterate, self.start_infukor_logo),
              (2 * self.config.updaterate, self.add_infukor_title),
              (4 * self.config.updaterate, self.remove_corporate),
              (6 * self.config.updaterate, self.next_phase)
            ),
            ( (0,                          self.add_background),
              (2 * self.config.updaterate, self.add_titles),
              (3 * self.config.updaterate, self.add_prompt),
              (4 * self.config.updaterate, self.next_phase)
            ),
            ( (0,                           self.add_credits),
              (4  * self.config.updaterate, self.remove_credits),
              (5  * self.config.updaterate, self.add_scores),
              (5  * self.config.updaterate, self.add_players),
              (9  * self.config.updaterate, self.remove_players),
              (10 * self.config.updaterate, self.add_locations),
              (14 * self.config.updaterate, self.remove_locations),
              (14 * self.config.updaterate, self.remove_scores),
              (15 * self.config.updaterate, self.add_instructions),
              (15 * self.config.updaterate, self.add_aliens),
              (18 * self.config.updaterate, self.add_objects),
              (19 * self.config.updaterate, self.remove_aliens),
              (22 * self.config.updaterate, self.remove_objects),
              (22 * self.config.updaterate, self.remove_instructions),
              (23 * self.config.updaterate, self.repeat_phase)
            ) )

        # Credits to use.
        self.game_credits = self.config.game_credits
        
        if phase == 0:
            # Play a sound.
            if self.resources.sound_status:
                self.resources.samples["title sound"].play()

    def event_handler(self, event):

        events = []

        if isinstance(event, KeyPress):

            if event.key == self.config.key_exit:

                # Exit the application.

                # Fade the objects.
                self.fade_objects()

                # Set the exit flag.
                self.exiting = "exiting"

            elif event.key == self.config.key_hidden:

                # Temporarily show some hidden information at the appropriate
                # time.

                self.game_credits = self.config.game_hidden_credits

            elif event.key == self.config.key_define_keys:

                # Fade the objects.
                self.fade_objects()

                self.exiting = "defining"

            elif event.key == self.config.key_fire:

                # Set the exiting flag.
                self.exiting = "launching"

                # Start the game by fading all the objects in all layers.
                self.fade_objects()

        elif isinstance(event, MouseButton):

            # Read the mouse buttons state.
            if event.button == self.config.mouse_fire_button:

                # Set the exiting flag.
                self.exiting = "launching"

                # Start the game by fading all the objects in all layers.
                self.fade_objects()

        return events

    def update(self):

        # If we are exiting this screen then check the numbers of game
        # objects left. If there are none left then remove this object
        # from the parent's object list and add a Gameplay object.

        if self.exiting == "exiting" or \
            self.exiting == "launching" or \
            self.exiting == "defining":

            # Just check that the background has been removed as the
            # other objects should fade faster than it.
            if (not self.parent.find_object(
                gameobjects.GameObject, layer = 1 )
                ):

                # Remove all objects in the other layers.
                self.parent.objects[1:4] = [[], [], []]

                # Request that the parent remove this object from its
                # list.
                self.parent.add_event( RemoveObject(self) )

                if self.exiting == "exiting":

                    # Exit the application.
                    self.parent.quit = 1

                elif self.exiting == "launching":

                    # Request that the parent add a Gameplay object to its
                    # list.
                    self.parent.add_event( AddObject(
                        LaunchScreen(self.parent), layer = 0
                        ) )

                elif self.exiting == "defining":

                    # Request that the parent add a Gameplay object to its
                    # list.
                    self.parent.add_event( AddObject(
                        DefineControls(self.parent), layer = 0
                        ) )

        else:

            # We should always encounter all updates, so just create objects
            # when the relevant frame number is reached.

            while 1:

                frame, action = self.frames[self.phase][self.item]

                if self.frame >= frame:

                    # Increment the item number.
                    self.item = self.item + 1

                    # Execute the action associated with this frame.
                    action()

                else:

                    # Increment the frame number.
                    self.frame = self.frame + 1

                    # Stop processing actions.
                    break

    def next_phase(self):

        # Move to the next phase.
        self.phase = self.phase + 1

        # Reset the item number.
        self.item = 0

        # Reset the frame number.
        self.frame = 0

    def previous_phase(self):
    
        # Move to the next phase.
        self.phase = self.phase - 1
        
        # Reset the item number.
        self.item = 0

        # Reset the frame number.
        self.frame = 0
    
    def goto_phase(self, phase):
    
        # Move to the phase given.
        self.phase = phase
        
        # Reset the item number.
        self.item = 0

        # Reset the frame number.
        self.frame = 0
    
    def repeat_phase(self):
    
        # Reset the item number.
        self.item = 0
        
        # Reset the frame number.
        self.frame = 0
    
    def add_blank_background(self):

        # Define the background layer object and add it to the parent's
        # background layer.
        self.parent.add_object(
            gameobjects.BlankBackground( self.parent, (0, 0, 0) ),
            layer = 1, index = 0
            )
    
    def start_infukor_logo(self):
    
        # Add two copies of the Infukor logo: one which expands horizontally
        # and one which expands vertically.
        
        self.parent.add_object(
            gameobjects.InfukorLogo(
                self.parent,
                ( self.config.screen_size[0]/2,
                  0.375 * self.config.screen_size[1] ),
                "infukor logo", alpha = 127, width = 0,
                steps = self.config.updaterate * 2
                ),
            layer = 3, index = 0
            )
        
        self.parent.add_object(
            gameobjects.InfukorLogo(
                self.parent,
                ( self.config.screen_size[0]/2,
                  0.375 * self.config.screen_size[1] ),
                "infukor logo", alpha = 127, height = 0,
                steps = self.config.updaterate * 2
                ),
            layer = 3, index = 0
            )
    
    def add_infukor_title(self):
    
        # Add the Infukor title logo.
        self.parent.add_object(
            gameobjects.InfukorLogo(
                self.parent,
                ( self.config.screen_size[0]/2,
                  0.75 * self.config.screen_size[1] ),
                "infukor title", alpha = 255
                ),
            layer = 3, index = 0
            )
    
    def remove_corporate(self):
    
        # Fade all corporate objects.
        for object in self.parent.objects[3]:
        
            object.fading = "out"
        
        # Remove all corporate objects.
        #self.parent.objects[1:4] = [[], [], []]
    
    def add_background(self):
    
        # Remove the old background layer as this one will ensure that
        # the black background is maintained.
        self.parent.objects[1] = []
        
        # Define the background layer object and add it to the parent's
        # background layer.
        self.parent.add_object(
            gameobjects.StarryBackground(self.parent), layer = 1, index = 0
            )
    
    def add_titles(self):

        # Add the title text.
        self.parent.add_object( gameobjects.TitleText(
            self.parent,
            ( self.config.screen_size[0]/2, self.config.screen_size[1]/8 ),
            self.config.game_title_text, self.config.title_size,
            scale_radius = 0.025, scale_angular_speed = 33.0
            ),
            layer = 3
            )
        
        self.parent.add_object(
            gameobjects.AlienText(
                self.parent,
                ( self.config.screen_size[0]/2,
                  self.config.screen_size[1]/8 + 2 ),
                self.config.game_title_text, 2 * self.config.title_size,
                end_char = " ", colour = (55, 63, 15),
                scale_radius = 0.01, scale_angular_speed = 33.0
                ),
                layer = 3, index = 0
            )

    def add_prompt(self):
    
        y = int(7/8.0 * self.config.screen_size[1])
        
        # Add a prompt.
        self.parent.add_object(
            gameobjects.TitleText( self.parent,
                (self.config.screen_size[0]/2, y),
                self.config.game_start_prompt, self.config.subtitle_size,
                colour = (0, 0, 191)
                ),
            layer = 3
            )

    def add_credits(self):
    
        # Add the game credits.
        x = self.config.screen_size[0]/2
        y = self.config.screen_size[1]/4

        self.credits = []
        
        # Each line has its own phase angle.
        angle_step = 360.0/len(self.config.game_credits)
        
        angle = 0.0

        for credit in self.game_credits:
        
            if credit != "":

                # Only create non-empty text labels.
                self.credits.append(
                    gameobjects.TitleText(
                        self.parent, (x, y), credit, self.config.subtitle_size,
                        colour = (191, 191, 0),
                        scale_angle = angle, scale_angular_speed = 33.0
                        )
                    )

                self.parent.add_object( self.credits[-1], layer = 3 )
            
            y = y + (1.5 * self.config.subtitle_size)
            angle = angle + angle_step
        
        # Reset the credits to use.
        self.game_credits = self.config.game_credits
    
    def remove_credits(self):
    
        for credit in self.credits:

            # Ask each credit to fade.
            credit.fading = "out"
    
    def add_scores(self):

        # Add the game credits.
        x = self.config.screen_size[0]/4 - 8
        y = self.config.screen_size[1]/4
        
        self.scores = []
        
        # Each line has its own phase angle.
        angle_step = 360.0/len(self.config.high_scores)
        
        angle = 0.0

        for score, name, last_location in self.config.high_scores:
        
            self.scores.append(
                gameobjects.TitleText(
                    self.parent, (x, y), score, self.config.subtitle_size,
                    colour = (191, 191, 0),
                    scale_angle = angle, scale_angular_speed = 33.0,
                    align = "E"
                    )
                )
            
            self.parent.add_object( self.scores[-1], layer = 3 )
            
            y = y + (1.5 * self.config.subtitle_size)
            angle = angle + angle_step
    
    def remove_scores(self):
    
        for score in self.scores:

            # Ask each credit to fade.
            score.fading = "out"
    
    def add_players(self):
    
        # Add the game credits.
        x = self.config.screen_size[0]/4 + 8
        y = self.config.screen_size[1]/4
        
        self.players = []
        
        # Each line has its own phase angle.
        angle_step = 360.0/len(self.config.high_scores)
        
        angle = 0.0
        
        for score, name, last_location in self.config.high_scores:

            self.players.append(
                gameobjects.TitleText(
                    self.parent, (x, y), name, self.config.subtitle_size,
                    colour = (191, 0, 0),
                    scale_angle = angle, scale_angular_speed = 33.0,
                    align = "W"
                    )
                )
            
            self.parent.add_object( self.players[-1], layer = 3 )

            y = y + (1.5 * self.config.subtitle_size)
            angle = angle + angle_step
    
    def remove_players(self):
    
        for player in self.players:
        
            # Ask each credit to fade.
            player.fading = "out"
    
    def add_locations(self):
    
        # Add the game credits.
        x = self.config.screen_size[0]/4 + 8
        y = self.config.screen_size[1]/4
        
        self.locations = []
        
        # Each line has its own phase angle.
        angle_step = 360.0/len(self.config.high_scores)
        
        angle = 0.0
        
        for score, name, last_location in self.config.high_scores:

            self.locations.append(
                gameobjects.TitleText(
                    self.parent, (x, y),
                    self.config.game_level_intro_text % last_location,
                    self.config.subtitle_size,
                    colour = (191, 191, 191),
                    scale_angle = angle, scale_angular_speed = 33.0,
                    align = "W"
                    )
                )
            
            self.parent.add_object( self.locations[-1], layer = 3 )
            
            y = y + (1.5 * self.config.subtitle_size)
            angle = angle + angle_step
    
    def remove_locations(self):
    
        for location in self.locations:
        
            # Ask each credit to fade.
            location.fading = "out"
    
    def add_instructions(self):
    
        # Add some instructions.
        self.instructions_text = gameobjects.TitleText(
            self.parent,
            (self.config.screen_size[0]/2, self.config.screen_size[1]/4),
            self.config.instructions_main_text,
            self.config.subtitle_size,
            colour = (191, 191, 0),
            scale_angular_speed = 33.0
            )

        self.parent.add_object(self.instructions_text, layer = 3)
    
    def remove_instructions(self):
    
        # Remove the instructions.
        self.instructions_text.fading = "out"
    
    def add_aliens(self):
    
        # Add the alien instructions.
        y = self.config.screen_size[1]/4 + (2 * self.config.subtitle_size)

        self.aliens_text = gameobjects.TitleText(
            self.parent,
            ( self.config.screen_size[0]/2, y ),
            self.config.instructions_aliens_text,
            self.config.subtitle_size,
            colour = (191, 0, 0),
            scale_angular_speed = 33.0
            )

        self.parent.add_object(self.aliens_text, layer = 3)

        # Add five aliens underneath.
        y = y + (2 * self.config.subtitle_size)
        
        self.aliens = []
        
        self.aliens.append(
            gameobjects.StartStop(
                self.parent, ( self.config.screen_size[0]/2 - 96, y)
                )
            )
        
        self.aliens.append(
            gameobjects.Follower(
                self.parent, ( self.config.screen_size[0]/2 - 48, y)
                )
            )

        self.aliens.append(
            gameobjects.Interceptor(
                self.parent, ( self.config.screen_size[0]/2, y)
                )
            )
        
        self.aliens.append(
            gameobjects.Capturer(
                self.parent, ( self.config.screen_size[0]/2 + 48, y)
                )
            )
        
        self.aliens.append(
            gameobjects.Generator(
                self.parent, ( self.config.screen_size[0]/2 + 96, y),
                [ ( self.config.screen_size[0]/2 + 96, y) ],
                generate_time = 60
                )
            )

        for object in self.aliens:
        
            self.parent.add_object(object, layer = 3)
    
    def remove_aliens(self):

        # Remove the alien instructions.
        self.aliens_text.fading = "out"
        
        for object in self.aliens:
        
            object.fading = "out"
    
    def add_objects(self):

        # Add the object instructions.
        y = self.config.screen_size[1]/2
        
        self.rescue_text = gameobjects.TitleText(
            self.parent,
            ( self.config.screen_size[0]/2, y ),
            self.config.instructions_rescue_text,
            self.config.subtitle_size,
            colour = (0, 0, 191),
            scale_angular_speed = 33.0
            )

        self.parent.add_object(self.rescue_text, layer = 3)
        
        # Add a starship underneath.
        y = y + (2 * self.config.subtitle_size)
        
        self.rescue = []
        
        self.rescue.append(
            gameobjects.Starship(
                self.parent, ( 0.5 * self.config.screen_size[0], y),
                controlled = 0
                )
            )
        
        for object in self.rescue:

            self.parent.add_object(object, layer = 3)

    def remove_objects(self):
    
        # Remove the object instructions.
        self.rescue_text.fading = "out"
        
        for object in self.rescue:

            object.fading = "out"



class DefineControls(GameManager):

    def __init__(self, parent):

        GameManager.__init__(self, parent)

        # Add some objects to the parent's object list.

        # Define the background layer object and add it to the parent's
        # background layer.
        self.parent.add_object(
            gameobjects.StarryBackground(self.parent), layer = 1, index = 0
            )

        self.parent.add_object( gameobjects.TitleText(
            self.parent,
            ( self.config.screen_size[0]/2, self.config.screen_size[1]/8 ),
            self.config.define_controls_text, self.config.title_size,
            colour = (127, 191, 255),
            scale_radius = 0.02, scale_angular_speed = 33.0
            ),
            layer = 3
            )

        self.parent.add_object( gameobjects.TitleText(
            self.parent,
            ( self.config.screen_size[0]/2,
              self.config.screen_size[1]/3 - (2 * self.config.subtitle_size)
            ),
            self.config.define_controls_instruct,
            self.config.subtitle_size,
            colour = (255, 191, 127),
            scale_radius = 0.02, scale_angular_speed = 33.0
            ),
            layer = 3
            )

        # Set the state.
        self._state = "displaying"

        # Show all the controls to be defined.
        self.controls_dict = self.config.define_controls_messages

        self.controls_messages = []
        
        c = 0
        
        for key, value in self.controls_dict.items():
        
            try:
                keyname = keyboard.inverse_keys[getattr(self.config, value[0])]
            
            except KeyError:
            
                keyname = "Unknown"
            
            self.controls_messages.append(
                gameobjects.TitleText(
                    self.parent,
                    ( self.config.screen_size[0]/2,
                      self.config.screen_size[1]/3 + \
                          (c * self.config.subtitle_size)
                    ),

                    # Label with name of control and the key currently used.
                    key + "   " + keyname,
                    
                    self.config.subtitle_size,
                    colour = (127, 127, 127),
                    scale_radius = 0.02, scale_angular_speed = 33.0
                ) )

            self.parent.add_object( self.controls_messages[-1], layer = 3 )
            
            c = c + 1
        
        # The control to be defined by the user.
        self.control = 0

    def event_handler(self, event):

        actions = []

        if isinstance(event, KeyPress):

            if event.key == self.config.key_exit:

                # Return to the title screen.

                # Set the exiting flag.
                self._state = "exiting"

                # Start fading the objects.
                self.fade_objects()

            elif self._state == "defining":

                # Store the key press in the relevant configuration
                # variable. We use a class hack to achieve this.

                # Ensure that the key does not clash with a previous
                # one.

                clash = 0

                for key_text, button_text in \
                    self.controls_dict.values()[:self.control]:

                    key_val = self.config.__dict__[key_text]

                    if key_val == event.key:

                        clash = 1
                        break

                if clash == 0 and \
                    event.key != self.config.key_define_keys and \
                    event.key != self.config.key_hidden and \
                    event.key != self.config.key_exit:

                    key_text, button_text = \
                        self.controls_dict.values()[self.control]

                    if key_text is not None:

                        self.config.__dict__[key_text] = event.key
                    
                    key, value = self.controls_dict.items()[self.control]
                    
                    # Fade the control message and replace it with an
                    # unhighlighted version.
                    self.controls_messages[self.control].fading = "out"
                    
                    try:
                        keyname = keyboard.inverse_keys[getattr(self.config, value[0])]
                    
                    except KeyError:
                    
                        keyname = "Unknown"
                    
                    self.controls_messages[self.control] = gameobjects.TitleText(
                        self.parent,
                        ( self.config.screen_size[0]/2,
                          self.config.screen_size[1]/3 + \
                              (self.control * self.config.subtitle_size) ),
                        
                        # Label with name of control and the key currently used.
                        key + "   " + keyname,
                        
                        self.config.subtitle_size,
                        colour = (127, 191, 127)
                        )
                    
                    self.parent.add_object(
                        self.controls_messages[self.control], layer = 3
                        )
                    
                    # Move onto the next message if possible.
                    self.control = self.control + 1

                    if self.control < len(self.controls_dict):

                        # Set the state to allow the next message to be
                        # displayed.
                        self._state = "displaying"

                    else:
                    
                        # Prompt for a keypress.
                        self.parent.add_object(
                            gameobjects.TitleText(
                                self.parent,
                                ( self.config.screen_size[0]/2,
                                  0.75 * self.config.screen_size[1] ),
                                self.config.define_controls_prompt,
                                self.config.subtitle_size,
                                colour = (255, 255, 127)
                                ),
                            layer = 3 )
                        
                        # Wait for a keypress before exiting.
                        self._state = "waiting"
            
            elif self._state == "waiting":
            
                # Fade the objects.
                self.fade_objects()
                
                # Exit the control definition screen.
                self._state = "exiting"

        return actions

    def update(self):

        if self._state == "exiting":

            # Just check that the background has been removed as the
            # other objects should fade faster than it.
            if (not self.parent.find_object(
                gameobjects.GameObject, layer = 1 )
                ):

                # Remove all objects in the other layers.
                self.parent.objects[1:4] = [[], [], []]

                # Request that the parent remove this object from its
                # list.
                self.parent.add_event( RemoveObject(self) )

                # Request that the parent add a TitleScreen object to its
                # list.
                self.parent.add_event( AddObject(
                    TitleScreen(self.parent, phase = 1), layer = 0
                    ) )

        elif self._state == "displaying":

            # Fade out the next control to be defined and replace it with
            # a highlighted message.

            self.controls_messages[self.control].fading = "out"
            
            key, value = self.controls_dict.items()[self.control]
            
            try:
                keyname = keyboard.inverse_keys[getattr(self.config, value[0])]
            
            except KeyError:
            
                keyname = "Unknown"
            
            self.controls_messages[self.control] = gameobjects.TitleText(
                self.parent,
                ( self.config.screen_size[0]/2,
                  self.config.screen_size[1]/3 + \
                      (self.control * self.config.subtitle_size) ),
                
                # Label with name of control and the key currently used.
                key + "   " + keyname,
                
                self.config.subtitle_size,
                colour = (255, 255, 255)
                )

            self.parent.add_object(
                self.controls_messages[self.control], layer = 3
                )
            
            # Set the state to allow the user to define the control.
            self._state = "defining"



class LaunchScreen(GameManager):

    def __init__(self, parent):

        GameManager.__init__(self, parent)

        # Add some objects to the parent's object list.

        # Define the background layer object and add it to the parent's
        # background layer.
        self.parent.add_object(
            gameobjects.StarryBackground(self.parent), layer = 1, index = 0
            )

        self.parent.add_object( gameobjects.TitleText(
            self.parent,
            ( self.config.screen_size[0]/2, self.config.screen_size[1]/8 ),
            self.config.game_launch_text, self.config.title_size,
            colour = (127, 191, 255),
            scale_radius = 0.02, scale_angular_speed = 33.0
            ),
            layer = 3
            )

        # Show the choices to the player.
        choices = self.config.game_launch_destinations[:6]

        angle = 0.0
        angle_step = (180.0 / (len(choices)/2.0))
        i = 0

        cx, cy = self.config.screen_size[0]/2, self.config.screen_size[1]/2
        r = min(
            0.4 * self.config.screen_size[0],
            0.4 * self.config.screen_size[1]/2
            )

        for caption, colour, level in choices:

            # Display captions for each destination.
            if i % 2 == 0:
            
                display_angle = (270.0 + angle)
            
            else:
            
                display_angle = (270.0 - angle)
            
            self.parent.add_object( gameobjects.TitleText(
                self.parent,
                ( cx + (r * math.cos(display_angle * math.pi / 180.0)),
                  cy + (r * math.sin(display_angle * math.pi / 180.0)) ),
                caption, self.config.subtitle_size,
                colour = colour,
                scale_angle = angle
                ),
                layer = 3
                )

            # Create a gateway for each destination, storing the level
            # number in the Gateway object's label attribute.

            self.parent.add_object( gameobjects.Gateway(
                self.parent, label = level,
                position = (
                    cx + (r * math.cos(display_angle * math.pi / 180.0)),
                    cy + (r * math.sin(display_angle * math.pi / 180.0)) + \
                        self.config.subtitle_size * 1.5
                    )
                ),
                layer = 2
                )

            i = i + 1

            if i % 2 == 1:
            
                angle = angle + angle_step
        
        # Add a starship.
        self.parent.add_object( gameobjects.Starship(
            self.parent,
            (self.config.screen_size[0]/2, self.config.screen_size[1]/2)
            ),
            layer = 2, index = -1
            )
        
        # Set the launch state.
        self.launch_state = "choosing"

        # The chosen level number.
        self.level_number = 1

        # Grab the mouse focus.
        self.grab_cursor()

    def event_handler(self, event):

        actions = []

        if isinstance(event, KeyPress):

            if event.key == self.config.key_pause:

                # Pause the application.
                self.parent.pause = 1

                # Release the mouse focus.
                self.release_cursor()

            elif event.key == self.config.key_unpause:

                # Pause the application.
                self.parent.pause = 0

                # Grab the mouse focus.
                self.grab_cursor()

            elif event.key == self.config.key_exit:

                # Return to the title screen.

                # Set the exiting flag.
                self.launch_state = "exiting"

                # Start fading the objects.
                self.fade_objects()

                # Release the mouse focus.
                self.release_cursor()

        elif isinstance(event, EnteredGateway):

            # Find the destination of the gateway.
            self.level_number = event.gameobject.label

            # Leave the selection screen.
            self.launch_state = "launching"

            # Play a sound.
            if self.resources.sound_status:
                self.resources.samples["hyperspace"].play()
            
            # Start fading the objects.
            self.fade_objects()
        
        return actions
    
    def update(self):

        if self.launch_state == "exiting":

            # Just check that the background has been removed as the
            # other objects should fade faster than it.
            if (not self.parent.find_object(
                gameobjects.GameObject, layer = 1 )
                ):

                # Remove all objects in the other layers.
                self.parent.objects[1:4] = [[], [], []]

                # Request that the parent remove this object from its
                # list.
                self.parent.add_event( RemoveObject(self) )

                # Request that the parent add a TitleScreen object to its
                # list.
                self.parent.add_event( AddObject(
                    TitleScreen(self.parent, phase = 1), layer = 0
                    ) )

        elif self.launch_state == "launching":

            # Just check that the background has been removed as the
            # other objects should fade faster than it.
            if (not self.parent.find_object(
                gameobjects.GameObject, layer = 1 )
                ):

                # Remove all objects in the other layers.
                self.parent.objects[1:4] = [[], [], []]

                # Request that the parent remove this object from its
                # list.
                self.parent.add_event( RemoveObject(self) )

                # Request that the parent add a Gameplay object to its
                # list.
                self.parent.add_event( AddObject(
                    Gameplay(self.parent, level = self.level_number),
                    layer = 0
                    ) )



class Gameplay(GameManager):

    def __init__(self, parent, level = 1):
    
        GameManager.__init__(self, parent)
        
        # Set some properties.
        
        # Number of ships left
        self.lives = 3
        
        # Level number
        self.level_number = level
        
        # Score
        self.score = 0
        
        # Objects under the control of the player (for use between levels).
        self.controlled = []
        
        # Current level URL
        self.url = self.config.game_initial_url
        
        # Music object
        self.music = None
        
        # We are starting a new game.
        self.game_state = "start game"
        
        # Grab the mouse focus.
        self.grab_cursor()
    
    def event_handler(self, event):
    
        actions = []
        
        if isinstance(event, KeyPress):
        
            if event.key == self.config.key_pause:
            
                # Pause the application.
                self.parent.pause = 1
                
                # Release the mouse focus.
                self.release_cursor()
            
            elif event.key == self.config.key_unpause:
            
                # Pause the application.
                self.parent.pause = 0
                
                # Grab the mouse focus.
                self.grab_cursor()
            
            elif event.key == self.config.key_exit:
            
                # Return to the title screen.
                
                # Set the exiting flag.
                self.game_state = "exiting"
                
                # Start fading the objects.
                self.fade_objects()
        
        elif isinstance(event, AddScore):
        
            self.score = self.score + event.value
            
            # Update the score text.
            self.score_text.set_text(str(self.score))
        
        elif isinstance(event, GameObjectDestroyed):
        
            # Play a sound.
            if self.resources.sound_status:
            
                self.resources.samples["explosion"].play()
        
            # Record the alpha component of the destroyed object.
            alpha = event.gameobject.alpha
            
            if isinstance(event.gameobject, gameobjects.Starship):
            
                # A starship has been destroyed.
                
                if event.gameobject in self.controlled:

                    # Remove this object from the list of controlled objects.
                    self.controlled.remove(event.gameobject)
                    
                    # Fade out all controlled objects which are not starships
                    # from the parent's object list and keep one to use as
                    # the main starship if possible.
                    starship = None
                    
                    for object in self.controlled:
                    
                        if isinstance(object, gameobjects.Starship):
                        
                            if starship == None: starship = object
                        
                        else:
                        
                            object.fading = "out"
                    
                    # Remove all controlled objects which are not starships
                    # from the controlled list.
                    self.controlled = filter(
                        lambda x: isinstance(x, gameobjects.Starship),
                        self.controlled
                        )
                    
                    # Replace the starship with an explosion in the parent's
                    # object list.
                    index = self.parent.objects[2].index(event.gameobject)
                    
                    self.parent.objects[2][index] = gameobjects.Explosion(
                        self.parent, event.gameobject.position, alpha = alpha
                        )
                    
                    # Create another starship if necessary (the destroyed
                    # starship was the main one) or just realign another
                    # (if there are others).
                    
                    if starship:
                    
                        if event.gameobject.displace == (0, 0):
                        
                            starship.displace = (0, 0)
                    
                    elif self.lives > 0:
                    
                        # Create a new starship.
                        self.new_starship()
                        
                        # Remove the target cursor.
                        cursor = self.parent.find_object(
                            gameobjects.TargetCursor, layer = 3
                            )
                        
                        if cursor:
                        
                            self.parent.remove_object(cursor, layer = 3)
                    
                    elif self.game_state == "playing":
                    
                        # Only perform the game over sequence if the game
                        # is being played.
                        self.game_state = "game over"
                        
                        # Remove the target cursor.
                        cursor = self.parent.find_object(
                            gameobjects.TargetCursor, layer = 3
                            )

                        if cursor:
                        
                            self.parent.remove_object(cursor, layer = 3)
            
            elif isinstance(event.gameobject, gameobjects.Alien):
            
                # An alien has been destroyed.
                
                if event.gameobject in self.parent.objects[2]:
                
                    # Increase the player's score.
                    self.parent.add_event( AddScore(event.gameobject.value) )
                    
                    # Replace the alien with an explosion in the parent's
                    # object list.
                    index = self.parent.objects[2].index(event.gameobject)
                    
                    self.parent.objects[2][index] = gameobjects.Explosion(
                        self.parent, event.gameobject.position, alpha = alpha
                        )
                    
                    if self.game_state == "playing":
                    
                        # Try to fetch a replacement alien.
                        self.current_level.deploy_next()
                        
                        # Check whether there are any aliens present on this
                        # level and whether there are any more to come.
                        if ( not self.parent.find_object(
                            gameobjects.Alien, layer = 2
                            ) ) and self.current_level.finished():
                        
                            # We have left the level.
                            self.game_state = "next level"
            
            else:
            
                if event.gameobject in self.parent.objects[2]:
                
                    # Replace the object with an explosion in the parent's
                    # object list.
                    index = self.parent.objects[2].index(event.gameobject)
                    
                    self.parent.objects[2][index] = gameobjects.Explosion(
                        self.parent, event.gameobject.position, alpha = alpha
                        )
        
        elif isinstance(event, Captured):
        
            if isinstance(event.gameobject, gameobjects.Starship):
            
                # A starship has been captured.
                
                if event.gameobject in self.controlled:
                
                    # Remove this object from the list of controlled objects.
                    self.controlled.remove(event.gameobject)
                    
                    # Find a new starship to use as the main starship.
                    starship = None
                    
                    for object in self.controlled:
                    
                        if isinstance(object, gameobjects.Starship):
                        
                            if starship == None: starship = object
                    
                    # Create another starship if necessary (the destroyed
                    # starship was the main one) or just realign another
                    # (if there are others).
                    if starship:
                    
                        if event.gameobject.displace == (0, 0):
                        
                            starship.displace = (0, 0)
                    
                    elif self.lives > 0:
                    
                        # Create a new starship.
                        self.new_starship()
                        
                        # Remove the target cursor.
                        cursor = self.parent.find_object(
                            gameobjects.TargetCursor, layer = 3
                            )
                        
                        if cursor:
                        
                            self.parent.remove_object(cursor, layer = 3)
                    
                    elif self.game_state == "playing":

                        # Only perform the game over sequence if the game
                        # is playing.
                        self.game_state = "game over"
                        
                        # Remove the target cursor.
                        cursor = self.parent.find_object(
                            gameobjects.TargetCursor, layer = 3
                            )
                        
                        if cursor:
                        
                            self.parent.remove_object(cursor, layer = 3)
                    
                    # Send the captured starship to the capturer's target
                    # position.
                    
                    event.gameobject.target_position = event.position
                    event.gameobject.displace = (0, -32)
                    event.gameobject.target_angle = 0.0
                    
                    # It is not controlled.
                    event.gameobject.controlled = 2
        
        elif isinstance(event, Recaptured):
        
            if event.gameobject not in self.controlled:
            
                gameobject = event.gameobject
                
                # Check the list of controlled objects for new displacement
                # positions.
                positions = [(0, 0), (-24, -24), (24, -24), (-24, 24), (24, 24)]
                
                for object in self.controlled:
                
                    if isinstance(object, gameobjects.Starship):
                    
                        try:
                            positions.remove(object.displace)

                        except ValueError:
                        
                            pass
                
                if positions:
                
                    # Use the first available position.
                    gameobject.displace = positions[0]
                    gameobject.target_position = (
                        self.controlled[0].target_position[0] + positions[0][0],
                        self.controlled[0].target_position[1] + positions[0][1]
                        )
                    
                    gameobject.controlled = 1
                    self.controlled.append(gameobject)
                    
                    # Show notification of extra ship.
                    self.parent.add_object( gameobjects.TemporaryText(
                        self.parent, gameobject.position,
                        self.config.game_recaptured_text,
                        self.config.game_text_size,
                        (63, 63, 127)
                        ),
                        layer = 3, index = -1
                        )
                
                else:

                    # Otherwise fade this object and give the player an
                    # extra life.
                    gameobject.fading = "out"
                    gameobject.target_position = gameobject.position
                    
                    self.lives = self.lives + 1
                    
                    # Update the life indicator.
                    self.life_indicator.set_text(str(self.lives))
                    
                    # Show notification of extra life.
                    self.parent.add_object( gameobjects.TemporaryText(
                        self.parent, gameobject.position,
                        self.config.game_extra_life_text,
                        self.config.game_text_size,
                        (63, 63, 127)
                        ),
                        layer = 3, index = -1
                        )
        
        return actions
    
    def update(self):

        # Music
        #self.music.play_music()
        
        if self.game_state == "exiting":
        
            # Exiting the gameplay
            self.exiting_gameplay()
        
        elif self.game_state == "after game":
        
            # After game
            self.after_game()
        
        elif self.game_state == "after game over":
        
            # After game over
            self.after_game_over()
        
        elif self.game_state == "game over":
        
            # Game over
            self.game_over()
        
        elif self.game_state == "next level":
        
            # Leaving this level to enter another
            self.leaving_level()
        
        elif self.game_state == "playing":
        
            # Playing the level
            self.playing_level()
        
        elif self.game_state == "starting":
        
            # Starting the level
            self.starting_level()
        
        elif self.game_state == "initialise":
        
            # Loading the level
            self.initialise_level()
        
        elif self.game_state == "start game":
        
            # Prepare to load the new level.
            self.start_game()
    
    def exiting_gameplay(self):
    
        # Just check that the background has been removed as the
        # other objects should fade faster than it.
        if not self.parent.find_object(gameobjects.GameObject, layer = 1 ):
        
            # Remove all objects in the other layers.
            self.parent.objects[1:4] = [[], [], []]
            
            # Request that the parent remove this object from its
            # list.
            self.parent.add_event( RemoveObject(self) )
            
            # Request that the parent add a TitleScreen object to its
            # list. Skip the Infukor banner phase on the title screen.
            self.parent.add_event( AddObject(
                TitleScreen(self.parent, phase = 1), layer = 0
                ) )
            
            # Release the mouse focus.
            self.release_cursor()
            
            # Stop the music.
            #self.music.stop_music()
            
            # Enable garbage collection.
            gc.enable()
    
    def after_game(self):
    
        if not self.parent.find_object(gameobjects.GameObject, layer = 2):
        
            # Remove the blank background.
            self.parent.objects[1] = []
            
            # Request that the parent remove this object from its
            # list.
            self.parent.add_event( RemoveObject(self) )
            
            # Check the score against the high scores.
            higher = 0
            
            for score, name, level in self.config.high_scores:
            
                if self.score > int(score):
                
                    # Score is higher than this score.
                    break
                
                elif self.score == int(score) and \
                    self.level_number > int(level):
                
                    # Score is equal to this score but the level is higher.
                    break
                
                higher = higher + 1
            
            if higher < len(self.config.high_scores):
            
                # Request that the parent add a HighScoreScreen object to its
                # list.
                self.parent.add_event( AddObject(
                    HighScoreScreen(
                        self.parent, higher, self.score, self.level_number
                        ),
                    layer = 0
                    ) )
            
            else:
            
                # Request that the parent add a TitleScreen object to its
                # list. Skip the Infukor banner phase on the title screen.
                self.parent.add_event( AddObject(
                    TitleScreen(self.parent, phase = 1), layer = 0
                    ) )
                
                # Release the mouse focus.
                self.release_cursor()
    
    def after_game_over(self):
    
        if not self.parent.find_object(gameobjects.GameObject, layer = 3):
        
            # Fade the background layer and game objects
            self.fade_objects([1, 2])
            
            # Create blank background behind the starry background.
            self.parent.add_object(
                gameobjects.BlankBackground(self.parent, (0, 0, 0)),
                layer = 1, index = 0
                )
            
            self.game_state = "after game"
    
    def game_over(self):
    
        # Fade the labels.
        self.fade_objects([3])
        
        # Create game over text.
        self.parent.add_object(
            gameobjects.TemporaryText(
                self.parent,
                ( self.config.screen_size[0]/2,
                  self.config.screen_size[1]/2 - self.config.game_title_size ),
                self.config.game_over_text,
                self.config.game_title_size,
                colour = (191, 191, 191),
                fading = "in"
                ),
                layer = 3
            )
        
        self.game_state = "after game over"
        
        # Enable garbage collection.
        gc.enable()
    
    def leaving_level(self):
    
        # Fade all the uncontrolled friendly game objects.

        objects = self.parent.find_object(
            gameobjects.GameObject, layer = 2, all = 1
            )

        for object in objects:

            if isinstance(object, gameobjects.Friend) and \
                object.controlled != 1:

                object.fading = "out"

        # Stop scrolling.
        self.current_level.set_scroll_direction(None)

        # Run the garbage collector.
        gc.collect()

        # Increase the level number.
        self.level_number = self.level_number + 1

        # Start the next level.
        self.game_state = "initialise"

    def playing_level(self):

        # Update the level.
        if self.current_level.update_level():

            # Go to the next level.
            self.game_state = "next level"
    
    def starting_level(self):

        # Disable garbage collection.
        gc.disable()
        
        # Playing the level
        self.game_state = "playing"
    
    def initialise_level(self):
    
        # Create introductory text.
        self.parent.add_object(
            gameobjects.TemporaryText(
                self.parent,
                ( self.config.screen_size[0]/2,
                  self.config.screen_size[1]/2 - self.config.title_size ),
                self.config.game_level_intro_text % self.level_number,
                self.config.game_title_size,
                colour = (191, 191, 191)
                ),
                layer = 3
            )
        
        # Create a Level object.
        self.current_level = level.Level(self.parent, self.level_number)
        
        # Retrieve the level text for the current level.
        level_text = self.current_level.create_level()
        
        if level_text != None:
        
            # Create level subtitle text.
            self.parent.add_object(level_text, layer = 3)
        
        # Add a starship if none exists.
        if self.controlled == []:
        
            if self.lives > 0:
            
                self.new_starship()
            
            else:
            
                self.game_state = "game over"
                return
        
        # Start the level.
        self.game_state = "starting"
    
    def start_game(self):
    
        # Create background if necessary.
        if not self.parent.find_object(gameobjects.GameObject, layer = 1):
        
            self.parent.add_object(
                gameobjects.StarryBackground(self.parent),
                layer = 1, index = 0
                )
        
        # Create a score text label object at the top left of the screen.
        self.parent.add_object( gameobjects.GameText(
            self.parent, (4, 4), self.config.game_score_text,
            self.config.game_text_size, (127, 127, 0),
            align = "NW"
            ), layer = 3 )
        
        # Create a score text object at the top left of the screen.
        self.score_text = gameobjects.GameText(
            self.parent, (4, 2 + self.config.game_text_size), str(self.score),
            self.config.game_text_size, (127, 0, 0),
            align = "NW"
            )
        
        # Add the score object to the parent's object list.
        self.parent.add_object(self.score_text, layer = 3)
        
        # Add a life indicator label at the top right of the screen.
        self.parent.add_object( gameobjects.GameText(
            self.parent, (self.config.screen_size[0], 4),
            self.config.game_lives_text,
            self.config.game_text_size, (127, 127, 0),
            align = "NE"
            ), layer = 3 )
        
        # Add a life indicator.
        yscale = float(self.config.game_text_size) / \
            self.resources.images["starship"].get_height()
        
        self.life_image = gameobjects.GameImage(
            self.parent, "starship",
            (self.config.screen_size[0] - 8, 8 + self.config.game_text_size),
            scale = yscale, align = "NE"
            )
        
        self.life_indicator = gameobjects.GameText(
            self.parent,
            ( self.config.screen_size[0] - \
                (yscale * self.resources.images["starship"].get_width()),
              2 + self.config.game_text_size ),
            str(self.lives),
            self.config.game_text_size, (127, 0, 0),
            align = "NE"
            )
        
        # Add the life indicator to the parent's object list.
        self.parent.add_object(self.life_image, layer = 3)
        self.parent.add_object(self.life_indicator, layer = 3)
        
        # Create a music object.
        #self.music = music.Music(self.resources)
        
        # Set up the music.
        #self.music.setup_music( int(self.config.updaterate) / 8, 16 )
        
        # Start the music.
        #self.music.start_music()
        
        # Initialise the level.
        self.game_state = "initialise"
    
    def new_starship(self):
    
        # Create a starship object.
        starship = gameobjects.Starship(
            self.parent,
            (self.config.screen_size[0]/2, self.config.screen_size[1]/2)
            )
        
        # Add the new object to the parent's object list.
        self.parent.add_object(starship, layer = 2, index = -1)
        
        # Remember this object.
        self.controlled.append(starship)
        
        # Decrement the number of lives.
        self.lives = self.lives - 1
        
        # Update the life indicator.
        self.life_indicator.set_text(str(self.lives))



class HighScoreScreen(GameManager):

    characters = \
    (
      ( "A", "B", "C", "D", "E", "F" ),
      ( "G", "H", "I", "J", "K", "L" ),
      ( "M", "N", "O", "P", "Q", "R" ),
      ( "S", "T", "U", "V", "W", "X" ),
      ( "Y", "Z", " ", ".", "Del", "End" )
    )
    
    colours = \
    (
      ( (191, 191, 191), (127, 127, 191), (191, 191, 191),
        (191, 191, 191), (191, 191, 191), (191, 191, 127) ),
      ( (191, 191, 191), (127, 191, 191), (191, 191, 191),
        (127, 191, 127), (191, 191, 191), (191, 191, 191) ),
      ( (191, 191, 127), (191, 191, 191), (127, 127, 191),
        (191, 191, 127), (127, 191, 191), (191, 191, 191) ),
      ( (127, 127, 191), (191, 191, 191), (127, 191, 191),
        (191, 191, 191), (191, 127, 127), (191, 191, 191) ),
      ( (191, 127, 127), (191, 191, 191), (127, 127, 191),
        (191, 191, 191), (191, 191, 63), (191, 63, 63) ),
    )
    
    def __init__(self, parent, index, score, level):
    
        GameManager.__init__(self, parent)
        
        # Set some properties.
        
        self.index = index
        self.score = score
        self.name = ""
        self.level = level
        
        # We are starting the name entry.
        self.game_state = "starting"
    
    def event_handler(self, event):
    
        actions = []
        
        if isinstance(event, KeyPress):
        
            if event.key == self.config.key_pause:
            
                # Pause the application.
                self.parent.pause = 1
                
                # Release the mouse focus.
                self.release_cursor()
            
            elif event.key == self.config.key_unpause:
            
                # Pause the application.
                self.parent.pause = 0
                
                # Grab the mouse focus.
                self.grab_cursor()
            
            elif event.key == self.config.key_exit:
            
                # Return to the title screen.
                
                # Set the exiting flag.
                self.game_state = "exiting"
                
                # Start fading the objects.
                self.fade_objects()
        
        elif isinstance(event, GameObjectDestroyed):
        
            # Record the alpha component of the destroyed object.
            alpha = event.gameobject.alpha
            
            # Create an explosion.
            self.parent.add_object(
                gameobjects.Explosion(
                    self.parent, event.gameobject.position, alpha = alpha
                    ),
                layer = 3, index = -1
                )
            
            if isinstance(event.gameobject, gameobjects.HighScoreCharacter):
            
                # Add this character to the high score name.
                text = event.gameobject.text
                
                if text == self.config.game_high_end_text:
                
                    if self.game_state == "entering":
                    
                        self.game_state = "leaving"
                
                elif text == self.config.game_high_del_text:
                
                    self.name = self.name[:-1]
                    
                    # Reset the colour.
                    self.high_name.colour = (191, 191, 191)
                    
                    # Set the label text.
                    self.high_name.set_text(self.name)
                
                elif len(self.name) < self.config.high_name_max_length:
                
                    self.name = self.name + text
                    
                    # Change the colour if the maximum number of characters
                    # has been reached.
                    if len(self.name) == self.config.high_name_max_length:
                    
                        self.high_name.colour = (255, 63, 63)
                    
                    # Set the label text.
                    self.high_name.set_text(self.name)
        
        return actions
    
    def update(self):
    
        if self.game_state == "exiting":
        
            # Exiting
            self.exiting_screen()
        
        elif self.game_state == "left":
        
            # Left
            self.left()
        
        elif self.game_state == "leaving":
        
            # Leaving
            self.leaving()
        
        elif self.game_state == "entering":
        
            # Entering text
            self.entering()
        
        elif self.game_state == "starting":
        
            # Starting input
            self.starting()
    
    def exiting_screen(self):
    
        # Just check that the background has been removed as the
        # other objects should fade faster than it.
        if not self.parent.find_object(gameobjects.GameObject, layer = 1 ):
        
            # Remove all objects in the other layers.
            self.parent.objects[1:4] = [[], [], []]
            
            # Request that the parent remove this object from its
            # list.
            self.parent.add_event( RemoveObject(self) )
            
            # Request that the parent add a TitleScreen object to its
            # list. Skip the Infukor banner phase on the title screen.
            self.parent.add_event( AddObject(
                TitleScreen(self.parent, phase = 1), layer = 0
                ) )
            
            # Release the mouse focus.
            self.release_cursor()
    
    def left(self):
    
        if not self.parent.find_object(gameobjects.GameObject, layer = 2):
        
            # Set the entry in the high score table.
            self.config.high_scores.insert(
                self.index,
                ( str(self.score), self.name, str(self.level))
                )
            
            self.config.high_scores = self.config.high_scores[:10]
            
            # Remove the blank background.
            self.parent.objects[1] = []
            
            # Request that the parent remove this object from its
            # list.
            self.parent.add_event( RemoveObject(self) )
            
            # Request that the parent add a TitleScreen object to its
            # list. Skip the Infukor banner phase on the title screen.
            self.parent.add_event( AddObject(
                TitleScreen(self.parent, phase = 1), layer = 0
                ) )
            
            # Release the mouse focus.
            self.release_cursor()
    
    def leaving(self):
    
        # Fade the background layer, game objects and labels.
        self.fade_objects([1, 2, 3])
        
        # Create blank background behind the starry background.
        self.parent.add_object(
            gameobjects.BlankBackground(self.parent, (0, 0, 0)),
            layer = 1, index = 0
            )
        
        self.game_state = "left"
    
    def entering(self):
    
        pass
    
    def starting(self):
    
        # Define the background layer object and add it to the parent's
        # background layer.
        self.parent.add_object(
            gameobjects.StarryBackground(self.parent), layer = 1, index = 0
            )
        
        # Create a message.
        self.parent.add_object( gameobjects.TitleText(
            self.parent,
            ( self.config.screen_size[0]/2, self.config.screen_size[1]/8 ),
            self.config.game_high_text, self.config.title_size,
            scale_radius = 0.025, scale_angular_speed = 33.0
            ),
            layer = 3
            )
        
        # Add some characters.
        dy = 0.5 / (len(self.characters) - 1)
        y = 0.25
        
        for i in range(len(self.characters)):
        
            line = self.characters[i]
            dx = 0.5 / (len(line) - 1)
            x = 0.25
            
            for j in range(len(line)):
            
                self.parent.add_object( gameobjects.HighScoreCharacter(
                    self.parent,
                    ( self.config.screen_size[0] * x,
                      self.config.screen_size[1] * y ),
                    self.characters[i][j],
                    self.config.high_text_size,
                    scale_radius = 0.05, scale_angular_speed = 66.0,
                    scale_angle = 360.0 * (x + y),
                    colour = self.colours[i][j]
                    ),
                    layer = 2
                    )
                
                x = x + dx
            
            y = y + dy
        
        # The player's name.
        self.high_name = gameobjects.TitleText(
            self.parent,
            ( self.config.screen_size[0]/2, (7*self.config.screen_size[1])/8 ),
            "", self.config.high_text_size,
            scale_radius = 0.025, scale_angular_speed = 33.0
            )
        
        self.parent.add_object(self.high_name, layer = 3, index = -1)
        
        # Add a starship.
        self.parent.add_object( gameobjects.Starship(
            self.parent,
            (self.config.screen_size[0]/2, self.config.screen_size[1]/2)
            ),
            layer = 2, index = -1
            )
        
        self.game_state = "entering"
