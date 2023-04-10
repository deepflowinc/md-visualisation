import numpy as np

def tensor(nx: float, ny: float, nz: float, scale: float, ratio: float):
	# input
	# orientation of the major axis: nx, ny, nz
	# scale and ratio of the eigenvectors representing size and shape of particles

	# output 
	# tensor components: XX XY XZ YX YY YZ ZX ZY ZZ
	# [XX XY XZ]
	# [YX YY YZ]
	# [ZX ZY ZZ]

	# setting eigen vectors
	XZ = nx
	YZ = ny
	ZZ = nz

	# you need a scale factor, d to ensure the eigenvalue is 1 for every eigen vector. Otherwise the cross product won't be orthogonal   
	d = 1/(np.sqrt(np.power(XZ,2)+ np.power(ZZ,2)))
	XX = d*ZZ
	YX = 0.0
	ZX = -d*XZ

	XY = -d*XZ*YZ
	YY = d*(np.power(XZ,2) + np.power(ZZ,2))
	ZY = -d*YZ*ZZ

	# now scale eigenvectors using eigenvalues to stretch the size and shape of particles
	XX = scale*XX
	XY = scale*XY
	XZ = ratio*scale*XZ
	YX = scale*YX
	YY = scale*YY
	YZ = ratio*scale*YZ
	ZX = scale*ZX
	ZY = scale*ZY
	ZZ = ratio*scale*ZZ

	return XX,YX,ZX,XY,YY,ZY,XZ,YZ,ZZ



