"""This function identifies the diatonic relation 
    of inputted chords to scales
"""

SCALES = {
       'ka0ma': [0,2,4,5,7,9,11],
       'ka1ma': [1,3,5,6,8,10,0],
       'ka2ma': [2,4,6,7,9,11,1],
       'ka3ma': [3,5,7,8,10,0,2],
       'ka4ma': [4,6,8,9,11,1,3],
       'ka5ma': [5,7,9,10,0,2,4],
       'ka6ma': [6,8,10,11,1,3,5],
       'ka7ma': [7,9,11,0,2,4,6],
       'ka8ma': [8,10,0,1,3,5,7],
       'ka9ma': [9,11,1,2,4,6,8],
       'ka10ma': [10,0,2,3,5,7,9],
       'ka11ma': [11,1,3,4,6,8,10]}

def diatonicity(chord,epsilon = 1):
    """The function below goes through the inputted chord 
    and identifies where it is in each scale
    """ 
    def parser(x):
        inscale = [note % 12 for note in chord if note % 12 in SCALES[x]]
        SCALES[x] = len(inscale)

    for i in SCALES:
        parser(i) 
    # Finding the diatonic relation 
    weightssum = []
    for key in SCALES: 
        weighting = (SCALES[key]+epsilon) / (7+epsilon) * (SCALES[key]+epsilon) / (len(chord)+epsilon)
        SCALES[key] = weighting
        weightssum.append(weighting)
    for key in SCALES: 
        weighting2 = SCALES[key] / sum(weightssum)
        SCALES[key] = round(weighting2,3)
    return SCALES