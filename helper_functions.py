import numpy as np

def conv_dt_to_epoch(dt):
    # dt is an array of datetimes

    #2018-05-02T23:10:02.000000000-0000
    dt2 = [datetime.datetime.strptime(m, '%Y-%m-%dT%H:%M:%S.000000000-0000') for m in dt]
    
    tarr = 1000.0 * np.array([mktime(m.timetuple()) + m.microsecond/1000.0 for m in dt2])

    return tarr


def trunc(s, digits = 1):
    return np.round(10**digits * s)/10**digits

