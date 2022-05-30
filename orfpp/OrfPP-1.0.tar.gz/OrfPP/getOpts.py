#!/usr/bin/python3
import sys, os, getopt, time
def opts():
    usage = """
    OrfPP version 1.0 by Bo Song (songbo446@yeah.net)

    Usage:
        OrfPP [options]* --genome <reference> --gtf <annotation> --pi <diversity>

        <reference>     Sequence of reference genome (fasta)
        <annotation>    Annotation of reference genome (gtf)
        <diversity>     Nucleotide diversity (tabbed table "Chr\\tCoordinate\\tPi")

    Options:

        --start         Start codons (spearate by comma) [default: AUG]
        --cov          	Minimum RPF coverage of Psites (0-1) [default: 0.001]
        --nCores        Number of multiprocessors [default: 5]
        --outdir        Output directory [default: ./OutOrfPP]
        --prefix        Prefix of output files [default: orfpp]

"""
    startCodon, outdir, prefix = 'AUG', 'OutOrfPP', 'orfpp'
    nCores = 5
    pcov = 0.0001

    try:
        opts, args = getopt.getopt(sys.argv[1:], "h", ["help", "genome=", "gtf=", "pi=", "cov=", "nCores=", "start=", "outdir=", "prefix="])
    except:
        sys.stdout.write(usage)
        sys.exit()

    if len(sys.argv[1:]) < 3:
        sys.stdout.write(usage)
        sys.exit()
    
    for opt, arg in opts:
        if opt in ('-h', '-help'):
            sys.stdout.write(usage)	    
            sys.exit()
        elif opt in ('--genome'):
            if arg is None:
                sys.stdout.write(usage)	
                sys.exit()
            else:
                sys.stdout.write("Genome is: "+arg+'\n')
                genome = arg
        elif opt in ('--gtf'):
            gtf = arg
            sys.stdout.write("GTF is: "+gtf+'\n')
        elif opt in ('--pi'):
            pi = arg
            sys.stdout.write("pi is: "+pi+'\n')
        elif opt in ('--startCodon'):
            startCodon = arg
            sys.stdout.write("Start codons are: "+startCodon+'\n')
        elif opt in ('--outdir'):
            outdir = arg
            sys.stdout.write("Output directory is: "+outdir+'\n')
        elif opt in ('--prefix'):
            prefix = arg
        elif opt in ('--cov'):
            pcov = float(arg)
        elif opt in ('--nCores'):
            nCores = int(arg)

    genome = os.path.abspath(genome)
    gtf = os.path.abspath(gtf)
    pi = os.path.abspath(pi)
    timetick = str(time.time()).split(".")[0]
    logout = "log"+str(timetick)

    return(genome, gtf, pi, startCodon, outdir, prefix, pcov, nCores)
