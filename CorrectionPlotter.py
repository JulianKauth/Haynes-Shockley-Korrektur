import numpy
from matplotlib import pyplot as plt

import const


def plot(xs, min_volt, corr_min_volt, fit, name):
    full_xs = numpy.linspace(0, xs[-1], len(min_volt))

    plot = const.fig.add_subplot(const.y_max, const.x_max, const.coordinate)
    plt.title(name)
    plt.plot(full_xs, fit(full_xs), label="fit")
    plt.plot(full_xs, min_volt, label="minority voltage")
    plt.plot(full_xs, corr_min_volt, label="corrected minority voltage")
    plt.plot(full_xs, numpy.zeros(len(full_xs)), label="zero reference")

    const.coordinate += 1


def plot_single(time_step, xs, min_volt, corr_min_volt, fit):
    fig = plt.figure(figsize=(10, 6), dpi=200)
    full_xs = numpy.linspace(0, xs[-1], len(min_volt))
    plt.plot(full_xs * time_step, fit(full_xs), label="Regressionsgerade")
    plt.plot(full_xs * time_step, min_volt, label="Minoritätsladungsträger")
    plt.plot(full_xs * time_step, corr_min_volt, label="Minoritätsladungsträger, korrigiert")
    plt.plot(full_xs * time_step, numpy.zeros(len(full_xs)), label="Null Referenz")
    plt.legend(loc="lower left")
    plt.xlabel("Zeit in Sekunden")
    plt.ylabel("Spannung in Volt")
    plt.savefig("Example.png")


def save(name):
    plt.savefig(name)
