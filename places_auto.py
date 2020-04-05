from googlemaps import * 
import populartimes
place_id=["ChIJC4fvXa8EdkgRQX1Mjup8vOQ","ChIJFXqFpOYcdkgR-c7TYfZuGhM"]
paces=len(place_id)
for i in range(0,paces):
	place_details=populartimes.get_id("API Key",place_id[i])
	print(place_details)
