from . import Cn2cf
import argparse
parser = argparse.ArgumentParser(prog='cn2cf')
parser.add_argument('-c', "--cname",
                    help="ChemicalName")
args = parser.parse_args()
if args.cname:
    print(Cn2cf.get(args.cname))
