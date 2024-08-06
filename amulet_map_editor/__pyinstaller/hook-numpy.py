import os
import glob
import sys

import numpy

if sys.platform == "win32":
    numpy_path = numpy.__path__[0]
    numpy_lib_path = numpy_path + ".libs"

    datas = [
        (dll_path, "numpy.libs")
        for dll_path in glob.glob(os.path.join(glob.escape(numpy_lib_path), "*.dll"))
    ] + [
        (pyd_path, os.path.relpath(os.path.dirname(pyd_path), os.path.dirname(numpy_path)))
        for pyd_path in glob.glob(
            os.path.join(glob.escape(numpy.__path__[0]), "**", "*.pyd"), recursive=True
        )
    ]
