'''
    Get the retention time for a mass list
'''
from SlidingWindow import SlidingWindow
from ExtractChrom import ExtractSpec
import pymzml

def main():
    ms_file   = "./Data/CCG224144MIDSample5minMS2.mzML"
    #ms_file   = "./Data/CCG224144MIDSample5min.mzML"
    exspec = ExtractSpec(ms_file)
    mass_list = [423.3, 268.2]
    run = pymzml.run.Reader(ms_file, noiseThreshold = 100)
    SlidingWindow(mass_list, run, exspec)

if __name__ == "__main__":
    main()
