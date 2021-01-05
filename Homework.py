#script for analysing betweenness centrality in the road network of the Canton of ZH
import numpy as np
import pandas as pd
import networkx as nx
import geopandas as gpd
import matplotlib.pyplot as plt
import descartes

print("Packages imported")
#general workspace settings for me
myworkspace="/Users/evaammann/Desktop/DataScienceNetworkAnalysis/zh"

#input data normal: the csv file for nodes and edges
nodesfilenormal=myworkspace+"/zh_nodes.shp"
edgesfilenormal=myworkspace+"/zh_roads.shp"
#input data flooded: the csv file for flooded nodes and edges
nodesfileflooded=myworkspace+"/zh_nodes_flooded.shp"
edgesfileflooded=myworkspace+"/zh_roads_flooded.shp"
floodmap=myworkspace+"/WB_HW_IK100_F_LV03dissolve.shp"

print("files imported")

#input data normal: the roads file
nodesnormalgdf = gpd.read_file(nodesfilenormal)
#nodesnormalgdf.columns
edgesnormalgdf = gpd.read_file(edgesfilenormal)
#edgesnormalgdf.columns
#input data flooded
nodesfloodedgdf = gpd.read_file(nodesfileflooded)
edgesfloodedgdf = gpd.read_file(edgesfileflooded)
floodmapgdf=gpd.read_file(floodmap)
#floodmapgdf.columns

print("files read")

#output data: the nodes betweenness centrality file in nomral situation
nodesnormalbetweennesscentralityfile=open(myworkspace+"/betweennesscentrality_normalsituation.csv","w")
#Header line
nodesnormalbetweennesscentralityfile.write("nodeid"+";"+"betweennesscentrality_normalsituation"+"\n")
#output data: the nodes betweenness centrality file in flooded situation
nodesfloodedbetweennesscentralityfile=open(myworkspace+"/betweennesscentrality_floodedsituation.csv","w")
#Header line
nodesfloodedbetweennesscentralityfile.write("nodeid"+";"+"betweennesscentrality_floodedsituation"+"\n")

#Output data: both values in one CSV
total_nodesbetweennesscentralityfile=open(myworkspace+"/betweennesscentrality_total.csv","w")
#Header line
total_nodesbetweennesscentralityfile.write("nodeid"+";"+"betweennesscentrality_normalsituation"+";"+"betweennesscentrality_floodedsituation"+"\n")

print("all CSV files created")

#create graph
G_normal = nx.Graph()
#loop through the road shapefile
for index, row in edgesnormalgdf.iterrows():
    length = row.SHAPE_Leng
    nodeid1=row.nodeid1
    nodeid2 = row.nodeid2
    xcoord1=nodesnormalgdf[nodesnormalgdf["nodeid"]==row.nodeid1].x
    ycoord1 = nodesnormalgdf[nodesnormalgdf["nodeid"] == row.nodeid1].y
    G_normal.add_node(row.nodeid1, pos=(xcoord1, ycoord1))
    xcoord2=nodesnormalgdf[nodesnormalgdf["nodeid"]==row.nodeid2].x
    ycoord2 = nodesnormalgdf[nodesnormalgdf["nodeid"] == row.nodeid2].y
    G_normal.add_node(row.nodeid2, pos=(xcoord2, ycoord2))
    G_normal.add_edge(row.nodeid1, row.nodeid2, weight=length)
print("network graph for normal situation created ...")


#plot the geodata
nodesfloodedgdf.plot()
edgesfloodedgdf.plot()
floodmapgdf.plot()

#create lists of flooded nodes and flooded edges (will not be part of the created graph)
listoffloodednodes=nodesfloodedgdf["nodeid"].unique().tolist()
listoffloodededges=edgesfloodedgdf["ID_Road"].unique().tolist()
print(str(len(listoffloodednodes))+" nodes are flooded")
print(str(len(listoffloodededges))+" road segments are flooded")


#create graph
G_flooded = nx.Graph()
nodesidlist=[]
edgesidlist=[]
#loop through the road shapefile
counter=0
for index, row in edgesnormalgdf.iterrows():
    if row.ID_Road not in listoffloodededges:
        #print(counter)
        length = row.SHAPE_Leng
        nodeid1=row.nodeid1
        nodeid2 = row.nodeid2
        if row.nodeid1 not in listoffloodednodes:
            xcoord=nodesnormalgdf[nodesnormalgdf["nodeid"]==row.nodeid1].x
            ycoord = nodesnormalgdf[nodesnormalgdf["nodeid"] == row.nodeid1].y
            if row.nodeid1 not in G_flooded:
                G_flooded.add_node(row.nodeid1, pos=(xcoord, ycoord))
                nodesidlist.append(row.nodeid1)
        if row.nodeid2 not in listoffloodednodes:
            xcoord=nodesnormalgdf[nodesnormalgdf["nodeid"]==row.nodeid2].x
            ycoord = nodesnormalgdf[nodesnormalgdf["nodeid"] == row.nodeid2].y
            if row.nodeid2 not in G_flooded:
                G_flooded.add_node(row.nodeid2, pos=(xcoord, ycoord))
                nodesidlist.append(row.nodeid2)
        edgesidlist.append(row.ID_Road)
        if row.nodeid1 not in listoffloodednodes and row.nodeid2 not in listoffloodednodes:
            G_flooded.add_edge(row.nodeid1, row.nodeid2, weight=length)
        counter+=1
print("network graph of flooded situation created ...")




#calculate betweenness centrality for all nodes and write it to the output file
#Betweenness centrality of a node v is the sum of the fraction of all-pairs shortest paths that pass through v.
#parameter k is the number of the sample to safe time, k=1000 --> ca. 1% of the total network is taken as a sample
#if k=None, the full network will be considered. This needs some hours of computation
# The betweennesscentrality will be a dictionary

#Calculate normal and flooded betweennesscentrality and write it into the CSV file
normal_betweennesscentrality=nx.betweenness_centrality(G_normal, k=None, normalized=True, endpoints=True)
print("Betweennesscentrality for normal situation calculated")
#betweennesscentrality=nx.betweenness_centrality(G, k=None, normalized=True, endpoints=True)
flooded_betweennesscentrality=nx.betweenness_centrality(G_flooded, k=None, normalized=True, endpoints=True)
print("betweennesscentrality for flooded situation calculated")
for n in normal_betweennesscentrality:
    nodesnormalbetweennesscentralityfile.write(str(n) + ";" + str(normal_betweennesscentrality[n]) + "\n")
    if n in flooded_betweennesscentrality:
        nodesfloodedbetweennesscentralityfile.write(str(n) + ";" + str(flooded_betweennesscentrality[n]) + "\n")
        total_nodesbetweennesscentralityfile.write(str(n) + ";" + str(normal_betweennesscentrality[n]) + ";"+ str(flooded_betweennesscentrality[n]) + "\n")
    else:
        total_nodesbetweennesscentralityfile.write(str(n) + ";" + str(normal_betweennesscentrality[n]) + ";"+ "-9999" + "\n")
    print(n)
    # You cannot combine a number with a string. That's why we need to convert the number to a string
    # n will be the key to the dictionary, the bc will be the value

nodesnormalbetweennesscentralityfile.close()
nodesfloodedbetweennesscentralityfile.close()
total_nodesbetweennesscentralityfile.close()
print("normal betweenness centrality for nodes in ZH traffic network computed and exported to file ...")




