import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os, glob

if __name__ == "__main__":
    # find files
    starttime_time = datetime.now()
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "output")
    files = glob.glob(os.path.join(output_path,"*.csv"))

    # combine files
    df_data = pd.DataFrame()
    for file in files:
        print(file)
        filetime = file.split("/")[-1].split("-")[-1]
        filetime = filetime.replace(".csv", "")
        print(filetime)
        df_logfile = pd.read_csv(file)
        df_logfile["time"] = filetime
        #df_logfile["hour"] = filetime.split("_")[-1]
        df_data = pd.concat([df_logfile, df_data])

    df_data = df_data.sort_values("time")
    df_data = df_data.reset_index(drop=True)
    print(df_data)
    particle_cols = [col for col in df_data.columns if "particle" in col]
    print(df_data[particle_cols].describe())

    # visualize
    fig = plt.figure(figsize=(16, 8))
    ax = fig.add_subplot()

    for col in df_data.columns:
        if "particle" in col:
            ax.plot(df_data[col], label=col)

    ax.set_ylabel("Particle Concentration [ug/m^3]")
    plt.legend()
    plt.yscale('log')
    outpath = os.path.join(output_path, f"test_vis_{starttime_time.hour}{starttime_time.minute}.png")
    print(f"saving image to: ", outpath)
    plt.savefig(outpath)