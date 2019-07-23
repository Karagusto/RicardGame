
"""
objects.py

Low level rendering object classes for Space Explorer.

Initially written by Paul Boddie.

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

# Rendering objects ------------------------------------------------------------

class Object:

    "An object that is updated periodically."
    
    def _init_surface(self):
        pass
    
    def _init_rendering(self):
        pass
    
    def start(self):
        pass
    
#    def update(self):
#        pass
    
    def setup_color_key(self):

        if self.colorkey:
            if pygame.vernum >= (1, 8, 0):
                self.rendering.set_colorkey(self.colorkey, flags = pygame.RLEACCEL)
            else:
                self.rendering.set_colorkey(self.colorkey)

    def render(self, screen):
    
        "Render the effect onto the 'screen'."
        
        if self.position is None:
            return
        
        if self.rendering is None:
            return
        
        size = self.rendering.get_size()
        
        if self.align == None:
        
            position = (
                self.position[0] - size[0] / 2,
                self.position[1] - size[1] / 2
                )
        
        elif self.align == "W":
        
            position = (
                self.position[0],
                self.position[1] - size[1] / 2
                )
        
        elif self.align == "E":
        
            position = (
                self.position[0] - size[0],
                self.position[1] - size[1] / 2
                )
        
        elif self.align == "N":
        
            position = (
                self.position[0] - size[0] / 2,
                self.position[1]
                )
        
        elif self.align == "S":
        
            position = (
                self.position[0] - size[0] / 2,
                self.position[1] - size[1]
                )
        
        elif self.align == "NW":
        
            position = (
                self.position[0],
                self.position[1]
                )
        
        elif self.align == "NE":
        
            position = (
                self.position[0] - size[0],
                self.position[1]
                )
        
        elif self.align == "SW":
        
            position = (
                self.position[0],
                self.position[1] - size[1]
                )
        
        elif self.align == "SE":
        
            position = (
                self.position[0] - size[0],
                self.position[1] - size[1]
                )
        
        screen.blit(self.rendering, position)
    
    def about_to_finish(self):
        pass
    
    def finished(self):
        pass
    
    def put_at_back(self):
        return 0


class ImageObject(Object):

    "An image object that is updated periodically."

    def __init__(self, image, position = None, angle = 0.0,
                       scale = 1.0, align = None, alpha = 255,
                       colorkey = None):

        """
        Initialise with the 'image' and 'position' (a tuple).
        Note that the 'position' refers to the centre of the image.
        """

        # Define the image, its position and its velocity vector.
        self.image = image
        self.position = position
        self.angle = angle
        self.scale = scale
        self.align = align

        # Organise the alpha properties.
        self.alpha = alpha
        self.colorkey = colorkey

        # Draw the image on a rendering surface.
        self.surface = None
        self.initialise_surface()

        # Create the working rendering surface.
        self.prepare_surface()

    def initialise_surface(self):

        # Create a copy of the image on a suitable rendering surface.
        self.surface = self.image

    def prepare_surface(self):

        # Rotate and scale the image.

        if self.angle != 0.0 or self.scale != 1.0:
            working = pygame.transform.rotozoom(
                self.surface, self.angle, self.scale
                )
        else:
            working = self.surface

        self.rendering = pygame.Surface(working.get_size(), SRCALPHA)
        self.rendering.blit(working, (0, 0))

        # Set the alpha properties of the surface.
        self.setup_color_key()
        self.rendering.set_alpha(self.alpha)

    def render(self, screen):

        "Render the effect onto the 'screen'."

        if self.position is None:
            return

        size = self.rendering.get_size()

        if self.align == None:

            position = (
                self.position[0] - size[0] / 2,
                self.position[1] - size[1] / 2
                )
        
        elif self.align == "W":
        
            position = (
                self.position[0],
                self.position[1] - size[1] / 2
                )
        
        elif self.align == "E":
        
            position = (
                self.position[0] - size[0],
                self.position[1] - size[1] / 2
                )
        
        elif self.align == "N":
        
            position = (
                self.position[0] - size[0] / 2,
                self.position[1]
                )
        
        elif self.align == "S":

            position = (
                self.position[0] - size[0] / 2,
                self.position[1] - size[1]
                )
        
        elif self.align == "NW":
        
            position = (
                self.position[0],
                self.position[1]
                )
        
        elif self.align == "NE":
        
            position = (
                self.position[0] - size[0],
                self.position[1]
                )
        
        elif self.align == "SW":
        
            position = (
                self.position[0],
                self.position[1] - size[1]
                )
        
        elif self.align == "SE":
        
            position = (
                self.position[0] - size[0],
                self.position[1] - size[1]
                )

        screen.blit(self.rendering, position)



class AnimatedImage(ImageObject):

    def __init__(self, images, position = None, angle = 0.0,
                       scale = 1.0, align = None, alpha = 255,
                       colorkey = None, frame_delay = 0):
    
        # Define the image, its position and its velocity vector.
        self.images = images
        
        self.position = position
        self.angle = angle
        self.scale = scale
        self.align = align
        
        # Organise the alpha properties.
        self.alpha = alpha
        self.colorkey = colorkey
        
        # Frame number
        self.frame = 0
        
        # Delay between frames
        self.frame_delay = frame_delay
        self.delay_counter = self.frame_delay
        
        # Draw the image on a rendering surface.
        self.surfaces = []
        self.initialise_surface()
        
        # Create the working rendering surface.
        self.prepare_surface()
    
    def initialise_surface(self):
    
        # Create a copy of the images on suitable rendering surfaces.
        self.surfaces = []

        for image in self.images:

            self.surfaces.append(
                pygame.Surface(image.get_size(), SRCALPHA)
                )
        
        for i in range(len(self.surfaces)):
        
            self.surfaces[i].blit(self.images[i], (0, 0))
    
    def prepare_surface(self):
    
        # Rotate and scale the image.
        
        if self.angle != 0.0 or self.scale != 1.0:
            self.rendering = pygame.transform.rotozoom(
                self.surfaces[self.frame], self.angle, self.scale
                )
        else:
            self.rendering = self.surfaces[self.frame]
        
        #self.rendering = pygame.Surface(working.get_size(), SRCALPHA)
        
        # Set the alpha properties of the surface.
        self.setup_color_key()
        self.rendering.set_alpha(self.alpha)
        
        #self.rendering.blit(working, (0, 0))
    
    def next_frame(self):
    
        if self.delay_counter == 0:
        
            self.frame = (self.frame + 1) % len(self.images)
            self.delay_counter = self.frame_delay
        
            # Prepare the surface.
            self.prepare_surface()
        
        else:
        
            self.delay_counter = self.delay_counter - 1
    
    def previous_frame(self):
    
        if self.delay_counter == 0:
        
            self.frame = (self.frame - 1) % len(self.images)
            self.delay_counter = self.frame_delay
            
            # Prepare the surface.
            self.prepare_surface()
        
        else:
        
            self.delay_counter = self.delay_counter - 1



class DrawingObject(Object):

    def __init__(self, operations, size, position = None, angle = 0.0,
                       scale = 1.0, align = None, alpha = 255, colorkey = None):
    
        # Define the operations, their overall position and velocity vector.
        self.operations = operations
        
        self.position = position
        self.angle = angle
        self.scale = scale
        self.align = align
        
        self.size = size
        
        # Organise the alpha properties.
        self.alpha = alpha
        self.colorkey = colorkey
        
        # Draw the image on a rendering surface.
        self.initialise_surface()
        
        # Create the working rendering surface.
        self.prepare_surface()
    
    def initialise_surface(self):
    
        "Perform various drawing operations onto a surface."
        
        self.surface = pygame.Surface( (int(self.size[0]), int(self.size[1])) )
        
        if self.colorkey:
            self.surface.fill( self.colorkey )
        else:
            self.surface.fill( (0, 0, 0) )
        
        for fn, args in self.operations:
        
            apply(fn, (self.surface,) + tuple(args))
    
    def prepare_surface(self):
    
        if self.surface is None:
            self.rendering = None
            return
        
        # Rotate and scale the image.
        
        if self.angle != 0.0 or self.scale != 1.0:
            working = pygame.transform.rotozoom(
                self.surface, self.angle, self.scale
                )
        else:
            working = self.surface
        
        self.rendering = pygame.Surface(working.get_size(), SRCALPHA)
        
        # Set the alpha properties of the surface.
        self.setup_color_key()
        self.rendering.set_alpha(self.alpha)
        
        self.rendering.blit(working, (0, 0))


class TextObject(Object):

    def __init__(self, text, font_name, size, colour, position = None,
                       angle = 0.0, scale = 1.0, align = None,
                       alpha = 255, colorkey = None):
        
        self.text = text
        self.font_name = font_name
        self.size = size
        self.colour = colour
        self.position = position
        self.angle = angle
        self.scale = scale
        self.align = align
        
        # Organise the alpha properties.
        self.alpha = alpha
        self.colorkey = colorkey
        
        # Find the relevant font.
        self.font = pygame.font.Font(self.font_name, self.size)
        
        # Draw the image on a rendering surface.
        self.initialise_surface()
        
        # Create the working rendering surface.
        self.prepare_surface()
    
    def set_text(self, text):
    
        self.text = text
        self.initialise_surface()
        self.prepare_surface()
    
    def initialise_surface(self):
    
        # Render the text on a surface.
        if self.text != "":
            self.font_surface = self.font.render(self.text, 1, self.colour)
        else:
            self.font_surface = None
    
    def prepare_surface(self):
    
        if self.font_surface is None:
            self.rendering = None
            return
        
        # Rotate and scale the image.
        
        if self.angle != 0.0 or self.scale != 1.0:
            working = pygame.transform.rotozoom(
                self.font_surface, self.angle, self.scale
                )
        else:
            working = self.font_surface
        
        self.rendering = pygame.Surface(working.get_size(), SRCALPHA)
        
        # Set the alpha properties of the surface.
        self.setup_color_key()
        self.rendering.set_alpha(self.alpha)
        
        self.rendering.blit(working, (0, 0))


class ObjectGroup(Object):

    def __init__(self, objects):
    
        # Define the image, its position and its velocity vector.
        self.objects = objects
        
    def render(self, screen):
    
        "Render the group onto the 'screen'."
        
        for object in self.objects:
        
            object.render(screen)
