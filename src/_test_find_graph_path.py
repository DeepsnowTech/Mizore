from Network._quantum_chips import *
from Network._utilities import find_paths

# Initial quantum chip
chip = Rigetti_8Q_Agave()

# Find paths
paths = find_paths(chip)
print(paths)
