import sys, os

class HiddenPrints:
    """Allows to temporarily hide sdtout messages, e.g. from print.

    usage:
            with HiddenPrints():
                do something

    This code snipped was published (posted) on Stackoverflow:

    Code Author: Alexander Chzhen
    Date       : Jul 27 2018 at 20:02
    URL        : https://stackoverflow.com/a/45669280

    Code license not explicitly given, is assumed to be MIT license (see URL:
    https://meta.stackexchange.com/questions/272956/a-new-code-license-the-mit-this-time-with-attribution-required?cb=1)
    """
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')
    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout