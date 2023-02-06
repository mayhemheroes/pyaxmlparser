#!/usr/bin/env python3

import atheris
import sys
import fuzz_helpers
from contextlib import contextmanager
import io

with atheris.instrument_imports(include=["pyaxmlparser", "pyaxmlparser.apk"]):
    from pyaxmlparser.arscparser import ARSCParser
    from pyaxmlparser.axmlparser import AXMLParser
    from zipfile import BadZipFile
    from struct import error

@contextmanager
def nostdout():
    save_stdout = sys.stdout
    save_stderr = sys.stderr
    sys.stdout = io.StringIO()
    sys.stderr = io.StringIO()
    yield
    sys.stdout = save_stdout
    sys.stderr = save_stderr

def TestOneInput(data):
    fdp = fuzz_helpers.EnhancedFuzzedDataProvider(data)
    try:
        with nostdout():
            if fdp.ConsumeBool():
               ARSCParser(fdp.ConsumeRemainingBytes())
            else:
              AXMLParser(fdp.ConsumeRemainingBytes())

    except (BadZipFile, OSError, AssertionError, error):
        return -1

def main():
    atheris.Setup(sys.argv, TestOneInput)
    atheris.Fuzz()


if __name__ == "__main__":
    main()
