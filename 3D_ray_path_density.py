import numpy as np
from operator import itemgetter

print('This program shows the number of rays passing through each differential cube in space.')
#taking valid inputs from the user, rejecting invalid inputs.
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
		dpth = input('Enter the depth of the grid mesh:  ')
	except NameError:
		print('Please Enter a number!')
		continue
	if dpth < 0 or dpth > 6371:
		print('Please Enter a valid depth value  between 0 to +6371!') #radius of earth
	else:
		break		

while True:
	try:
		dw = input('Enter the incremental width : ')
	except NameError:
		print('Please Enter a number!')
		continue
	if dw > (lat2-lat1) or dw > (long2-long1) or dw > dpth:
		print('Please Enter a valid increment!')
	else:
		break
#list of latitudes,longitudes and depth of grids in the chosen area.
latitude = []
longitude = []
depth = []
lat = lat1
while lat<=lat2:
	latitude.append(lat)
	lat += dw
lon = long1 #can't use long as it is a reserved word
while lon<=long2:
	longitude.append(lon)
	lon += dw
dep = 0.0
while dep<=dpth:
	depth.append(dep)
	dep += dw
#getting sources and receivers information from a txt file
source_lat = []
source_long = []
source_depth = []
ff_source = open('source_3D.txt','r')
lines = ff_source.readlines()
for x in lines:
	source_lat.append(x.split()[0])
for y in lines:
	source_long.append(y.split()[1])
for z in lines:
	source_depth.append(z.split()[2])
#converting string elements of lists to float
for i in range(len(source_lat)):
	source_lat[i] = float(source_lat[i])
for j in range(len(source_long)):
	source_long[j] = float(source_long[j])
for k in range(len(source_depth)):
	source_depth[k] = float(source_depth[k])
station_lat = []
station_long = []
station_depth = []
ff_station = open('receiver_3D.txt','r')
lines = ff_station.readlines()
for x in lines:
	station_lat.append((x.split()[0]))
for y in lines:
	station_long.append((y.split()[1]))
for z in lines:
	station_depth.append((z.split()[2]))
#converting string elements to float
for i in range(len(station_lat)):
	station_lat[i] = float(station_lat[i])
for j in range(len(station_long)):
	station_long[j] = float(station_long[j])
for k in range(len(station_depth)):
	station_depth[k] = float(station_depth[k])
#combining source_lat,source_long and source_depth in a singe list
source = []
for i in range(len(source_lat)):
	a = source_lat[i]
	b = source_long[i]
	c = source_depth[i]
	source.append([a,b,c])
#combining station_lat,station_long and station_depth in a singe list
receiver = []
for j in range(len(station_lat)):
	a = station_lat[j]
	b = station_long[j]
	c = station_depth[j]
	receiver.append([a,b,c])
#Now, we have the information about the grid, sources and stations
#counting starts
a_count = (lat2-lat1)/dw
b_count = (long2-long1)/dw
count_grid = np.zeros((int(a_count),int(b_count))) #matrix in a plane
#count_grid should vary as we move along depth
count_3D = []
dep = 0
while dep<=dpth:
	count_3D.append(count_grid)
	dep += dw
#count_3D stores the count_grid as we vary the depth and hence counts in 3D space.
#assinging number to grids
lat_no = []
for i in range(len(latitude)-1):
	lat_no.append(i)
lat_ex_lat1 = latitude[:]
del lat_ex_lat1[0] #to make latitude and lat_no of equal length.
lat_dict = dict(zip(lat_ex_lat1,lat_no))
long_no = []
for j in range(len(longitude)-1):
	long_no.append(j)
long_ex_long1 = longitude[:]
del long_ex_long1[0] 
long_dict = dict(zip(long_ex_long1,long_no))
depth_no = []
for k in range(len(depth)-1):
	depth_no.append(k)
depth_ex_dep1 = depth[:]
del depth_ex_dep1[0]
depth_dict = dict(zip(depth_ex_dep1,depth_no))

#NO OF RAYS WHICH PASSES THROUGH EACH CUBE IS CALCULATED TROUGH A LOOP
for i in range(len(source)):
	source_lat = (source[i])[0]
	source_long = (source[i])[1]
	source_depth = (source[i])[2]
	rec_lat = (receiver[i])[0]
	rec_long = (receiver[i])[1]
	rec_depth = (receiver[i])[2]
	#assuming source is located deeper than station;change source and reciever,otherwise 
	if rec_depth > source_depth:
		source_lat,source_long,source_depth,rec_lat,rec_long,rec_depth = rec_lat,rec_long,rec_depth,source_lat,source_long,source_depth
	#Line equation in 3D
	#return x given the value of z
	def line_eqx(z):
		try:             
			x = source_long + (float(rec_long-source_long))*(z-source_depth)/(rec_depth-source_depth)
			return x
		except ZeroDivisionError:
			pass
	#return y given the value of z
	def line_eqy(z):
		try:
			y = source_lat + (float(rec_lat-source_lat))*(z-source_depth)/(rec_depth-source_depth)
			return y
		except ZeroDivisionError:
			pass
	#finding the co-ordinate of the point of intersection of the line and depth planes
	intersection = []
	if source_depth == rec_depth:	#gives ZeroDivisionError while calculating x,y values for a given z
		z = source_depth
		#2D case
		def line_eq(x):             
			y = (rec_long-source_long)*(x-source_lat)/(rec_lat-source_lat) + source_long
			return y		
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
		#location of the nodes - intersection point of ray and grid lines in plane contaning source and receiver.
		nodes = horizontal_dots + vertical_dots
		nodes.append([source_lat,source_long,0])
		nodes.append([rec_lat,rec_long,rec_lat**2+rec_long**2])
		sort_list = sorted(nodes,key=itemgetter(2))
		for i in sort_list:
			del i[2]
			i.append(z)
		intersection = sort_list[:]
	else:
		#The nearest z plane to the source,depth less than the source and depth plane
		for i in depth:
			if i > source_depth:
				source_depth = i-dw
				break
		#similarly for receiver	
		for j in depth:
			if j > rec_depth:
				rec_depth = j
				break
		z = source_depth
		while z >= rec_depth:
			x = line_eqx(z)
			y = line_eqy(z)
			intersection.append([y,x,z])
			z = z-dw
	#finding the co-ordinates of the mid point of adjecent points
	mid_point = []
	for i in range(len(intersection)-1):
		a = intersection[i]
		b = intersection[i+1]
		mid_x = (a[0]+b[0])/2.0
		mid_y = (a[1]+b[1])/2.0
		mid_z = (a[2]+b[2])/2.0
		mid_point.append([mid_x,mid_y,mid_z])	
	for i in mid_point:
		x = i[0]
		y = i[1]
		z = i[2]
		for j in latitude:
			if j>x:
				p = lat_dict[j]
				break
		for k in longitude:
			if k>y:
				q = long_dict[k]
				break
		for l in depth:
			if l>z:
				r = depth_dict[l]
				break
		#need to update count_3D
		count_3D[r][p,q] += 1
#generating the required data points to plot it in GMT
f = open('gmt_3D.txt','w')
for i in range(len(count_3D)-1):
	for j in range(int(a_count)):
		for k in range(int(b_count)):		
			count = count_3D[i][j,k]
			depth1 = depth[i]
			depth2 = depth[i+1]
			longitude1 = long1+k*dw
			longitude2 = long1+(k+1)*dw
			latitude1 = lat1+j*dw 
			latitude2 = lat1+(j+1)*dw
			print >>f,count,depth1,depth2,longitude1,longitude2,latitude1,latitude2
		
