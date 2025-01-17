#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
#  This file is part of the `lipyd` python module
#
#  Copyright (c) 2015-2019 - EMBL
#
#  File author(s):
#  Dénes Türei (turei.denes@gmail.com)
#  Igor Bulanov
#
#  Distributed under the GNU GPLv3 License.
#  See accompanying file LICENSE.txt or copy at
#      http://www.gnu.org/licenses/gpl-3.0.html
#
#  Website: http://denes.omnipathdb.org/
#

from __future__ import print_function
from future.utils import iteritems
from past.builtins import xrange, range, reduce

import sys
import os
import re
import warnings
import traceback
import itertools
import numpy as np
try:
    from cStringIO import StringIO
except ModuleNotFoundError:
    from io import StringIO


ROOT = os.path.abspath(os.path.dirname(__file__))

if 'unicode' not in __builtins__:
    unicode = str

simpleTypes = {int, float, str, unicode}

charTypes = {str, unicode}

try:
    basestring
except NameError:
    basestring = str


renumeric = re.compile(r'[-\.\d]+')
reint = re.compile(r'[-\d]+')
refloat = re.compile(r'-?\d*\.\d+')


class CaptureStdout(list):
    """
    Context capturing stdout.
    From https://stackoverflow.com/a/16571630/854988.
    """
    
    def __enter__(self):
        
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self
    
    
    def __exit__(self, *args):
        
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio    # free up some memory
        sys.stdout = self._stdout


def random_string(length = 10):
    """

    Parameters
    ----------
    length :
         (Default value = 10)

    Returns
    -------

    """
    
    return ''.join(chr(i) for i in np.random.randint(97, 123, length))


def uniqList(seq):
    """

    Parameters
    ----------
    seq :
        

    Returns
    -------

    """
    # Not order preserving
    # from http://www.peterbe.com/plog/uniqifiers-benchmark
    keys = {}
    for e in seq:
        try:
            keys[e] = 1
        except:
            sys.stdout.write(e)
            sys.stdout.write('\n')
            sys.stdout.write(seq)
            sys.stdout.write('\n')
            sys.stdout.write(keys)
            sys.stdout.write('\n')
    return keys.keys()

def flatList(lst):
    """

    Parameters
    ----------
    lst :
        

    Returns
    -------

    """
    return [it for sl in lst for it in sl]

def delEmpty(lst):
    """

    Parameters
    ----------
    lst :
        

    Returns
    -------

    """
    return [i for i in lst if len(i) > 0]

def uniqOrdList(seq, idfun = None): 
    """

    Parameters
    ----------
    seq :
        
    idfun :
         (Default value = None)

    Returns
    -------

    """
    # Order preserving
    # from http://www.peterbe.com/plog/uniqifiers-benchmark
    if idfun is None:
        def idfun(x): return x
    seen = {}
    result = []
    for item in seq:
        
        marker = idfun(item)
        if marker in seen: continue
        seen[marker] = 1
        result.append(item)
    
    return result

def addToList(lst, toadd):
    """

    Parameters
    ----------
    lst :
        
    toadd :
        

    Returns
    -------

    """
    if isinstance(toadd, list):
        lst += toadd
    else:
        lst.append(toadd)
    if None in lst:
        lst.remove(None)
    return uniqList(lst)


def warn_with_traceback(
        message, category, filename, lineno, file=None, line=None
    ):
    """Prints warnings with traceback.
    From https://stackoverflow.com/a/22376126/854988

    Parameters
    ----------
    message :
        
    category :
        
    filename :
        
    lineno :
        
    file :
         (Default value = None)
    line :
         (Default value = None)

    Returns
    -------

    """
    traceback.print_stack()
    log = file if hasattr(file,'write') else sys.stderr
    log.write(
        warnings.formatwarning(message, category, filename, lineno, line)
    )


class _const:
    """ """
    
    class ConstError(TypeError):
        """ """
        
        pass

    def __setattr__(self, name, value):
        
        if name in self.__dict__:
            
            raise(self.ConstError, "Can't rebind const(%s)" % name)
        
        self.__dict__[name] = value


