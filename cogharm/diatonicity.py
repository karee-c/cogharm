"""This function identifies the diatonic relation 
    of inputted chords to DIATONIC_SETS
"""
# Diatonic Sets, represented by pitch class root (0 = C) and mode (ma = major).
# Values are represented in pitch classes.
DIATONIC_SETS = {
       '0ma': [0,2,4,5,7,9,11],
       '1ma': [1,3,5,6,8,10,0],
       '2ma': [2,4,6,7,9,11,1],
       '3ma': [3,5,7,8,10,0,2],
       '4ma': [4,6,8,9,11,1,3],
       '5ma': [5,7,9,10,0,2,4],
       '6ma': [6,8,10,11,1,3,5],
       '7ma': [7,9,11,0,2,4,6],
       '8ma': [8,10,0,1,3,5,7],
       '9ma': [9,11,1,2,4,6,8],
       '10ma': [10,0,2,3,5,7,9],
       '11ma': [11,1,3,4,6,8,10]}

def diatonicity(chord, epsilon = 1):
    """ chord = midi
        epsilon = 
    """
    cardinality = len(chord)
    unique_pc = list(set([note%12 for note in chord]))
    counts = [(len(set(unique_pc).intersection(DIATONIC_SETS[scale]))) for scale in DIATONIC_SETS]
    diatonic_weight = [round((scale_count + epsilon) / (7 + epsilon) * (scale_count + epsilon) / (cardinality + epsilon),3) for scale_count in counts]
    diatonicity = {}
    for scale, weight in zip(DIATONIC_SETS.keys(), diatonic_weight):
        diatonicity.update({scale: weight})
    return diatonicity