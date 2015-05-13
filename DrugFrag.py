'''
    Get drug fragment mass
'''

def DrugFragMass(masslist, i):
    '''
        The function sort masslist first and then add mass for each element before index i
        for example if masslist = [439, 421, 312.2, 252, 170.8], i = 2
        result is [455, 437, 312.2, 252, 170.8]
    '''
    mass_list_mod = list(masslist)
    for j in range(i):
        mass_list_mod[j] = mass_list_mod[j] + 16
    return mass_list_mod

if __name__ == "__main__":
    mass_list = [439, 421, 312.2, 252, 170.8]
    print DrugFragMass(mass_list, 2)
