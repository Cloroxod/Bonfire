

class DiscretizedSphere(object):
    MAX_LON = 180
    MAX_LAT = 60
    INV_RES = 25
    def __init__(self):
        self.indices = []
        self._construct()

    def _construct(self):
        lon = -float(self.MAX_LON)
        lat = -float(self.MAX_LAT)
        d_lat = 1./self.INV_RES
        d_lon = 1./self.INV_RES
        index = 0
        while lon < self.MAX_LON:
            while lat < self.MAX_LAT:
                self.indices.append((lon, lat))
                lat += d_lat
                index += 1
            lat = -self.MAX_LAT
            lon += d_lon

    def get_index(lon, lat):
        if abs(lat) > self.MAX_LAT:
            raise ValueError
        i = (lon + self.MAX_LON) * self.INV_RES
        j = (lat + self.MAX_LAT) * self.INV_RES
        return (i * self.MAX_LAT * self.NV_RES) + j