fa_greek_parts = {
    'cc': {
        'hex': 6,
        'hept': 7,
        'oct': 8,
        'non': 9,
        'dec': 10,
        'undec': 11,
        'dodec': 12,
        'tridec': 13,
        'tetradec': 14,
        'pentadec': 15,
        'hexadec': 16,
        'heptadec': 17,
        'octadec': 18,
        'nonadec': 19,
        'eicos': 20,
        'icos': 20,
        'heneicos': 21,
        'docos': 22,
        'tricos': 23,
        'tetracos': 24,
        'pentacos': 25,
        'hexacos': 26,
        'heptacos': 27,
        'octacos': 28,
        'nonacos': 29,
        'triacont': 30
    },
    'uns': {
        '': 1,
        'adi': 2,
        'atri': 3,
        'atetra': 4,
        'apenta': 5,
        'ahexa': 6,
        'ahepta': 7,
        'aocta': 8
    },
    'end': {
        'enoate': 1,
        'anoate': 0,
        'enoic acid': 1,
        'anoic acid': 0
    }
}

count_prefix = {
    1: 'mono',
    2: 'di',
    3: 'tri',
    4: 'tetra',
    5: 'penta',
    6: 'hexa',
    7: 'hepta',
    8: 'octa',
    9: 'nona'
}

fa_greek = {}

for cc, uns, end in itertools.product(
    fa_greek_parts['cc'].items(),
    fa_greek_parts['uns'].items(),
    fa_greek_parts['end'].items()):
    
    if len(uns[0]) and end[1] == 0:
        continue
    
    fa_greek['%s%s%s' % (cc[0], uns[0], end[0])] = (cc[1], uns[1] * end[1])


adducts = {
    'pos': ['[M+H]+', '[M+NH4]+', '[M+Na]+'],
    'neg': ['[M-H]-', '[M+HCOO]-']
}


ad2ex = {
    1: {
        'pos': {
            '[M+H]+': 'remove_h',
            '[M+NH4]+': 'remove_nh4',
            '[M+Na]+': 'remove_na',
        },
        'neg': {
            '[M-H]-': 'add_h',
            '[M+HCOO]-': 'remove_fo'
        }
    },
    2: {
        'pos': {},
        'neg': {
            '[M-2H]2-': 'add_2h'
        }
    },
    3: {
        'pos': {},
        'neg': {
            '[M-3H]3-': 'add_3h'
        }
    }
}

exact_method = {
    '[M+OAc]-': 'remove_ac',
    '[M+H]+': 'remove_h',
    '[M-H]-': 'add_h',
    '[M+HCOO]-': 'remove_fo',
    '[M+NH4]+': 'remove_nh4',
    '[M+Na]+': 'remove_na',
    '[M+H-H2O]+': 'add_oh',
}

# method names to convert between exact and adduct masses
adduct_method = {
    '[M+OAc]-': 'add_ac',
    '[M+H]+': 'add_h',
    '[M-H]-': 'remove_h',
    '[M+HCOO]-': 'add_fo',
    '[M+NH4]+': 'add_nh4',
    '[M+Na]+': 'add_na'
}

ex2ad = {
    1: {
        'pos': {
            '[M+H]+': 'add_h',
            '[M+NH4]+': 'add_nh4',
            '[M+Na]+': 'add_na'
        },
        'neg': {
            '[M-H]-': 'remove_h',
            '[M+HCOO]-': 'add_fo'
        }
    },
    2: {
        'pos': {},
        'neg': {
            '[M-2H]2-': 'remove_2h'
        }
    },
    3: {
        'pos': {},
        'neg': {
            '[M-3H]3-': 'remove_3h'
        }
    }
}


def iterator_insert(full_length, insert):
    """Yields indices from two iterators.
    At the index `insert` it inserts a `None` instead of the second index.
    
    E.g. if full_length = 3 and insert = 1 it yields:
        (0, 0), (1, None), (2, 1)
    
    If insert is None or greater or equal than full_length, it yields
    always tuples of the same indices.

    Parameters
    ----------
    full_length :
        
    insert :
        

    Returns
    -------

    """
    
    j = 0
    
    for i in xrange(full_length):
        
        if i == insert:
            
            yield i, None
            
        else:
            
            yield i, j
            
            j += 1


IONMODE_POS = 'pos'
IONMODE_NEG = 'neg'

refloat = re.compile(r'([-]?[0-9]*[\.]?[0-9]+[eE]?[-\+]?[0-9]*)')
reint   = re.compile(r'([-]?[0-9]+[\.]?[0-9]*)')

try:
    basestring
except NameError:
    basestring = str

def guess_ionmode(*args):
    """

    Parameters
    ----------
    *args :
        

    Returns
    -------

    """
    
    for a in args:
        
        if hasattr(a, 'lower'):
            
            a = a.lower()
            
            if IONMODE_POS in a:
                
                return IONMODE_POS
                
            elif IONMODE_NEG in a:
                
                return IONMODE_NEG


