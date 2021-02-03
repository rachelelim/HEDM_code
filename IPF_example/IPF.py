from hexrd.material import Material
from hexrd.valunits import valWUnit
import numpy as np
"""
Done in 3 steps:
1. initialize a materials class

2. just get a bunch of rotation matrices should be nx3x3. 

3. call color_orientations routine.
By default the IPFZ is calculated 
if you want to pass different reference direction, use the "ref_dir" keyword
In the example below I'm  explicitly passing x-axis, so IPFX will be calculated.
That's it.
"""

beamenergy = valWUnit('kev','energy',10.0,'keV')
dmin = valWUnit('lp', 'length',  0.05, 'nm')

xtal = 'spacegroups.h5' # just an example h5 materials file

name = 'sg194' # space group 194; same as Ti or Zr

alpha = Material(name=name, material_file=xtal, dmin=dmin, kev=beamenergy)

"""
just some identity matrices as examples
"""
rmat1 = np.eye(3)
rmat2 = np.eye(3)

rmats = np.array([rmat1, rmat2])

rgb = alpha.unitcell.color_orientations(rmats, ref_dir=np.array([1.,0.,0.]))
