from sqlalchemy import create_engine, desc, func
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Bus_Stops
import folium
import pandas as pd

engine = create_engine('sqlite:///busstops2012.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

# Longest bus routes by number of stops
most_stops = session.query(func.count(Bus_Stops.id).label('count'), \
							Bus_Stops.routes).filter(Bus_Stops.routes != "")\
							.group_by(Bus_Stops.routes)\
							.order_by(func.count(Bus_Stops.id).desc()).all()
stops = []
print "Longest Bus Routes by Number of Stops"
for stop in most_stops:
	print stop.routes, stop.count
	stops.append([stop.routes, stop.count])
print ""

# Bus stop that appears on the most bus routes
most_routes = session.query(func.count(Bus_Stops.routes).label('count'), \
							Bus_Stops.stop_id).filter(Bus_Stops.routes != "")\
							.group_by(Bus_Stops.stop_id)\
							.order_by(func.count(Bus_Stops.routes)\
							.desc()).all()
routes = []
print "Bus Stop that Appears on the Most Bus Routes"
for route in most_routes:
	print route.stop_id, route.count
	routes.append([route.count, route.stop_id])

# Bus stop with the most boardings by bus route (i.e., avoid)
most_boardings = session.query(Bus_Stops.routes, Bus_Stops.stop_id, \
								func.max(Bus_Stops.boardings).label('max_boardings'), \
								Bus_Stops.latitude, Bus_Stops.longitude)\
								.filter(Bus_Stops.routes != "")\
								.group_by(Bus_Stops.routes)\
								.order_by(Bus_Stops.routes.desc()).all()
boardings = []
for boarding in most_boardings:
	boardings.append([boarding.routes, boarding.stop_id, boarding.max_boardings, \
						boarding.latitude, boarding.longitude])

least_boardings = session.query(Bus_Stops.routes, Bus_Stops.stop_id, \
								func.min(Bus_Stops.boardings).label('min_boardings'), \
								Bus_Stops.latitude, Bus_Stops.longitude)\
								.filter(Bus_Stops.routes != "")\
								.group_by(Bus_Stops.routes)\
								.order_by(Bus_Stops.routes.desc()).all()
boardings_2 = []
for boarding in least_boardings:
	boardings_2.append([boarding.routes, boarding.stop_id, boarding.min_boardings, \
						boarding.latitude, boarding.longitude])

chicago_coordinates = (41.8781, -87.6298)
chi_map = folium.Map(location = chicago_coordinates, zoom_start = 12)
for each in boardings:
	folium.Marker([each[3],each[4]], popup = str(each[0])+ " has " + str(each[2]) \
					+ " boardings at this stop", icon=folium.Icon(color='red'))\
					.add_to(chi_map)
for each in boardings_2:
	folium.Marker([each[3],each[4]], popup = str(each[0])+ " has " + str(each[2]) \
					+ " boardings at this stop", icon=folium.Icon(color='green'))\
					.add_to(chi_map)
chi_map.save('busstops2012.html')
chi_map
