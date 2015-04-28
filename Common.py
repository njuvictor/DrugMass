'''
    Common functions
'''

def InRange(spec, rtrange):
    try:
        rt_time = spec["scan time"]
        if not rtrange is None:
            if rt_time < rtrange[0]:
                return False
            elif rt_time > rtrange[1]:
                return False
    except:
        return False
    return rt_time
