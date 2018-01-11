__author__ = "mfreer"
__date__ = "2013-02-17 18:01"
__version__ = "1.5"
__all__ = ['CompareParamLcss']

import egads.core.egads_core as egads_core
import egads.core.metadata as egads_metadata
import numpy, math

class CompareParamLcss(egads_core.EgadsAlgorithm):

    """
    
    FILE        compare_param_lcss.py

    VERSION     1.5

    CATEGORY    Comparisons

    PURPOSE     This algorithm computes a similarity factor between two timeseries using
                the Longest Common Subsequence (LCSS) method.

    DESCRIPTION This algorithm uses the Morse-Patel method to evaluate the Longest
                Common Subsequence for two timeseries. The timeseries compared can be
                multi-dimensional. The returned value represents the longest common
                subsequence length, i.e. the number of corresponding points.

    INPUT       R        vector        _        first timeseries to compare
                S        vector        _        second timeseries for comparison
                epsilon  coeff         _        matching criteria

    OUTPUT      max      coeff         _        maximum common subsequence length

    SOURCE      

    REFERENCES  Morse, M. and J. M. Patel, 2007: An Efficient and Accurate Method
                for Evaluating Time Series Similarity. SIGMOD'07, June 11-14 2007,
                Beijing, China.

    """

    def __init__(self, return_Egads=True):
        egads_core.EgadsAlgorithm.__init__(self, return_Egads)

        self.output_metadata = egads_metadata.VariableMetadata({'units':'',
                                                               'long_name':'maximum common subsequence length',
                                                               'standard_name':'',
                                                               'Category':['']})

        self.metadata = egads_metadata.AlgorithmMetadata({'Inputs':['R','S','epsilon'],
                                                          'InputUnits':[None, None, None],
                                                          'InputTypes':['vector','vector','coeff'],
                                                          'InputDescription':['First timeseries to compare',
                                                                              'Second timeseries for comparison',
                                                                              'Matching criteria'],
                                                          'Outputs':['max'],
                                                          'OutputUnits':[None],
                                                          'OutputTypes':['coeff'],
                                                          'OutputDescription':['Maximum common subsequence length'],
                                                          'Purpose':'This algorithm computes a similarity factor between two timeseries using the Longest Common Subsequence (LCSS) method',
                                                          'Description':'This algorithm uses the Morse-Patel method to evaluate the Longest Common Subsequence for two timeseries. The timeseries compared can be multi-dimensional. The returned value represents the longest common subsequence length, i.e. the number of corresponding points',
                                                          'Category':'Comparisons',
                                                          'Source':'',
                                                          'References':"Morse, M. and J. M. Patel, 2007: An Efficient and Accurate Method for Evaluating Time Series Similarity. SIGMOD'07, June 11-14 2007, Beijing, China.",
                                                          'Processor':self.name,
                                                          'ProcessorDate':__date__,
                                                          'ProcessorVersion':__version__,
                                                          'DateProcessed':self.now()},
                                                          self.output_metadata)

    def run(self, R, S, epsilon, norm=True):
        
        return egads_core.EgadsAlgorithm.run(self, R, S, epsilon, norm)

    def _algorithm(self, R, S, epsilon, norm):
        
        # normalize S and R using standard deviation and mean if desired
        if norm:
            R = (R-numpy.mean(R))/numpy.std(R)
            S = (S-numpy.mean(S))/numpy.std(S)
        m = len(R)
        n = len(S)
        d = R.ndim

        # Find range of data for each dimension to build correspondance grid G
        if R.min(0) < S.min(0):
            data_min = R.min(0)
        else:
            data_min = S.min(0)
        if R.max(0) > S.max(0):
            data_max = R.max(0)
        else:
            data_max = S.max(0)

        # Define properties of correspondance grid G and initialize G
        if d > 1:
            G_shape = []
            G_coords = []
            for k in range(d + 1):
                G_shape.append(int(math.floor(((data_max[k] + 3 * epsilon) - (data_min[k] - epsilon)))) / epsilon)
                G_coords.append(numpy.arange(data_min[k] - epsilon, data_max[k] + 3 * epsilon, epsilon))
            G = numpy.ndarray(tuple(G_shape), dtype=list)
        else:
            G_shape = int(math.floor(((data_max + 3 * epsilon) - (data_min - epsilon)) / epsilon))
            G_coords = numpy.arange(data_min - epsilon, data_max + 3 * epsilon, epsilon)
            G = numpy.ndarray(G_shape, dtype=list)
        for item, _ in numpy.ndenumerate(G):
            G[item] = []

        # Populate G with lists of intersections from R (using R +/- epsilon in all dimensions)
        for i in range(m):
            if d > 1:
                nearest_idx = []
                nearest_idx_up = []
                nearest_idx_down = []
                for k in range(d):
                    nearest_idx.append(numpy.abs(R[i, k] - G_coords[:, k]).argmin())
                    nearest_idx_up.append(numpy.abs(R[i, k] + epsilon - G_coords[:, k]).argmin())
                    nearest_idx_down.append(numpy.abs(R[i, k] - epsilon - G_coords[:, k]).argmin())
                for k in range(d):
                    G[tuple(nearest_idx)].append(i)
                    G[tuple(nearest_idx_up)].append(i)
                    G[tuple(nearest_idx_down)].append(i)
            else:
                nearest_idx = numpy.abs(R[i] - G_coords[:]).argmin()
                nearest_idx_up = numpy.abs(R[i] + epsilon - G_coords[:]).argmin()
                nearest_idx_down = numpy.abs(R[i] - epsilon - G_coords[:]).argmin()
                G[nearest_idx].append(i)
                G[nearest_idx_up].append(i)
                G[nearest_idx_down].append(i)
        L = numpy.ndarray(n, dtype=list)
        for item, _ in numpy.ndenumerate(L):
            L[item] = []

        # Determine matches between R and S using correspondance matrix G and store matches in 
        # L. All dimensions must match with maximum difference of epsilon in order to be stored
        # in L.
        for i in range(n):
            if d > 1:
                nearest_idx = []
                for k in range(d):
                    nearest_idx.append(numpy.abs(S[i, k] - G_coords[:, k]).argmin())
                for item in G[tuple(nearest_idx)]:
                    all_flag = True
                    for k in range(d):
                        if abs(S[i, k] - R[item[k], k]) >= epsilon:
                            all_flag = False
                            break
                    if all_flag is True:
                        L[i].append(item[k])
            else:
                nearest_idx = numpy.abs(S[i] - G_coords[:]).argmin()
                for item in G[nearest_idx]:
                    all_flag = True
                    if abs(S[i] - R[item]) >= epsilon:
                        all_flag = False
                        break
                    if all_flag is True:
                        L[i].append(item)
        matches = numpy.zeros(n)
        matches.fill(m)
        matches[0] = 0
        max_seq = 0

        # Find longest sequence of matches between R and S using matching list L.
        for j in range(n):
            c = 0
            temp = matches[0]

            for k in L[j]:
                if temp < k:
                    while matches[c] < k:
                        c += 1

                    temp = matches[c]
                    matches[c] = k
                    
                    if c > max:
                        max_seq = c


        return max_seq


