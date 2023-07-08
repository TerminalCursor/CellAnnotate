from geometry_shapes import Ellipsoid
import numpy as np
import time

z_stack_count = 14
a,b,c = 4, 4, 0.25
r = 4
#COUNT = 5
COUNT_X = 2
COUNT_Y = 1
offset = 4
z_off = 6

def save_zstack(data, filepath=None):
	"""
	INPUTS
	-----------------------------------------------------
	data = 3D np array shape H x W x Z
		data should be the output 'Iall' from run_analysis

	filepath = string, filepath with filename and ending '.ome.tif'

	OUTPUTS
	------------------------------------------------------
	Saves a .ome.tif file to the home directory or directory specified in
	filepath
	"""
	#data should be shape
	A = np.rollaxis(data,0,3)
	A = np.rollaxis(A,0,3)
	import tifffile
	if filepath is None:
		tifffile.imwrite("test.ome.tif",A)
	else:
		tifffile.imwrite(filepath,A)

def apply_noise(mask):
	"""
	Create an intensity image to accompany mask
	"""
	sig_obj = 0.2
	mu_obj = 0.6
	sig_bg = 0.01
	mu_bg = 0.05
	#draw from normal distributions.
	IM = np.zeros(shape=mask.shape, dtype=np.float32)
	obj = np.random.normal(mu_obj, sig_obj, mask.shape)
	bg = np.random.normal(mu_bg, sig_bg, mask.shape)
	IM = np.where(mask, obj, bg)
	IM = np.clip(IM, 0., 1.)
	return IM

SIZE_X = 1024
SIZE_Y = SIZE_X
SIZE_Z = z_stack_count
x = np.linspace(0,SIZE_X-1,SIZE_X)
y = np.linspace(0,SIZE_Y-1,SIZE_Y)
z = np.linspace(0,SIZE_Z-1,SIZE_Z)
u,_,_ = np.meshgrid(x,y,z) #x,y,z coordinates. H x W x Z matrix.

z_ini = np.random.rand()

mask = np.zeros_like(u)
es = []

## for ey in range(1, COUNT+1):
## 	for ex in range(1, COUNT+1):
## 		es.append(Ellipsoid((2*r*a * 1.5)*ex, (2*r*b * 1.5)*ey, 1, a, b, c, r))
## 		es.append(Ellipsoid((2*r*a * 1.5)*ex + (ex - 1), (2*r*b * 1.5)*ey + (ey - 1), 1+z_off, a, b, c, r))
## 
## for i in range(int(np.ceil(2*r*a * 1.5 *(COUNT + 1))) + 1):
## 	print((i, int(np.ceil(2*r*a * 1.5 *(COUNT + 1))) + 1))
## 	for j in range(int(np.ceil(2*r*b* 1.5 * (COUNT + 1))) + 1):
## 		for k in range(SIZE_Z):
## 			for e in es:
## 				if e.check(x[i], y[j], z[k]):
## 					mask[i,j,k]=1.
## 					break

E = Ellipsoid(2*r*a, 2*r*b, 1, a, b, c, r)
X = int(np.ceil(2*r*a * 1.5))
Y = int(np.ceil(2*r*b * 1.5))
Z = int(np.ceil(2*r*c * 1.5))
ellipsoid_mask = np.zeros((X, Y, Z))
for i in range(0, X):
	for j in range(0, Y):
		for k in range(0, Z):
			if E.check(x[i], y[j], z[k]):
				ellipsoid_mask[i,j,k]=1.

X_INI_li = [(c * X) for c in range(COUNT_X)]
Y_INI_li = [(c * Y) for c in range(COUNT_Y)]
Z_INI_li = [0]
for X_INI in X_INI_li:
	for Y_INI in Y_INI_li:
		for Z_INI in Z_INI_li:
			mask[X_INI:X_INI+X,Y_INI:Y_INI+Y,Z_INI:Z_INI+Z] = ellipsoid_mask

X_INI_li = [(c * X + c) for c in range(COUNT_X)]
Y_INI_li = [(c * Y + c) for c in range(COUNT_Y)]
Z_INI_li = [2]
for X_INI in X_INI_li:
	for Y_INI in Y_INI_li:
		for Z_INI in Z_INI_li:
			mask[X_INI:X_INI+X,Y_INI:Y_INI+Y,Z_INI:Z_INI+Z] = ellipsoid_mask


M = mask.astype(np.bool_)
M = mask.astype(np.int32)
NM = apply_noise(M)

## TEST CASE of two ellipsoids.
out_prefix = f'./datasets/temp/images/mask'

np.savez(out_prefix + '.npz', exact_mask=M, noise_mask=NM)

M = mask.astype(np.int32)

save_zstack(NM, out_prefix + '.ome.tif')
save_zstack(M, out_prefix + '_m.ome.tif')
