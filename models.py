class LocationMeta(object):
    def __init__(self, title, desc, lon, lat, link):
        self.title = title
        self.desc = desc
        self.lon = lon
        self.lat = lat
        self.link = link

    def __str__(self):
        return f'Location name: {self.name}'