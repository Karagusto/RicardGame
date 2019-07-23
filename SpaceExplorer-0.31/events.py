
"""
events.py

Event definitions for Space Explorer.

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

# Actions ----------------------------------------------------------------------

class Action:

    def __init__(self, object = None):
    
        self.object = object

class RemoveObject(Action):

    pass

class AddObject(Action):

    def __init__(self, object = None, layer = 0, index = -1):
    
        self.object = object
        self.layer = layer
        self.index = index

class ClaimEvent(Action):

    pass

class UpdateObject(Action):

    pass

class RenderObject(Action):

    pass

class ExitApplication(Action):

    pass

class AddEvent(Action):

    pass

class KeyPress(Action):

    def __init__(self, key, object = None):
    
        self.key = key
        self.object = object

class MouseButton(Action):

    def __init__(self, button, object = None):
    
        self.button = button
        self.object = object

class AddScore(Action):

    def __init__(self, value, object = None):

        self.value = value
        self.object = object

class AddReload(Action):

    def __init__(self, value, object = None):
    
        self.value = value
        self.object = object

class GameObjectDestroyed(Action):

    def __init__(self, gameobject, object = None):
    
        self.gameobject = gameobject
        self.object = object

class Captured(Action):

    def __init__(self, gameobject, position, object = None):
    
        self.gameobject = gameobject
        self.position = position
        self.object = object

class Recaptured(Action):

    def __init__(self, gameobject, object = None):
    
        self.gameobject = gameobject
        self.object = object

class EnteredGateway(Action):

    def __init__(self, gameobject, object = None):
    
        self.gameobject = gameobject
        self.object = object
