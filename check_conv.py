#!/usr/bin/env python3

import sys
import os, argparse, logging
from pymatgen.io.vasp import Vasprun

def check_conv(argv):
    """"""

    #-------------------------------------------------------------------------------
    # Argument parser
    #-------------------------------------------------------------------------------
    parser = argparse.ArgumentParser(description=__doc__)
    # Positional arguments
    parser.add_argument('filename',
                        default="vasprun.xml",
                        type=str, nargs='?',
                        help='set input xml file. Default vasprun.xml;')
    # Optional args
    parser.add_argument('--mal',
		        action="store_true", dest="malformed",
                        help='allow parsing of malformed XML;')
    parser.add_argument('--debug',
                        action='store_true', dest='debug',
                        help='show debug informations.')

    #-------------------------------------------------------------------------------
    # Initialize and check variables
    #-------------------------------------------------------------------------------
    args = parser.parse_args(argv)

    # Set up LOGGER
    c_log = logging.getLogger(__name__)
    # Adopted format: level - current function name - mess. Width is fixed as visual aid
    std_format = '[%(levelname)5s - %(funcName)10s] %(message)s'
    logging.basicConfig(format=std_format)
    c_log.setLevel(logging.INFO)
    # Set debug option
    if args.debug: c_log.setLevel(logging.DEBUG)

    c_log.debug(args)

    #-------------------------------------------------------------------------------
    # Load geometry and print in cartesian
    #-------------------------------------------------------------------------------

    completed = True
    # Quickly load the xml, skip big parts to go faster
    try:
        vasprun= Vasprun(args.filename,
                         parse_projected_eigen=False,
                         parse_eigen=False,
                         parse_dos=False,
                         exception_on_bad_xml=args.malformed,
                         parse_potcar_file=False)
    except Exception as e:
        completed = False
        c_log.warning("Following error during parsing")
        c_log.warning(e)
        print("%s" % completed)
        return completed

    c_log.info("Electronic conv: %s. Ion conv %s. Completed: %s",
               vasprun.converged_electronic,
               vasprun.converged_ionic,
               vasprun.converged
    )

    completed = vasprun.converged
    print("%s" % completed)
    return completed

# If executed as bash script, execute function and return exit status to bash
if __name__ == "__main__":
    check_conv(sys.argv[1:])
