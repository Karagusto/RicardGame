==============
Space Explorer
==============

:Authors: `David Boddie`_, Paul Boddie
:Date: 2009-03-08
:Version: 0.30

*Note: This text is marked up using reStructuredText formatting. It should be
readable in a text editor but can be processed to produce versions of this
document in other formats.*


.. contents::


Introduction
------------

Space Explorer is a single player game written in the Python_ programming
language. The object of the game is to shoot aliens and rescue any captured
spaceships you may find.


Requirements
------------

This game requires the Pygame_ package. This can be installed separately using
the instructions given in the documentation for that package.


Installation and Configuration
------------------------------

This game is not designed to be installed. Instead, you should unpack the game
archive in a directory and run it from there. For example, at the command line,
enter the directory containing the spacegame.py file and type the following::

  python spacegame.py

Configuration files, such as the user-defined keys and high scores are stored
within the Resources directory.


How to Play
-----------

The controls used in Space Explorer are quite different to many other games.
The direction of the spaceship is determined by the location of the mouse
cursor. Clicking the right mouse button causes the spaceship to fire at this
position and clicking the left mouse button causes it to fly there.

By default, the A key can also be used to move the spaceship and the S key
can also be used to fire. These keys can be changed by pressing the K key when
the game is showing any of the title screens or the high score table.

The game can be paused with the P key and unpaused with the O key.


License
-------

The contents of this package are licensed under the GNU General Public License
(version 3 or later)::

 Space Explorer, a game of space exploration and rescue.
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



.. _Python:         http://www.python.org/
.. _Pygame:         http://www.pygame.org/
.. _`David Boddie`: mailto:david@boddie.org.uk
