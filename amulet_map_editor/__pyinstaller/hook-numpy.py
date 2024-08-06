import os
import glob

import numpy

numpy_lib_path = numpy.__path__[0] + ".libs"

datas = [
    (dll_path, "numpy.libs")
    for dll_path in glob.glob(os.path.join(glob.escape(numpy_lib_path), "*.dll"))
]
