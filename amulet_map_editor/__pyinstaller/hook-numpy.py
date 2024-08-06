import os
import glob
import sys

import numpy

if sys.platform == "win32":
    numpy_lib_path = numpy.__path__[0] + ".libs"

    datas = [
        (dll_path, "numpy.libs")
        for dll_path in glob.glob(os.path.join(glob.escape(numpy_lib_path), "*.dll"))
    ] + [
        (pyd_path, "numpy")
        for pyd_path in glob.glob(os.path.join(glob.escape(numpy.__path__[0]), "**", "*.pyd"), recursive=True)
    ]
