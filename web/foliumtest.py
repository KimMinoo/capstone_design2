import folium
import math




# dep_lat = 37.28293695757347
# dep_lon = 127.0434230405271
# des_lat = 37.28312042096528
# des_lon = 127.04739397575078

dep_lat, dep_lon = 37.27711051820087, 127.04079216093226
des_lat, des_lon = 37.27559414340661, 127.04224810694416

def makeMap(dep_lat, dep_lon, des_lat, des_lon):

    euclid_dist = math.sqrt((des_lat - dep_lat)**2 + (des_lon - dep_lon)**2)
    print(euclid_dist)


    map_osm = folium.Map(location=[(dep_lat + des_lat)/2, (dep_lon + des_lon)/2], zoom_start=17)
    folium.Marker([dep_lat, dep_lon], popup='원천관').add_to(map_osm)
    folium.Marker([des_lat, des_lon], popup='광교중앙역', icon=folium.Icon(color='red',icon='star')).add_to(map_osm)

    # Define coordinates for a line
    line_coordinates = [[37.27559414340661, 127.04224810694416],
    [37.27591319348564, 127.04244778152082],
    [37.275927256040845, 127.04245545688902],
    [37.27598576032505, 127.04248071240649],
    [37.27600806717677, 127.04241333410408],
    [37.27611122200804, 127.04210173919992],
    [37.27619472621016, 127.04183127820328],
    [37.27619961463696, 127.0418175819563],
    [37.27621930375612, 127.04176238780047],
    [37.27625301631317, 127.04165074559926],
    [37.27625700222419, 127.0416386272092],
    [37.27641034209876, 127.04117287770228],
    [37.27651638352273, 127.04084222829093],
    [37.27654541948208, 127.0407516776704],
    [37.27711051820087, 127.04079216093226]]
    # Create a PolyLine object with the line coordinates and add it to the map
    folium.PolyLine(locations=line_coordinates, color='blue').add_to(map_osm)




    map_osm.save('./templates/map.html') #파일이 저장될 위치
    print("saved")

makeMap(dep_lat, dep_lon, des_lat, des_lon)