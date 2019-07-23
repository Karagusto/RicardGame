
"""
level.py

Level generation class for Space Explorer.

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

import math, random, types

# URL fetching
#import urllib
#from urlparse import urljoin

# HTML parsing
#from xml.dom.ext.reader import HtmlLib

# Document navigation
#import xml.xpath

# Game objects
import gameobjects


class Level:

    """Level(parent, url)
    
    An object describing the contents of a level.
    """
    
    sounds = \
    (
        "explosion", "explosion", "explosion", "explosion", "explosion",
        "explosion", "explosion", "explosion", "explosion", "explosion",
        "explosion", "explosion", "explosion", "explosion", "explosion"
    )
    
    def __init__(self, parent, number):
    
        # Set the object's parent and configuration object.
        self.parent = parent
        self.config = parent.config
        
        # Set the level number; this will be used for object generation.
        self.number = number
        
        # The level type is derived from the level number.
        self.type = ""
        
        # No objects are defined initially.
        # These lists will eventually contain objects to add in the case of
        # the first list, and objects to remove in the case of the second.
        self.add_objects = []
        self.remove_objects = []
        
        # Frame number
        self.frame = 0
        
        # The maximum type of alien to be introduced is this value minus one.
        self.alien_max = 6
    
    def create_level(self):
    
        """create_level(self)
        
        Interpret the level number and produce level objects based on its
        inerpretation.
        """
        
        # Create a list of items from the level number given.
        
        # Number of items allowed on this level.
        #items_limit = min(24, ( int(self.number / 9) + 1 ) * 6)
        
        # By resticting the number of items available to below the number
        # of objects expected, we can force aliens in the wave to be
        # "upgraded" to different types.
        
        # Level at which an increase in objects occurs.
        #increase_level = max(3, int(self.config.game_max_objects / 2))
        increase_level = 12
        
        # Amount by which the number increases at the increase level.
        #increase_amount = max(2, int(self.config.game_max_objects / 3))
        increase_amount = 6
        
        items_limit = min(
            self.config.game_max_objects,
            (int(self.number / increase_level) + 1) * increase_amount
            )
        
        # First item appearance (seconds)
        t = 1.0
        
        # Time between appearances
        dt = 1.5
        
        items = []
        times = []
        positions = []
        
        # Generate objects depending on the level type.
        
        if self.number < 3:
        
            # Introductory levels
            self.type = "intro"
            
            items, times = \
                self.intro_level(2 << self.number, t, dt)
            level_subtitle = self.config.game_level_subtitle_text["intro"]
            level_colour = self.config.game_level_subtitle_colour["intro"]
        
        elif self.number % 10 == 2:
        
            # Generation levels
            self.type = "generation"
            
            items, times = \
                self.generation_level(self.config.game_max_objects, t, dt)
            level_subtitle = self.config.game_level_subtitle_text["generation"]
            level_colour = self.config.game_level_subtitle_colour["generation"]
        
        elif self.number % 10 == 5:
        
            # Formation levels
            self.type = "formation"
            
            items, times = \
                self.formation_level(self.config.game_max_objects, t, 0.5)
            level_subtitle = self.config.game_level_subtitle_text["formation"]
            level_colour = self.config.game_level_subtitle_colour["formation"]
        
        elif self.number % 10 == 8:
        
            # Free form levels
            self.type = "free form"
            
            items, times = \
                self.free_form_level(items_limit, t, dt)
            level_subtitle = self.config.game_level_subtitle_text["free form"]
            level_colour = self.config.game_level_subtitle_colour["free form"]
        
        elif self.number % 10 == 0:
        
            # Rescue levels
            self.type = "rescue"
            
            items, times = \
                self.free_form_level(items_limit, t, dt)
            level_subtitle = self.config.game_level_subtitle_text["rescue"]
            level_colour = self.config.game_level_subtitle_colour["rescue"]
        
        elif self.number % 10 == 3 or self.number % 10 == 7:
        
            # Legacy attack levels
            self.type = "legacy"
            
            items, times = \
                self.legacy_level(self.config.game_max_objects, t, dt)
            level_subtitle = self.config.game_level_subtitle_text["legacy"]
        
        else:
        
            # Standard attack levels
            self.type = "standard"
            
            items, times = \
                self.standard_level(self.config.game_max_objects, t, dt)
            level_subtitle = self.config.game_level_subtitle_text["standard"]
        
        
        # Sometimes, introduce an unescorted starship.
        if self.number > 2 and random.randrange(0, 50) == 49:
        
            # Choose an index in the list of items.
            index = random.randrange(0, len(items))
            
            # Read the times for the corresponding object.
            add_frame, remove_frame = times[index]
            
            add_time = add_frame / self.config.updaterate
            
            # Create an off-screen position for the starship.
            edge, x, y = self.random_position()
            
            # Insert objects into the list at this point.
            objects = self.create_object( 0, add_time, (x, y) )
            
            for object, add_frame, remove_frame in objects:
            
                items.insert(index, object)
                times.insert( index, (add_frame, remove_frame) )
        
        
        # Compile lists of objects to be added and removed at various times.
        
        for i in range(len(items)):
        
            objects = items[i]
            
            add_frame = times[i][0]
            remove_frame = times[i][1]
            
            if objects:
            
                # Find the correct place to add the object in each list.
                if add_frame != None:
                
                    at = 0
                    for details in self.add_objects:
                    
                        if add_frame < details[0]:
                            break
                        
                        at = at + 1
                    
                    self.add_objects.insert(at, (add_frame, objects))
                
                if remove_frame != None:
                
                    at = 0
                    for details in self.remove_objects:
                    
                        if remove_frame < details[0]:
                            break
                        
                        at = at + 1
                    
                    self.remove_objects.insert(at, (remove_frame, objects))
        
        # Create a level subtitle if required.
        
        if level_subtitle:
        
            level_text = gameobjects.TemporaryText(
                self.parent,
                ( self.config.screen_size[0]/2,
                  self.config.screen_size[1]/2 + self.config.title_size ),
                level_subtitle, self.config.game_title_size,
                colour = level_colour
                )
        
        else:
        
            level_text = None
        
        # Return the level subtitle
        return level_text
    
    # Introductory level generator
    
    def intro_level(self, limit, t, dt):
    
        items = []
        times = []
        positions = []
        
        # The type of alien to be used.
        alien = 1
        
        # Number of aliens/objects to appear.
        number = min(2 + (self.number * 3), limit)
        
        edge = self.number % 2
        
        # Dodgy hack to change the direction of background scrolling.
        # Ideally, a background object would be returned to the management
        # object.
        self.set_scroll_direction(None)
        
        # Start slightly later than for the usual levels.
        t = t + (3 - self.number)
        
        for i in range(0, number):
        
            if len(items) < limit:
            
                # We can add more aliens.
                
                # Give them positions off-screen corresponding to the major
                # and minor coordinates, depending on the edge of the screen
                # at which they will appear.
                
                if edge == 0:
                
                    if i % 2 == 0:
                    
                        # Left column
                        x = self.config.screen_size[0] * 0.2
                        y = -0.1 * self.config.screen_size[1]
                        target_positions = \
                        [
                            ( x, 0.9 * self.config.screen_size[1] )
                        ]
                    
                    elif i % 2 == 1:
                    
                        # Right column
                        x = self.config.screen_size[0] * 0.8
                        y = 1.1 * self.config.screen_size[1]
                        target_positions = \
                        [
                            ( x, 0.1 * self.config.screen_size[0] )
                        ]
                
                else:
                
                    if i % 2 == 0:
                    
                        # Top row
                        x = -0.1 * self.config.screen_size[0]
                        y = self.config.screen_size[1] * 0.2
                        target_positions = \
                        [
                            ( 0.9 * self.config.screen_size[0], y)
                        ]
                    
                    elif i % 2 == 1:
                    
                        # Bottom row
                        x = 1.1 * self.config.screen_size[0]
                        y = self.config.screen_size[1] * 0.8
                        target_positions = \
                        [
                            ( 0.1 * self.config.screen_size[0], y)
                        ]
                
                objects = self.create_object(alien, t, (x, y), target_positions)
                
                for object, add_time, remove_time in objects:
                
                    items.append(object)
                    times.append((add_time, remove_time))
                
                t = t + dt
        
        return items, times
    
    # Standard level generator
    
    def standard_level(self, limit, t_start, dt_start):
    
        # Create a list of alien numbers, possibly containing further lists
        # of aliens to represent groups of them.
        items = []
        times = []
        
        # Define two coordinates for positioning the aliens as they appear
        # on-screen.
        major_max = 12
        minor_max = 8
        
        # Number of aliens/objects to appear.
        number = min(( int(self.number / 10) + 1 ) * minor_max, limit)
        
        # The type of alien to be introduced on the level.
        # Increases every 20 levels and starts at 1 again every 160 levels.
        #alien = (int(self.number / 20) % self.alien_max) + 1
        alien = 1
        
        # Alien counter
        alien_counter = 0
        
        # The number of objects introduced at which the type of alien is
        # changed.
        alien_level = minor_max
        
        # Determine the alien types.
        aliens = []
        
        for i in range(0, number):
        
            # Add an alien type to the list.
            if alien < 4:
            
                aliens.append(alien)
            
            else:
            
                # Only add Capturers at the centre of a row/column.
                
                if minor_max % 2 == 1 and (i % minor_max) == (minor_max - 1)/2:
                
                    aliens.append(alien)
                
                elif minor_max % 2 == 0:
                
                    if i % minor_max == minor_max/2 - 1:
                    
                        aliens.append(alien)
                    
                    elif i % minor_max == minor_max/2:
                    
                        aliens.append(alien)
                    
                    else:
                    
                        aliens.append(1)
                
                else:
                
                    aliens.append(1)
            
            # Increase the alien counter.
            alien_counter = alien_counter + 1
            
            if (alien_counter % alien_level) == 0:
            
                # Increase the alien type up to the maximum.
                alien = ((alien + 1) % self.alien_max) or 1
        
        edge = self.number % 4
        
        if edge % 2 == 0:
        
            # Top and bottom edges
            minor_step = (0.75 * self.config.screen_size[0]) / (minor_max - 1)
            
            if edge % 4 == 2:
            
                # Bottom edge
                major_step = -self.config.screen_size[1] / major_max
                major_start = 1.1 * self.config.screen_size[1]
                major_offset = self.config.screen_size[1]
            
            else:
            
                # Top edge
                major_step = self.config.screen_size[1] / major_max
                major_start = -0.1 * self.config.screen_size[1]
                major_offset = 0
            
            minor_offset = 0.125 * self.config.screen_size[0]
        
        else:
        
            # Left and right edges
            minor_step = (0.75 * self.config.screen_size[1]) / (minor_max - 1)
            
            if edge % 4 == 1:
            
                # Right edge
                major_step = -self.config.screen_size[0] / major_max
                major_start = 1.1 * self.config.screen_size[0]
                major_offset = self.config.screen_size[0]
            
            else:
            
                # Left edge
                major_step = self.config.screen_size[0] / major_max
                major_start = -0.1 * self.config.screen_size[0]
                major_offset = 0
            
            minor_offset = 0.125 * self.config.screen_size[1]
        
        # Dodgy hack to change the direction of background scrolling.
        # Ideally, a background object would be returned to the management
        # object.
        self.set_scroll_direction(edge % 4, speed = int(self.number / 16) + 1)
        
        # Generate the objects and aliens.
        t = t_start
        dt = dt_start
        
        # Time counters and limits.
        time_counter = 0
        time_limit = max(1, minor_max >> int(self.number/10))
        
        # Set up major and minor coordinates.

        # Use the number of starships in play to make the start positions
        # of the aliens more difficult to deal with, if necessary.
        
        starships = self.parent.count_objects(
            gameobjects.Starship, layer = 2
            )
        
        # There may be no starships present when the level is being created
        # so ensure that we take into account the future presence of at
        # least one.
        starships = max(1, starships)
        
        # Determine the largest major axis coordinate to be used.
        
        largest_major = min(major_max, int((number - 1) / minor_max) + 1)
        major = range(largest_major, largest_major - int(number/minor_max), -1)
        
        # A row/column of aliens will cross the screen for every extra
        # starship that is in play.
        
        for i in range(0, min(starships - 1, len(major))):
        
            major[i] = max(1, major_max - i - 1)
        
        minor = 0
        
        for i in range(0, number):
        
            # We can add more aliens.
            
            # Give them positions off-screen corresponding to the major
            # and minor coordinates, depending on the edge of the screen
            # at which they will appear.
            
            if (edge % 2) == 0:
            
                # Top and bottom borders
                x = (minor * minor_step) + minor_offset
                y = major_start
                target_positions = \
                [
                    (x, major_offset + (major[0] * major_step))
                ]
            
            elif (edge % 2) == 1:
            
                # Left and right borders
                y = (minor * minor_step) + minor_offset
                x = major_start
                target_positions = \
                [
                    (major_offset + (major[0] * major_step), y)
                ]
            
            objects = self.create_object(aliens[i], t, (x, y), target_positions)
            
            for object, add_time, remove_time in objects:
            
                items.append(object)
                times.append((add_time, remove_time))
            
            t = t + dt
            
            # Increase the minor counter until the maximum is reached.
            minor = minor + 1
            
            if minor == minor_max:
            
                minor = 0
                major.pop(0)
                
                dt = min(1.0, dt - 0.5)
            
            time_counter = time_counter + 1
            
            if time_counter % time_limit == 0:
            
                # Reset the times so that the next set of aliens arrives
                # with the corresponding aliens in the previous set.
                t_start = t_start + 0.25
                
                t = t_start
                dt = dt_start
        
        return items, times
    
    # Legacy attack level generator
    
    def legacy_level(self, limit, t_start, dt_start):
    
        # Create a list of alien numbers, possibly containing further lists
        # of aliens to represent groups of them.
        items = []
        times = []
        
        major_max = 12
        minor_max = 12
        
        # Use the number of starships in play to make the start positions
        # of the aliens more difficult to deal with, if necessary.
        
        starships = self.parent.count_objects(
            gameobjects.Starship, layer = 2
            )
        
        # There may be no starships present when the level is being created
        # so ensure that we take into account the future presence of at
        # least one.
        starships = max(1, starships)
        
        # Number of formations to create.
        
        # Adjust the number of formations depending on the number of extra
        # starships present. There can be no more than the object limit
        # will allow and no more than four.
        
        formations = min(4, (int(self.number / 15) % 4) + 1 + (starships - 1))
        
        # The desired number of aliens in each formation.
        ideal_rows = min( int(self.number / 30) + 3, 4 )
        
        # Calculate the number of rows that can be used to give that many
        # equally sized formations.
        equal_rows = max(1, int(math.sqrt(limit / formations)))
        
        # Number of rows of aliens in each formation.
        aliens = limit
        
        rows = []
        
        # Initially use equally sized formations or the ideal size, if that
        # is smaller.
        for f in range(0, formations):
        
            rows.append(min(ideal_rows, equal_rows))
            aliens = aliens - equal_rows
        
        # Try to increase the size of all of the formations as many times as
        # possible.
        
        failed = 0
        full_size = 0
        
        while aliens > 0 and failed == 0 and full_size < formations:
        
            for f in range(0, formations):
            
                # If there are enough aliens to extend this formation
                # then add the required number.
                if rows[f] < ideal_rows:
                
                    if aliens >= (2 * rows[f]) + 1:
                    
                        rows[f] = rows[f] + 1
                        aliens = aliens - ((2 * rows[f]) + 1)
                        
                        if rows[f] == ideal_rows:
                        
                            full_size = full_size + 1
                    
                    else:
                    
                        failed = 1
                
                else:
                
                    full_size = full_size + 1
        
        edges = ( (0, 2, 1, 3), (1, 3, 0, 2), (2, 0, 3, 1), (3, 1, 2, 0) )
        
        # Generate each formation.
        
        dt = dt_start / 2.0
        
        for f in range(0, formations):
        
            sw, sh = self.config.screen_size
            
            # Determine the corners of the screen the aliens are to appear in.
            edge = edges[self.number % 4][f]
            
            if edge == 0:
            
                # Top left of the screen. Aliens descend from above the screen.
                major_step = (0, sh / major_max)
                minor_step = (sw / minor_max, 0)
                offset = (0, 0)
            
            elif edge == 1:
            
                # Top right of the screen. Aliens come from the right of
                # the screen.
                major_step = (-sw / major_max, 0)
                minor_step = (0, sh / minor_max)
                offset = (sw, 0)
            
            elif edge == 2:
            
                # Bottom right of the screen. Aliens descend from below the screen.
                major_step = (0, -sh / major_max)
                minor_step = (-sw / minor_max, 0)
                offset = (sw, sh)
            
            else:
            
                # Bottom left of the screen. Aliens come from the left of
                # the screen.
                major_step = (sw / major_max, 0)
                minor_step = (0, -sh / minor_max)
                offset = (0, sh)
            
            # Generate the objects and aliens in this formation.
            t = t_start
            
            size = rows.pop(0)
            
            for major in range(size, 0, -1):
            
                for minor in range(1, size + 1):
        
                    # Give them positions off-screen corresponding to the major
                    # and minor coordinates, depending on the edge of the screen
                    # at which they will appear.
                    
                    x = offset[0] + (minor * minor_step[0]) - major_step[0]
                    y = offset[1] + (minor * minor_step[1]) - major_step[1]
                    
                    target_positions = \
                    [
                        ( offset[0] + (minor * minor_step[0]) + \
                            (major * major_step[0]),
                          offset[1] + (minor * minor_step[1]) + \
                            (major * major_step[1]) )
                    ]
                    
                    if minor <= size - 3 and major <= size - 3:
                    
                        alien = 9
                    
                    elif minor <= size - 2 and major <= size - 2:
                    
                        alien = 8
                    
                    elif minor <= size - 1 and major <= size - 1:
                    
                        alien = 7
                    
                    else:
                    
                        alien = 6
                    
                    objects = self.create_object(
                        alien, t, (x, y), target_positions
                        )
                    
                    for object, add_time, remove_time in objects:
                    
                        items.append(object)
                        times.append((add_time, remove_time))
                
                # Add the next row a little later.
                t = t + dt
            
            # Add each formation a little later than the last.
            t_start = t_start + dt
        
        # Dodgy hack to change the direction of background scrolling.
        # Ideally, a background object would be returned to the management
        # object.
        self.set_scroll_direction(None)
        
        return items, times
    
    # Formation level generator
    
    def formation_level(self, limit, t_start, dt_start):
    
        # Dodgy hack to change the direction of background scrolling.
        # Ideally, a background object would be returned to the management
        # object.
        self.set_scroll_direction(None)
        
        # Number of aliens/objects to appear.
        aliens_per_stream = 8
        
        number = min(max(8, ( int(self.number/7) * aliens_per_stream)), limit)
        
        # Split the objects into many streams, if possible.
        number_of_streams = int(number / aliens_per_stream) + 1
        
        if (self.number / 10) % 3 == 1:
        
            streams = self.box_formation(number_of_streams, t_start, dt_start)
        
        elif (self.number / 10) % 3 == 2:
        
            streams = self.swirl_formation(number_of_streams, t_start, dt_start)
        
        else:
        
            streams = self.snake_formation(number_of_streams, t_start, dt_start)
        
        # Generate the objects and aliens.
        items = []
        times = []
        
        t = t_start
        dt = dt_start
        
        # The stream number
        stream = 0
        
        # The type of alien to be introduced on the level.
        # Increases every 20 levels and starts at 1 again every 160 levels.
        alien = 1
        
        # Alien counter
        alien_counter = 0
        
        # Number of aliens at which the type of alien is changed.
        alien_level = aliens_per_stream * 2
        
        # Certain aliens break formation.
        breakers = []
        i = 0
        
        while i < number:
        
            i = i + random.randrange(1, 4)
            
            if i < number:
            
                breakers.append(i)
        
        for i in range(0, number):
        
            if i % 8 == 7:
            
                #use_alien = ((alien + 1) % self.alien_max) or 1
                use_alien = alien
            
            else:
            
                use_alien = alien
            
            # We can add more aliens.
            x, y = streams[stream][0]
            
            # The target positions for each alien are usually the whole stream,
            # but some aliens break formation earlier.
            if i in breakers:
            
                l = 1 + random.randrange(0, len(streams[stream]))
                target_positions = streams[stream][1:l]
            
            else:
            
                target_positions = streams[stream][1:]
            
            objects = self.create_object(use_alien, t, (x, y), target_positions)
            
            for object, add_time, remove_time in objects:
            
                items.append(object)
                times.append((add_time, remove_time))
            
            t = t + dt
            
            alien_counter = alien_counter + 1
            
            if (alien_counter % aliens_per_stream) == 0:
            
                # Increase the alien type up to the maximum.
                alien = ((alien + 1) % self.alien_max) or 1
                
                stream = stream + 1
                
                # Reset the times so that the next set of aliens arrives
                # with the corresponding aliens in the previous set.
                t = t_start
                dt = dt_start
        
        return items, times
    
    def box_formation(self, number_of_streams, t_start, dt_start):
    
        # Screen dimensions
        half_x = self.config.screen_size[0]/2
        half_y = self.config.screen_size[1]/2
        
        # Set up each stream and the start position of aliens in each
        # stream.
        streams = []
        
        # Number of stream start positions.
        minor_max = 8
        minor_step = 0.75 / (minor_max - 1)
        minor_offset = 0.125
        minor = 0
        
        for i in range(0, number_of_streams):
        
            # Position the streams off-screen.
            
            if (i + int(self.number/9)) % 4 == 0:
            
                # Top border
                x = (minor_offset + (minor * minor_step)) * \
                    self.config.screen_size[0]
                
                y = -0.1 * self.config.screen_size[1]
            
            elif (i + int(self.number/9)) % 4 == 1:
            
                # Right border
                y = (minor_offset + (minor * minor_step)) * \
                    self.config.screen_size[1]
                
                x = 1.1 * self.config.screen_size[0]
            
            elif (i + int(self.number/9)) % 4 == 2:
            
                # Bottom border
                x = (minor_offset + (minor * minor_step)) * \
                    self.config.screen_size[0]
                
                y = 1.1 * self.config.screen_size[1]
            
            else:
            
                # Left border
                y = (minor_offset + (minor * minor_step)) * \
                    self.config.screen_size[1]
                
                x = -0.1 * self.config.screen_size[0]
            
            stream = [(x, y)]
            
            # Add positions to each stream.
            for j in range(0, 20):
            
                # Determine a new position for the stream.
                if j % 2 == 0:
                
                    x = half_x - 0.8 * (x - half_y)
                
                else:
                
                    y = half_y - 0.8 * (y - half_y)
                
                if x < (0.1 * self.config.screen_size[0]):
                
                    x = 0.1 * self.config.screen_size[0]
                
                elif x > (0.9 * self.config.screen_size[0]):
                
                    x = 0.9 * self.config.screen_size[0]
                
                elif y < (0.1 * self.config.screen_size[1]):
                
                    y = 0.1 * self.config.screen_size[1]
                
                elif y > (0.9 * self.config.screen_size[1]):
                
                    y = 0.9 * self.config.screen_size[1]
                
                # Add this coordinate pair to the stream.
                stream.append( (x, y) )
            
            # Change the stream start position counter.
            minor = (minor + 1) % minor_max
            
            # Add this stream to the list of streams.
            streams.append(stream)
        
        # Return the streams information.
        return streams
    
    def swirl_formation(self, number_of_streams, t_start, dt_start):
    
        # Screen dimensions
        half_x = self.config.screen_size[0]/2
        half_y = self.config.screen_size[1]/2
        
        # Set up each stream and the start position of aliens in each
        # stream.
        streams = []
        
        # Number of stream start positions.
        minor_max = 8
        minor_step = 0.75 / (minor_max - 1)
        minor_offset = 0.125
        minor = 0
        
        for i in range(0, number_of_streams):
        
            # Position the streams off-screen.
            
            if (i + int(self.number/9)) % 4 == 0:
            
                # Top border
                x = (minor_offset + (minor * minor_step)) * \
                    self.config.screen_size[0]
                
                y = -0.1 * self.config.screen_size[1]
            
            elif (i + int(self.number/9)) % 4 == 1:
            
                # Right border
                y = (minor_offset + (minor * minor_step)) * \
                    self.config.screen_size[1]
                
                x = 1.1 * self.config.screen_size[0]
            
            elif (i + int(self.number/9)) % 4 == 2:
            
                # Bottom border
                x = (minor_offset + (minor * minor_step)) * \
                    self.config.screen_size[0]
                
                y = 1.1 * self.config.screen_size[1]
            
            else:
            
                # Left border
                y = (minor_offset + (minor * minor_step)) * \
                    self.config.screen_size[1]
                
                x = -0.1 * self.config.screen_size[0]
            
            stream = [(x, y)]
            
            steps = 32
            
            radius = min(half_x, half_y)
            angle = math.atan2(half_y - y, x - half_x)
            
            dr = float(radius/steps)
            da = (2 * math.pi) / steps
            
            # Add positions to each stream.
            for j in range(0, steps):
            
                # Determine a new position for the stream.
                radius = radius - dr
                angle = angle + da
                
                x = half_x + (radius * math.cos(angle))
                y = half_y - (radius * math.sin(angle))
                
                # Add this coordinate pair to the stream.
                stream.append( (x, y) )
            
            # Change the stream start position counter.
            minor = (minor + 1) % minor_max
            
            # Add this stream to the list of streams.
            streams.append(stream)
        
        # Return the streams information.
        return streams
    
    def snake_formation(self, number_of_streams, t_start, dt_start):
    
        # Screen dimensions
        half_x = self.config.screen_size[0]/2
        half_y = self.config.screen_size[1]/2
        
        # Set up each stream and the start position of aliens in each
        # stream.
        streams = []
        
        # Number of stream start positions.
        minor_max = 8
        minor_step = 0.75 / (minor_max - 1)
        minor_offset = 0.125
        minor = 0
        
        major_max = 12
        
        for i in range(0, number_of_streams):
        
            stream = []
            
            # Position the streams off-screen.
            edge = (i + int(self.number/9)) % 4
            
            if edge == 0:
            
                # Top border
                x = (minor_offset + (minor * minor_step)) * \
                    self.config.screen_size[0]
                
                y = -0.1 * self.config.screen_size[1]
                
                stream.append( (x, y) )
                
                major_step = 0.8 / (major_max - 1)
                major_offset = 0.1
            
            elif edge == 1:
            
                # Right border
                y = (minor_offset + (minor * minor_step)) * \
                    self.config.screen_size[1]
                
                x = 1.1 * self.config.screen_size[0]
                
                stream.append( (x, y) )
                
                major_step = -0.8 / (major_max - 1)
                major_offset = 0.9
                
                stream.append( (major_offset * self.config.screen_size[1], y) )
            
            elif edge == 2:
            
                # Bottom border
                x = (minor_offset + (minor * minor_step)) * \
                    self.config.screen_size[0]
                
                y = 1.1 * self.config.screen_size[1]
                
                stream.append( (x, y) )
                
                major_step = -0.8 / (major_max - 1)
                major_offset = 0.9
                
                stream.append( (x, major_offset * self.config.screen_size[1]) )
            
            else:
            
                # Left border
                y = (minor_offset + (minor * minor_step)) * \
                    self.config.screen_size[1]
                
                x = -0.1 * self.config.screen_size[0]
                
                stream.append( (x, y) )
                
                major_step = 0.8 / (major_max - 1)
                major_offset = 0.1
                
                stream.append( (major_offset * self.config.screen_size[1], y) )
            
            stream = [(x, y)]
            
            # Add positions to each stream.
            for major in range(0, major_max):
            
                # Determine a new position for the stream.
                if edge == 0:
                
                    # Top downwards
                    stream.append(
                        ( x,
                          (major_offset + (major * major_step)) * \
                          self.config.screen_size[1]
                        ) )
                    
                    if x != ((1.0 - minor_offset) * self.config.screen_size[0]):
                    
                        x = (1.0 - minor_offset) * self.config.screen_size[0]
                    
                    else:
                    
                        x = minor_offset * self.config.screen_size[0]
                    
                    stream.append(
                        ( x,
                          (major_offset + (major * major_step)) * \
                          self.config.screen_size[1]
                        ) )
                
                elif edge == 1:
                
                    # Right leftwards
                    stream.append(
                        ( (major_offset + (major * major_step)) * \
                          self.config.screen_size[0],
                          y
                        ) )
                    
                    if y != ((1.0 - minor_offset) * self.config.screen_size[1]):
                    
                        y = (1.0 - minor_offset) * self.config.screen_size[1]
                    
                    else:
                    
                        y = minor_offset * self.config.screen_size[1]
                    
                    stream.append(
                        ( (major_offset + (major * major_step)) * \
                          self.config.screen_size[0],
                          y
                        ) )
                
                elif edge == 2:
                
                    # Bottom upwards
                    stream.append(
                        ( x,
                          (major_offset + (major * major_step)) * \
                          self.config.screen_size[1]
                        ) )
                    
                    if x != ((1.0 - minor_offset) * self.config.screen_size[0]):
                    
                        x = (1.0 - minor_offset) * self.config.screen_size[0]
                    
                    else:
                    
                        x = minor_offset * self.config.screen_size[0]
                    
                    stream.append(
                        ( x,
                          (major_offset + (major * major_step)) * \
                          self.config.screen_size[1]
                        ) )
                
                else:
                
                    # Left rightwards
                    stream.append(
                        ( (major_offset + (major * major_step)) * \
                          self.config.screen_size[0],
                          y
                        ) )
                    
                    if y != ((1.0 - minor_offset) * self.config.screen_size[1]):
                    
                        y = (1.0 - minor_offset) * self.config.screen_size[1]
                    
                    else:
                    
                        y = minor_offset * self.config.screen_size[1]
                    
                    stream.append(
                        ( (major_offset + (major * major_step)) * \
                          self.config.screen_size[0],
                          y
                        ) )
            
            # Change the stream start position counter.
            minor = (minor + 1) % minor_max
            
            # Add this stream to the list of streams.
            streams.append(stream)
        
        # Return the streams information.
        return streams
    
    # Free form level generator
    
    def free_form_level(self, limit, t, dt):
    
        # Dodgy hack to change the direction of background scrolling.
        # Ideally, a background object would be returned to the management
        # object.
        self.set_scroll_direction(None)
        
        # Number of aliens/objects to appear.
        starships = self.parent.count_objects(
            gameobjects.Starship, layer = 2
            )
        
        # There may be no starships present when the level is being created
        # so ensure that we take into account the future presence of at
        # least one.
        starships = max(1, starships)
        
        factor = 4 + starships
        
        number = min(limit, (int(self.number/10) + 1) * factor)
        
        # The type of alien to be introduced on the level.
        # Increases every 20 levels and starts at 1 again every 160 levels.
        alien = (int(self.number / 20) % self.alien_max) or 1
        
        # Alien counter
        alien_counter = 0
        
        # The number of objects introduced at which the type of alien is
        # changed.
        alien_level = max(number - 2, 8)
        
        # Create a list of alien numbers, possibly containing further lists
        # of aliens to represent groups of them.
        aliens = []
        positions = []
        
        for i in range(0, number):
        
            if len(aliens) < limit:
            
                # We can add more aliens.
                
                # Give them a random position off-screen.
                
                edge, x, y = self.random_position()
                
                if (i % 20 == 4) and (self.number % 10 == 0):
                
                    # Introduce a captured starship every twenty items on
                    # every tenth level.
                    
                    if self.number % 20 == 10:
                    
                        aliens.append([4, 0])
                        
                        positions.append([(x, y), (x, y - 32)])
                    
                    else:
                    
                        aliens.append([0, 1, 1])
                        
                        positions.append(
                            [(x, y), (x - 16, y + 16), (x + 16, y + 16)]
                            )
                
                elif i % 5 == 4:
                
                    # Every five iterations add a group of aliens.
                    aliens.append([alien, 1, 1])
                    
                    positions.append([(x, y), (x - 16, y + 16), (x + 16, y + 16)])
                
                else:
                
                    aliens.append(alien)
                    positions.append((x, y))
                
                # Increase the alien counter.
                alien_counter = alien_counter + 1
                
                if (alien_counter % alien_level) == 0:
                
                    # Increase the alien type up to the maximum.
                    alien = ((alien + 1) % self.alien_max) or 1
            
            else:
            
                # No more aliens allowed, so increase the item number.
                change = limit - (i % limit) - 1
                
                if type(aliens[change]) != types.ListType:
                
                    # Single alien
                    
                    aliens[change] = \
                        ((aliens[change] + 1) % self.alien_max) or 1
                
                else:
                
                    # Group of aliens
                    
                    # Change one of the aliens.
                    number = 0 # self.number % len(aliens[i % limit])
                    
                    new_value = \
                        (
                            (aliens[change][number] + 1) % self.alien_max
                        ) or 1
                    
                    if new_value != 1:
                    
                        aliens[change][number] = new_value
        
        # Convert the list of alien numbers into a list of objects with
        # associated lists of entry and exit times.
        
        items = []
        times = []
        
        for i in range(len(aliens)):
        
            objects = self.create_object(aliens[i], t, positions[i])
            
            for object, add_time, remove_time in objects:
            
                items.append(object)
                times.append((add_time, remove_time))
            
            t = t + dt
            dt = max(1.5, dt - 0.2)
        
        return items, times
    
    # Generation level generator
    
    def generation_level(self, limit, t, dt):
    
        # Dodgy hack to change the direction of background scrolling.
        # Ideally, a background object would be returned to the management
        # object.
        self.set_scroll_direction(None)
        
        # Number of aliens/objects to appear.
        starships = self.parent.count_objects(
            gameobjects.Starship, layer = 2
            )
        
        # There may be no starships present when the level is being created
        # so ensure that we take into account the future presence of at
        # least one.
        starships = max(1, starships)
        
        factor = (int(self.number / 15) + 1)
        
        number = min(limit, factor * starships)
        
        # The type of alien to be introduced on the level.
        alien = 5
        
        # Create a list of alien numbers, possibly containing further lists
        # of aliens to represent groups of them.
        aliens = []
        positions = []
        target_positions = []
        
        sw, sh = self.config.screen_size
        
        for i in range(0, number):
        
            if len(aliens) < limit:
            
                # We can add more aliens.
                
                # Give them random positions off-screen and appropriate
                # position on-screen.
                
                edge, x, y = self.random_position()
                
                if edge < 1.0:
                
                    # Top border
                    target_position = \
                    [
                        (x, sh + y),
                        (sw - x, sh + y),
                        (sw - x, -y),
                        (x, -y)
                    ]
                
                elif edge < 2.0:
                
                    # Right border
                    target_position = \
                    [
                        (x - sw, y),
                        (x - sw, sh - y),
                        (sw - (x - sw), sh - y),
                        (sw - (x - sw), y)
                    ]
                
                elif edge < 3.0:
                
                    # Bottom border
                    target_position = \
                    [
                        (x, y - sh),
                        (sw - x, y - sh),
                        (sw - x, sh - (y - sh)),
                        (x, sh - (y - sh))
                    ]
                
                else:
                
                    # Left border
                    target_position = \
                    [
                        (sw + x, y),
                        (sw + x, sh - y),
                        (-x, sh - y),
                        (-x, y)
                    ]
                
                if i % 5 == 4:
                
                    # Every five iterations add an escort to the generator.
                    aliens.append([alien, 1])
                    positions.append([(x, y), (x, y + 24)])
                    target_positions.append(target_position)
                
                else:
                
                    aliens.append(alien)
                    positions.append((x, y))
                    target_positions.append(target_position)
        
        # Convert the list of alien numbers into a list of objects with
        # associated lists of entry and exit times.
        
        items = []
        times = []
        
        for i in range(len(aliens)):
        
            objects = self.create_object(
                aliens[i], t, positions[i], target_positions[i]
                )
            
            for object, add_time, remove_time in objects:
            
                items.append(object)
                times.append((add_time, remove_time))
            
            t = t + dt
            dt = min(1.5, dt - 0.2)
        
        return items, times
    
    # Object creation
    
    def create_object(self, items, time, positions, target_positions = None):
    
        if type(items) != types.ListType:
        
            items = [items]
            positions = [positions]
        
        objects = []
        
        # Check whether the first object in this group is a captured starship.
        if items[0] == 0 and target_positions == None:
        
            target_positions = \
            [
                ( (0.1 + (random.random() * 0.8)) * self.config.screen_size[0],
                  (0.1 + (random.random() * 0.8)) * self.config.screen_size[1] )
            ]
        
        elif target_positions == None:
        
            target_positions = \
            [
                ( (0.1 + (random.random() * 0.8)) * self.config.screen_size[0],
                  (0.1 + (random.random() * 0.8)) * self.config.screen_size[1] )
            ]
        
        for i in range(len(items)):
        
            item = items[i]
            position = positions[i]
            displace = (
                position[0] - positions[0][0], position[1] - positions[0][1]
                )
            
            if item == 0:
            
                # Create an uncontrolled starship.
                starship = gameobjects.Starship(
                    self.parent, position,
                    target_positions = target_positions[:],
                    displace = displace,
                    controlled = 0,
                    )
                
                # Return the starship. It will not disappear until the end of
                # the level.
                
                #objects.append(
                #    ( ( starship, 2, -1 ), int(time * self.config.updaterate),
                #      int((time + 10.0) * self.config.updaterate) )
                #    )
                objects.append(
                    ( ( starship, 2, -1 ), int(time * self.config.updaterate),
                      None )
                    )
            
            elif item == 99:
            
                # Create a gateway object.
                gateway = gameobjects.Gateway(self.parent)
                
                # Return the gateway object. It will disappear between 30
                # seconds and a minute after it was created.
                objects.append(
                    ( ( gateway, 1, -1 ), int(time) * self.config.updaterate,
                      int((time + (random.random() * 30)) * \
                        self.config.updaterate) )
                    )
            
            else:
            
                if item == 1:
                
                    # Create an alien of the relevant type.
                    alien = gameobjects.StartStop(
                        self.parent, position,
                        target_positions = target_positions[:],
                        displace = displace,
                        )
                
                elif item == 2:
                
                    # Create an alien of the relevant type.
                    alien = gameobjects.Follower(
                        self.parent, position,
                        target_positions = target_positions[:],
                        displace = displace,
                        )
                
                elif item == 3:
                
                    # Create an alien of the relevant type.
                    alien = gameobjects.Interceptor(
                        self.parent, position,
                        target_positions = target_positions[:],
                        displace = displace,
                        )
                
                elif item == 4:
                
                    # Create an alien of the relevant type.
                    alien = gameobjects.Capturer(
                        self.parent, position,
                        target_positions = target_positions[:],
                        displace = displace,
                        )
                
                elif item == 5:
                
                    # Create an alien of the relevant type.
                    alien = gameobjects.Generator(
                        self.parent, position,
                        target_positions = target_positions[:],
                        displace = displace,
                        generate_time = 2.0, alien_type = gameobjects.StartStop
                        )
                
                elif item == 6:
                
                    # Create an alien of the relevant type.
                    alien = gameobjects.LegacyStartStop(
                        self.parent, position,
                        target_positions = target_positions[:],
                        displace = displace,
                        )
                
                elif item == 7:
                
                    # Create an alien of the relevant type.
                    alien = gameobjects.LegacyFollower(
                        self.parent, position,
                        target_positions = target_positions[:],
                        displace = displace,
                        )
                
                elif item == 8:
                
                    # Create an alien of the relevant type.
                    alien = gameobjects.LegacyInterceptor(
                        self.parent, position,
                        target_positions = target_positions[:],
                        displace = displace,
                        )
                
                elif item == 9:
                
                    # Create an alien of the relevant type.
                    alien = gameobjects.LegacyCapturer(
                        self.parent, position,
                        target_positions = target_positions[:],
                        displace = displace,
                        )
                
                else:
                
                    # Safety net. This should never be used.
                    alien = gameobjects.StartStop(
                        self.parent, position,
                        target_positions = target_positions[:],
                        displace = displace,
                        )
                
                # Return the alien object. It will disappear after one
                # minute.
                objects.append(
                    ( ( alien, 2, -1 ), int(time * self.config.updaterate),
                      int((time + 60) * self.config.updaterate) )
                    )
        
        return objects
    
    def random_position(self):
    
        l = random.random() * 4.0
        
        if l < 1.0:
        
            # Top border
            x = l * self.config.screen_size[0]
            y = -0.1 * self.config.screen_size[1]
        
        elif l < 2.0:
        
            # Right border
            y = (l % 1.0) * self.config.screen_size[1]
            x = 1.1 * self.config.screen_size[0]
        
        elif l < 3.0:
        
            # Bottom border
            x = (l % 1.0) * self.config.screen_size[0]
            y = 1.1 * self.config.screen_size[1]
        
        else:
        
            # Left border
            y = (l % 1.0) * self.config.screen_size[1]
            x = -0.1 * self.config.screen_size[0]
        
        return l, x, y
    
    def set_scroll_direction(self, edge, speed = 1):
    
        # Dodgy hack to change the direction of background scrolling.
        # Ideally, a background object would be returned to the management
        # object.
        
        background = self.parent.find_object(gameobjects.Background, layer = 1)
        
        # Restrict the speed of scrolling.
        speed = min(8, speed)
        
        if hasattr(background, "direction"):
        
            if edge == 0:
            
                # Scroll upwards.
                background.direction = (0, speed)
            
            elif edge == 1:
            
                # Scroll rightwards.
                background.direction = (-speed, 0)
            
            elif edge == 2:
            
                # Scroll downwards.
                background.direction = (0, -speed)
            
            elif edge == 3:
            
                # Scroll leftwards.
                background.direction = (speed, 0)
            
            else:
            
                # No scrolling.
                background.direction = (0, 0)

    def update_level(self):
    
        # Check whether the current item in the add objects list has
        # a frame number equal to that of the current frame.
        
        while self.add_objects and self.frame >= self.add_objects[0][0]:
        
            # Add the object/objects to the specified layer and at the
            # index given, removing it/them from this list.
            object, layer, index = self.add_objects.pop(0)[1]
            
            self.parent.add_object(object, layer, index)
        
        while self.remove_objects and self.remove_objects[0][0] != None and \
            self.frame >= self.remove_objects[0][0]:
        
            # Remove the object/objects from the specified layer, removing
            # it/them from this list.
            
            object, layer, index = self.remove_objects.pop(0)[1]
            
            if object.controlled != 1:
            
                # The object should have a "fading" attribute which we can use
                # to remove it from the parent's object list, if the object is
                # not controlled. Note that this entry in the removal list
                # possibly should have been removed when the starship was
                # recaptured.
                object.fading = "out"
        
        # If there are more items in each list then increment the frame
        # counter and return 0; otherwise return 1.
        
        if self.add_objects or self.remove_objects:
        
            self.frame = self.frame + 1
            return 0
        
        else:
        
            return 1
    
    def deploy_next(self):
    
        # Take an object immediately, if possible.
        if self.add_objects:
        
            # If the next object is more than half a second in the future,
            # deploy it now.
            
            if self.add_objects[0][0] > \
                (self.frame + (0.5 * self.config.updaterate)):
            
                self.frame, object_tuple = self.add_objects.pop(0)
                
                object, layer, index = object_tuple
                
                self.parent.add_object(object, layer, index)
    
    def finished(self):
    
        if self.add_objects:
        
            return 0
        
        else:
        
            return 1

    def set_tempo(self, music):

        if music.status == 0: return
            
        # Determine the type of music to use depending on the type of
        # level being played.
        
        if self.type == "intro":
        
            tempo = int(self.config.updaterate / 4)
        
        else:
        
            tempo = int(self.config.updaterate / 8)
        
        # Set up the music object.
        music.tempo = tempo
