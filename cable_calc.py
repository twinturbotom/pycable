import pandas as pd
import math
import numpy as np
import sys
import matplotlib.pyplot as plt


conduit_dia = 50.0
conductor_dia = 5.0
N = 12

num_shells = int( (conduit_dia/2) / conductor_dia  )

shells = pd.DataFrame(data = list(range(1,num_shells+1)),columns=['Number'])


shells['Radius'] = (shells['Number'] * (conductor_dia)) - (conductor_dia/2)
shells['Circumference'] = (2*math.pi)*shells['Radius'] 
shells['Max Elements'] = ( shells['Circumference'] / (conductor_dia)  ).apply(lambda x: int(x)) #int rounds down.
shells['Element Spacing'] = shells['Circumference'] / (shells['Max Elements'])
shells['Spacing Angle'] = ( shells['Element Spacing'] / shells['Radius'] ) #* (180/math.pi)

#print(shells)
#filled_shells = int(shells.loc[ shells['Max Elements'].cumsum() >= N  ].iloc[0]['Number'])
# filled_shells = shells.loc[ shells['Max Elements'].cumsum() >= N  ].iloc[0]['Number']
try:
	shells_needed = shells[ :shells.loc[ shells['Max Elements'].cumsum() >= N  ].index[0]+ 1]
except Exception as e:
	print('More conductors than conduit size')
	print("\nException: %s" % str(e) )
	sys.exit(1)


def radii_gen(row, list_, column1, column2):
	for i in [row[column1]] * int(row[column2] ):
		list_.append(i)
def thetas_gen(row, list_, column1, column2):
	for i in np.arange( row[column1], row[column1]* row[column2]+1, row[column1]):
		list_.append(i)

radii = []
shells_needed.apply(radii_gen, axis=1, args=(radii, 'Radius','Max Elements'))
thetas = []
shells_needed.apply(thetas_gen, axis=1, args=(thetas, 'Spacing Angle','Max Elements'))

conductors = pd.DataFrame(data = {'Number' : list(range(1,N+1)), 'Radius' : radii[:N], 'Theta' : thetas[:N] } )
xs = []
ys = []
def cyl_to_orth(row, xs, ys, r,theta):
	x = row[r]*math.cos(row[theta])
	y = row[r]*math.cos(row[theta])
	xs.append(x)
	ys.append(y)
conductors.apply(cyl_to_orth, axis=1, args=(xs, ys,'Radius','Theta') )
conductors['X'] = xs
conductors['Y'] = ys
print(conductors)
#print(filled_shells)

# list_ = []
# shell_cumsum = shells.loc[ shells['Max Elements'].cumsum() <= N  ]['Max Elements']#.apply(lambda x: x+2)

# print(shell_cumsum)


# elements = pd.DataFrame( index = range(0,N) )
# elements['Radius'] = 1.4
# elements['Shell Number'] = 1

# print(elements)