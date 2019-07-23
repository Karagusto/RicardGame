
"""
music.py

Unused music class and features for Space Explorer.

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

class Music:

    def __init__(self, resources):
    
        self.resources = resources
        
        # Don't try to play music if the sound system is not set up;
        # the samples won't have been loaded and the mixer won't work.
        self.status = self.resources.sound_status
        
        if self.status == 1:
        
            # The samples are given in a dictionary of samples which were
            # initialised in the main program.
            self.samples = self.resources.samples
            
            # The index into the sequence of samples.
            self.sequence_pos = 0
        
        # Playing flag        
        self.playing = 0
        
        # Update counter
        self.update = 0
        
        # Reset flag
        self.reset = None

    def setup_music(self, tempo, sequence_length):
    
        """setup_music(tempo, sequence_length)
        
        Set up the tempo and music sequence.
        
        The tempo is the number of minimum number of updates between
        two samples.
        
        The length of the repeating sequence used for the music is
        given by the sequence_length parameter. Samples are placed in
        a sequence list 
        """
        
        if self.status == 1:
        
            # The tempo is the minimum number of updates between two samples
            # on the same channel.
            
            self.tempo = tempo
            
            # The sequence length defines how many samples can be played
            # before the sequence repeats.
            self.sequence = [[None]] * sequence_length
            self.sequence_length = sequence_length

    def start_music(self, reset_sequence = 0):
    
        # Ensure that all the necessary information has been set up.
        if self.status == 0: return
        
        # Set the playing flag
        self.playing = 1
        
        # Set the current sequence position, if necessary.
        if reset_sequence == 1:
        
            self.sequence_pos = 0
        
            # Reset the update frame.
            self.update = 0
    
    def play_music(self):
    
        # Only play samples if the playing flag is set.
        if self.playing == 0: return

        # Update the update frame counter.
        self.update = self.update + 1
        
        if self.update < self.tempo: return
        
        # Enough updates have occurred.
        
        # Reset the update counter.
        self.update = 0

        # Play all the samples in the current sequence entry.
        samples = self.sequence[self.sequence_pos]
        
        for name in samples:
        
            # Play each sample.
            if name is not None:
            
                sample = self.samples[name]
            
                if sample is not None:
            
                    sample.play()
        
        # Clear this entry in the sequence.
        #self.sequence[self.sequence_pos] = [None] * self.number_of_channels
        
        # Move to the next entry in the sequence.
        self.sequence_pos = (self.sequence_pos + 1) % self.sequence_length
        
        if self.reset is not None and self.sequence_pos == 1:

            self.setup_music(self.reset[0], self.reset[1])
            self.reset = None

    def ready(self):
    
        return self.update == 0

    def stop_music(self):
    
        # Unset the playing flag.
        self.playing = 0

    def add_samples(self, samples, places = 0, relative = 1):
    
        """add_samples(samples, places = 0, relative = 1)
        
        Add samples to the sequence. If relative is set then samples
        will be added at the current sequence position (so that they
        will be played immediately) or at a number of places further
        ahead in the sequence list.
        
        Absolute positions in the sequence list can be specified by
        unsetting the relative flag and giving the position in the
        places parameter.
        """
        
        if self.playing == 0: return
        
        if relative:
        
            place = (self.sequence_pos + places) % self.sequence_length
        
        else:
        
            place = places % self.sequence_length
        
        # Store the samples list in the relevant place in the sequence
        # list.
        self.sequence[place] = samples
