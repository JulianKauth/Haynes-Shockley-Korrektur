import numpy
from numpy.polynomial import Polynomial as Poly

import CorrectionPlotter


class DataFile:
    column_sep = ","
    columns = ["#filename", "distance", "laser_voltage", "drift_voltage", "time_resolution_of_measurement", "peak_time",
         "area", "t_FWHM"]

    def __init__(self, filename, distance, laser_voltage):
        self.filename = filename
        self.distance = distance
        self.laser_voltage = laser_voltage
        self.dic = self._read_file_to_dictionary()  # copies all given data in nice format
        self.time_step = self.get_time_step()  # calculates the average time step
        self.drift_voltage = self._get_drift_voltage()  # determines the drift voltage
        self.correct_minority_voltage()  # removes the slope from the minority voltage
        self.peak_time = self.find_peak()  # finds the time of the peak of the minority voltage
        self.area = self.get_area()  # find the area of the corrected minority voltage graph
        self.t_fwhm = self.get_delta_t()  # find the FWHM of the peak

        # save corrected data
        self.write_to_file()

    def write_to_file(self):
        """write all the data to a file for plotting etc."""
        # construct header
        header = self.column_sep.join(self.columns) + "\n"
        header += "#" + self.summary() + "\n"
        header += "#" + self.column_sep.join(
            ["corrected_minority_voltage", "drift_voltage", "minority_voltage", "time", "trigger_signal"]) + "\n"
        out = ""

        # construct data to string
        data = [self.dic[key] for key in sorted(self.dic.keys())]
        for line in zip(*data):
            line = [str(x) for x in line]  # transform numbers to strings
            out += self.column_sep.join(line) + "\n"

        # write to file
        ending = self.filename.split(".")[-1]
        name = self.filename + ".corrected." + ending
        with open(name, "w+") as f:
            f.write(header + out)

    def summary(self):
        """returns a long string of all the constants we determined here"""
        re = "\""
        re += self.filename + "\"" + self.column_sep
        re += str(self.distance) + self.column_sep
        re += str(self.laser_voltage) + self.column_sep
        re += str(self.drift_voltage) + self.column_sep
        re += str(self.time_step) + self.column_sep
        re += str(self.peak_time) + self.column_sep
        re += str(self.area) + self.column_sep
        re += str(self.t_fwhm)
        return re

    def get_delta_t(self):
        """get the FWHM of the gaussian peak"""
        peak_index = self.find_peak_index()
        corr_minor_volt = self.dic["corr_minor_volt"]
        # half_max = max(corr_minor_volt) * 0.5  # inverted (peak goes up)
        half_max = min(corr_minor_volt) * 0.5  # not inverted (peak goes down)
        # find left side
        left_index = peak_index
        # while corr_minor_volt[left_index] > half_max:  # inverted
        while corr_minor_volt[left_index] < half_max:  # not inverted
            left_index -= 1
        # find right side
        right_index = peak_index
        # while corr_minor_volt[right_index] > half_max:  # inverted
        while corr_minor_volt[right_index] < half_max:  # not inverted
            right_index += 1

        diff = right_index - left_index + 1  # plus 1 to fix the conservative approach from both sides
        return diff * self.time_step

    def get_area(self):
        corr_volt = self.dic["corr_minor_volt"]
        corr_volt = corr_volt[400:]
        return sum(corr_volt) * self.time_step

    def find_peak(self):
        """find the peak and set the self.peak variable to the corresponding time"""
        return self.dic["time"][self.find_peak_index()]

    def find_peak_index(self):
        corrected_voltage = self.dic["corr_minor_volt"]
        # value = max(corrected_voltage[350:])  # sometimes the interference is bigger than the actual peak # inverted
        value = min(corrected_voltage[350:])  # not inverted (peak goes down)
        return corrected_voltage.index(value)

    def correct_minority_voltage(self):
        """correct for the slope of the voltage curve
        fit a line to the beginning and end of the minority voltage
        curve. then subtract the curve from the line to get an 
        upright peak and remove the slope.
        """
        min_volt = self.dic["minor_volt"]
        xs = numpy.linspace(0, 239, 240)
        xs = numpy.concatenate((xs, numpy.linspace(310, 399, 90)))
        xs = numpy.concatenate((xs, numpy.linspace(1200, len(min_volt) - 1, len(min_volt) - 1200)))
        selected_min_volt = min_volt[0:240] + min_volt[310:400] + min_volt[1200:]

        fit = Poly.fit(xs, selected_min_volt, 1)

        arr = []
        for i, min_v in enumerate(min_volt):
            arr.append(min_v - fit(i))
            # arr.append(fit(i) - min_v)  # inverted (peak goes up)
        self.dic["corr_minor_volt"] = arr

        # to make sure we don't correct wrong
        CorrectionPlotter.plot(xs, min_volt, arr, fit, self.filename)
        # a more detailed example of a correction. choose the number to show a nice plot
        #if "31" in self.filename:
        #    CorrectionPlotter.plot_single(self.time_step, xs, min_volt, arr, fit)

    def _get_drift_voltage(self):
        """calculate the average drift voltage from the data dictionary"""
        values = self.dic["drift_volt"]
        return sum(values) / len(values) * 0.68  # 0.68 because reasons

    def get_time_step(self):
        """get the average time delta between two measurements"""
        time_list = self.dic["time"]
        return time_list[-1] / len(time_list)
        # old way:
        # time = []
        # for i in range(1, len(time_list)):
        #   time.append(math.fabs(time_list[i - 1] - time_list[i]))
        # return sum(time) / len(time)

    def _read_file_to_dictionary(self):
        """return the contents of filename as a dictionary of lists
        """
        with open(self.filename, "r") as f:
            lines = f.readlines()
        lines = [line for line in lines if not line.startswith("#")]
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
        return {"time": time, "trigger": trigger, "drift_volt": drift_volt, "minor_volt": minor_volt}

