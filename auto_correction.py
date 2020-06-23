import sys
import time

import numpy
from matplotlib import pyplot as plt
from numpy.polynomial import Polynomial as Poly

license_text = """
MIT License

Copyright (c) 2020 Julian Kauth

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

help_text = """
A program to fix the data from the Reinraumpraktikum Haynes Shockley experiment

Prerequistes:
 This program assumes some stuff about the folder structure and its input data:
 1. There needs to be a 'settings.txt' file in the same folder as this program. 
 2. The settings file needs to contains at least one line of the format 
    "<path to datafile>, <laser-probe distance>, <laser voltage>" the 
    <path to datafile> may be relative or absolute, 
    eg. C:Users\\....\\data\\scope_0.csv or .\\data\\scope_0.csv
    Different experiments are separated by an empty line.
    Lines starting with "#" are ignored and can be used as comments.
 3. The data file has to be in the format 
    <time> <trigger> <drift voltage> <minority voltage>. It is only read from 
    the third line onwards. The datafiles from the experiment should have this 
    format already.
    
Options:
 help     print this help text
 license  print the license (MIT)
 excel    output with semicolons as separators; replace . with , in numbers 
          to be 'german excel friendly' (DEFAULT)
 gnuplot  output with spaces as separators. Do not replace . with ,
 english  output with commas as separators. Do not replace . with ,

Example:
 python3 auto_correction.py gnuplot
 
