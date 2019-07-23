#! /usr/bin/env python

"""
spacegame.py

The main classes and control structures for Space Explorer.

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

import pygame, sys
from pygame.locals import *

import os, sys, types

try:

    import gc

except ImportError:

    print "Sorry: a version of Python which supports garbage collection " + \
        "is required to run this game."

    sys.exit()

import config, manage
from events import *

__version__ = config.__version__



# Communications objects -------------------------------------------------------

class CommunicationsHandler:

    def __init__(self, parent):
    
        self.parent = parent
        self.config = self.parent.config
        self.resources = self.parent.resources
    
    def unlink(self):
    
        """Unlink the object from its parent by deleting the parent member."""
        del self.parent
        del self.config
        del self.resources


# SDL Event Handler

class SDLEventHandler(CommunicationsHandler):

    """SDLEventHandler(parent)
    
    Listen for events from SDL (via Pygame) and pass them to the
    parent's event handler.
    """

    def event_handler(self):
    
        # Read the Pygame events list.
        events = pygame.event.get()
        
        # A list of actions/events to return to the Game instance.
        actions = []
        
        for event in events:
        
            if event.type == QUIT:
            
                # Return a quit event.
                actions.append( ExitApplication() )
            
            elif event.type == KEYDOWN:

                # Return a KeyPress event.
                actions.append( KeyPress(event.key) )
            
            elif event.type == MOUSEBUTTONDOWN:

                # Return a MouseButton event using a translation
                # to the non-event numbering of mouse buttons.
                actions.append( MouseButton(event.button - 1) )

        # Return the events for processing by the parent.
        return actions



# Main game object -------------------------------------------------------------

class Game:

    def __init__(self, path = ""):
    
        # Use the default configuration.
        self.config = config.Configuration(os.path.join(path, "Resources"))
        
        # Load the high scores.
        self.config.load_scores()
        
        # Load the control definitions
        self.config.load_controls()

        # Set the resolution of the display.
        self.screen = pygame.display.set_mode(
            self.config.screen_size
            )
        
        # Resources (images and sounds)
        self.resources = config.Resources(
#            os.path.join("Resources", "Pictures"), self.screen
            os.path.join(path, "Resources"), screen = None,
                sound = self.config.sound_status
            )

        # Set up an object list with four layers.
        self.objects = [ [], [], [], [] ]

        # Queued events.
        self.events = []

        # Set up the event handlers.
        self.sdl_event = SDLEventHandler(self)

        # Initialise some objects (the title screen).
        self.add_object(manage.TitleScreen(self), layer = 0)

    def mainloop(self):

        # Frame rate
        framerate = self.config.framerate

        # Updates per millisecond
        updaterate = self.config.updaterate
        updaterate_ms = self.config.updaterate / 1000.0
        framerate = self.config.framerate

        # Main loop

        clock = pygame.time.Clock()

        updates = 0

        # Quit flag
        self.quit = 0
        
        # Pause flag
        self.pause = 0
        
        self.simple_eventloop(clock, framerate)
        
        # Save the high scores.
        self.config.save_scores()

        # Save the control definitions
        self.config.save_controls()
    
    def simple_eventloop(self, clock, framerate):
    
        while self.quit == 0:
        
            # Render the objects.
            self.render(self.screen)
            
            # Display the completed buffer.
            pygame.display.flip()

            # Wait until the next frame.
            elapsed = clock.tick(framerate)
            
            # Receive and act on events.
            self.listen()
            
            self.update()
    
    def dynamic_eventloop(self, clock, framerate, updaterate):
    
        while self.quit == 0:
        
            # Render the objects.
            self.render(self.screen)
            
            # Display the completed buffer.
            pygame.display.flip()

            # Wait until the next frame.
            elapsed = clock.tick(framerate)
            
            # Calculate the number of updates required before the next
            # frame.
            updates = updates + (elapsed * updaterate) / 1000.0
            
            while updates >= 1.0:
            
                # Receive and act on events.
                self.listen()
                
                self.update()
                updates = updates - 1.0
            
            # We only need to wait long enough to increase our required
            # number of updates to 1.0.
            try:
            
                framerate = self.config.framerate / (1 - updates)
            
            except ZeroDivisionError:
            
                framerate = self.config.framerate
            
            #print self.objects[1]
    
    def add_object(self, object, layer = 0, index = -1):
    
        """add_object(self, object, layer = 0, index = -1)
        
        Add an Object to the list of maintained objects.
        """
        
        if index == -1:
            self.objects[layer].append(object)
        else:
            self.objects[layer].insert(index, object)
    
    def remove_object(self, object, layer = 0):
    
        """remove_object(self, object, layer = 0)
        
        Remove an Object from the list of maintained objects.
        """

        self.objects[layer].remove(object)
    
    def find_object(self, class_object, layer = 0, all = 0):
    
        """find_object(self, class, layer = 0, all = 0)
        
        Find the first instance (all = 0) or all instances (all = 1)
        of a particular class.
        """
        
        if type(class_object) != types.ClassType:
        
            if all == 1:
                return []
            else:
                return None
        
        found = []
        
        for object in self.objects[layer]:
        
            if isinstance(object, class_object):
            
                if all == 1:
                    # Collect all appropriate instances.
                    found.append(object)
                else:
                    # Return the first instance found.
                    return object
        
        return found
    
    def count_objects(self, class_object, layer = 0):
    
        """count_objects(self, class, layer = 0)
        
        Count the number of instances of a particular class in a given layer.
        """

        if type(class_object) != types.ClassType:
        
            return 0
        
        found = 0
        
        for object in self.objects[layer]:
        
            if isinstance(object, class_object):
            
                # Count all appropriate instances.
                if object.fading != "out":
                
                    found = found + 1
        
        return found
    
    def collide_object(self, object, class_object, layer = 2, all = 0):
    
        """collide_object(self, class, layer = 2, all = 0)
        
        Find the first instance (all = 0) or all instances (all = 1)
        of a particular class.
        """
        
        # Determine the bounding box of the object to be checked.
        try:
            bbox = pygame.Rect(list(object.position) + list(object.image_size))
        
        except AttributeError:
            return []
        
        # Retrieve all objects of the required class in the level specified.
        found = self.find_object(class_object, layer, all = 1)
        
        collide = []
        
        for target in found:

            try:
                this_bbox = list(target.position) + list(target.image_size)
                
                if bbox.colliderect(this_bbox):
                
                    if all == 1:
                        # Collect all appropriate instances.
                        collide.append(target)
                    else:
                        # Return the first instance found.
                        return target
            
            except AttributeError:
            
                pass
        
        return collide
    
    def add_event(self, event):
    
        """add_event(self, event)
        
        Add an event to the list of maintained events.
        """
        
        self.events.append(event)
    
    def remove_event(self, event):
    
        """remove_event(self, event)
        
        Remove an event from the list of maintained events.
        """
        
        self.events.remove(event)
    
    def find_event(self, class_event, all = 0):
    
        """find_event(self, class, all = 0)
        
        Find the first instance (all = 0) or all instances (all = 1)
        of a particular class.
        """
        
        if type(class_event) != types.ClassType:
        
            if all == 1:
                return []
            else:
                return None
        
        found = []
        
        for event in self.events:
        
            if isinstance(event, class_event):
            
                if all == 1:
                    # Collect all appropriate instances.
                    found.append(event)
                else:
                    # Return the first instance found.
                    return event
        
        return found
    
    def render(self, screen):
    
        # Render the objects
        for layer in self.objects:
        
            for object in layer:
            
                # Render this object.
                object.render(screen)
    
    def update(self):

        # Update the objects
        for layer in self.objects:
        
            for object in layer:
            
                if not self.pause:
                
                    # Update this object.
                    object.update()
    
    def listen(self):
    
        # Determine whether rendering is required or whether the application
        # should quit.
        
        events = self.sdl_event.event_handler()
                    
        return self.event_handler(events)
    
    def event_handler(self, events):
    
        """event_handler(self, event)
        
        Pass events from subclasses of CommunicationHandler to objects
        and perform the actions they return.
        """
        
        # Act on events kept from last time the handler was invoked.
        events = self.events + events
        
        #if events != []:
        #
        #    print events
        #    print self.objects
        
        # Clear the internal list, ready for queued events to be stored.
        self.events = []
        
        # List of objects to be rendered.
        rendered = []
        
        removed = []
        
        # List of objects to be added to the object list.
        added = []
        
        for event in events:
        
            if isinstance(event, Action) and event.object != None:
            
                # If this event is sent to a particular object then
                # try to pass it to that object's event handler.
                #actions = event.object.event_handler(event)
                
                claimed, to_add, to_remove = \
                    self.execute_actions([event], event.object)
                
                # Add the objects to be rendered, added and removed onto their
                # respective lists.
                added = added + to_add
                removed = removed + to_remove
            
            elif isinstance(event, ExitApplication):
            
                # Cause application to exit.
                self.quit = 1
                
            else:
            
                # Allow each object to act on this event.
                
                for layer in self.objects:
                
                    for object in layer:
                    
                        # Pass the event to this object and receive a list of
                        # actions to perform on its behalf (events to be
                        # queued).
                        actions = object.event_handler(event)
                        
                        claimed, to_add, to_remove = \
                            self.execute_actions(actions, object)
                        
                        # Add the objects to be rendered, added and removed
                        # onto their respective lists.
                        added = added + to_add
                        removed = removed + to_remove
                        
                        # If the event has been claimed then leave this layer.
                        if claimed == 1:
                        
                            break
        
        #if removed: print removed
        
        # Remove objects from the object list.
        for layer in range(len(self.objects)):
        
            new_objects = []
            
            for object in self.objects[layer]:
            
                # Remove the object from the object list.
                if object not in removed:
                
                    new_objects.append(object)
                
                #else:
                #
                #    # Unlink the object from its parent prior to its
                #    # deletion.
                #    object.unlink()
        
            # Store the new list of objects.
            self.objects[layer] = new_objects
        
        for object, layer, index in added:
        
            if index != -1:
                self.objects[layer].insert(index, object)
            else:
                self.objects[layer].append(object)
    
    
    def execute_actions(self, actions, object):
    
        # Flag determining whether this event has been claimed and is
        # not to be passed to subsequent objects.
        claimed = 0
        
        # List of objects to be added to the object list.
        to_add = []
        
        # List of objects to be removed from the object list.
        to_remove = []
        
        for action in actions:
        
            if isinstance(action, RemoveObject):
            
                # Remove an object from the object list.
                
                if action.object != None:
                
                    # An object was specified.
                    to_remove.append(action.object)
                else:
                    # This object was implied.
                    to_remove.append(object)
                
            elif isinstance(action, AddObject):
            
                # Add an object to the object list.
                
                to_add.append( (action.object, action.layer, action.index) )

            elif isinstance(action, ClaimEvent):

                # Do not pass this event to other objects.
                claimed = 1
            
            elif isinstance(action, UpdateObject):
            
                # Cause object to be updated immediately.
                if action.object != None:
                
                    # An object was specified.
                    action.object.update()
                else:
                    # This object was implied.
                    object.update()
            
            elif isinstance(action, AddEvent):
            
                # Queue an event.
                self.events.append(action.object)
        
        return claimed, to_add, to_remove



if __name__ == "__main__":

    # Split the path to determine the path to prepend to resource paths.
    path = os.path.split(sys.argv[0])[0]
    
    # Initialise Pygame.
    pygame.init()
    
    # Create a Game instance.
    game = Game(path)
    
    # Execute the main loop.
    game.mainloop()
    
    # Exit
    sys.exit()
