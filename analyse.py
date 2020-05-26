from time import time

import CorrectionPlotter
from data_file import DataFile

start = time()

data = [[
    DataFile("data/scope_0.csv", 3, 4.8),
    DataFile("data/scope_1.csv", 3, 6.0),
    DataFile("data/scope_2.csv", 3, 8.2),
    DataFile("data/scope_3.csv", 3, 10.2),
    DataFile("data/scope_4.csv", 3, 12.3),
    DataFile("data/scope_5.csv", 3, 14.1),
    DataFile("data/scope_6.csv", 3, 16.3),
    DataFile("data/scope_7.csv", 3, 18.7),
    DataFile("data/scope_8.csv", 3, 20.0),
    DataFile("data/scope_9.csv", 3, 22.4),
    DataFile("data/scope_10.csv", 3, 24.1),
    DataFile("data/scope_11.csv", 3, 26.4),
], [
    DataFile("data/scope_12.csv", 3, 26.4),
    DataFile("data/scope_13.csv", 3, 26.4),
    DataFile("data/scope_14.csv", 3, 26.4),
    DataFile("data/scope_15.csv", 3, 26.4),
    DataFile("data/scope_16.csv", 3, 26.4),
    DataFile("data/scope_17.csv", 3, 26.4),
    DataFile("data/scope_18.csv", 3, 26.4),
    DataFile("data/scope_19.csv", 3, 26.4),
    DataFile("data/scope_20.csv", 3, 26.4),
    DataFile("data/scope_21.csv", 3, 26.4),
    DataFile("data/scope_22.csv", 3, 26.4),
    DataFile("data/scope_23.csv", 3, 26.4),
    DataFile("data/scope_24.csv", 3, 26.4),
    DataFile("data/scope_25.csv", 3, 26.4),
    DataFile("data/scope_26.csv", 3, 26.4),
    DataFile("data/scope_27.csv", 3, 26.4),
    DataFile("data/scope_28.csv", 3, 26.4),
    DataFile("data/scope_29.csv", 3, 26.4),
    DataFile("data/scope_30.csv", 3, 26.4),
    DataFile("data/scope_31.csv", 3, 26.4),
], [
    DataFile("data/scope_32.csv", 3.0, 25),
    DataFile("data/scope_33.csv", 3.2, 25),
    DataFile("data/scope_34.csv", 3.4, 25),
    DataFile("data/scope_35.csv", 3.6, 25),
    DataFile("data/scope_36.csv", 3.8, 25),
    DataFile("data/scope_37.csv", 4.0, 25),
    DataFile("data/scope_38.csv", 4.2, 25),
    DataFile("data/scope_39.csv", 4.4, 25),
    DataFile("data/scope_40.csv", 4.6, 25),
    DataFile("data/scope_41.csv", 4.8, 25),
    DataFile("data/scope_42.csv", 5.0, 25)
]]

for i, experiment in enumerate(data):
    out = DataFile.column_sep.join(DataFile.columns) + "\n"
    for measurement in experiment:
        out += measurement.summary() + "\n"
    with open("summary" + str(i), "w+") as f:
        f.write(out)

CorrectionPlotter.save("plot.png")
print("Done in {0:.2f} seconds".format(time() - start))
