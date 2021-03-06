# -*- coding: UTF-8 -*-

# ONLY EDIT THIS FILE IF YOU KNOW WHAT YOU DO!

def _():
    import sys, os
    if 'FEFLOW72_ROOT' in os.environ:
        feflow_root = os.environ['FEFLOW72_ROOT']
        sys.path.append(feflow_root + 'bin64')
    #       if sys.version_info > (3, 0):
    #           sys.path.append(feflow_root+'python/pyscriptlib37.zip')
    #       else:
    #           sys.path.append(feflow_root+'python/pyscriptlib27.zip')
    if sys.platform == 'cli':
        import clr
        clr.AddReference('IronPython.Feflow72')


_()
del _

import sys

if sys.platform == 'cli':
    from feflow import *


    def loadDocument(f):
        return PyFeflowKernel.loadDocument(f)


    def forceLicense(l):
        return PyFeflowKernel.forceLicense(l)
else:
    if sys.version_info >= (3, 7) and sys.version_info < (3, 8):
        from ifm37 import *
        from ifm37 import loadDocument as _loadDocument
    elif sys.version_info >= (3, 6) and sys.version_info < (3, 7):
        from ifm36 import *
        from ifm36 import loadDocument as _loadDocument
    elif sys.version_info >= (3, 5) and sys.version_info < (3, 6):
        from ifm35 import *
        from ifm35 import loadDocument as _loadDocument
    elif sys.version_info >= (2, 7) and sys.version_info < (2, 8):
        from ifm27 import *
        from ifm27 import loadDocument as _loadDocument
    else:
        raise ImportError('This python version is not supported by FEFLOW!')

    import colormaps

    def loadDocument(f):
        """
        This replaces the original ifm.loadDocument function.
        it returns a copy of an IFM Document including the ifm_contrib extension.
        :param f: filename of fem or dac
        :return: doctype including ifm_contrib extension
        """
        return doc_contrib(f)


    class doc_contrib():
        """
        Contributors IfmDocument class.
        This class loads the original IfmDocument class and adds the contributors methods.
        """

        def __init__(self, filename):
            # load document as standard IFM object and transfer all attributes to contributors IFM object
            self.pdoc = _loadDocument(filename)
            for item in dir(self.pdoc):
                self.__dict__[item] = self.pdoc.__getattribute__(item)

            # import contributors library
            import contrib_lib
            self.c = contrib_lib.IfmContrib(self)
