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

IGNORE_LIST = []
def GetPeakbyMZRange(filename, mz_list, rtrange = None, tolerance = 0.2):
    # input is mzrange (a tuple), the output is the retention time, intensity of the peak

    # for m mz values
    max_int_dict = dict()
    for eachmz in mz_list:
        max_int_dict[eachmz] = {"max_int": 0, "max_mz": None, "max_time": None, "max_id": None}
    max_intensity = 0
    run = pymzml.run.Reader(filename, noiseThreshold = 100)
    for spec in run:
        rt_time = InRange(spec, rtrange)
        if not rt_time:
            continue
        for eachmz in mz_list:
            eachrange = (eachmz - tolerance, eachmz + tolerance)
            try:
                mz, intensity = HighestPeaks(SelectPeaks(spec.peaks, eachrange))
            except Exception as e:
                #print e.message
                continue
            max_intensity = max_int_dict[eachmz]["max_int"]
            if intensity > max_intensity:
                max_int_dict[eachmz] = {"max_int": intensity, "max_mz": mz, "max_time": spec["scan time"], "max_id": spec["id"]}
    return max_int_dict


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


def MassToCharge(mass):
    if mass > 3200:
        mz16 = (mass- 3*1.007)/3
        mz18 = ((mass+2)-3*1.007)/3
    elif mass > 1300:
        mz16 = (mass - 2*1.007)/2
        mz18 = ((mass+2)-2*1.007)/2
    else:
        mz16 = mass -1.007
        mz18 =  mass + 2 - 1.007
    return mz16, mz18

def GetRT(mass, rtinterval):
    rt = 0.007 * mass + 8.3466
    rt1 = rt - rtinterval/2
    rt2 = rt + rtinterval/2
    return rt1, rt2

def GetPeaksWithRTEstimate(inputfile, masslist):
    #inputmass  = 1638.8
    rtinterval = 6
    #rtinterval = 20
    mass_iso_dict = dict()
    for inputmass in masslist:
        mz16, mz18 = MassToCharge(inputmass)
        rt1 , rt2  = GetRT(inputmass, rtinterval)
        #print mz16, mz18
        #print rt1, rt2
        mass_iso_dict[inputmass] = GetPeakbyMZRange(inputfile, [mz16, mz18], [rt1, rt2])
    return mass_iso_dict

def GetDeconvolutedPeak(infile, amass):
    run = pymzml.run.Reader(filename, noiseThreshold = 100)
    for spec in run:
        pass


def main(inputfile, masslist):
    returndict = GetPeaksWithRTEstimate(inputfile, masslist)
    for mass in returndict:
        for iso_mass in returndict[mass]:
            print returndict[mass][iso_mass]["max_int"], returndict[mass][iso_mass]["max_mz"], returndict[mass][iso_mass]["max_time"], returndict[mass][iso_mass]["max_id"]

def Test():
    filename = "E165ug.mzML"
    run = pymzml.run.Reader(filename)
    print run[1701].extremeValues('i')
    print run[1700].extremeValues('i')
    print run[1702].extremeValues('i')
    print run[1702].peaks

def examples(inputfile):
    # first example
    #run = pymzml.run.Reader("E165ug.mzML", noiseThreshold = 100, MSn_Precision = 250e-6)
    #GetPeakbyMZRange("E165ug.mzML", (818.2, 818.7), (19.82, 20.34))
    #GetPeakbyMZRange("E165ug.mzML", (819.2, 819.7), (19.82, 20.34))
    GetPeakbyMZRange(inputfile, (818.2, 818.7), (15, 41))
    GetPeakbyMZRange(inputfile, (819.2, 819.7), (15, 41))
    GetPeakbyMZRange(inputfile, (1255.4, 1255.9), (15, 41))
    GetPeakbyMZRange(inputfile, (1256.1, 1256.6), (15, 41))
    GetPeakbyMZRange(inputfile, (1365, 1365.2), (15, 41))
    GetPeakbyMZRange(inputfile, (1365.6, 1365.8), (15, 41))
    #print Test()

if __name__ == "__main__":
    root = Tkinter.Tk()
    root.withdraw()
    inputfile = tkFileDialog.askopenfilename()
    #inputfile = "E165ug.mzML"
    masslist_raw  = raw_input('Please enter a list of mass splited by comma --> ')
    masslist  = masslist_raw.split(",")
    print masslist
    main(inputfile, map(float, masslist))
    #main(inputfile, [1639.2])
