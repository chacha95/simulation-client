class WorldSet:
    host: str 
    port: int
    longitude: float
    latitude: float 
    x_0: float = 592759.1186
    y_0: float = 4134482.1499

    @property
    @classmethod
    def host(cls):
        return cls.host
    
    @host.setter
    @classmethod
    def host(cls, host):
        cls.host = host
    
    @property
    @classmethod
    def port(cls):
        return cls.port
    
    @port.setter
    @classmethod
    def port(cls, port):
        cls.port = port
    
    @property
    @classmethod
    def longitude(cls):
        return cls.longitude
    
    @longitude.setter
    @classmethod
    def longitude(cls, longitude):
        cls.longitude = longitude
    
    @property
    @classmethod
    def latitude(cls):
        return cls.latitude
    
    @latitude.setter
    @classmethod
    def latitude(cls, latitude):
        cls.latitude = latitude