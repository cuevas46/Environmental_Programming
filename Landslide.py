import os
import numpy as np
import tifffile

dirname = r"Data\\Clipped_images\\"
final = []

for fname in os.listdir(dirname):
    im = tifffile.imread(os.path.join(dirname, fname))
    imarray = np.array(im)
    final.append(imarray)

final = np.asarray(final)












