import geohash

class HashConstants(object):
    BIT_RADIUS_MAP = {
        52: 0.5971,
        50: 1.1943,
        48: 2.3889,
        46: 4.7774,
        44: 9.5547,
        42: 19.1095,
        40: 38.2189,
        38: 76.4378,
        36: 152.8757,
        34: 305.751,
        32: 611.5028,
        30: 1223.0056,
        28: 2446.0112,
        26: 4892.0224,
        24: 9784.0449,
        22: 19568.0898,
        20: 39136.1797,
    }


class LocationManager(object):
    def __init__(self, db):
        self.redis = db
        self.RADIUS_BIT_MAP = {v: k for k, v in HashConstants.BIT_RADIUS_MAP.iteritems()}

    def _encode(self, lat, lon):
        return geohash.encode_uint64(lat, lon)

    def _expand(self, ui64, depth):
        return geohash.expand_uint64(ui64, depth)

    def _decode(self, key):
        return geohash.decode_uint64(key)

    def add(self, lat, lon, msg):
        self.redis.zadd('msg', self._encode(lat, lon), msg)

    def rem(self, lat, lon):
        self.redis.zrem('msg', self._encode(lat, lon), msg)

    def _search(self, lat, lon, start=0, num=0, radius=9.5547):
        rbm = self.RADIUS_BIT_MAP
        depth = rbm[radius] if radius in rbm else rbm[min(rbm.keys(), key=lambda k: abs(k-radius))]
        gh_int64 = self._encode(lat, lon)
        gh_int64 = gh_int64 >> (64 - depth)
        G = self._get_neighbors(gh_int64, depth)
        r = []
        for lb in G:
            ub = lb + 1
            if ub and lb:
                m = lb << (64 - depth)
                n = ub << (64 - depth)
                r.extend(self.redis.zrangebyscore('msg', m, n, withscores=True))
        return r

    def _get_neighbors(self, _hash, depth):
        n = self._move(_hash, 0, 1, depth)
        e = self._move(_hash, 1, 0, depth)
        s = self._move(_hash, 0, -1, depth)
        w = self._move(_hash, -1, 0, depth)
        nw = self._move(_hash, -1, 1, depth)
        ne = self._move(_hash, 1, 1, depth)
        se = self._move(_hash, 1, -1, depth)
        sw = self._move(_hash, -1, -1, depth)
        return [n, e, s, w, ne, nw, se, sw, _hash]

    def _move(self, _hash, x, y, depth):
        if x and y:
            t = self._movex(_hash, x, depth)
            return self._movey(t, y, depth)
        elif x:
            return self._movex(_hash, x, depth)
        elif y:
            return self._movey(_hash, y, depth)

    def _movex(self, _hash, d, depth):
        if not d:
            return 0
        x = _hash & 0xaaaaaaaaaaaaaaaa
        y = _hash & 0x5555555555555555
        zz = 0x5555555555555555 >> (64 - depth)
        if d > 0:
            x += zz + 1
        else:
            x = x | zz
            x -= zz + 1
        x &= 0xaaaaaaaaaaaaaaaa >> (64 - depth)
        return x | y

    def _movey(self, _hash, d, depth):
        if not d:
            return 0
        x = _hash & 0xaaaaaaaaaaaaaaaa
        y = _hash & 0x5555555555555555
        zz = 0xaaaaaaaaaaaaaaaa >> (64 - depth)
        if d > 0:
            y += zz + 1
        else:
            y = y | zz
            y -= zz + 1
        y &= 0x5555555555555555 >> (64 - depth)
        return x | y


def test():
    from app.utilities.redis import TestRedis
    redis = TestRedis()
    m = LocationManager(redis)
    m.add(41.8781, -87.6298, 'Chicago')
    m.add(41.9436, -87.6584, 'Lakeview')
    m.add(41.7959, -87.9756, 'Westmont')

    print m._search(41.95, -87.65, 0, 3, radius=20000)
    print m._search(41.95, -87.65, 0, 3, radius=1000)
    print m._search(41.95, -87.65, 0, 3, radius=100)
    print m._search(41.886, -87.628, 0, 3, radius=10000)
    print m._search(41.794796, -87.974327, 0, 3, radius=1000)
    print m._search(41.9434, -87.657849, 0, 3, radius=300)
    print m._search(41.9413, -87.654270, 0, 3, radius=20)
