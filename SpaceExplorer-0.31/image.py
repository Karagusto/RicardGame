
"""
image.py

Image loading and storage class for Space Explorer.

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

import os

import pygame
from pygame.locals import *

class Images:
    """Images(directory, files = None)
    
    Load the images stored in the directory given.
    
    A list of filenames should be passed, but if none are given then all
    files in the directory are loaded.
    
    The optional list of names allows the images to be referenced by name.
    If no names are specified then their filenames are used instead.
    """
    
    def __init__(self, directory, files = None, names = None, screen = None):
    
        # Select all the files in the directory if none are specified.
        if files == None:
        
            files = os.listdir(directory)
        
        if names == None:
        
            names = files
        
        # Store the image instances in a member of the instance.
        self.images = {}
        
        for i in range(len(files)):
        
            file = files[i]
            
            try:
                name = names[i]
            
            except IndexError:
            
                name = file
            
            image = pygame.image.load(os.path.join(directory, file))
            
            ## Images must not have per-pixel alpha.
            #self.images[name] = pygame.Surface(
            #    image.get_size(), SRCALPHA
            #    )
            #
            #self.images[name].blit(image, (0, 0))
            if screen is not None:
            
                self.images[name] = image.convert(screen, SRCALPHA)
            
            else:
            
                self.images[name] = image.convert() #32, SRCALPHA)

    def __repr__(self):
    
        return repr(self.images)
    
    # Mapping/dictionary methods.
    
    def __len__(self):
    
        return len(self.images)
    
    def __getitem__(self, key):
    
        return self.images[key]
    
    def __setitem__(self, key, value):
    
        self.images[key] = value
    
    def __delitem__(self, key):
    
        del self.images[key]
    
    def clear(self):
    
        return self.images.clear()
    
    def copy(self):
    
        return self.images.copy()
    
    def get(self, item, default = None):
    
        return self.images(item, default)
    
    def has_key(self, item):
    
        return self.images.has_key(item)
    
    def items(self):
    
        return self.images.items()
    
    def keys(self):
    
        return self.images.keys()
    
    def popitem(self):
    
        return self.images.popitem()
    
    def setdefault(self, item, default = None):
    
        return self.images.setdefault(item, default)
    
    def update(self, dict):
    
        return self.images.update(dict)
    
    def values(self):
    
        return self.images.values()

class Cursors:

    def __init__(self, directory, files = None, names = None):
    
        # Store the cursor instances in a member of the instance.
        self.cursors = {}
        
        for i in range(len(files)):
        
            cursor_file, mask_file = files[i]
            
            try:
                name = names[i]
            
            except IndexError:
            
                name = file
            
            self.cursors[name] = pygame.cursors.load_xbm(
                os.path.join(directory, cursor_file),
                os.path.join(directory, mask_file)
                )
    
    def __repr__(self):
    
        return repr(self.cursors)
    
    # Mapping/dictionary methods.
    
    def __len__(self):
    
        return len(self.cursors)
    
    def __getitem__(self, key):
    
        return self.cursors[key]
    
    def __setitem__(self, key, value):
    
        self.cursors[key] = value
    
    def __delitem__(self, key):
    
        del self.cursors[key]
    
    def clear(self):
    
        return self.cursors.clear()
    
    def copy(self):
    
        return self.cursors.copy()
    
    def get(self, item, default = None):
    
        return self.cursors(item, default)
    
    def has_key(self, item):
    
        return self.cursors.has_key(item)
    
    def items(self):
    
        return self.cursors.items()
    
    def keys(self):
    
        return self.cursors.keys()
    
    def popitem(self):
    
        return self.cursors.popitem()
    
    def setdefault(self, item, default = None):
    
        return self.cursors.setdefault(item, default)
    
    def update(self, dict):
    
        return self.cursors.update(dict)
    
    def values(self):
    
        return self.cursors.values()
