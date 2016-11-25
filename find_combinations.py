# -*- coding: utf-8 -*-
"""
Created on Fri Nov 25 14:13:49 2016

@author: Oliver
"""
#from itertools import product
import sys
import pandas as pd
import numpy as np

#flights = pd.read_csv("flights.csv")
flights = pd.read_csv(sys.stdin)

flights.departure = pd.to_datetime(flights.departure, errors = 'coerce')
flights.arrival = pd.to_datetime(flights.arrival,  errors = 'coerce')

#print(flights.dtypes)

def find_trips_from(source, bags = 0):
    source_flights = flights[flights.source == source]
    trips = []    
    for first_flight in source_flights.itertuples():
        compatible_transfer = (flights.departure - first_flight[4] <= np.timedelta64(4,'h')) & (flights.departure - first_flight[4] >= np.timedelta64(1,'h'))
        compatible_bags = flights.bags_allowed >= bags
        compatible_airport = flights.source == first_flight[2]
        compatible = compatible_airport & compatible_transfer & compatible_bags 
        #print(compatible)
        if flights[compatible].empty:
            continue
        for next_flight in flights[compatible].itertuples():
            trip_price = first_flight[6] + first_flight[8]*bags 
            trip_path = [first_flight[1], first_flight[2]]
            (trip_paths, trip_prices) = find_next_path(next_flight, bags, [], [])
            if len(trip_prices) == 0:
                trips += [[str(first_flight[3].day)+"."+str(first_flight[3].month)+"."+str(first_flight[3].year)+" "+str(first_flight[3].hour)+":"+str(first_flight[3].minute),trip_path, bags, trip_price]]
            else:
                for i in range(len(trip_prices)):
                    trip_price = trip_price + trip_prices[i]
                    trip_path = trip_path + trip_paths[i]
                    trips += [[first_flight[3],trip_path, bags, trip_price]]
    return trips
            
def find_next_path(source_flight, bags, paths, prices):
    compatible_transfer = (flights.departure - source_flight[4] <= np.timedelta64(4,'h')) & (flights.departure - source_flight[4] >= np.timedelta64(1,'h'))
    compatible_bags = flights.bags_allowed >= bags
    compatible_airport = flights.source == source_flight[2]
    compatible = compatible_airport & compatible_transfer & compatible_bags
    if flights[compatible].empty:
        return (paths, prices)
    for next_flight in flights[compatible].itertuples():
        (next_paths, next_prices) = find_next_path(next_flight, bags, paths, prices)
        for i in range(len(next_prices)):
            next_prices[i] = next_flight[6] + next_flight[8]*bags + next_prices[i]
            next_paths[i] = [next_flight[2]] + next_paths[i]
    return (next_paths, next_prices) 
    
                
if __name__ == "__main__":
    
    sources = pd.unique(flights.source)
    destinations = pd.unique(flights.destination)
    
#    all_combinations = product(sources, destinations)
        
    
    for source in sources:
        for bags in range(3):
            print(pd.DataFrame(find_trips_from(source, bags)))
            
            
        
        
    