def to_float(num):
    """Extracts ``float`` from string, or returns ``numpy.nan``.

    Parameters
    ----------
    num :
        

    Returns
    -------

    """
    
    if isinstance(num, float):
        
        return num
    
    if isinstance(num, int):
        
        return float(num)
    
    if isinstance(num, basestring):
        
        num = num.strip()
        match = refloat.match(num)
        
        if match:
            
            return float(match.groups()[0])
            
        else:
            
            if num.lower() == 'inf':
                
                return np.inf
            
            if num.lower() == '-inf':
                
                return -np.inf
    
    return np.nan


def to_int(num):
    """
    Attempts to make sure ``num`` is ``int``. Tries to convert from string,
    round from float, integers returns unchanged, raises error if could not
    convert ``num`` to ``int``.

    Parameters
    ----------
    num : str,float,int
        A number.

    Returns
    -------
    Integer.
    """
    
    if isinstance(num, int):
        
        return num
    
    if isinstance(num, (float, np.float64)):
        
        return int(np.round(num))
    
    match = reint.match(num.strip())
    
    if match:
        
        return int(np.round(float(match.groups(0)[0])))
        
    else:
        
        raise ValueError('Integer expected: %g' % num)


def bool_array_dilation(array, extent = 1):
    """
    Applies dilation on a boolean array with a certain extent.
    """
    
    if not isinstance(array, np.ndarray):
        
        array = np.array(array)
    
    indices = (
        np.arange(extent + 2)[None, :] +
        np.arange(len(array))[:,None] - 1
    )
    indices[indices < 0] = 0
    indices[indices >= len(array)] = len(array) - 1
    
    dilated = np.array([np.any(array[win]) for win in indices])
    
    return np.array(dilated)


def to_bytes(s, encoding = 'utf8'):
    """
    If a string is not bytes type encodes it.
    """
    
    return s.encode(encoding) if hasattr(s, 'encode') else s


def ensure_bytes(value):
    """
    Makes sure that ``value`` is a string type it is a bytes string.
    Other types it returns unchanged.
    """
    
    return to_bytes(value) if hasattr(value, 'encode') else value


def ensure_unicode(value):
    """
    Makes sure that ``value`` is a unicode string. Other types it converts
    to string by their default method. Note, in Python2 it does not
    definitely converts to unicode type, its main purpose to prepare fields
    for insertion into messages.
    """
    
    return (
        value
            if hasattr(value, 'encode') else
        value.decode('utf8')
            if hasattr(value, 'decode') else
        '%.08f' % value
            if isinstance(value, (float, np.float64)) else
        str(value)
    )


def dict_ensure_bytes(d):
    """
    Makes sure both keys and values in a dict are bytes strings.
    """
    
    return dict(
        (
            ensure_bytes(key),
            ensure_bytes(val),
        )
        for key, val in iteritems(d)
    )


def ppm(reference, other):
    """
    Returns the difference in PPM between a reference mass or m/z
    and an other value.
    
    PPM values are negative if the other value is lower than the reference.
    """
    
    reference = reference.mass if hasattr(reference, 'mass') else reference
    other = other.mass if hasattr(other, 'mass') else other
    
    return (other - reference) / reference * 1e6


def ensure_array(arr):
    """
    If `arr` is not a `numpy.ndarray` instance attempts to convert it.
    """
    
    if not isinstance(arr, np.ndarray):
        
        arr = np.array(arr)
    
    return arr


def _is_numeric(value, regex):
    
    if hasattr(value, 'decode'):
        
        value = value.decode()
    
    return (
        isinstance(value, basestring) and
        regex.fullmatch(value) is not None
    )


def is_int(value):
    """
    Tells if `value` is a string representation of an integer.
    
    Returns
    -------
        `bool`.
    """
    
    return _is_numeric(value, reint)


def is_float(value):
    """
    Tells if `value` is a string representation of a floating point number.
    
    Returns
    -------
        `bool`.
    """
    
    return _is_numeric(value, refloat)


def is_numeric(value):
    """
    Tells if `value` is a string representation of a number (either float
    or int).
    
    Returns
    -------
        `bool`.
    """
    
    return _is_numeric(value, renumeric)


def to_number(value):
    """
    Returns `float` if `value` is a string representation of a floating point
    number, otherwise `int` if `value` is a string representation of an
    integer, otherwise `None`.
    
    Returns
    -------
        `float`, `int` or `None`.
    """
    
    if hasattr(value, decode):
        
        value = value.decode()
    
    try:
        
        return int(value)
        
    except ValueError:
        
        try:
            
            return float(value)
            
        except:
            
            pass
