import csv
from StringIO import StringIO
#use this nice library to find spark's location
import findspark
#import pyspark
from pyspark import SparkConf, SparkContext
#libs dealing with date format
from datetime import datetime
import dateutil.parser as dparser
#for plotting
import matplotlib.pyplot as plt


spark_home='/usr/local/cellar/spark'



def line_split(line):
	reader=csv.reader(StringIO(line), fieldnames=['Date', 'West', 'East'])
	return reader.next()

def strip_datetime(date_string):
    d=dparser.parse(date_string)
    return d



def main(sc):
	bike_data=sc.textFile('FremontBridge.csv')\
	.map(lambda line: (line.split(',')[0], line.split(',')[1], line.split(',')[2]))

	#use 'take' function to turn everything into a list
	bike_data=bike_data.take(20000)

	#to skip the header
	header=0
	time_table={}
	
	for line in bike_data:
		if header==0:
			header=1
		else:
			time_slot=strip_datetime(line[0])


			if time_table.get(time_slot.time())==None:
				if line[1] and line[2]:
					time_table[str(time_slot.time())]=[int(line[1]), int(line[2])]
				elif line[1]:
					time_table[str(time_slot.time())]=[int(line[1]), 0]
				elif line[2]:
					time_table[str(time_slot.time())]=[0,int(line[2])]

			else:
				time_table[str(time_slot.time())][0]+=int(line[1])
				time_table[str(time_slot.time())][1]+=int(line[2])

	#plotting
	time_sorted=sorted(time_table.items())
	y1=[]
	y2=[]
	x=[]
	for i in range(len(time_sorted)):

		y1.append(time_sorted[i][1][0])
		y2.append(time_sorted[i][1][1])
		x.append(time_sorted[i][0])
	x_domain=[i for i in range(len(x))]
	plt.scatter(x_domain, y1, color='red')
	plt.scatter(x_domain, y2, color='blue')
	plt.legend(('west side', 'east side'), loc='best')
	plt.xlabel('Hour of Day')
	plt.ylabel('Amount of Bikes')
	plt.show()




if __name__ == '__main__':
	#setting spark_home
	
	findspark.init(spark_home)
	conf=SparkConf().setMaster('local').setAppName('Fremont Bridge Bike Analysis')
	sc=SparkContext(conf=conf)
	main(sc)
