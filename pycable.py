import pandas as pd
import math
import numpy as np

pd.set_option('display.width', 1000)
pd.options.display.float_format = '{:,.2f}'.format

N = 24
Dia = 5.0 #mm
fill_percent = .4

def circle_area(radius=None, diameter=None):
	if not radius:
		radius = diameter / 2

	area = math.pi*math.pow( radius,2)

	return area

def gauge_to_dia_mm(gauge):
	if gauge == ('00' or '000' or '0000'):
		gauge = -(len(gauge)-1)
		
	dia_mm = 0.127 * math.pow(92, ((36.0-gauge)/39.0) )
	return dia_mm

def inch_to_mm(inch):
	return inch * 25.4

cable_table = pd.DataFrame()
cable_table['Gauge'] = pd.Series([14,12,10,8,6,4,3,0])
cable_table['Amperage'] = pd.Series([15,20,30,50,60,85,100,115])
cable_table['Diameter (mm)'] = cable_table['Gauge'].apply(gauge_to_dia_mm)
cable_table['Radius (mm)'] = cable_table['Diameter (mm)']
cable_table['Area (mm2)'] = cable_table['Radius (mm)'].apply( lambda r: math.pi*math.pow( r,2) )
cable_table['Circumference (mm)'] = 2*math.pi*cable_table['Area (mm2)']
cable_table['Bend Radius (mm)'] = cable_table['Diameter (mm)'] * 8

harness = pd.DataFrame( range(1,(N+1)), columns=['Number'])
harness['Amperage'] = [60]*12 + [30]*12 
harness = harness.merge(cable_table, on='Amperage')
harness['Inner Label'] = [  '{x}{y}'.format(x=x,y=y) for x in range(1,7) for y in ['A','B']]*2

conduits = pd.DataFrame({'Diameter (in)': [0.5,1.0,1.5,2.0]})
conduits['Diameter (mm)'] = inch_to_mm( conduits['Diameter (in)'] )
conduits['Area (mm2)'] = conduits['Diameter (mm)'].apply(lambda A: circle_area( diameter = A ) )
conduits['40% Area'] = conduits['Area (mm2)']*.4
conduits['30A Bundle Area (mm2)'] = harness.loc[ harness['Amperage'] == 30]['Area (mm2)'].sum()
conduits['% of 30A bundle'] = conduits['30A Bundle Area (mm2)'] / conduits['Area (mm2)']
conduits['60A Bundle Area (mm2)'] = harness.loc[ harness['Amperage'] == 60]['Area (mm2)'].sum()
conduits['% of 60A bundle'] = conduits['60A Bundle Area (mm2)'] / conduits['Area (mm2)']


print '\nCable Table:\n\n', cable_table
print '\nHarness:\n\n', harness
print '\nBundle Area (mm2): \n', harness.groupby('Amperage')['Area (mm2)'].sum()
print '\nTotal area of harness: ', harness['Area (mm2)'].sum()
print '\nConduits:\n', conduits

num_bundle_wires = 12
shells = pd.DataFrame(data = list(range(1,num_bundle_wires+1)),columns=['Number'])

conductor_dia = float(cable_table.loc[cable_table['Amperage'] == 60]['Diameter (mm)'])

shells['Radius'] = (shells['Number'] * (conductor_dia)) - (conductor_dia/2)
shells['Circumference'] = (2*math.pi)*shells['Radius'] 
shells['Max Elements'] = ( shells['Circumference'] / (conductor_dia)  ).apply(lambda x: int(x)) #int rounds down.
shells['Element Spacing'] = shells['Circumference'] / (shells['Max Elements'])
shells['Spacing Angle'] = ( shells['Element Spacing'] / shells['Radius'] ) 
shells['Spacing Angle (deg)'] = ( shells['Element Spacing'] / shells['Radius'] ) * (180/math.pi)

try:
	shells_needed = shells[ :shells.loc[ shells['Max Elements'].cumsum() >= num_bundle_wires  ].index[0]+ 1]
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

bundle = pd.DataFrame(data = {'Number' : list(range(1,num_bundle_wires+1)), 'Radius' : radii[:num_bundle_wires], 'Theta' : thetas[:num_bundle_wires] } )
xs = []
ys = []
def cyl_to_orth(row, xs, ys, r,theta):
	x = row[r]*math.cos(row[theta])
	y = row[r]*math.cos(row[theta])
	xs.append(x)
	ys.append(y)
bundle.apply(cyl_to_orth, axis=1, args=(xs, ys,'Radius','Theta') )
bundle['X'] = xs
bundle['Y'] = ys

print '\n', bundle

