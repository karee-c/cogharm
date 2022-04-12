""" Corpus analysis program.
    Implemented by Konrad Swierczek 2022
    Digital Music Lab, McMaster University
"""

# Standard Imports
import os
import fnmatch

# External Imports
from music21 import *

# Local Imports
from cogharm.woolhouse09 import event_attraction
from cogharm.parn88 import PitchSalience
from cogharm.roughness import roughnessChord
from cogharm.diatonicity import diatonicity

# Writing a class for corpus analysis
class Analysis:
    def __init__(self, filepath):
        self.filepath = filepath
        self.filename = os.path.basename(self.filepath)
        self.raw = converter.parse(self.filepath)
        self.chords = [[pitch.midi for pitch in chord.pitches] for chord in (self.raw).chordify().recurse().getElementsByClass('Chord')]   
        self.rhythm = [chord.duration.quarterLength/(self.raw.duration.quarterLength) for chord in (self.raw).chordify().recurse().getElementsByClass('Chord')]
        self.roughness = [roughnessChord(chord) for chord in self.chords]
        self.mean_roughness = sum(self.roughness)/len(self.roughness)
        """self.diatonicity = [diatonicity(chord) for chord in self.chords]"""
        self.harmonicity = None
        pitch_salience = [PitchSalience(chord) for chord in self.chords]
        self.ra = [chord.ra for chord in pitch_salience]
        self.ps = [chord.ps for chord in pitch_salience]
        self.root = [chord.root for chord in pitch_salience]
        chords_len = len(self.chords)
        self.ea = [0]
        for count, value in enumerate(self.chords):
            if count + 1 == chords_len:
                break
            else:
                pre_chord = (self.chords[count])
                succ_chord = (self.chords[count + 1])
                self.ea.append(event_attraction(pre_chord, succ_chord))        
        self.ca = None
        self.ka = None

def corpus_analysis(corpus_path):
    # Set directory to folder with corpus.
    # Extract file names.
    corpus_folder = os.listdir(corpus_path)

    # Filter out files with unuasble extensions.
    corpus_filepaths = []
    extensions =  ['*.krn','*.mid','*.mxl']
    for extension in extensions:
        for name in fnmatch.filter(corpus_folder,extension):
            corpus_filepaths.append(corpus_path+'/'+name)

    # Analyze corpus
    corpus_analyzed={}
    for file in corpus_filepaths:
        corpus_analyzed.update({os.path.basename(file):Analysis(file)})
    return corpus_analyzed

# TODO:
# Export to .csv
# comparisons within corpus
# graphs
