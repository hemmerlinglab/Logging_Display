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


        # set defaults
        if not 'format' in sensors[s]:
            sensors[s]['format'] = "3.2f"
        if not 'conversion' in sensors[s]:
            sensors[s]['conversion'] = "x"
        if not 'plot_scale' in sensors[s]:
            sensors[s]['plot_scale'] = "linear"
        if not 'plot_miny' in sensors[s]:
            sensors[s]['plot_miny'] = "0.0"
        if not 'plot_maxy' in sensors[s]:
            sensors[s]['plot_maxy'] = "100.0"


    return sensors

#read_config()
