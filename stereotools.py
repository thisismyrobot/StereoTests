import cv


def grayscale(img):
    """ Returns a new grayscale image from a colour one.
    """
    grayscale = cv.CreateImage(cv.GetSize(img), 8, 1)
    cv.CvtColor(img, grayscale, cv.CV_BGR2GRAY)
    return grayscale


def normalise(img):
    """ Returns a normalised copy of a grayscale image
    """
    normalised = cv.CreateImage(cv.GetSize(img), 8, 1)
    cv.EqualizeHist(img, normalised)
    return normalised


def add_dot(img, row, col, diam=5):
    """ Adds a black dot *in-place* on an image a row, col.
    """
    cv.Circle(img, (col, row), diam, (0,), -1)
    cv.Circle(img, (col, row), diam, (255,))


def get_vert_edges(img, cuts=20, stepsize = 5):
    """ Returns a list (len cuts) of lists of distinct vertical edges in
        the image.

        img is a cv image from cv.LoadImage
    """
    edges = {}
    end = img.height
    step = end / cuts
    start = step / 2
    for row in range(start, end, step):
        rowedges = []
        lastval = None
        for col in range(0, img.width, stepsize):
            val = img[row, col]
            if lastval is not None and abs(val - lastval) > 100:
                rowedges.append(col - (stepsize / 2))
            lastval = val
        if len(rowedges) >= 2:
            edges[row] = rowedges
    return edges


def calc_distances(edgedata):
    """ Returns the distance between every point and every other for a list
        of edges found by get_vert_edges.
    """
    results = {}
    for row, edges in edgedata.items():
        rowdists = {}
        for e_from in range(len(edges)):
            for e_to in range(e_from, len(edges)):
                if e_from != e_to:
                    rowdists[abs(edges[e_from] - edges[e_to])] = (edges[e_from], edges[e_to])
        results[row] = rowdists
    return results


def get_common_dists(left, right, prox=5):
    """ Compares two sets of edge distances
    """
    matching = {}
    for row in left.keys():
        if row in right.keys():
            rowmatches = []
            l_dists = left[row].keys()
            r_dists = right[row].keys()
            for ld in l_dists:
                for rd in r_dists:
                    if abs(ld - rd) < prox:
                        rowmatches.append(((ld, left[row][ld]), (rd, right[row][rd])))
            if len(rowmatches) > 0:
                matching[row] = rowmatches
    return matching
