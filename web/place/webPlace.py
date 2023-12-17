# from flask import Flask, render_template, request

# app = Flask(__name__)

# @app.route('/')
# def index():
#     return render_template('search.html')

# @app.route('/show_map', methods=['POST'])
# def show_map():
#     departure_lat = float(request.form['departure_lat'])
#     departure_long = float(request.form['departure_long'])
#     destination_lat = float(request.form['destination_lat'])
#     destination_long = float(request.form['destination_long'])
#     return render_template('map.html', departure_lat=departure_lat, departure_long=departure_long, destination_lat=destination_lat, destination_long=destination_long)

# if __name__ == '__main__':
#     app.run(debug=True)


from flask import Flask, render_template, request
from back import makeMap as makeMap
from searchPlace import search_coordinates as search_coordinates

app = Flask(__name__)

@app.route('/')
def main():
    return render_template('idxht.html')

@app.route('/map')
def embedded():
    return render_template('map.html')

@app.route('/search', methods=['POST'])
def search():

    departure = request.form['departure']
    destination = request.form['destination']


    departure_lat, departure_lon = search_coordinates(departure)
    destination_lat, destination_lon = search_coordinates(destination)

    print(f'Departure Latitude: {departure_lat}')
    print(f'Departure Longitude: {departure_lon}')
    print(f'Destination Latitude: {destination_lat}')
    print(f'Destination Longitude: {destination_lon}')

    makeMap(departure_lat, departure_lon, destination_lat, destination_lon)

    return render_template('idxht.html')

if __name__ == '__main__':
    app.run(debug=True)