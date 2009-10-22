import os.path
import unittest
from persistent import Persistent
from zope.testing import doctest, module
from zope.app.testing import functional

ftesting_zcml = os.path.join(os.path.dirname(__file__), 'ftesting.zcml')
FunctionalLayer = functional.ZCMLLayer(
    ftesting_zcml, __name__, 'FunctionalLayer',allow_teardown=True)


class Mammoth(Persistent):
    """A test model.
    """
    pass


def test_suite():
    """Testing suite.
    """
    readme = functional.FunctionalDocFileSuite(
        'README.txt',
        globs={"__name__": "dolmen.widget.image"},
        optionflags=(doctest.ELLIPSIS + doctest.NORMALIZE_WHITESPACE),
        )

    readme.layer = FunctionalLayer
    suite = unittest.TestSuite()
    suite.addTest(readme)
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
