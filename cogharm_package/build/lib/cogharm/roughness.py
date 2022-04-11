""" Roughness Algorithm based on Hutchinson & Knopoff 1978 & 1979, 
    Mashinter 2006, Parncutt 2006, Harrison & Pearce 2020. Changes 
    Implemented by Konrad Swierczek, Karen Chan, & Matthew Woolhouse. 
    Digital Music Lab, McMaster University
"""
# Standard Imports
import numpy
from math import *
import pandas as pa

# Local Imports
from itertools import combinations

# Constants
CBWA = 1.72
CBWB = 0.65
CBWCUTOFF = 1.2
A = 0.25
B = 2

def roughnessDyad(dyad, rolloff = 1, partials = 11):
    """ DOC STRING GOES HERE IN A FUNCTION
    ARGUMENT 1 = THESE ARE MIDI NUMBERS
    ARGUMENT 2 = WHAT IS ROLLOFF?
    ARGUMENT 3 = WHAT IS PARTIALS?
    """

    #create overtones in freq space
    # Identifying notes of the dyad to their frequency
    partials_list = list(range(1, partials+1))
    dyad_freqs = [[(440*((2**(1/12))**(note-69))) * overtone for index, overtone in enumerate(partials_list)] for note in dyad]
    note1 = dyad_freqs[0]
    note2 = dyad_freqs[1]
    
    # Idenitfying which frequencies are applicable with our
    # input and creating a frequency matrix
    cbw = [[CBWA * ((note1_partial+note2_partial)/2)**CBWB for note2_count, note2_partial in enumerate(note2)] for note1_partial in note1 ] 
    cbw_matrix = numpy.array(cbw).reshape(len(note1),len(note2))
    roughness_matrix = cbw_matrix.copy()
    freq_dif_list = [[abs(note1[note1_count]-note2[note2_count]) for note2_count, note2_freq in enumerate(note2) for note1_count, note1_freq in enumerate(note1)]]
    freq_matrix = numpy.array(freq_dif_list).reshape(len(note1),len(note2)).transpose()
    cbw_distance_matrix = freq_matrix / cbw_matrix
    for row_index, row in enumerate(cbw_distance_matrix):
        for cell_index, cbw_distance in enumerate(row): 
            if cbw_distance > CBWCUTOFF:
                    roughness_value = 0
                    roughness_matrix[row_index][cell_index] = roughness_value
            else: 
                roughness_value = (((cbw_distance/A)*exp(1-(cbw_distance/A)))**B)         
                roughness_matrix[row_index][cell_index] = roughness_value
                
    # Creating a matrix with weights 
    weights = {str(num):num**(rolloff*-1) for num in partials_list}
    weightmatrix = cbw_matrix.copy()
    for note1_count, note1_freq in enumerate(note1):
        for note2_count, note2_freq in enumerate(note2):
            if note2_count < len(note2):
                weightmatrix[note1_count][note2_count] = (weights[str(note1_count+1)]) * (weights[str(note2_count+1)])
            else:
                weightmatrix[note1_count][note2_count] = (weights[str(note1_count+1)]) * (weights[str(note2_count)])
    
    # Calculate roughness for entire dyad.  
    numerator = 0.5*(numpy.sum(roughness_matrix * weightmatrix))
    denominator = sum([weight**2 for weight in list(weights.values())])
    roughness = numerator / denominator
    return roughness

def roughnessChord(chord, rolloff = 1, partials = 11):
    """ Calculating roughness for a chord
    """
    rolloff = rolloff
    partials = partials 
    dyads = [dyad for dyad in (combinations(chord,2))]
    dyads_roughness = [roughnessDyad(dyad) for dyad in dyads]
    roughness = 2/len(chord)*(sum(dyads_roughness))
    return roughness