This program requires numpy and matplotlib to be installed for python
This program is distributed under the MIT license
"""

input_separator = ","
column_separator = " "
columns = ["#filename", "distance", "laser_voltage", "drift_voltage", "time_resolution_of_measurement", "peak_time",
           "area", "time_FWHM"]

fig = plt.figure(figsize=(30, 18), dpi=200)
coordinate = 1
x_max = 9
y_max = 5


class Measurement:

    def __init__(self, _filename, _distance, _laser_voltage):
        self.filename = _filename
        self.distance = _distance
        self.laser_voltage = _laser_voltage
        self.time_input, self.trigger_input, self.drift_voltage_input, self.minority_voltage_input = read_file_contents(self.filename)
        self.time_step = get_time_step(self.time_input)  # calculates the average time step
        self.drift_voltage = get_drift_voltage(self.drift_voltage_input)  # determines the drift voltage
        self.corrected_minority_voltage = correct_minority_voltage(self.filename, self.minority_voltage_input)  # removes the slope from the minority voltage
        self.peak_value = get_peak_value(self.corrected_minority_voltage)
        self.peak_index = get_peak_index(self.corrected_minority_voltage, self.peak_value)
        self.peak_time = get_peak_time(self.time_input, self.peak_index)
        self.area = get_area(self.corrected_minority_voltage, self.time_step)  # find the area of the corrected minority voltage graph
        self.time_fwhm = get_time_fwhm(self.corrected_minority_voltage, self.peak_index, self.peak_value, self.time_step)  # find the FWHM of the peak

        # save corrected data
        write_to_file(self)

    def summary(self):
        """returns a single line of text containing all the important values that were determined."""
        re = "\""
        re += self.filename + "\"" + column_separator
        re += str(self.distance) + column_separator
        re += str(self.laser_voltage) + column_separator
        re += str(self.drift_voltage) + column_separator
        re += str(self.time_step) + column_separator
        re += str(self.peak_time) + column_separator
        re += str(self.area) + column_separator
        re += str(self.time_fwhm)
        return re


def read_file_contents(filename):
    """return the contents of filename"""
    try:
        with open(filename, "r") as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"The spezified file {filename} was not found. Make sure the path given"
              f"in settings.txt is correct. Use an absolute path if you are not sure")
    lines = lines[3:]  # exclude header and the first line because it is partly empty
    split_lines = [line.strip().split(",") for line in lines]
    time = []
    trigger = []
    drift_volt = []
    minor_volt = []
    for line in split_lines:
        time.append(float(line[0]))
        trigger.append(float(line[1]))
        drift_volt.append(float(line[2]))
        minor_volt.append(float(line[3]))
    return time, trigger, drift_volt, minor_volt


def get_time_step(time_array):
    """get the average time delta between two measurements"""
    return (time_array[-1] - time_array[0]) / len(time_array)


def get_drift_voltage(drift_voltage):
    """calculate the average drift voltage from the data dictionary"""
    return sum(drift_voltage) / len(drift_voltage) * 0.68  # 0.68 because reasons


def correct_minority_voltage(plot_name, minority_voltage):
    """correct for the slope of the voltage curve
    fit a line to the beginning and end of the minority voltage
    curve. then subtract the line from the curve to remove the slope.
    The special selection of the x values is, because we can't fit the peak,
    we can only fit the more or less linear parts of the input curve.
    """
    global coordinate
    xs = numpy.linspace(0, 239, 240)
    xs = numpy.concatenate((xs, numpy.linspace(310, 399, 90)))
    xs = numpy.concatenate((xs, numpy.linspace(1200, len(minority_voltage) - 1, len(minority_voltage) - 1200)))
    selected_minority_voltage = minority_voltage[0:240] + minority_voltage[310:400] + minority_voltage[1200:]

    corrected = []
    fit = Poly.fit(xs, selected_minority_voltage, 1)
    for i, min_v in enumerate(minority_voltage):
        corrected.append(min_v - fit(i))

    # make a plot for visual inspection of the fit quality
    full_xs = numpy.linspace(0, xs[-1], len(minority_voltage))
    plot = fig.add_subplot(y_max, x_max, coordinate)
    plt.title(plot_name)
    plt.plot(full_xs, fit(full_xs), label="fit")
    plt.plot(full_xs, minority_voltage, label="minority voltage")
    plt.plot(full_xs, corrected, label="corrected minority voltage")
    plt.plot(full_xs, numpy.zeros(len(full_xs)), label="zero reference")
    coordinate += 1

    return corrected


def get_peak_value(corrected_minority_voltage):
    return min(corrected_minority_voltage[350:])


def get_peak_index(corrected_minority_voltage, peak_value):
    return corrected_minority_voltage.index(peak_value)


def get_peak_time(time_input, peak_index):
    return time_input[peak_index]


def get_area(corrected_minority_voltage, time_step):
    """calculate the area under the curve
    ignoring the interference from pulsing the laser"""
    return sum(corrected_minority_voltage[400:]) * time_step


def get_time_fwhm(corrected_minority_voltage, peak_index, peak_value, time_step):
    """returns the full width - half maximum of the peak"""
    half_max = peak_value * 0.5

    # find left side
    left_index = peak_index
    while corrected_minority_voltage[left_index] < half_max:
        left_index -= 1

    # find right side
    right_index = peak_index
    while corrected_minority_voltage[right_index] < half_max:
        right_index += 1

    diff = right_index - left_index + 1  # plus 1 to fix the conservative approach from both sides
    return diff * time_step


def write_to_file(meas):
    """write all the data to a file for plotting etc."""
    header = column_separator.join(columns) + "\n"
    header += "#" + meas.summary() + "\n"
    header += "#" + column_separator.join(
        ["time", "trigger_signal", "drift_voltage", "minority_voltage", "corrected_minority_voltage"]) + "\n"
    out = ""

    # construct data to string
    for line in zip(meas.time_input, meas.trigger_input, meas.drift_voltage_input, meas.minority_voltage_input,
                    meas.corrected_minority_voltage):
        line = [str(x) for x in line]  # transform numbers to strings
        out += column_separator.join(line) + "\n"
    if excel_friend:
        out.replace(".", ",")

    # write to file
    ending = meas.filename.split(".")[-1]
    name = meas.filename + ".corrected." + ending  # data.csv -> data.csv.corrected.csv
    with open(name, "w+") as f:
        f.write(header + out)


def determine_figure_sizes(n, aspect=1.5):
    """set x_max and y_max to "nice" values
    such that x_max * y_max >= n with x_max and y_max being the lowest possible pair of numbers that fulfills
    this requirement and also differs minimally from the perfect aspect ratio given with the keyword argument
    'aspect'"""
    x = numpy.sqrt(n * aspect)
    y = numpy.sqrt(n / aspect)
    xl, xh = int(numpy.floor(x)), int(numpy.ceil(x))
    yl, yh = int(numpy.floor(y)), int(numpy.ceil(y))
    if xl * yh >= n and xh * yl >= n:
        diff1 = aspect - xl / yh
        diff2 = xh / yl - aspect
        return (xl, yh) if (diff1 < diff2) else (xh, yl)
    elif xl * yh >= n > xh * yl:
        return xl, yh
    elif xl * yh < n <= xh * yl:
        return xh, yl
    else:
        return xh, yh


if __name__ == '__main__':
    """load data specs from settings.txt and then perform data correction on all files specified there"""
    start = time.time()

    # read commandline arguments
    if "help" in sys.argv:
        print(help_text)
        sys.exit(0)
    if "license" in sys.argv:
        print(license_text)
        sys.exit(0)
    gnuplot_friend = "gnuplot" in sys.argv
    english_friend = "english" in sys.argv
    if english_friend:
        column_separator = ","
    excel_friend = "excel" in sys.argv or not (gnuplot_friend or english_friend)
    if excel_friend:
        column_separator = ";"

    # load from settings.txt
    with open("settings.txt", "r") as f:
        lines = f.readlines()
    lines = [line.strip() for line in lines if not line.startswith("#")]
    content = "\n".join(lines)
    experiments = content.split("\n\n")
    # determine the size of the plot. it needs to fit all graphs on a ~15:9 figure
    x_max, y_max = determine_figure_sizes(len([line for line in lines if line]))  # all lines with content on them

    # calculating for each measurement in each experiment
    for i, exp in enumerate(experiments):
        print(f"calculating for part {i + 1} of {len(experiments)}. Time is {time.time() - start:0.2f}s")
        summary = "#" + column_separator.join(columns) + "\n"
        for line in exp.split("\n"):
            if not line:
                continue
            filename, distance, laser_voltage = line.split(input_separator)
            filename = filename.strip()
            distance = float(distance.strip().replace(",", "."))
            laser_voltage = float(laser_voltage.strip().replace(",", "."))

            measurement = Measurement(filename, distance, laser_voltage)
            summary += measurement.summary() + "\n"
        if excel_friend:
            summary = summary.replace(".", ",")
        with open(f"summary{i}.txt", "w+") as f:
            f.write(summary)
    print("saving picture")
    plt.savefig("plot.png")
    print(f"finished calculating. time taken: {time.time() - start:0.2f}s")
