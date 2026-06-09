import math
import logging

class CoordinateCalculator:
    def __init__(self, config):
        self.config = config
        # Constants for earth radius
        self.R = 6371000 # Meters

    def calculate_object_gps(self, station_gps, azimuth, elevation, pixel_width, frame_width_pixels):
        """
        Estimates object GPS based on station position, camera angles, and observed size.
        """
        lat1 = math.radians(station_gps['lat'])
        lon1 = math.radians(station_gps['lon'])
        
        # Estimate distance
        # Assuming an average aircraft wingspan of 35 meters
        # and a FOV of about 60 degrees.
        fov_deg = 60 
        estimated_wingspan = 35 # meters
        
        # Distance calculation (rough estimate)
        # width_rad = (pixel_width / frame_width_pixels) * math.radians(fov_deg)
        # distance = estimated_wingspan / width_rad
        
        # simplified heuristic:
        if pixel_width > 0:
            distance = (estimated_wingspan * frame_width_pixels) / (pixel_width * 2 * math.tan(math.radians(fov_deg/2)))
        else:
            distance = 5000 # Default 5km
            
        # Limit distance to reasonable range (1km to 50km)
        distance = max(1000, min(distance, 50000))
        
        # Calculate destination coordinates
        # d/R is the angular distance
        ad = distance / self.R
        az = math.radians(azimuth)
        
        lat2 = math.asin(math.sin(lat1) * math.cos(ad) + 
                         math.cos(lat1) * math.sin(ad) * math.cos(az))
        
        lon2 = lon1 + math.atan2(math.sin(az) * math.sin(ad) * math.cos(lat1),
                                 math.cos(ad) - math.sin(lat1) * math.sin(lat2))
        
        # Estimate altitude
        # altitude = station_alt + distance * tan(elevation)
        alt_est = station_gps['alt'] + distance * math.tan(math.radians(elevation))
        
        return {
            'lat': math.degrees(lat2),
            'lon': math.degrees(lon2),
            'alt': alt_est,
            'distance_km': distance / 1000.0
        }

    def get_cardinal_direction(self, azimuth):
        dirs = ["North", "Northeast", "East", "Southeast", "South", "Southwest", "West", "Northwest"]
        idx = int((azimuth + 22.5) / 45) % 8
        return dirs[idx]
