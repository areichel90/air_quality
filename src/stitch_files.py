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
        fileday = file.split("/")[-1].split("-")[1]
        filetime = file.split("/")[-1].split("-")[-1]
        filetime = filetime.replace(".csv", "")
        print(filetime)
        df_logfile = pd.read_csv(file)
        df_logfile["day"] = fileday[4:]
        #df_logfile["time"] = filetime
        df_logfile["hr"] = filetime[:2]
        df_logfile["min"] = filetime[2:]

        particle_cols = [col for col in df_logfile.columns if "standard" in col]
        df_particles = df_logfile[particle_cols]
        print(df_particles)
        #df_logfile["1.0 um PPM"] = df_particles.apply(lambda x: x[0] - x[1:].sum(), axis=1)
        #df_logfile["2.5 um PPM"] = df_particles.apply(lambda x: x[1] - x[2:].sum(), axis=1)
        #df_logfile["10. um PPM"] = df_particles.apply(lambda x: x[2] - x[3:].sum(), axis=1)

        df_data = pd.concat([df_logfile, df_data])

    df_data = df_data.sort_values(["hr", "min"])
    df_data = df_data.reset_index(drop=True)
    print(df_data.iloc[:,:3])
    particle_cols = [col for col in df_data.columns if "particle" not in col]
    print(df_data[particle_cols].describe())

    # visualize
    df_sub = df_data.iloc[:, df_data.columns.str.contains("standard")]
    print(">>>", df_sub)
    fig = plt.figure(figsize=(16, 8))

    for c,col in enumerate(df_data.columns):
        if "standard" in col:
            ax = fig.add_subplot(1,3,c+1)
            ax.plot(df_data[col], label=col)
            ax.set_ylabel("Particle Concentration [ug/m^3]")
            ax.legend()
            ax.set_ylim(bottom=0, top=df_sub.max().max())

    #plt.yscale('log')
    outpath = os.path.join(output_path, f"test_vis_{starttime_time.hour}{starttime_time.minute}.png")
    print(f"saving image to: ", outpath)
    plt.savefig(outpath)

    plt.show()