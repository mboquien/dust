import astropy.constants as cst
import astropy.units as units
import numpy as np

# ----------------------------------------------------------
# Generic constants

# Speed of light
clight = cst.c.to('cm/s')

# Planck's h constant
hplanck = cst.h.to('keV s')

# Electron radius
r_e = (2.8179403227e-15 * units.m).to('cm')

# Mass of proton
m_p = cst.m_p.to('g')

# ----------------------------------------------------------
# Constants for converting things

micron2cm = units.um.to('cm')
pc2cm = cst.pc.to('cm')

arcs2rad = units.arcsec.to('radian')
arcm2rad = units.arcmin.to('radian')

hc = clight * hplanck
hc_angs = hc.to('keV Anstrom')

# ----------------------------------------------------------
# Cosmology related constants

# Hubble's constant
h0 = 75.  # km/s/Mpc

# Critical density for Universe
rho_crit = np.float64(1.1e-29)

# Density in units of rho_crit
omega_d = 1.e-5  # dust
omega_m = 0.3    # matter
omega_l = 0.7    # dark energy

# c/H term in distance integral (a distance)
# c/H = Mpc, then convert to cm
cperh0 = (clight * 1.e-5 / h0) * (1.e6 * pc2cm)


# ----- Very basic integration functions ------#
# I think I used these for checking something
# way back in the day

# Wrapper for numpy integration, used in cosmology integral
def intz(x, y):
    return np.trapz(y, x)
# Note that scipy calls integration in reverse order as I do

# ------- Save and restore functions, similar to IDL -------#
# http://idl2python.blogspot.com/2010/10/save-and-restore-2.html
# Updated April 20, 2012 to store objects
# http://wiki.python.org/moin/UsingPickle


def save(file, varnames, values):
    """
    Usage: save('mydata.pysav', ['a','b','c'], [a,b,c] )
    """
    import cPickle
    f = open(file, "wb")
    super_var = dict(zip(varnames, values))
    cPickle.dump(super_var, f)
    f.close


def restore(file):
    """
    Read data saved with save function.
    Usage: data = restore('mydata.pysav')
    a = data['a']
    b = data['b']
    c = data['c']
    """
    import cPickle
    f = open(file, "rb")
    result = cPickle.load(f)
    f.close
    return result

# ------- Read ascii tables --------#
# June 11, 2013
# needed for computers that don't have access to asciidata (hotfoot)


def read_table(filename, ncols, ignore='#'):
    """
    Read data saved in an ascii table
    Assumes data is separated by white space
    Assumes all the data are floats
    Ignores lines that start with the ignore character / sequence
    ---------------
    Usage : read_table( filename, ncols, ignore='#' )
    Returns : A dictionary with the column index as keys and the column data as
    lists
    """

    # Initialize result dictionary
    result = {}
    for i in range(ncols):
        result[i] = []

    try:
        f = open(filename, 'r')
    except:
        print('ERROR: file not found')
        return

    end_of_file = False
    while not end_of_file:
        try:
            temp = f.readline()
            if temp[0] == ignore:
                pass  # Ignore the ignore character
            else:
                temp = temp.split()
                for i in range(ncols):
                    result[i].append(np.float(temp[i]))
        except:
            end_of_file = True

    f.close()
    return result
