import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "scottviz.settings")
from scottviz import settings
import numpy
import mdp
from msp.models import MSP, Division

__author__ = '2168879m'


def run_pca(votes):
    # votes has 3 columns:
    # msp, division, vote

    #Create null matrix (to be replaced with value wherever an msp voted on a division)
    len_msps = MSP.objects.count()
    len_divisions = Division.objects.count()
    matrix = numpy.zeros(shape=(len_msps,len_divisions))

    # get a list of the msps selected, in the exact same order as they are entered in the matrix
    # safer than order by's
    msp_list = []

    # matrix rows from 0 to len_msps-1, but msps id from x to x+len_msps-1
    # so, normalize that shift
    # same for divisions
    shift_msps = int(votes[0][0])
    shift_division = int(votes[0][1])
    for vote in votes:
        msp_entry = int(vote[0])
        division_entry = int(vote[1])
        vote_entry = int(vote[2])
        matrix[msp_entry-shift_msps][division_entry-shift_division] = vote_entry
        if not msp_entry in msp_list:
            msp_list += [msp_entry]

    #Deletes every all-zero row in the input matrix (this is necessary for the filters to work correctly)
    matrix = matrix[~numpy.all(matrix == 0, axis=1)]
    
    #Uncomment to see matrix being sent to MDP
    #numpy.savetxt(settings.STATIC_PATH + "/csv/InputMatrix.csv", matrix, fmt="%s", delimiter=",")


    #PCA magic happens here using MDP
    imdp = mdp.nodes.PCANode(output_dim=2)
    scores = imdp(matrix)

    scores_pairings = []
    for i in range(len(msp_list)):
        scores_pairings += [[msp_list[i], scores[i]]]

    return scores_pairings