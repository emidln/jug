# -*- coding: utf-8 -*-
# Copyright (C) 2011, Luis Pedro Coelho <luis@luispedro.org>
# vim: set ts=4 sts=4 sw=4 expandtab smartindent:
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#  THE SOFTWARE.

def hash_update(M, elems):
    '''
    M = hash_update(M, elems)

    Update the hash object ``M`` with the sequence ``elems``.

    Parameters
    ----------
    M : hashlib object
        An object on which the update method will be called
    elems : sequence of 2-tuples

    Returns
    -------
    M : hashlib object
        This is the same object as the argument
    '''
    import cPickle as pickle
    try:
        import numpy as np
    except ImportError:
        np = None
    for n,e in elems:
        M.update(pickle.dumps(n))
        if hasattr(e, '__jug_hash__'):
            M.update(e.__jug_hash__())
        elif type(e) in (list, tuple):
            hash_update(M, enumerate(e))
        elif type(e) == dict:
            hash_update(M, e.iteritems())
        elif np is not None and type(e) == np.ndarray:
            M.update('np.ndarray')
            M.update(pickle.dumps(e.dtype))
            M.update(pickle.dumps(e.shape))
            try:
                buffer = e.data
                M.update(buffer)
            except:
                M.update(e.copy().data)
        else:
            M.update(pickle.dumps(e))
    return M

def new_hash_object():
    '''
    M = new_hash_object()

    Returns a new hash object

    Returns
    -------
    M : hashlib object
    '''
    import hashlib
    return hashlib.sha1()

