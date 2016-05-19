The file "run.sh" is the shell script that should be run that runs the complete functionality of the application.

The file "clean_csv.py" is the first file that runs and takes the original data file (a CSV file) and a column with multiple entries (denoted as "cutby" in the file) that must be separated into different rows based off of commas. Additionally, the file adds another column that provides an additional entry for the final column (latitude and longitude coordinates) to be separated. The script then takes away the parantheses and separates the final column by commas. 

The file "database_setup.py" creates an SQLite database and imports contents of the CSV file using mainly numpy and SQLAlchemy. Please note that the database will only be setup and contents will be imported if the script is run directly, and not merely if the module is imported.

The file "visualize_queries.py" creates three queries that measure: 1) Bus routes by number of stops (i.e., which bus routes are the longest?) 2) Bus stops that appear on the most bus routes 3) Bus stops with the most boardings by bus route (i.e., I would try to avoid) 4) Bus stops with the least boardings by bus route (i.e., I would get on at these places). The first two queries are printed to the console, and the final two queries are printed to a map, with a pin point for each data point.

The file was created by Lauren Friedmann at lauren.fr@gmail.com in May, 2016 using Python 2.7.6, VirtualBox 5.0.20, and Vagrant 1.8.1.