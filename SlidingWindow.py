'''
    Sliding window algorithm for tRNA unique mass
    function need attention: removeNoise, deconvolute_peaks
'''

from ExtractChrom import ExtractSpec
from Common import InRange
from GetPeaks import SelectPeaks, HighestPeaks
import pymzml
from pprint import pprint

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


if __name__ == "__main__":
    main()
