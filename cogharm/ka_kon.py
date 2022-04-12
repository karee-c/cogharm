from cogharm.ca_kon import chroma_attraction

# Constants
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

def key_attraction(chord):
    """"""
    ca = chroma_attraction(chord)
    ka = {}
    for name, scale in SCALES.items():
        ka_list = []
        for pc in SCALES[name]:
            ka_list.append(ca[pc])
            ka[name] = round(sum(ka_list)/len(ka_list),3)
    return ka