#
#  Eval Network
#  Testing neural network evaluation.
#  Copyright Megalodon Chess 2021
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

import os
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers

PARENT = os.path.dirname(os.path.realpath(__file__))
PATH = os.path.join(PARENT, "out.dat")


positions = []
evals = []
with open(PATH, "rb") as file:
    while True:
        pos = file.read(64)
        if len(pos) < 64:
            break
        ev = file.read(4)
        if len(ev) < 4:
            break
