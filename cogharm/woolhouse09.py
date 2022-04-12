# Standard Imports
import numpy
from math import *
from itertools import combinations

# Local Imports
from cogharm.parn88 import PitchSalience

# Constants
CDDICT = {0:"C",1:"D",2:"D",3:"C",
          4:"C",5:"C",6:"D",7:"C",
          8:"C",9:"C",10:"D",11:"D",12:"C"}

# Defining functions used in event attraction
def cd_chord(chord):
    """ Calculate if chord contains consonant or dissonant intervals. 
        Returns "D" if chord contains any dissonant intervals.
        Returns "C" if chord only contains consonant intervals. 
        Based on Woolhouse 2009, see CDDICT for list of dissonant intervals.
    """
    intervals = [abs((interval[0]%12)- (interval[1]%12)) for interval in list(combinations(chord,2))]
    cd_intervals = [CDDICT[interval] for interval in intervals]
    if "D" in cd_intervals:
        return "D"
    else:
        return "C" 

def pd(note1,note2):
    """ Calculate semitone distance between two notes. """
    return abs(note1 - note2)

def ic(pd):
    """ Calculate interval cycle of given interval. """
    return int(12/(gcd(int(pd),12)))

def event_attraction(pre_chord, suc_chord, alpha = 99999, beta = 4, Gamma = 8, delta = 0.1):
    """ Pairwise Tonal Attraction after Woolhouse 2009.
        pre_chord = preceding chord.
        succ chord = succeding chord.
        alpha = Voice Leading weighting variable.
        beta = Preceding chord Root Salience weighting variable.
        Gamma = Succeding chord Root Salience weighting variable.
        delta = Consonance/Dissonance weighting variable.
    """
    # Pitch Distance Matrix
    pdlist = [[pd(pre_note, suc_note) for suc_note in suc_chord] for pre_note in pre_chord]
    
    # Interval Cycle Matrix
    iclist = [[ic(cell) for cell in row] for row in pdlist]
    ic_mat = numpy.array(iclist).reshape(len(pre_chord),len(suc_chord))
    
    # Voice Leading Matrix
    vllist = [[None if pd is None else (alpha/(pd+alpha)) for pd in row] for row in pdlist]
    vl_mat = numpy.array(vllist).reshape(len(pre_chord),len(suc_chord))
    
    # Interval Cycle/Voice Leading Matrix   
    icvl = ic_mat * vl_mat
    
    # Root Salience 1 Matrix (placeholder)
    rs1list= [[1 if vl > 0 else 0 for vl in row] for row in vllist]
    rs1 = numpy.array(rs1list).reshape(len(pre_chord),len(suc_chord))
    
    # Calculate root of chords based on Parncutt 1988
    prec_root = PitchSalience(pre_chord).root
    succ_root = PitchSalience(suc_chord).root

    rs_prec = []
    for note in pre_chord:
        if note == prec_root:
            rs_prec.append(beta)
        else: 
            rs_prec.append(1)
    rs_succ = []
    for note in suc_chord:
        if note == succ_root:
            rs_succ.append(Gamma)
        else: 
            rs_succ.append(1)
    rs2list = [[pre_note * suc_note for suc_note in rs_succ] for pre_note in rs_prec]
    rs2_sum = sum([sum(rs2) for rs2 in rs2list])
    rs2_matrix = numpy.array(rs2list).reshape(len(pre_chord),len(suc_chord))

    # Root Salience 3 Matrix
    rs3 = numpy.array([num/rs2_sum for cell in rs2_matrix for num in cell]).reshape(len(pre_chord),len(suc_chord))
    
    # Consonance/Dissonance Matrix
    prec_cd = cd_chord(pre_chord)
    succ_cd = cd_chord(suc_chord)
    if prec_cd == succ_cd:
        cd = rs3
    if prec_cd == "D" and succ_cd == "C":
        cd = (1+delta) * rs3
    if prec_cd == "C" and succ_cd == "D":
        cd = (1-delta) * rs3
    
    # Calculate Event Attraction
    ea_matrix = icvl * cd
    ea = round(sum(sum(ea_matrix))/12,3)
    return(ea)