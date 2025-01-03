#from sensor_methods import Sensor
from datetime import datetime
import pandas as pd
import numpy as np
import sys, os, glob, time
import matplotlib.pyplot as plt

class Sensor:
    def __init__(self):
        print("sensor spoofed")

    def measure(self):
        return {'particles 03um': 2,
                'particles 05um': 3,
                'particles 10um': 4,
                'particles 50um': 5,
                'particles 100um':6}

if __name__ == "__main__":
    # instantiate sensor obj
    sensor = Sensor()
    print("here")

    # create log file
    starttime_time = datetime.now()
    print(starttime_time, ">> ", starttime_time.minute)
    filename = f"logFile-{starttime_time.year}{starttime_time.month}{starttime_time.day}-" \
               f"{str(starttime_time.hour).zfill(2)}{str(starttime_time.minute).zfill(2)}"
    print(filename)

    # setup logging and write file to disk
    df_data = pd.DataFrame()
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "output")

    iters = 0
    while iters < 5:
        # read sensor data
        reading = sensor.measure()
        df_reading = pd.DataFrame.from_dict(reading, orient='index').T
        print(df_reading)

        # add data to log file
        files = glob.glob(os.path.join(output_path, "*"))
        print(">>>", files)
        if any(filename+".csv" in file for file in files):
            logfile = pd.read_csv(os.path.join(output_path, filename+".csv"))
            logfile = pd.concat([logfile, df_reading], ignore_index=True)
            logfile.to_csv(os.path.join(output_path, filename+".csv"), index=False)
        else:
            _filename = filename+".csv"
            print("writing logfile to disk: ", _filename)
            df_reading.to_csv(os.path.join(output_path, _filename), index=False)
            logfile = df_reading
        iters += 1
        time.sleep(1)

    print(logfile)
    # visualize
    fig = plt.figure(figsize=(16,8))
    ax = fig.add_subplot()

    for col in logfile.columns:
        if "standard" in col:
            pass
            #ax.plot(logfile[col], label=col)
    outpath = os.path.join(output_path, f"test_vis_{starttime_time.hour}{starttime_time.minute}.png")
    print(f"saving image to: ", outpath)
    #plt.savefig(outpath)