from sqlalchemy import create_engine, desc, func
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Bus_Stops

engine = create_engine('sqlite:///busstops2012.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

# Counts stops and orders descending
most_stops = session.query(func.count(Bus_Stops.id).label('count'), \
							Bus_Stops.routes).filter(Bus_Stops.routes != "")\
							.group_by(Bus_Stops.routes)\
							.order_by(func.count(Bus_Stops.id).desc()).all()
stops = []
for stop in most_stops:
	print stop.count, stop.routes
	stops.append([stop.count, stop.routes])
print ""

most_routes = session.query(func.count(Bus_Stops.routes).label('count'), \
							Bus_Stops.stop_id).filter(Bus_Stops.routes != "")\
							.group_by(Bus_Stops.stop_id)\
							.order_by(func.count(Bus_Stops.routes)\
							.desc()).all()
routes = []
for route in most_routes:
	routes.append([route.count, route.stop_id])

most_boardings = session.query(Bus_Stops.routes, Bus_Stops.stop_id, \
								Bus_Stops.on_street, Bus_Stops.cross_street, \
								func.max(Bus_Stops.boardings).label('max_boardings'))\
								.filter(Bus_Stops.routes != "")\
								.group_by(Bus_Stops.routes)\
								.order_by(Bus_Stops.routes.desc()).all()
boardings = []
for boarding in most_boardings:
	print boarding.routes, boarding.stop_id, boarding.on_street, \
		boarding.cross_street, boarding.max_boardings
	boardings.append([Bus_Stops.routes, Bus_Stops.stop_id, Bus_Stops.on_street, \
						Bus_Stops.cross_street, Bus_Stops.boardings])
