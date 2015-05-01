'''
    Get the retention time for a mass list
'''
from ExtractChrom import ExtractSpec
import pymzml
from pprint import pprint
import Tkinter, tkFileDialog

def HighestPeaks(peaklist):
    max_item= (0,0)
    for eachitem in peaklist:
        if eachitem[1] > max_item[1]:
            max_item = eachitem
    return max_item

def SelectPeaks(peaks, mzRange):
    return [ (mz,i) for mz, i in peaks if mzRange[0] <= mz <= mzRange[1] ]

def AllMassPossibility(a_mass):
    return [a_mass, a_mass / 2, a_mass / 3, a_mass / 4]

def GetMaxPeakInSpecs(mz_list, specs, run, tolerance = 0.2):
    # get the maximun peaks in a collection of specs
    max_int_dict = dict()
    max_intensity = 0
    rule = MostPeaks()
    for spec_basic in specs:
        idx  = spec_basic.index
        #spec = run[idx]
        max_int_dict = dict()
        spec = spec_basic.spec
        #if abs(spec["scan time"] - 7.48) < 0.01:
        #    print spec["peaks"]
        for eachmz in mz_list:
            eachrange = (eachmz - tolerance, eachmz + tolerance)
            try:
                mz, intensity = HighestPeaks(SelectPeaks(spec["peaks"], eachrange))
                #print "min:", min([x[0] for x in spec["peaks"]])
                #print "max:", max([x[0] for x in spec["peaks"]])
                #print mz, intensity
            except Exception as e:
                #print e.message
                continue
            #print spec_basic
            #print eachrange
            #print "scan time:", spec["scan time"]
            max_int_dict[eachmz] = {"max_int": intensity, "max_mz": mz, "max_time": spec["scan time"], "max_id": spec["id"]}
        if max_int_dict:
            rule.compare(max_int_dict)
    return rule._cur_max_dict

class MostPeaks:
    # Rule to pick the best match in mass spec with a list of mass
    # Basically, find the one with most peaks. The way to break tie is sum of intensity
    def __init__(self):
        self._max_num_peaks = 0
        self._max_intensity = 0
        self._cur_max_dict  = None

    def compare(self, new_int_dict):
        new_num_peaks = len([x for x in new_int_dict if new_int_dict[x]["max_int"] > 0])
        #print "new_num_peaks", new_num_peaks
        if new_num_peaks == 0:
            return
        new_intensity = sum([new_int_dict[x]["max_int"] for x in new_int_dict.keys()])
        #print "new_intensity", new_intensity
        if new_num_peaks > self._max_num_peaks or (new_num_peaks == self._max_num_peaks and new_intensity > self._max_intensity):
            self._max_num_peaks = new_num_peaks
            self._max_intensity = new_intensity
            self._cur_max_dict  = new_int_dict


def drange(start, stop, step):
    r = start
    while r < stop:
        yield r
        r += step

def SlidingWindow(masslist, run, exspec, rtrange = None, s_win = 0.001):
    # s_win: sliding window size, which is in minute
    rule   = MostPeaks()
    for rt_time in drange(exspec.start_time, exspec.end_time, exspec.interval):
        # ignore the spec out of rtrange
        if (not rtrange is None) and (rt_time < min(rtrange) or rt_time > max(rtrange)):
            continue
        specs  = exspec.extractWithTimeRange(rt_time, rt_time + s_win)
        max_int_dict = GetMaxPeakInSpecs(masslist, specs, run)
        if max_int_dict:
            rule.compare(max_int_dict)
    print rule._cur_max_dict


def main():
    root = Tkinter.Tk()
    root.withdraw()
    ms_file = tkFileDialog.askopenfilename()
    #ms_file   = "./Data/CCG224144MIDSample5minMS2.mzML"
    #ms_file   = "./Data/CCG224144MIDSample5min.mzML"
    exspec = ExtractSpec(ms_file)
    mass_list = [423.3, 268.2]
    run = pymzml.run.Reader(ms_file, noiseThreshold = 100)
    SlidingWindow(mass_list, run, exspec)

if __name__ == "__main__":
    main()
