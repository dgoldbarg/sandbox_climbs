import psycopg2
import sys
import os
import getpass
from flask import Flask, render_template, request, Markup, current_app, Response
import argparse
import folium

app= Flask(__name__)

@app.route("/")
def home():
	# get a connection, if a connect cannot be made an exception will be raised here
	conn = psycopg2.connect(host='localhost', dbname='postgres', user='sbarron', password= "comegetsandy")
 
	# conn.cursor will return a cursor object, you can use this cursor to perform queries
	cursor = conn.cursor()
	cursor.execute("select oid, * from sandbox.boulders")

	boulder_map = folium.Map(location=[37.389041, -122.021810], 
						 tiles= "http://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}", 
						 attr='Tiles &copy; Esri &mdash; Source: Esri, DeLorme, NAVTEQ, USGS, Intermap, iPC, NRCAN, Esri Japan, METI, Esri China (Hong Kong), Esri (Thailand), TomTom, 2012',
						 zoom_start= 6,
						 width=1000,
						 height=500)

	# feats= {"type": "FeatureCollection",
	# 		"features": []}
	for record in cursor.fetchall():
		print record
		folium.Marker([record[4], record[5]], popup=record[2]).add_to(boulder_map)
		# feats['features'].append({"type": "Feature", "id": record[0], "climber": record[1], "climb": record[2], "grade": record[3], "properties": {"LATTITUDE": record[4], "LONGITUDE": record[5]}, "geometry": {"type": "Point", "coordinates": [ record[4], record[5]] }})
	# page_info= ""
	# for climb in feats['features']:
	# 	print climb['geometry']['coordinates']
	# 	print climb['id']
		# print "L.marker(" + str(climb['geometry']['coordinates']) + ").addTo(map)\n.bindPopup('" + str(climb['id']) + "').openPopup();"
		# page_info+= Markup("new L.marker(" + str(climb['geometry']['coordinates']) + ').addTo(map)\n.bindPopup("' + str(climb['climb']) + '").openPopup();')

	#Shows lat/long on click
	folium.LatLngPopup().add_to(boulder_map)
	#Adds point on click
	# folium.ClickForMarker(popup='Waypoint').add_to(boulder_map)
	# boulder_map.save('templates/boulder_map.html')

	

	
	return render_template("boulder_map.html")

 
if __name__ == "__main__":
	app.run()