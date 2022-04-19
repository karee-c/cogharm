# Local Imports
from cogharm.woolhouse09 import event_attraction

# Consants
ALLPC = [[pc] for pc in range(0,12)]

def chroma_attraction(chord, alpha = 9999999, beta = 4):
        ca = [(round(event_attraction(chord, pc, alpha = alpha, beta = beta, Gamma = 1, delta = 0),3)) for pc in ALLPC]
        return ca