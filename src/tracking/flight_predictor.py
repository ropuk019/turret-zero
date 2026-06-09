import time
import math

class FlightPredictor:
    def __init__(self):
        self.history = [] # List of (timestamp, lat, lon, alt)
        
    def add_datapoint(self, lat, lon, alt):
        self.history.append((time.time(), lat, lon, alt))
        # Keep only last 10 points
        if len(self.history) > 10:
            self.history.pop(0)

    def predict(self):
        if len(self.history) < 2:
            return None

        t1, lat1, lon1, alt1 = self.history[-2]
        t2, lat2, lon2, alt2 = self.history[-1]
        
        dt = t2 - t1
        if dt <= 0: return None
        
        # Simple linear projection
        v_lat = (lat2 - lat1) / dt
        v_lon = (lon2 - lon1) / dt
        v_alt = (alt2 - alt1) / dt
        
        # Calculate speed in knots (rough)
        # 1 degree lat ~ 111km
        dist_km = math.sqrt(((lat2-lat1)*111)**2 + ((lon2-lon1)*111*math.cos(math.radians(lat1)))**2)
        speed_mps = (dist_km * 1000) / dt
        speed_knots = speed_mps * 1.94384
        
        predictions = {}
        for seconds in [30, 60, 90, 120]:
            p_lat = lat2 + v_lat * seconds
            p_lon = lon2 + v_lon * seconds
            predictions[seconds] = (p_lat, p_lon)
            
        return {
            'speed_knots': speed_knots,
            'predictions': predictions,
            'heading': math.degrees(math.atan2(v_lon, v_lat)) % 360
        }

    def clear(self):
        self.history = []
