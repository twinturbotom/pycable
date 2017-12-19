import pandas as pd
import math
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

cable_table = pd.DataFrame()
cable_table['Gauge'] = pd.Series([14,12,10,8,6,4,3,0])
cable_table['Amperage'] = pd.Series([15,20,30,50,60,85,100,115])
cable_table['Diameter (mm)'] = cable_table['Gauge'].apply(gauge_to_dia_mm)
cable_table['Radius (mm)'] = cable_table['Diameter (mm)']
cable_table['Area (mm2)'] = cable_table['Radius (mm)'].apply( lambda r: math.pi*math.pow( r,2) )
cable_table['Circumference (mm)'] = 2*math.pi*cable_table['Area (mm2)']
cable_table['Bend Radius (mm)'] = cable_table['Diameter (mm)'] * 8

print '\nCable Table:\n\n', cable_table

# print '\n', cable_table.loc[ (cable_table['Amperage'] == 60) | (cable_table['Amperage'] == 30) ]

harness = pd.DataFrame( range(1,(N+1)), columns=['Number'])
harness['Amperage'] = [60]*12 + [30]*12 
harness = harness.merge(cable_table, on='Amperage')
	
print '\nHarness:\n\n', harness

print '\nTotal area of 30 gauge: ', harness.loc[ harness['Amperage'] == 30]['Area (mm2)'].sum()
print 'Total area of 60 gauge: ', harness.loc[ harness['Amperage'] == 60]['Area (mm2)'].sum()
print '\nTotal area of harness: ', harness['Area (mm2)'].sum()
print '40% of 2" diameter conduit: ', circle_area(radius=25.4) * .4

print harness.groupby('Amperage').sum()

#conduit_ratio = harness.loc[ harness['Amperage'] == 60]['Area (mm2)'].sum() / circle_area(radius=25.4)

#print '\n', '{:,.2f}'.format(conduit_ratio)

# #DF for each conductor=
# conductors = pd.DataFrame({ 'Number': range(1,N+1) })

# #Define properties of conductors
# conductors['Diameter'] = Dia
# conductors['Circumference'] = 2*math.pi*(conductors['Diameter']/2)
# conductors['Area'] = conductors['Diameter'].apply(lambda D: math.pi*math.pow((D/2),2) )

# bundle_area = conductors['Area'].sum()
# bundle_dia = 2* math.sqrt( bundle_area / math.pi ) 
# print('Bundle Dia: {}'.format(bundle_dia))

# conduit_area = (conductors['Area'].sum())/fill_percent
# conduit_dia = 2* math.sqrt( conduit_area / math.pi ) 

# print('Conduit Area: {conduit_area} = Total bundle area {bundle_area} / fill percent {fill}'.format(conduit_area=conduit_area, bundle_area=bundle_area,fill=fill_percent, dia=conduit_dia) )