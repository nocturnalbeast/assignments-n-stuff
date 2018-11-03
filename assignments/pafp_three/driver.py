def inputbuild():
    inputfile = open("input.dat","r")
    inputlist = inputfile.readlines()
    inputfile.close()
    inputlist = [line.strip("\n") for line in inputlist]
    lstind = [0,8,15,23,30,38,45]
    fin_inp = {ind+1:[line.split() for line in inputlist[lstind[ind]:lstind[ind+1]]] for ind in xrange(6)}
    for k,v in fin_inp.items():
        print k,v

inputbuild()