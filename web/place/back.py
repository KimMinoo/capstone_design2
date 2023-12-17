import folium
import math
import pandas as pd
#import json
import numpy as np

total_node = pd.read_csv("./total_node.csv")
total_link = pd.read_csv("./modified_link.csv")
print("loaded data")

# dep_lat, dep_lon = 37.29434662428948, 127.00356275215876
# des_lat, des_lon = 37.294687615679564, 127.0043062225033


def compose_coordinate(latitude, longitude):
    composed_coordinate = '['+ str(longitude)+ ','+ str(latitude)+ ']'
    return composed_coordinate


def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371.0  # Earth's radius in km
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c

    return distance

def get_Nearest_Node(latitude, longitude, total_node, length_filter = 0.001):
    min_distance = 1e9
    nearest_lat = 0
    nearest_lon = 0
    nearest_idx = 0
    
    filtered_df = total_node.loc[(total_node['위도'] > latitude - length_filter) & (total_node['위도'] < latitude + length_filter) & (total_node['경도'] > longitude - length_filter) & (total_node['경도'] < longitude + length_filter)]
    for index, row in filtered_df.iterrows():

        cur_node_lat = row['위도']
        cur_node_lon = row['경도']
        cur_distance = haversine_distance(latitude, longitude, cur_node_lat, cur_node_lon)

        if cur_distance < min_distance:
            min_distance = cur_distance
            nearest_lat = cur_node_lat
            nearest_lon = cur_node_lon
            nearest_idx = index

    #return filtered_df

    if nearest_idx == 0:
        print("nearestIDX is zero")
        nearest_idx, nearest_lat, nearest_lon = get_Nearest_Node(latitude, longitude, total_node, length_filter = 0.01)
    
    print("returning", nearest_idx)
    return nearest_idx, nearest_lat, nearest_lon

def make_areal_link(dep_lat, dep_lon, des_lat, des_lon, total_link):
    length_filter = 0.003
    area_N = max(dep_lat, des_lat) + length_filter
    area_S = min(dep_lat, des_lat) - length_filter
    area_E = max(dep_lon, des_lon) + length_filter
    area_W = min(dep_lon, des_lon) - length_filter

    areal_link = total_link.loc[(total_link['노드1위도'] < area_N)
                                & (total_link['노드2위도'] < area_N)
                                & (total_link['노드1위도'] > area_S) 
                                & (total_link['노드2위도'] > area_S)
                                & (total_link['노드1경도'] < area_E)
                                & (total_link['노드2경도'] < area_E)
                                & (total_link['노드1경도'] > area_W)
                                & (total_link['노드2경도'] > area_W)]
    print("areal_link shape:", areal_link.shape)
    
    return areal_link
    

def dijkstra(dep_lat, dep_lon, des_lat, des_lon, start_idx, end_idx, total_node, areal_link):
    num_rows = total_node.shape[0]
    dijkstra_df = {'col1': [np.inf] * num_rows, 'col2': [False] * num_rows, 'col3': [np.nan] * num_rows}
    dijkstra_df = pd.DataFrame(data=dijkstra_df)
    dijkstra_df.columns=['length', 'visited', 'route']






    dijkstra_df.loc[start_idx, "length"] = 0
    dijkstra_df.at[start_idx, "route"] = start_idx
    now = start_idx

    #num_visited = 0
    while(True):

        unvisited_dijkstra_df = dijkstra_df.loc[(dijkstra_df['visited']  == False) & (dijkstra_df['length']  != np.inf)]
        if unvisited_dijkstra_df.empty:
            print('unvisited empty')
            break

        unvisited_dijkstra_df.sort_values(by=['length'])
        now = unvisited_dijkstra_df.index[0]
        #num_visited += 1
        #print("visited", now, "total visit:", num_visited)
        now_length = dijkstra_df.loc[now, "length"]########################startidx 가 아니라 now 아닌가?????
        
        dijkstra_df.loc[now, "visited"] = True
        #dijkstra_df.loc[now, "route"] = [start_idx]

        now_connected_link = areal_link.loc[(areal_link['idx노드1']  == now)]
        for index, row in now_connected_link.iterrows():
            search_node_num = row['idx노드2']
            search_node_weight = row['weight']
            #print(now, ' is connected to ', search_node_num)

            if dijkstra_df.loc[search_node_num, "visited"] == True:
                continue
            
            if dijkstra_df.loc[search_node_num, "length"] > (now_length + search_node_weight):
                dijkstra_df.loc[search_node_num, "length"] = now_length + search_node_weight
                # templist = dijkstra_df.loc[now, "route"].copy()
                # templist.append(now)
                # print(templist)
                dijkstra_df.at[search_node_num, "route"] = now
                #print("modified length of ",search_node_num)


        now_connected_link = areal_link.loc[(areal_link['idx노드2']  == now)]
        for index, row in now_connected_link.iterrows():
            search_node_num = row['idx노드1']
            search_node_weight = row['weight']
            #print(now, ' is connected to ', search_node_num)

            if dijkstra_df.loc[search_node_num, "visited"] == True:
                continue
            
            if dijkstra_df.loc[search_node_num, "length"] > (now_length + search_node_weight):
                dijkstra_df.loc[search_node_num, "length"] = now_length + search_node_weight
                # templist = dijkstra_df.loc[now, "route"].copy()
                # templist.append(now)
                # print(templist)
                dijkstra_df.at[search_node_num, "route"] = now
                #print("modified length of ",search_node_num)


    route_list = [[des_lat,des_lon]]
    cur_idx = end_idx


    while(True):
        
        cur_lat = total_node.loc[cur_idx, "위도"]
        cur_lon = total_node.loc[cur_idx, "경도"]
        route_list.append([cur_lat, cur_lon])
        if cur_idx == start_idx:
            break
        
        cur_idx = dijkstra_df.loc[cur_idx, "route"]

    route_list.append([dep_lat, dep_lon])

    return route_list


def get_route(dep_lat, dep_lon, des_lat, des_lon):


    start_idx, start_lat, start_lon = get_Nearest_Node(dep_lat, dep_lon, total_node)
    end_idx, end_lat, end_lon = get_Nearest_Node(des_lat, des_lon, total_node)
    print(start_idx, end_idx)

    areal_link = make_areal_link(dep_lat, dep_lon, des_lat, des_lon, total_link)

    route_list = dijkstra(dep_lat, dep_lon, des_lat, des_lon, start_idx, end_idx, total_node, areal_link)

    return route_list




def makeMap(dep_lat, dep_lon, des_lat, des_lon):

    #euclid_dist = math.sqrt((des_lat - dep_lat)**2 + (des_lon - dep_lon)**2)
    #print(euclid_dist)
    
    dep_lat = float(dep_lat)
    dep_lon = float(dep_lon)
    des_lat = float(des_lat)
    des_lon = float(des_lon)

    safemap = folium.Map(location=[(dep_lat + des_lat)/2, (dep_lon + des_lon)/2], zoom_start=17)
    folium.Marker([dep_lat, dep_lon], popup='원천관').add_to(safemap)
    folium.Marker([des_lat, des_lon], popup='광교중앙역', icon=folium.Icon(color='red',icon='star')).add_to(safemap)


    line_coordinates = get_route(dep_lat, dep_lon, des_lat, des_lon)
   
    folium.PolyLine(locations=line_coordinates, color='blue').add_to(safemap)




    safemap.save('./templates/map.html') #파일이 저장될 위치
    print("saved")

#makeMap(dep_lat, dep_lon, des_lat, des_lon)


