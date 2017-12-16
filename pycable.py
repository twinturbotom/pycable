import pandas as pd
import math
pd.set_option('display.width', 1000)
pd.options.display.float_format = '{:,.2f}'.format

def gauge_to_dia_mm(gauge):
	if gauge == ('00' or '000' or '0000'):
		gauge = -(len(gauge)-1)
		
	dia_mm = 0.127 * math.pow(92, ((36.0-gauge)/39.0) )
	return dia_mm

wire_ref = pd.DataFrame()
wire_ref['Gauge'] = pd.Series([14,12,10,8,6,4,3,0])
wire_ref['Amperage'] = pd.Series([15,20,30,50,60,85,100,115])
wire_ref['Diameter (mm)'] = wire_ref['Gauge'].apply(gauge_to_dia_mm)
wire_ref['Radius (mm)'] = wire_ref['Diameter (mm)']
wire_ref['Area (mm2)'] = wire_ref['Radius (mm)'].apply( lambda r: math.pi*math.pow( r,2) )
wire_ref['Circumference (mm)'] = 2*math.pi*wire_ref['Area (mm2)']
wire_ref['Bend Radius (mm)'] = wire_ref['Diameter (mm)'] * 8

print '\n', wire_ref

print '\n', wire_ref.loc[wire_ref['Gauge'] == 10]

print '\n'



N = 12
Dia = 5.0 #mm
fill_percent = .4

#DF for each conductor
conductors = pd.DataFrame({ 'Number': range(1,N+1) })

#Define properties of conductors
conductors['Diameter'] = Dia
conductors['Circumference'] = 2*math.pi*(conductors['Diameter']/2)
conductors['Area'] = conductors['Diameter'].apply(lambda D: math.pi*math.pow((D/2),2) )

bundle_area = conductors['Area'].sum()
bundle_dia = 2* math.sqrt( bundle_area / math.pi ) 
print('Bundle Dia: {}'.format(bundle_dia))

conduit_area = (conductors['Area'].sum())/fill_percent
conduit_dia = 2* math.sqrt( conduit_area / math.pi ) 

print('Conduit Area: {conduit_area} = Total bundle area {bundle_area} / fill percent {fill}'.format(conduit_area=conduit_area, bundle_area=bundle_area,fill=fill_percent, dia=conduit_dia) )