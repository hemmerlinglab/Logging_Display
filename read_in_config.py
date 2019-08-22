from configparser import ConfigParser
import ast

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
            sensors[s]['format'] = "3.1f"
        if not 'conversion' in sensors[s]:
            sensors[s]['conversion'] = "x"
        if not 'plot_scale' in sensors[s]:
            sensors[s]['plot_scale'] = "linear"
        if not 'plot_min' in sensors[s]:
            sensors[s]['plot_min'] = sensors[s]['low']
        if not 'plot_max' in sensors[s]:
            sensors[s]['plot_max'] = sensors[s]['high']
        if not 'label' in sensors[s]:
            sensors[s]['label'] = s
        if not 'label_conversion' in sensors[s]:
            sensors[s]['label_conversion'] = sensors[s]['conversion']
        if not 'invalid_values' in sensors[s]:
            sensors[s]['invalid_values'] = []
        else:
            sensors[s]['invalid_values'] = ast.literal_eval(sensors[s]['invalid_values']) # necessary to convert a string [[1,2],[3,4]] to a list

    return sensors

#read_config()
