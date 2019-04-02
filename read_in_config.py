from configparser import ConfigParser


def read_config(filename = 'config.ini'):
    
    config = ConfigParser()
    config.read('config.ini')

    sensor_ids = config.sections()
    # make dictionary out of config

    sensors = {}

    for s in sensor_ids:
        opts = config.options(s)
        
        sensors[s] = {}
        for o in opts:
            sensors[s][o] = config.get(s, o)

    return sensors

#read_config()
