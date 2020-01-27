import numpy as np
from operator import itemgetter

print('This program shows the number of rays passing through each grid point.')
#taking valid inputs from the user, rejecting invalid keyboard inputs
while True:
	try:
		lat1 = input('Enter the lowest latitude value : ')
	except NameError:
		print('Please Enter a number!')
		#again start the loop
		continue
	if lat1 < -90 or lat1 > 90:
		print('Please Enter a valid no between -90 to +90!')
	else:
		break

while True:
	try:
		lat2 = input('Enter the highest latitude value : ')
	except NameError:
		print('Please Enter a number!')
		continue
	if lat2 < -90 or lat2 > 90:
		print('Please Enter a valid no between -90 to +90!')
	else:
		break

while True:
	try:
		long1 = input('Enter the lowest longitude value : ')
	except NameError:
		print('Please Enter a number!')
		continue
	if long1 < -180 or long1 > 180:
		print('Please Enter a valid no between -180 to +180!')
	else:
		break

while True:
	try:
		long2 = input('Enter the highest longitude value : ')
	except NameError:
		print('Please Enter a number!')
		continue
	if long2 < -180 or long2 > 180:
		print('Please Enter a valid no between -180 to +180!')
	else:
		break

while True:
	try:
		dw = input('Enter the incremental width : ')
	except NameError:
		print('Please Enter a number!')
		continue
	if dw > (lat2-lat1) or dw > (long2-long1):
		print('Please Enter a valid increment!')
	else:
		break
#list of latitudes and longitudes of grids in the chosen area.
latitude = []
longitude = []
lat = lat1
while lat<=lat2:
	latitude.append(lat)
	lat += dw
lon = long1
while lon<=long2:
	longitude.append(lon)
	lon += dw

#getting source and receivers information from a txt file
source_lat = []
source_long = []
ff_source = open('source_2D.txt','r')
lines = ff_source.readlines()
for x in lines:
	source_lat.append(x.split()[0])
for y in lines:
	source_long.append(y.split()[1])
#converting string elements to float
for i in range(len(source_lat)):
	source_lat[i] = float(source_lat[i])
for j in range(len(source_long)):
	source_long[j] = float(source_long[j])

station_lat = []
station_long = []
ff_station = open('receiver_2D.txt','r')
lines = ff_station.readlines()
for x in lines:
	station_lat.append((x.split()[0]))
for y in lines:
	station_long.append((y.split()[1]))
#converting string elements to float
for i in range(len(station_lat)):
	station_lat[i] = float(station_lat[i])
for j in range(len(station_long)):
	station_long[j] = float(station_long[j])
#combining source_lat and source_long in a singe list
source = []
for i in range(len(source_lat)):
	a = source_lat[i]
	b = source_long[i]
	source.append([a,b])
#combining station_lat and station_long in a singe list
receiver = []
for j in range(len(station_lat)):
	a = station_lat[j]
	b = station_long[j]
	receiver.append([a,b])
#*********************Now, we have the information about the grid, source and station********************************#
#counting starts
a_count = (lat2-lat1)/dw
b_count = (long2-long1)/dw
count_grid = np.zeros((int(a_count),int(b_count))) #zero matrix, a_count by b_count
#assigning no to the latitudes & longitudes and storing it in a dictionary
lat_no = []
for i in range(len(latitude)-1):
	lat_no.append(i)
#the length of latitude and lat_no should be equal.
lat_ex_lat1 = latitude[:] #copying latitude
del lat_ex_lat1[0]
lat_dict = dict(zip(lat_ex_lat1,lat_no))
long_no = []
long_ex_long1 = longitude[:]
del long_ex_long1[0]
for j in range(len(longitude)-1):
	long_no.append(j)
long_dict = dict(zip(long_ex_long1,long_no))

#NO OF BOX THROUGH WHICH EACH RAY PASSES THROUGH IS CALCULATED TROUGH A LOOP
for i in range(len(source)):
	source_lat = (source[i])[0]
	source_long = (source[i])[1]
	rec_lat = (receiver[i])[0]
	rec_long = (receiver[i])[1]
	#since we assumed that source is in bottom left corner, if not then interchange source and receiver
	mag1 = source_lat**2+source_long**2
	mag2 = rec_lat**2+rec_long**2
	if mag1 > mag2:
		source_lat,source_long,rec_lat,rec_long = rec_lat,rec_long,source_lat,source_long
	def line_eq(x):             
		y = (rec_long-source_long)*(x-source_lat)/(rec_lat-source_lat) + source_long
		return y
	#taking note of the points cutting the vertical lines
	vertical_dots = [] 
	for i in latitude:      #finding the starting grid, if the source lies in a box and not in a grid
		if i>source_lat:
			lat = i
			break
	while lat<=rec_lat:
		y = line_eq(lat)
		dist = lat**2+y**2
		dot_location = [lat,y,dist]
		vertical_dots.append(dot_location)
		lat = lat+dw
	
	#taking notes of the points cutting the horizontal lines
	def eq_line(y): #x and y axis interchanged
		x = (rec_lat-source_lat)*(y-source_long)/(rec_long-source_long) + source_lat
		return x
	horizontal_dots = []
	for i in longitude:
			if i>source_long:
				lon = i
				break
	while lon<=rec_long:
		x = eq_line(lon)
		dist = lon**2+x**2
		dot_location = [x,lon,dist]
		horizontal_dots.append(dot_location)
		lon = lon+dw
	#location of the nodes - intersection point of ray and grid lines
	nodes = horizontal_dots + vertical_dots
	nodes.append([source_lat,source_long,0])
	nodes.append([rec_lat,rec_long,rec_lat**2+rec_long**2])
	sort_list = sorted(nodes,key=itemgetter(2))

	#finding the co-ordinates of the mid point of adjecent points
	mid_point = []
	for i in range(len(sort_list)-1):
		a = sort_list[i]
		b = sort_list[i+1]
		mid_x = (a[0]+b[0])/2.0
		mid_y = (a[1]+b[1])/2.0
		mid_point.append([mid_x,mid_y])	
	for i in mid_point:
		x = i[0] #lat of the point, lies inside the box
		y = i[1] #long of the point
		for j in latitude:
			if j>x:
				p = lat_dict[j] 
				break
		for k in longitude:
			if k>y:
				q = long_dict[k]
				break
		count_grid[p,q] += 1
#generating the required data points to plot it in GMT
ff = open('gmt_2D.txt','w')
for i in range(int(a_count)):
	for j in range(int(b_count)):
		count = count_grid[i,j]
		latitude1 = lat1+i*dw 
		latitude2 = lat1+(i+1)*dw
		longitude1 = long1+j*dw
		longitude2 = long1+(j+1)*dw
		print >>ff,latitude1,latitude2,longitude1,longitude2,count
		
#We have the information about corner points of the box and the value assigned to it.


































