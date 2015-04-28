#
#  Read ML file
#

import pymzml
import Tkinter, tkFileDialog
from Common import InRange

DEBUG = False

def HighestPeaks(peaklist):
    max_item= (0,0)
    for eachitem in peaklist:
        if eachitem[1] > max_item[1]:
            max_item = eachitem
    return max_item

def SelectPeaks(peaks, mzRange):
    return [ (mz,i) for mz, i in peaks if mzRange[0] <= mz <= mzRange[1] ]

def PlotRange(run):
    p = pymzml.plot.Factory()
    n = 0
    for spec in run:
        n = n + 1
        print n
        p.newPlot()
        p.add(spec.peaks, color=(200,00,00), style='circles')
        p.add(spec.centroidedPeaks, color=(00,00,00), style='sticks')
        p.add(spec.reprofiledPeaks, color=(00,255,00), style='circles')
        p.save( filename="output/plotAspect.xhtml")
        break

def Test():
    filename = "E165ug.mzML"
    run = pymzml.run.Reader(filename)
    print run[1701].extremeValues('i')
    print run[1700].extremeValues('i')
    print run[1702].extremeValues('i')
    print run[1702].peaks

if __name__ == "__main__":
    root = Tkinter.Tk()
    root.withdraw()
    inputfile = tkFileDialog.askopenfilename()
