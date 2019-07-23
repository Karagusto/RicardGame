
"""
gameobjects.py

Game object and text label object definitions for Space Explorer.

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

import math, objects, random, string
from events import *


degtorad = math.pi / 180.0

# Set random seed from current time.
random.seed()


#alien_chars = \
#[
#    ((0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0), (0.0, 0.0)),
#    ((0.1, 0.3), (0.3, 0.1), (0.9, 0.1), (0.9, 0.9), (0.1, 0.9), (0.1, 0.3)),
#    ((0.5, 0.2), (0.8, 0.2), (0.8, 0.5), (0.5, 0.2)),
#    ((0.4, 0.2), (0.7, 0.5), (0.5, 0.7), (0.4, 0.7), (0.4, 0.2)),
#    ((0.3, 0.6), (0.3, 0.5), (0.5, 0.5), (0.3, 0.7), (0.4, 0.8), (0.8, 0.8),
#     (0.8, 0.6), (0.4, 0.6)),
#    ((0.2, 0.2), (0.6, 0.2), (0.8, 0.5), (0.6, 0.8), (0.2, 0.8), (0.2, 0.2)),
#]

alien_chars = \
[
    ((0.0, 0.0), (0.2, 0.2), (0.0, 0.4), (0.2, 0.6)),
    ((0.1, 0.0), (0.3, 0.2), (0.5, 0.0), (0.7, 0.2)),
    ((0.2, 0.3), (0.1, 0.4), (0.3, 0.6), (0.1, 0.8)),
    ((0.5, 0.1), (0.7, 0.3), (0.9, 0.1), (1.0, 0.2)),
    ((0.2, 0.0), (0.3, 0.1), (0.4, 0.0)),
    ((0.6, 0.0), (0.7, 0.1), (0.8, 0.0)),
    ((0.7, 0.2), (0.8, 0.1), (0.9, 0.0), (1.0, 0.1)),
    ((0.2, 0.3), (0.3, 0.2)),
    ((0.0, 0.1), (0.1, 0.2), (0.0, 0.3)),
    ((0.0, 0.5), (0.1, 0.6), (0.0, 0.7)),
    ((0.2, 0.6), (0.0, 0.8), (0.1, 0.9)),
    ((0.0, 1.0), (0.1, 0.9)),
    ((0.1, 1.0), (0.3, 0.8), (0.5, 1.0), (0.7, 0.8)),
    ((0.2, 1.0), (0.3, 0.9), (0.4, 1.0)),
    ((0.6, 1.0), (0.8, 0.8), (0.7, 0.7), (0.5, 0.9)),
    ((0.5, 0.9), (0.3, 0.7), (0.1, 0.9)),
    ((0.7, 1.0), (0.8, 0.9), (0.9, 1.0), (1.0, 0.9)),
    ((0.8, 0.8), (0.9, 0.9)),
    ((1.0, 0.9), (0.7, 0.6), (0.5, 0.8), (0.3, 0.6)),
    ((0.5, 0.1), (0.2, 0.4), (0.4, 0.6), (0.5, 0.5)),
    ((0.5, 0.7), (0.7, 0.5), (0.8, 0.6)),
    ((0.4, 0.7), (0.6, 0.5), (0.5, 0.4), (0.4, 0.5)),
    ((1.0, 0.8), (0.9, 0.7), (1.0, 0.6), (0.9, 0.5), (1.0, 0.4), (0.9, 0.3)),
    ((1.0, 0.3), (0.9, 0.2), (0.8, 0.3), (0.9, 0.4), (0.8, 0.5)),
    ((0.8, 0.5), (0.9, 0.6), (0.8, 0.7)),
    ((0.7, 0.3), (0.8, 0.4), (0.7, 0.5), (0.5, 0.3)),
    ((0.7, 0.4), (0.5, 0.2), (0.3, 0.4), (0.4, 0.5)),
    ((0.5, 0.3), (0.4, 0.4))
]

alien_separators = \
[
    ((0.2, 0.5), (0.3, 0.3), (0.5, 0.2), (0.7, 0.3), (0.8, 0.5), (0.7, 0.65),
     (0.5, 0.7), (0.425, 0.6), (0.35, 0.5), (0.425, 0.425), (0.5, 0.35),
     (0.575, 0.475), (0.65, 0.5), (0.575, 0.55), (0.5, 0.6), (0.45, 0.55),
     (0.4, 0.5), (0.45, 0.45), (0.5, 0.4), (0.55, 0.45), (0.6, 0.5),
     (0.55, 0.525), (0.5, 0.55), (0.475, 0.525), (0.45, 0.5), (0.475, 0.475),
     (0.5, 0.45), (0.525, 0.475)),
]


capitals = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
letters = "abcdefghijklmnopqrstuvwxyz"
numbers = "0123456789"
symbols = " !\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"
    

# Game objects -----------------------------------------------------------------

class GameObject:

    def __init__(self, parent, fading = None, max_alpha = 255):
    
        self.parent = parent
        self.config = parent.config
        self.resources = parent.resources
        self.manager = parent.manager
        
        # Fading in/out flag (determine this from the manager object)
        self.fading = fading or self.manager.fading
        
        # Fading in speed (alpha per update)
        self.fade_in_speed = self.config.fade_in_speed
        
        # Fading out speed (alpha per update)
        self.fade_out_speed = self.config.fade_out_speed
        
        # Alpha value
        self.alpha = 0
        
        # Maximum alpha value
        self.max_alpha = max_alpha
        
        # Control flag
        self.controlled = 0
    
    def unlink(self):
    
        # Remove references to the parent and its objects.
        del self.parent
        del self.config
        del self.resources
    
    #def render(self, screen):
    #
    #    pass
    
    def update(self):
    
        pass
    
    def event_handler(self, event):

        return []
    
    def fade(self):
    
        # Change the alpha as required.
        
        if self.fading == "in":
        
            # Fade in the text.
            if self.alpha < self.max_alpha:
            
                # Ensure that the alpha never exceeds the maximum.
                self.alpha = min(
                    self.max_alpha, self.alpha + self.fade_in_speed
                    )
                
                # Set the alpha of the surface.
                if self.rendering != None:
                    self.rendering.set_alpha(self.alpha)
                
                return 1
            
            else:
            
                # No more fading in.
                self.fading = ""
        
        elif self.fading == "out":
        
            # Fade out the text.
            if self.alpha > 0:
            
                # Ensure that the alpha never falls below the minimum.
                self.alpha = max(0, self.alpha - self.fade_out_speed)
                
                # Set the alpha of the surface.
                if self.rendering != None:
                    self.rendering.set_alpha(self.alpha)

                return 1
            
            elif self.alpha == 0:
            
                # Request that this object be deleted.
                self.parent.add_event( RemoveObject(self) )
        
        # No updates required.
        return 0



# Background objects -----------------------------------------------------------

class Background:

    pass

class BlankBackground(GameObject, Background):

    def __init__(self, parent, colour):
    
        GameObject.__init__(self, parent)
        
        self.colour = colour
        self.working_colour = (0, 0, 0)
    
    def render(self, screen):
    
        # Fill the screen background.
        screen.fill(self.working_colour)
    
    def fade(self):
    
        # Change the alpha as required.
        
        if self.fading == "in":
        
            # Fade in the text.
            if self.alpha < 255:
            
                self.alpha = self.alpha + self.fade_in_speed
                
                # Ensure that the alpha never exceeds the maximum.
                if self.alpha > 255: self.alpha = 255
                
                # Set the working colour of the surface.
                self.working_colour = (
                    min(self.alpha, self.colour[0]),
                    min(self.alpha, self.colour[1]),
                    min(self.alpha, self.colour[2])
                    )
                
                return 1
            
            else:
            
                # No more fading in.
                self.fading = ""
        
        elif self.fading == "out":
        
            # Fade out the text.
            if self.alpha > 0:
            
                self.alpha = self.alpha - self.fade_out_speed
                if self.alpha <= 0:
                
                    # Ensure that the alpha never falls below the minimum.
                    self.alpha = 0
                    
                # Set the working colour of the surface.
                self.working_colour = (
                    min(self.alpha, self.colour[0]),
                    min(self.alpha, self.colour[1]),
                    min(self.alpha, self.colour[2])
                    )

                return 1
            
            elif self.alpha == 0:
            
                # Request that this object be deleted.
                self.parent.add_event( RemoveObject(self) )
        
        # No updates required.
        return 0
    
    def update(self):
    
        self.fade()



class StarryBackground(BlankBackground):

    def __init__(self, parent):
    
        BlankBackground.__init__(self, parent, (0, 0, 0))
        
        self.centre = (
            self.config.screen_size[0]/2, self.config.screen_size[1]/2
            )
        
        self.angle = 0.0
        self.scale = 1.0
        self.alpha = 0
        
        # Set the number of stars and a list for their positions.
        self.number_of_colours = self.config.number_of_star_colours
        self.colours = []
        self.stars_per_colour = self.config.number_of_stars_per_colour
        self.number_of_stars = self.number_of_colours * self.stars_per_colour
        self.stars = []
        
        # The star to be changed.
        self.next_star = 0
        
        # Direction of motion
        self.direction = (0, 0)
        
        # Star to be recoloured
        self.recolour = 0
        
        self.colour_cycle = (
            (255, 255, 255), (255, 255, 0), (255, 0, 0),
            (0, 0, 0), (255, 0, 0), (255, 255, 0)
            )
        
        self.max_colours = len(self.colour_cycle)
        
        #self.star = objects.ImageObject(
        #    self.resources.images["star"],
        #    colorkey = (0, 0, 0)
        #    )
        
        # Draw the stars on a rendering surface.
        self.initialise_surface()
        
        # Create the working rendering surface.
        self.prepare_surface()
    
    def initialise_surface(self):
    
        # Define colours and positions for the stars.
        stars = self.number_of_stars
        colours = self.number_of_colours
        
        width = self.config.screen_size[0]
        height = self.config.screen_size[1]
        
        # Create a rendering surface.
        self.surface = pygame.Surface(
            (width, height), SRCALPHA
            )

        # Clear the surface.
        self.surface.fill( (0, 0, 0) )
        
        # Render the stars and remember their positions.
        while colours > 0:
        
            colour = random.randrange(0, len(self.colour_cycle))
            self.colours.append( colour )
            
            colours = colours - 1
            
            i = self.stars_per_colour
            
            while i > 0:
            
                x = random.randrange(0, width)
                y = random.randrange(0, height)
                
                self.stars.append( (x, y) )
                
                self.surface.fill( self.colour_cycle[colour], ( x, y, 1, 1 ) )
                
                stars = stars - 1
                i = i - 1
    
    def prepare_surface(self):
    
        # Rotate and scale the image.
        
        if self.scale != 1.0:
            self.rendering = pygame.transform.rotozoom(
                self.surface, self.angle, self.scale
                )
        elif self.angle != 0.0 and self.scale == 1.0:
            self.rendering = pygame.transform.rotate(
                self.surface, self.angle
                )
        else:
            self.rendering = self.surface
        
        # Set the alpha of the surface.
        self.rendering.set_alpha(self.alpha)
    
    def render(self, screen):
    
        "Render the effect onto the 'screen'."
        
        BlankBackground.render(self, screen)
        
        size = self.rendering.get_size()
        
        position = (
            self.centre[0] - size[0] / 2,
            self.centre[1] - size[1] / 2
            )
        
        screen.blit(self.rendering, position)
    
    def update(self):
    
        # Update the stars.
        
        colour = 0
        star = 0
        
        width = self.surface.get_width()
        height = self.surface.get_height()
        
        i = 0
        
        while star < self.number_of_stars:
        
            if i == 0:
            
                c = self.colour_cycle[self.colours[colour]]
                colour = colour + 1
            
            # For each star, erase it and choose a new position.
            x, y = self.stars[star]

            self.surface.fill(
                (0, 0, 0), ( x, y, 1, 1 )
                )

            x = (x + self.direction[0]) % width
            y = (y + self.direction[1]) % height

            self.stars[star] = (x, y)

            self.surface.fill( c, ( x, y, 1, 1 ) )

            star = star + 1
            i = (i + 1) % self.stars_per_colour

        # Change the colour of a star.
        c = self.colours[self.recolour]
        self.colours[self.recolour] = (c + 1) % self.max_colours

        self.recolour = (self.recolour + 1) % self.number_of_colours

        # Fade the object as required.
        self.fade()

        self.prepare_surface()



class Friend:

    pass

# Derive Starship from GameObject after objects.ImageObject to ensure that
# objects.ImageObject's render method overrides the one from GameObject.

class Starship(objects.AnimatedImage, GameObject, Friend):

    def __init__(self, parent, position, target_positions = None,
                       displace = (0, 0), controlled = 1):
    
        GameObject.__init__(self, parent)

        # Displacement from the position given
        self.displace = displace
        
        if controlled == 1:
        
            # Initialise an animated image object for invulnerable starships.
            
            objects.AnimatedImage.__init__( self,
                ( self.resources.images["istarship1"],
                  self.resources.images["istarship2"],
                  self.resources.images["istarship3"],
                  self.resources.images["istarship4"] ),
                position = position,
                angle = 0.0, alpha = 0.0,
                colorkey = (0, 0, 0),
                frame_delay = int(self.config.updaterate / 12)
                )
        
        else:
        
            objects.AnimatedImage.__init__( self,
                ( self.resources.images["starship"], ),
                position = position,
                angle = 0.0, alpha = 0.0,
                colorkey = (0, 0, 0)
                )
        
        # Target position and angle
        self.target_positions = target_positions or []
        self.target_position = self.position
        
        self.target_angle = self.angle
        
        # Maximum speed and rotational speed
        self.image_size = self.images[0].get_size()
        self.max_speed = int( min(self.image_size[0], self.image_size[1]) / 4 )
        self.max_rot_speed = 30.0
        
        # Firing speed
        self.reload_frames = int(self.config.updaterate / 2)
        self.reload = 0
        
        # Control flag
        self.controlled = controlled
        
        # Invulnerability (for five seconds)
        self.invulnerability = self.config.updaterate * 5
    
    def update(self):
    
        # Updating
        
        to_update = 0
        
        # Count down the invulnerability.
        if self.controlled == 1 and self.invulnerability > 0:
        
            self.invulnerability = self.invulnerability - 1
            
            if self.invulnerability == 0:
            
                # Change the starship image.
                self.frame = 0
                self.images = (self.resources.images["starship"],)
                self.initialise_surface()
                to_update = 1
        
        # Input checks
        
        if pygame.mouse.get_focused() and self.controlled == 1:
        
            # Read the mouse position and buttons state.
            mouse_position = pygame.mouse.get_pos()
            mouse_buttons = pygame.mouse.get_pressed()
            
            # Determine the angle depending on the relative positions of the
            # mouse cursor and the starship.
            x = mouse_position[0] - self.position[0]
            y = mouse_position[1] - self.position[1]
            
            # The angle in the screen coordinate system.
            angle = math.atan2(y, x)
            
            if x != 0 or y != 0:
            
                # Translate the angle to the coordinate system used to
                # orientate the image.
                self.target_angle = int(270.0 - (angle/degtorad))
            
            keys = pygame.key.get_pressed()
            
            if keys[self.config.key_move] or \
                mouse_buttons[self.config.mouse_move_button]:
            
                # Set the new target position.
                self.target_position = (
                    int(mouse_position[0] + self.displace[0]),
                    int(mouse_position[1] + self.displace[1])
                    )
                
                # Create or move the target cursor.
                cursor = self.parent.find_object(TargetCursor, layer = 3)
                
                if not cursor:
                
                    # Add a target cursor only if the starship is the main
                    # starship in a formation.
                    
                    if self.displace == (0, 0):
                    
                        self.parent.add_event( AddObject(
                            TargetCursor(
                                self.parent, mouse_position
                                ),
                                layer = 3
                            ) )

                else:
                
                    cursor.position = mouse_position
            
            if keys[self.config.key_fire] or \
                mouse_buttons[self.config.mouse_fire_button]:
                
                if self.reload == 0 and self.fading == "":
                
                    # Fire a projectile.
                    
                    # * Using the add event rather than adding an object
                    # to the parent's list means that the list is extended
                    # outside the rendering loop. This hopefully prevents
                    # annoying delays and jumps every time a projectile is
                    # fired.
                    
                    self.parent.add_event( AddObject(
                        Fire(
                            self.parent, self.position, self.angle
                            ),
                            layer = 2, index = 0
                        ) )
                    
                    # Play a sound.
                    if self.resources.sound_status:
                    
                        self.resources.samples["laser"].play()
                    
                    # Set the number of frames required to reload.
                    self.reload = self.reload_frames
        
        elif self.controlled != 1:
        
            if self.position == self.target_position:
            
                if len(self.target_positions) > 0:
                
                    new_position = self.target_positions.pop(0)
                    
                    self.target_position = (
                        new_position[0] + self.displace[0],
                        new_position[1] + self.displace[1]
                        )
                
                else:
                
                    # The starship has reached its a target position. If it
                    # was previously captured (self.controlled = 2) then it
                    # is now available to be recaptured.
                    self.controlled = 0
        
        # Reloading
        if self.reload > 0:
        
            self.reload = self.reload - 1
        
        # Determine the direction of any motion.
        dx = int(self.target_position[0] - self.position[0])
        dy = int(self.target_position[1] - self.position[1])
        
        if dx != 0 or dy != 0:
        
            angle = math.atan2(dy, dx)
            
            distance = math.sqrt(dy**2 + dx**2)
            
            if self.controlled == 1:
            
                speed = max(1.0, min( distance, self.max_speed ) )
            
            else:
            
                speed = max(1.0, min( distance, self.max_speed / 2 ) )
            
            # Move the ship.
            self.position = (
                self.position[0] + (speed * math.cos(angle)),
                self.position[1] + (speed * math.sin(angle))
                )
            
            to_update = 1
        
        else:
        
            # Set the starship position to the target position.
            self.position = self.target_position
            
            # Remove the target cursor if this starship is controlled.
            if self.controlled == 1:
            
                if self.displace == (0, 0):
                
                    cursor = self.parent.find_object(TargetCursor, layer = 3)
                    
                    if cursor:
                    
                        self.parent.remove_object(cursor, layer = 3)
        
        if int(self.angle) != self.target_angle:
        
            change = self.target_angle - self.angle
            
            if change < -180.0:
                change = change + 360.0
            elif change >= 180.0:
                change = change - 360.0
            
            if change > 0.0:
            
                speed = max(1.0, min( change, self.max_rot_speed ) )
            
            else:
            
                speed = min(-1.0, max( change/2.0, -self.max_rot_speed ) )
            
            # Rotate the ship.
            self.angle = self.angle + speed
            
            if self.angle < 0.0:
            
                self.angle = self.angle + 360.0
            
            elif self.angle >= 360.0:
            
                self.angle = self.angle - 360.0
            
            to_update = 1
        
        # Fade the object as required.
        if self.fade():
        
            to_update = 1
        
        if len(self.images) > 1:
        
            # Move to the next frame in the animation.
            self.next_frame()
            to_update = 1
        
        if to_update:
        
            # Prepare the rendering surface.
            self.prepare_surface()
        
        # Check for starships and gateways.
        if self.controlled == 1:
        
            hits = self.parent.collide_object(
                self, Starship, layer = 2, all = 1
                )
            
            for hit in hits:
            
                if hit != self and hit.controlled == 0 and hit.fading != "out":
                
                    #print "recaptured", hit, hit.controlled
                    # Notify the Gameplay object that a starship has been
                    # recaptured.
                    self.parent.add_event( Recaptured(hit) )
                    
                    # Play a sound.
                    if self.resources.sound_status:
                        self.resources.samples["recovered"].play()
                    
                    # Increase the player's score.
                    self.parent.add_event( AddScore(10) )
            
            # Only check for gateways if the starship is stationary.
            if self.position == self.target_position:
            
                hit = self.parent.collide_object(
                    self, Gateway, layer = 2
                    )
                
                if hit:
                
                    # Notify the manager object that a gateway has been entered.
                    self.parent.add_event( EnteredGateway(hit) )



# Derive Fire from GameObject after objects.ImageObject to ensure that
# objects.ImageObject's render method overrides the one from GameObject.

class Fire(objects.ImageObject, GameObject):

    def __init__(self, parent, position, angle):
    
        GameObject.__init__(self, parent)
        
        # Initialise the image object.
        objects.ImageObject.__init__( self,
            self.resources.images["fire"],
            position = position, alpha = 0.0,
            angle = angle, colorkey = (0, 0, 0)
            )
        
        # Fading in speed (alpha per update)
        self.fade_in_speed = 255
        
        # Set the velocity from the angle given and the speed.
        self.image_size = self.image.get_size()
        speed = min(self.image_size[0], self.image_size[1])
        
        # The angle must be in radians.
        self.velocity = (
            speed * math.cos((270 - angle) * degtorad),
            speed * math.sin((270 - angle) * degtorad)
            )
        
        # Store a rectangle outside which projectiles will not appear.
        self.screen_rect = self.parent.screen.get_rect()
        self.screen_rect[0] = self.screen_rect[0] - 32
        self.screen_rect[1] = self.screen_rect[1] - 32
        self.screen_rect[2] = self.screen_rect[2] + 64
        self.screen_rect[3] = self.screen_rect[3] + 64
    
    def update(self):
    
        # If the object is off-screen then request for it to be deleted.
        if not self.screen_rect.collidepoint(self.position):
        
            self.parent.add_event( RemoveObject(self) )
        
        # Move the fire.
        self.position = (
            self.position[0] + self.velocity[0],
            self.position[1] + self.velocity[1]
            )
        
        # Fade the object as required.
        if self.fade():
        
            # Prepare the rendering surface for rendering.
            self.prepare_surface()



# Aliens

class Alien(objects.ImageObject, GameObject):

    def __init__(self, parent, position, target_positions = None,
                       displace = (0, 0)):
    
        GameObject.__init__(self, parent)
        
        # Object position
        self.position = (
            position[0] + displace[0],
            position[1] + displace[1]
            )
        
        # Displacement from the position given
        self.displace = displace
        
        # Target positions
        self.target_positions = target_positions or []
        self.target_position = (
            self.position[0] + self.displace[0],
            self.position[1] + self.displace[1]
            )
    
    def set_decision_timer(self):
    
        self.decision_timer = self.decision_time * self.config.updaterate
    
    def fade(self):
    
        # Change the alpha as required.
        
        if self.fading == "in":
        
            to_update = 0
            
            # Fade in the text.
            if self.alpha < 255:
            
                self.alpha = self.alpha + self.fade_in_speed
                
                # Ensure that the alpha never exceeds the maximum.
                if self.alpha > 255: self.alpha = 255
                
                # Set the alpha of the surface.
                if self.rendering != None:
                    self.rendering.set_alpha(self.alpha)
                
                to_update = 1
            
            # Scale the object as required.
            if self.scale > 1.0:
            
                self.scale = self.scale - 0.05
                
                if self.scale < 1.0:
                
                    self.scale = 1.0
                
                to_update = 1
            
            if self.scale == 1.0 and self.alpha == 255:
            
                # No more fading in.
                self.fading = ""
            
            return to_update
        
        elif self.fading == "out":
        
            # Fade out the text.
            if self.alpha > 0:
            
                self.alpha = self.alpha - self.fade_out_speed
                if self.alpha <= 0:
                
                    # Ensure that the alpha never falls below the minimum.
                    self.alpha = 0
                    
                # Set the alpha of the surface.
                if self.rendering != None:
                    self.rendering.set_alpha(self.alpha)
            
                return 1
            
            elif self.alpha == 0:
            
                # Request that this object be deleted.
                self.parent.add_event( RemoveObject(self) )
        
        # No updates required.
        return 0



class StartStop(Alien):

    def __init__(self, parent, position, target_positions = None,
                       displace = (0, 0)):
    
        Alien.__init__(
            self, parent, position, target_positions = target_positions,
            displace = displace
            )
        
        # Initialise the image object.
        objects.ImageObject.__init__( self,
            self.resources.images["alien1"],
            position = position,
            angle = 0.0, alpha = 0.0,
            colorkey = (0, 0, 0), scale = 2.0
            )
        
        # Target object
        self.target_object = None
        
        # Decision states
        self.decision = "aim"
        self.decision_time = 1.0
        
        # Set the decision timer.
        self.set_decision_timer()
        
        # Maximum speed
        self.image_size = self.image.get_size()
        self.max_speed = int( min(self.image_size[0], self.image_size[1]) / 8 )
        
        # Alien value
        self.value = 1
    
    def update(self):
    
        # Updating
        
        to_update = 0
        
        if self.decision == "think" and self.fading != "in":
        
            # Thinking
            self.decision_timer = self.decision_timer - 1
            
            if self.decision_timer <= 0:
            
                # Reset decision timer.
                self.set_decision_timer()
                
                # Look for a target object.
                objects = self.parent.find_object(
                    Starship, layer = 2, all = 1
                    )
                
                self.target_object = None
                
                for object in objects:
                
                    if object.controlled == 1:
                    
                        self.target_object = object
                        break
                
                if self.target_object:
                
                    # Set a new target position.
                    self.target_positions.append(self.target_object.position)
                    
                    # Return here after reaching the target position.
                    self.target_positions.append(
                        (
                            self.position[0] - self.displace[0],
                            self.position[1] - self.displace[1]
                        ) )
                    
                    self.decision = "aim"
                
                else:
                
                    self.decision = "think"
        
        if self.decision == "aim":
        
            if len(self.target_positions) > 0:
            
                # Set the new target position.
                new_position = self.target_positions.pop(0)
                
                self.target_position = (
                    new_position[0] + self.displace[0],
                    new_position[1] + self.displace[1]
                    )
            
                self.decision = "act"
            
            else:
            
                self.decision = "think"
        
        if self.decision == "act":
        
            # Acting
            
            # Check that the target object is in the same general direction
            # as expected.
            
            # Determine the direction of any motion.
            dx = int(self.target_position[0] - self.position[0])
            dy = int(self.target_position[1] - self.position[1])
            
            if dx != 0 or dy != 0:
            
                angle = math.atan2(dy, dx)
                
                distance = math.sqrt(dy**2 + dx**2)
                
                speed = max(1.0, min( distance, self.max_speed ) )
                
                # Move the alien.
                self.position = (
                    self.position[0] + (speed * math.cos(angle)),
                    self.position[1] + (speed * math.sin(angle))
                    )
                
                to_update = 1
            
            else:
            
                # The alien has reached its target position.
                self.decision = "aim"
                self.target_object = None
        
        # Fade the object as required.
        if self.fade():
        
            to_update = 1
        
        if to_update:
        
            # Prepare the rendering surface.
            self.prepare_surface()
        
        # Check for collisions.
        if self.fading != "in":
        
            hit = self.parent.collide_object(self, Starship, layer = 2)
            
            if hit and hit.invulnerability == 0 and hit.controlled == 1:
            
                # Notify the Gameplay object that a starship has been destroyed.
                self.parent.add_event( GameObjectDestroyed(hit) )
                
                # Notify the Gameplay object that this object has been destroyed.
                self.parent.add_event( GameObjectDestroyed(self) )
        
        # Check for projectiles.
        hit = self.parent.collide_object(self, Fire, layer = 2)
        
        if hit:
        
            # Notify the Gameplay object that an alien has been destroyed.
            self.parent.add_event( GameObjectDestroyed(self) )
            
            # Remove this object (usually an event would be used).
            self.parent.remove_object( hit, layer = 2 )
    


class Follower(Alien):

    def __init__(self, parent, position, target_positions = None,
                       displace = (0, 0)):
    
        Alien.__init__(
            self, parent, position, target_positions = target_positions,
            displace = displace
            )
        
        # Initialise the image object.
        objects.ImageObject.__init__( self,
            self.resources.images["alien2"],
            position = position,
            angle = 0.0, alpha = 0.0,
            colorkey = (0, 0, 0), scale = 2.0
            )
        
        # Target object
        self.target_object = None
        
        # Decision states
        self.decision = "aim"
        self.decision_time = 1.5

        # Set decision timer.
        self.set_decision_timer()
        
        # Maximum speed
        self.image_size = self.image.get_size()
        self.max_speed = int( min(self.image_size[0], self.image_size[1]) / 8 )
        self.slow_speed = max( self.max_speed - 0.5, 1 )
        
        # Alien value
        self.value = 2
    
    def update(self):
    
        # Updating
        
        to_update = 0
        
        if self.decision == "think" and self.fading != "in":
        
            # Thinking
            self.decision_timer = self.decision_timer - 1
            
            if self.decision_timer <= 0:
            
                # Reset decision timer.
                self.set_decision_timer()
                
                # Look for a target object.
                objects = self.parent.find_object(
                    Starship, layer = 2, all = 1
                    )
                
                self.target_object = None
                
                for object in objects:
                
                    if object.controlled == 1:
                    
                        self.target_object = object
                        break
                
                if self.target_object:
                 
                    # Set a new target position.
                    self.target_positions.append(self.target_object.position)
                    
                    # Return here after reaching the target position.
                    self.target_positions.append(
                        (
                            self.position[0] - self.displace[0],
                            self.position[1] - self.displace[1]
                        ) )
                    
                    self.decision = "aim"
                
                else:
                
                    self.decision = "think"
        
        if self.decision == "aim":
        
            if len(self.target_positions) > 0:
            
                # Set the new target position.
                new_position = self.target_positions.pop(0)
                
                self.target_position = (
                    new_position[0] + self.displace[0],
                    new_position[1] + self.displace[1]
                    )
            
                self.decision = "act"
            
            else:
            
                self.decision = "think"
        
        if self.decision == "act":
        
            # Acting
            
            # Determine the direction of any motion.
            
            if self.target_object:
            
                dx = int(
                    self.target_object.position[0] + self.displace[0] - \
                    self.position[0]
                    )
                dy = int(
                    self.target_object.position[1] + self.displace[1] - \
                    self.position[1]
                    )
                
                speed = self.slow_speed
                
                # If the alien is moving away from the target position then
                # retarget it.
                
                if (dx * (self.target_position[0] - self.position[0])) < 0.0:
                
                    if (dy * (self.target_position[1] - self.position[1])) <0.0:
                    
                        # Aim the alien at the next target position in its list
                        # and remove its target object.
                        self.decision = "aim"
                        self.target_object = None
            
            else:
            
                dx = int(self.target_position[0] - self.position[0])
                dy = int(self.target_position[1] - self.position[1])
                
                speed = self.max_speed
            
            if dx != 0 or dy != 0:
            
                angle = math.atan2(dy, dx)
                
                distance = math.sqrt(dy**2 + dx**2)
                
                speed = max(1.0, min( distance, speed ) )
                
                # Move the alien.
                self.position = (
                    self.position[0] + (speed * math.cos(angle)),
                    self.position[1] + (speed * math.sin(angle))
                    )
                
                to_update = 1
            
            else:
            
                # The alien has reached its target position.
                self.decision = "aim"
                self.target_object = None
        
        # Fade the object as required.
        if self.fade():
        
            to_update = 1
        
        if to_update:
        
            # Prepare the rendering surface.
            self.prepare_surface()
        
        # Check for collisions.
        if self.fading != "in":
        
            hit = self.parent.collide_object(self, Starship, layer = 2)
            
            if hit and hit.invulnerability == 0 and hit.controlled == 1:
            
                # Notify the Gameplay object that a starship has been destroyed.
                self.parent.add_event( GameObjectDestroyed(hit) )
                
                # Notify the Gameplay object that this object has been destroyed.
                self.parent.add_event( GameObjectDestroyed(self) )
        
        # Check for projectiles.
        hit = self.parent.collide_object(self, Fire, layer = 2)
        
        if hit:
        
            # Notify the Gameplay object that an alien has been destroyed.
            self.parent.add_event( GameObjectDestroyed(self) )
            
            # Remove this object (usually an event would be used).
            self.parent.remove_object( hit, layer = 2 )



class Interceptor(Alien):

    def __init__(self, parent, position, target_positions = None,
                       displace = (0, 0)):
    
        Alien.__init__(
            self, parent, position, target_positions = target_positions,
            displace = displace
            )
        
        # Initialise the image object.
        objects.ImageObject.__init__( self,
            self.resources.images["alien3"],
            position = position,
            angle = 0.0, alpha = 0.0,
            colorkey = (0, 0, 0), scale = 2.0
            )
        
        # Target object
        self.target_object = None
        
        # Decision states
        self.decision = "aim"
        self.decision_time = 0.75
        
        # Set decision timer.
        self.set_decision_timer()
        
        # Maximum speed
        self.image_size = self.image.get_size()
        self.max_speed = int( min(self.image_size[0], self.image_size[1]) / 8 )
        self.slow_speed = max( self.max_speed, 1 )
        
        # Alien value
        self.value = 3
    
    def update(self):
    
        # Updating
        
        to_update = 0
        
        if self.decision == "think" and self.fading != "in":
        
            # Thinking
            self.decision_timer = self.decision_timer - 1
            
            if self.decision_timer <= 0:
            
                # Reset decision timer.
                self.set_decision_timer()
                
                # Look for a target object.
                objects = self.parent.find_object(
                    Starship, layer = 2, all = 1
                    )
                
                for object in objects:
                
                    if object.controlled == 1:
                    
                        self.target_object = object
                        break
                
                if self.target_object:
                
                    # Set a new target position.
                    self.target_positions.append(
                        (
                            0.5 * (
                                self.target_object.position[0] + \
                                self.target_object.target_position[0]
                                ),
                            0.5 * (
                                self.target_object.position[1] + \
                                self.target_object.target_position[1]
                                )
                        ) )
                    
                    # Return here after reaching the target position.
                    self.target_positions.append(
                        (
                            0.5 * (
                                self.position[0] - self.displace[0] + \
                                self.target_object.target_position[0]
                                ),
                            0.5 * (
                                self.position[1] - self.displace[1] + \
                                self.target_object.target_position[1]
                                )
                        ) )
                    
                    self.decision = "aim"
                
                else:
                
                    self.decision = "think"
        
        if self.decision == "aim":
        
            if len(self.target_positions) > 0:
            
                # Set the new target position.
                new_position = self.target_positions.pop(0)
                
                self.target_position = (
                    new_position[0] + self.displace[0],
                    new_position[1] + self.displace[1]
                    )
            
                self.decision = "act"
            
            else:
            
                self.decision = "think"
        
        if self.decision == "act":
        
            # Acting
            
            # Go to the target object's target position.
            if self.target_object:
            
                speed = self.slow_speed
            
            else:
            
                speed = self.max_speed
            
            # Determine the direction of any motion.
            dx = int(self.target_position[0] - self.position[0])
            dy = int(self.target_position[1] - self.position[1])
            
            if dx != 0 or dy != 0:
            
                angle = math.atan2(dy, dx)
                
                distance = math.sqrt(dy**2 + dx**2)
                
                speed = max(1.0, min( distance, speed ) )
                
                # Move the alien.
                self.position = (
                    self.position[0] + (speed * math.cos(angle)),
                    self.position[1] + (speed * math.sin(angle))
                    )
                
                to_update = 1
            
            else:
            
                # The alien has reached its target position.
                self.decision = "aim"
                self.target_object = None
        
        # Fade the object as required.
        if self.fade():
        
            to_update = 1
        
        if to_update:
        
            # Prepare the rendering surface.
            self.prepare_surface()
        
        # Check for collisions.
        if self.fading != "in":
        
            hit = self.parent.collide_object(self, Starship, layer = 2)
            
            if hit and hit.invulnerability == 0 and hit.controlled == 1:
            
                # Notify the Gameplay object that a starship has been destroyed.
                self.parent.add_event( GameObjectDestroyed(hit) )
                
                # Notify the Gameplay object that this object has been destroyed.
                self.parent.add_event( GameObjectDestroyed(self) )
        
        # Check for projectiles.
        hit = self.parent.collide_object(self, Fire, layer = 2)
        
        if hit:
        
            # Notify the Gameplay object that an alien has been destroyed.
            self.parent.add_event( GameObjectDestroyed(self) )
            
            # Remove this object (usually an event would be used).
            self.parent.remove_object( hit, layer = 2 )



class Capturer(Alien):

    def __init__(self, parent, position, target_positions = None,
                       displace = (0, 0)):
    
        Alien.__init__(
            self, parent, position, target_positions = target_positions,
            displace = displace
            )
        
        # Initialise the image object.
        objects.ImageObject.__init__( self,
            self.resources.images["alien4"],
            position = position,
            angle = 0.0, alpha = 0.0,
            colorkey = (0, 0, 0), scale = 2.0
            )
        
        # Target object
        self.target_object = None
        
        # Captured object
        self.captured = None
        
        # Decision states
        self.decision = "aim"
        self.decision_time = 5.0
        
        # Set decision timer.
        self.set_decision_timer()
        
        # Maximum speed
        self.image_size = self.image.get_size()
        self.max_speed = int( min(self.image_size[0], self.image_size[1]) / 8 )
        
        # Alien value
        self.value = 4
    
    def update(self):
    
        # Updating
        
        to_update = 0
        
        if self.decision == "think" and self.fading != "in":
        
            # Thinking
            self.decision_timer = self.decision_timer - 1
            
            # Reset the alien's captured object status.
            self.captured = None
            
            if self.decision_timer <= 0:
            
                # Reset decision timer.
                self.set_decision_timer()
                
                # Look for a target object.
                objects = self.parent.find_object(
                    Starship, layer = 2, all = 1
                    )
                
                for object in objects:
                
                    if object.controlled == 1:
                    
                        self.target_object = object
                        break
                
                if self.target_object:
                 
                    # Set the new target position.
                    self.target_positions.append(self.target_object.position)
                    
                    # Return here after reaching the target position.
                    self.target_positions.append(
                        (
                            self.position[0] - self.displace[0],
                            self.position[1] - self.displace[1]
                        ) )
                    
                    self.decision = "aim"
                
                else:
                
                    self.decision = "think"
        
        if self.decision == "aim":
        
            if len(self.target_positions) > 0:
            
                # Set the new target position.
                new_position = self.target_positions.pop(0)
                
                self.target_position = (
                    new_position[0] + self.displace[0],
                    new_position[1] + self.displace[1]
                    )
                
                self.decision = "act"
            
            else:
            
                self.decision = "think"
        
        if self.decision == "act":
        
            # Acting
            
            # Check that the target object is in the same general direction
            # as expected.
            
            # Determine the direction of any motion.
            dx = int(self.target_position[0] - self.position[0])
            dy = int(self.target_position[1] - self.position[1])
            
            if dx != 0 or dy != 0:
            
                angle = math.atan2(dy, dx)
                
                distance = math.sqrt(dy**2 + dx**2)
                
                speed = max(1.0, min( distance, self.max_speed ) )
                
                # Move the alien.
                self.position = (
                    self.position[0] + (speed * math.cos(angle)),
                    self.position[1] + (speed * math.sin(angle))
                    )
                
                to_update = 1
            
            else:
            
                # The alien has reached its target position.
                self.decision = "aim"
                self.target_object = None
        
        # Fade the object as required.
        if self.fade():
        
            to_update = 1
        
        if to_update:
        
            # Prepare the rendering surface.
            self.prepare_surface()
        
        # Check for collisions with starships.
        if self.fading != "in" and self.captured is None:
        
            hit = self.parent.collide_object(self, Starship, layer = 2)
            
            if hit and hit.invulnerability == 0 and hit.controlled == 1:
            
                # Set a new target position far from its current position.
                x = self.position[0] + (0.5 * self.config.screen_size[0])
                
                if x > (0.9 * self.config.screen_size[0]):
                    x = (x - (0.9 * self.config.screen_size[0])) + \
                        (0.1 * self.config.screen_size[0])
                
                y = self.position[1] + (0.5 * self.config.screen_size[1])
                
                if y > (0.9 * self.config.screen_size[1]):
                    y = (y - (0.9 * self.config.screen_size[1])) + \
                        (0.1 * self.config.screen_size[1])
                
                # Tell the alien to move to its new location.
                self.target_object = None
                self.target_positions = [(x, y)]
                self.displace = (0, 0)
                self.decision = "aim"
                
                # Capture this starship.
                self.captured = hit
                self.parent.add_event( Captured(hit, (x, y - 32)) )
                # Play a sound.
                if self.resources.sound_status:
                    self.resources.samples["capture"].play()
                
                #print "captured", hit, hit.target_position, hit.controlled
        
        # Check for projectiles.
        hit = self.parent.collide_object(self, Fire, layer = 2)
        
        if hit:
        
            # Notify the Gameplay object that an alien has been destroyed.
            self.parent.add_event( GameObjectDestroyed(self) )
            
            # If this alien has captured an object then free it.
            if self.captured and self.captured.controlled == 2:
            
                self.captured.controlled = 0
            
            # Remove this object (usually an event would be used).
            self.parent.remove_object( hit, layer = 2 )



class Generator(Alien):

    def __init__(self, parent, position, target_positions,
                       displace = (0, 0), generate_time = 5,
                       alien_type = 1):
    
        Alien.__init__(
            self, parent, position, target_positions = target_positions,
            displace = displace
            )
        
        # Initialise the image object.
        objects.ImageObject.__init__( self,
            self.resources.images["alien5"],
            position = position,
            angle = 0.0, alpha = 0.0,
            colorkey = (0, 0, 0), scale = 2.0
            )
        
        # Target positions
        self.target_positions = target_positions
        
        # Target item in target positions list
        self.target_item = 0
        
        # Decision states
        self.decision = "aim"
        self.decision_time = generate_time
        
        # Set decision timer.
        self.set_decision_timer()
        
        # The type of alien to be generated
        self.alien_type = alien_type
        
        # Maximum speed
        self.image_size = self.image.get_size()
        self.max_speed = int( min(self.image_size[0], self.image_size[1]) / 8 )
        
        # Alien value
        self.value = 5
    
    def update(self):
    
        # Updating
        
        to_update = 0
        
        self.decision_timer = self.decision_timer - 1
        
        if self.decision_timer <= 0:
        
            # Reset decision timer.
            self.set_decision_timer()
            
            # Quickly check that we are not introducing too many game objects.
            
            if len(self.parent.objects[2]) < self.config.game_max_objects:
            
                # Generate a new alien.
                self.parent.add_event( AddObject(
                    self.alien_type( self.parent, self.position ),
                    layer = 2, index = -1
                    ) )
        
        if self.decision == "aim":
        
            # Set the new target position.
            new_position = self.target_positions[self.target_item]
            
            self.target_item = \
                (self.target_item + 1) % len(self.target_positions)
            
            self.target_position = (
                new_position[0] + self.displace[0],
                new_position[1] + self.displace[1]
                )
            
            self.decision = "act"
        
        if self.decision == "act":
        
            # Acting
            
            # Check that the target object is in the same general direction
            # as expected.
            
            # Determine the direction of any motion.
            dx = int(self.target_position[0] - self.position[0])
            dy = int(self.target_position[1] - self.position[1])
            
            if dx != 0 or dy != 0:
            
                angle = math.atan2(dy, dx)
                
                distance = math.sqrt(dy**2 + dx**2)
                
                speed = max(1.0, min( distance, self.max_speed ) )
                
                # Move the alien.
                self.position = (
                    self.position[0] + (speed * math.cos(angle)),
                    self.position[1] + (speed * math.sin(angle))
                    )
                
                to_update = 1
            
            else:
            
                # The alien has reached its target position.
                self.decision = "aim"
                self.target_object = None
        
        # Fade the object as required.
        if self.fade():
        
            to_update = 1
        
        if to_update:
        
            # Prepare the rendering surface.
            self.prepare_surface()
        
        # Check for collisions.
        if self.fading != "in":
        
            hit = self.parent.collide_object(self, Starship, layer = 2)
            
            if hit and hit.invulnerability == 0 and hit.controlled == 1:
            
                # Notify the Gameplay object that a starship has been destroyed.
                self.parent.add_event( GameObjectDestroyed(hit) )
                
                # Notify the Gameplay object that this object has been destroyed.
                self.parent.add_event( GameObjectDestroyed(self) )
        
        # Check for projectiles.
        hit = self.parent.collide_object(self, Fire, layer = 2)
        
        if hit:
        
            # Notify the Gameplay object that an alien has been destroyed.
            self.parent.add_event( GameObjectDestroyed(self) )
            
            # Remove this object (usually an event would be used).
            self.parent.remove_object( hit, layer = 2 )



# Aliens with unpredictable thinking times for legacy attack waves

class LegacyMixin:

    def set_decision_timer(self):
    
        # For the first time, wait for a while before attacking.
        if self.in_formation == 1:
        
            self.decision_timer = int(
                (self.decision_time + (random.random() * 2)) * \
                self.config.updaterate
                )
            
            self.in_formation = 0
        
        else:
        
            self.decision_timer = int(
                self.decision_time * self.config.updaterate
                )

class LegacyStartStop(LegacyMixin, StartStop):

    def __init__(self, parent, position, target_positions = None,
                       displace = (0, 0)):
        
        self.in_formation = 1
        
        StartStop.__init__(
            self, parent, position, target_positions, displace
            )

class LegacyFollower(LegacyMixin, Follower):

    def __init__(self, parent, position, target_positions = None,
                       displace = (0, 0)):
        
        self.in_formation = 1
        
        Follower.__init__(
            self, parent, position, target_positions, displace
            )

class LegacyInterceptor(LegacyMixin, Interceptor):

    def __init__(self, parent, position, target_positions = None,
                       displace = (0, 0)):
        
        self.in_formation = 1
        
        Interceptor.__init__(
            self, parent, position, target_positions, displace
            )

class LegacyCapturer(LegacyMixin, Capturer):

    def __init__(self, parent, position, target_positions = None,
                       displace = (0, 0)):
        
        self.in_formation = 1
        
        Capturer.__init__(
            self, parent, position, target_positions, displace
            )



# Other objects

class Gateway(objects.AnimatedImage, GameObject):

    def __init__(self, parent, label = None, position = None):
    
        GameObject.__init__(self, parent)
        
        if position == None:
        
            position = (
                random.random() * self.config.screen_size[0],
                random.random() * self.config.screen_size[1]
                )
        
        # Initialise the animated image object.
        objects.AnimatedImage.__init__(self,
            ( self.resources.images["gateway1"],
              self.resources.images["gateway2"],
              self.resources.images["gateway3"],
              self.resources.images["gateway4"] ),
            position = position, alpha = 0.0, colorkey = (0, 0, 0),
            frame_delay = int(self.config.updaterate / 25)
            )
        
        # Set the effective image size to be used for collisions.
        self.image_size = self.images[0].get_size()
        
        # Store the label.
        self.label = label
    
    def update(self):
    
        # Fade the gateway.
        self.fade()
        
        # Update the animation (this automatically updates the rendering
        # surface).
        self.next_frame()



class Effect:

    pass

class Explosion(objects.AnimatedImage, GameObject, Effect):

    def __init__(self, parent, position, alpha = 127.0):
    
        GameObject.__init__(self, parent)
        
        # Initialise the animated image object.
        objects.AnimatedImage.__init__(self,
            ( self.resources.images["explosion1"],
              self.resources.images["explosion2"],
              self.resources.images["explosion3"],
              self.resources.images["explosion4"] ),
            position = position, alpha = alpha, colorkey = (0, 0, 0)
            )
    
    def update(self):
    
        # Fade the explosion.
        self.fade()
        
        # Additionally, if the object is at full alpha then immediately
        # fade it out.
        if self.fading == "":
        
            self.fading = "out"
        
        # Update the animation (this automatically updates the rendering
        # surface).
        self.next_frame()



# Label layer objects

class TitleText(objects.TextObject, GameObject):

    def __init__(self, parent, position, text, font_size,
                       colour = (255, 255, 255),
                       scale_radius = 0.05, scale_angle = 0.0,
                       scale_angular_speed = 1.0, align = None):
    
        GameObject.__init__(self, parent)
        
        objects.TextObject.__init__( self,
            text, None, font_size, colour,
            position = position, colorkey = (0, 0, 0),
            alpha = 0.0, align = align
            )
        
        # Scale radius and angle
        self.scale_radius = scale_radius
        self.scale_angle = scale_angle
        self.scale_angular_speed = scale_angular_speed
    
    def update(self):
    
        # Change the scale according to the scale radius and angle.
        self.scale = 1.0 + (
            self.scale_radius * math.cos(self.scale_angle * degtorad)
            )
        
        self.scale_angle = self.scale_angle + self.scale_angular_speed
        
        if self.scale_angle >= 360.0:
        
            self.scale_angle = self.scale_angle - 360.0
        
        # Fade the object as required.
        self.fade()
        
        # Prepare the rendering surface.
        self.prepare_surface()



class AlienChars:

    def create_operations(self, text, font_size, colour):
    
        """operations = create_operations(self, text, font_size, colour)
        
        Create the rendering operations using the text information supplied.
        """
        
        operations = []
        
        char_x = 0.0
        in_space = 1
        
        for char in text:
        
            # Add the relevant symbol to the list of operations.
            number = ord(char) % len(alien_chars)
            
            operations = operations + \
                self.draw_character(
                    alien_chars[number], char_x, font_size, colour
                    )
            
            in_space = 0
            
            # Move the character cursor onwards if character break is found.
            if char in self.end_char:
            
                char_x = char_x + (font_size * 9/8.0)
                in_space = 1
        
        if in_space == 0:
        
            char_x = char_x + (font_size * 9/8.0)
        
        return operations, (char_x, font_size + 1)
    
    def draw_character(self, l, char_x, font_size, colour):
    
        operations = []
        
        symbol = []
        
        x, y = l[0]
        
        start_pos = (char_x + (x * font_size), y * font_size)
        
        for x, y in l[1:]:
        
            end_pos = (char_x + (x * font_size), y * font_size)
            operations.append( (
                pygame.draw.line, (colour, start_pos, end_pos, font_size/16)
                ) )
            
            start_pos = end_pos
        
        return operations



class AlienText(objects.DrawingObject, AlienChars, TitleText):

    def __init__(self, parent, position, text, font_size,
                       end_stroke = "", end_char = "",
                       colour = (255, 255, 255),
                       scale_radius = 0.05, scale_angle = 0.0,
                       scale_angular_speed = 1.0, align = None):
    
        GameObject.__init__(self, parent)
        
        # Characters which indicate the end of a stroke or character.
        self.end_stroke = end_stroke
        self.end_char = end_char
        
        ops, size = self.create_operations(text, font_size, colour)
        
        objects.DrawingObject.__init__( self,
            ops, size, position = position, colorkey = (0, 0, 0),
            alpha = 0.0, align = align
            )
        
        # Scale radius and angle
        self.scale_radius = scale_radius
        self.scale_angle = scale_angle
        self.scale_angular_speed = scale_angular_speed



class GameText(objects.TextObject, GameObject):

    def __init__(self, parent, position, text, font_size,
                       colour = (255, 255, 255), align = None):
    
        GameObject.__init__(self, parent)
        
        objects.TextObject.__init__( self,
            text, None, font_size, colour,
            position = position, colorkey = (0, 0, 0),
            alpha = 0.0, align = align
            )
        
        # Fading in/out flag (determine this from the manager object)
        self.fading = self.manager.fading
    
    def update(self):
    
        # Fade the object as required.
        if self.fade():
        
            # Prepare the rendering surface.
            self.prepare_surface()



class GameAlienText(objects.DrawingObject, AlienChars, GameObject):

    def __init__(self, parent, position, text, font_size,
                       end_stroke = "", end_char = "",
                       colour = (255, 255, 255), align = None):
    
        GameObject.__init__(self, parent)
        
        # Characters which indicate the end of a stroke or character.
        self.end_stroke = end_stroke
        self.end_char = end_char
        
        ops, size = self.create_operations(text, font_size, colour)
        
        objects.DrawingObject.__init__( self,
            ops, size, position = position, colorkey = (0, 0, 0),
            alpha = 0.0, align = align
            )
    
    def update(self):
    
        # Fade the object as required.
        if self.fade():
        
            # Prepare the rendering surface.
            self.prepare_surface()



class TemporaryText(GameText):

    def __init__(self, parent, position, text, font_size,
                       colour = (255, 255, 255), align = None, fading = None):
    
        GameObject.__init__(self, parent, fading = fading)
        
        objects.TextObject.__init__( self,
            text, None, font_size, colour,
            position = position, colorkey = (0, 0, 0),
            alpha = 0.0, align = align
            )
    
    def update(self):
    
        # Fade the object as required.
        self.fade()
        
        # Additionally, if the object is at full alpha then immediately
        # fade it out.
        if self.fading == "":
        
            self.fading = "out"
        
        # Prepare the rendering surface.
        self.prepare_surface()



class TemporaryAlienText(GameAlienText):

    def update(self):
    
        # Fade the object as required.
        self.fade()
        
        # Additionally, if the object is at full alpha then immediately
        # fade it out.
        if self.alpha >= 255:
        
            self.fading = "out"
        
        # Prepare the rendering surface.
        self.prepare_surface()



class TargetCursor(objects.AnimatedImage, GameObject, Effect):

    def __init__(self, parent, position, alpha = 255):
    
        GameObject.__init__(self, parent)
        
        # Initialise the animated image object.
        objects.AnimatedImage.__init__(self,
            ( self.resources.images["target1"],
              self.resources.images["target2"],
              self.resources.images["target3"],
              self.resources.images["target4"],
              self.resources.images["target5"],
              self.resources.images["target6"],
              self.resources.images["target7"],
              self.resources.images["target8"],
              self.resources.images["target9"],
              self.resources.images["target10"],
              self.resources.images["target11"],
              self.resources.images["target12"] ),
            position = position, alpha = alpha, colorkey = (0, 0, 0)
            )
        
        # Phase and phase counter.
        self.phase = 0
        self.counter = 0
        self.flash_frames = int(self.config.updaterate / 8)
        self.flashes_frames = 4 * self.flash_frames
    
    def update(self):
    
        # Fade the image.
        self.fade()
        
        # Update the animation (this automatically updates the rendering
        # surface).
        if self.phase == 0:
        
            # Large flashing cursor.
            self.counter = self.counter + 1
            
            if self.counter % self.flash_frames == 0:
            
                self.frame = int(self.counter / self.flash_frames) % 2
            
            if self.counter == self.flashes_frames:
            
                self.phase = 1
                self.counter = 0
        
        elif self.phase == 1:
        
            # Shrinking cursor.
            self.frame = 2 + self.counter
            self.counter = self.counter + 1
            
            if self.frame == 5:
            
                self.phase = 2
                self.counter = 0
        
        elif self.phase == 2:
        
            # Small flashing cursor.
            self.counter = self.counter + 1
            
            if self.counter % self.flash_frames == 0:
            
                self.frame = 6 + (int(self.counter / self.flash_frames) % 2)
            
            if self.counter == self.flashes_frames:
            
                self.phase = 3
                self.counter = 0
        
        elif self.phase == 3:
        
            # Growing cursor.
            self.frame = 8 + self.counter
            self.counter = self.counter + 1
            
            if self.frame == 11:
            
                self.phase = 0
                self.counter = 0
        
        # Prepare the surface.
        self.prepare_surface()



class GameImage(objects.ImageObject, GameObject):

    def __init__(self, parent, name, position = None, angle = 0.0,
                       scale = 1.0, align = None, alpha = 255,
                       colorkey = (0, 0, 0)):
    
        GameObject.__init__(self, parent)
        
        # Initialise the image object.
        objects.ImageObject.__init__( self,
            self.resources.images[name],
            position = position,
            angle = 0.0, alpha = 0.0,
            colorkey = colorkey, scale = scale
            )
    
    def update(self):
    
        # Update the indicator.
        
        # Fade the object as required.
        if self.fade():
        
            self.prepare_surface()



class GameAnimatedImage(objects.AnimatedImage, GameObject):

    def __init__(self, parent, names, position = None, angle = 0.0,
                       scale = 1.0, align = None, alpha = 255,
                       colorkey = (0, 0, 0), frame_delay = 0):
    
        GameObject.__init__(self, parent)
        
        # Initialise the image object.
        images = []
        
        for name in names:
        
            images.append(self.resources.images[name])
        
        objects.AnimatedImage.__init__( self,
            images,
            position = position,
            angle = 0.0, alpha = 0.0,
            colorkey = colorkey, scale = scale,
            frame_delay = frame_delay
            )
    
    def update(self):
    
        # Update the indicator.
        
        # Fade the object as required.
        self.fade()
        
        # Change the animation frame.
        self.next_frame()
        
        self.prepare_surface()



class LevelContents(GameObject):

    images = ( "starship", "alien1", "alien2", "alien2", "alien2",
               "alien2", "alien2", "alien2", "alien2", "gateway1" )
    
    def __init__(self, parent, position, width, height, indices = None):
    
        GameObject.__init__(self, parent)
        
        # Set the position.
        self.position = position
        
        # Set the indicator width and height.
        self.width = width
        self.height = height
        
        # The images to display (using evaluation to give a list which is
        # either populated or empty).
        self.indices = indices or []
        
        # Set the scale, alpha and colour key values.
        self.scale = 1.0
        self.alpha = 0
        self.colorkey = (0, 0, 0)
        
        # Draw the images onto a rendering surface.
        self.initialise_surface()
        
        # Create the working rendering surface.
        self.prepare_surface()
    
    def set_indices(self, indices):
    
        self.indices = indices
        self.initialise_surface()
        self.prepare_surface()
    
    def initialise_surface(self):
    
        # Create a rendering surface.
        self.surface = pygame.Surface( (self.width, self.height) )
        
        # Clear the surface.
        self.surface.fill( (0, 0, 0) )
        
        # Render a horizontal row of images on the indicator.
        x = 0
        
        for index in self.indices:
        
            # The vertical scale is important.
            image = self.resources.images[self.images[index]]
            w, h = image.get_size()
            yscale = float(self.height) / h
            
            # Plot the scaled image onto a working surface.
            working = pygame.transform.rotozoom(
                image, 0.0, yscale
                )
            
            # Blit the image onto the surface.
            self.surface.blit(working, (x, 0))
            
            # Move the cursor to the right by the scaled width of the image.
            x = x + working.get_width()
    
    def prepare_surface(self):
    
        # Rotate and scale the image.
        
        if self.scale != 1.0:
            self.rendering = pygame.transform.rotozoom(
                self.surface, 0.0, self.scale
                )
        else:
            self.rendering = self.surface
        
        # Set the alpha and colour key of the surface.
        if pygame.vernum >= (1, 8, 0):
            self.rendering.set_colorkey(self.colorkey, flags = pygame.RLEACCEL)
        else:
            self.rendering.set_colorkey(self.colorkey)
        self.rendering.set_alpha(self.alpha)
    
    def render(self, screen):
    
        "Render the effect onto the 'screen'."
        
        screen.blit(self.rendering, self.position)
    
    def update(self):
    
        # Update the indicator.
        
        # Fade the object as required.
        if self.fade():
        
            self.prepare_surface()



class HighScoreCharacter(TitleText):

    def __init__(self, parent, position, text, font_size,
                       colour = (255, 255, 255),
                       scale_radius = 0.05, scale_angle = 0.0,
                       scale_angular_speed = 1.0, align = None):
        
        TitleText.__init__(self,
            parent, position, text, font_size,
            colour = colour,
            scale_radius = scale_radius, scale_angle = scale_angle,
            scale_angular_speed = scale_angular_speed, align = align
            )
        
        if self.rendering:
        
            self.image_size = self.rendering.get_size()
    
    def update(self):
    
        TitleText.update(self)
        
        # Check for projectiles.
        hit = self.parent.collide_object(self, Fire, layer = 2)
        
        if hit:
        
            # Notify the Gameplay object that a letter has been hit.
            self.parent.add_event( GameObjectDestroyed(self) )
            
            # Remove the projectile immediately.
            self.parent.remove_object( hit, layer = 2 )



class InfukorLogo(objects.ImageObject, GameObject):

    def __init__(self, parent, position, image, alpha = 255, width = None,
                       height = None, steps = 1):

        GameObject.__init__(self, parent)
        
        # Initialise the width and height before the image object as we
        # are replacing the prepare_surface method which uses the
        # width and height values; the image object will call this method
        # so they must be defined here.
        
        if width == None:
        
            self.width = self.resources.images[image].get_width()
        
        else:
        
            self.width = width
        
        if height == None:
        
            self.height = self.resources.images[image].get_height()
        
        else:
        
            self.height = height
        
        # The actual dimensions of the image.
        self.image_width, self.image_height = \
            self.resources.images[image].get_size()
        
        # Calculate the size of each step between the initial image size
        # and the final size.
        self.wstep = float(self.image_width - self.width) / steps
        self.hstep = float(self.image_height - self.height) / steps
        
        # Initialise the image object.
        objects.ImageObject.__init__( self,
            self.resources.images[image],
            position = position,
            angle = 0.0, alpha = alpha,
            colorkey = (0, 0, 0)
            )
    
    def prepare_surface(self):
    
        # Resize the image.
        
        working = pygame.transform.scale(
            self.surface, (int(self.width), int(self.height))
            )
        
        self.rendering = pygame.Surface(working.get_size(), SRCALPHA)
        self.rendering.blit(working, (0, 0))
        
        # Set the alpha properties of the surface.
        self.setup_color_key()
        self.rendering.set_alpha(self.alpha)
    
    def update(self):
    
        # Increase the width and height of the surface until it is full size.
        to_update = 0
        
        if self.width < self.image_width:
        
            to_update = 1
            
            self.width = self.width + self.wstep
            
            if self.width > self.image_width:
            
                self.width = self.image_width
        
        if self.height < self.image_height:
        
            to_update = 1
            
            self.height = self.height + self.hstep
            
            if self.height > self.image_height:
            
                self.height = self.image_height
        
        # Fade the object if necessary.
        to_update = to_update or self.fade()
        
        if to_update == 1:
        
            # Prepare the surface.
            self.prepare_surface()
