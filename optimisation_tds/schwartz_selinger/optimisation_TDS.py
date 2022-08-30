import csv
from scipy.interpolate import interp1d
from scipy.optimize import minimize
import numpy as np

from sim import festim_sim, implantation_time, resting_time, atom_density_W


def mean_absolute_error(y1, y2, x=None, bounds=None, weight=None):
    """computes the mean absolute error between y1 and y2

    Args:
        y1 (array_like): the first y data
        y2 (array_like): the second y data
        x (list, optional): the x data with same shape as y1, y2. Defaults to
            None.
        bounds (list, optional): x bounds for weighing the error based on
            weight. Defaults to None.
        weight (float or list of floats, optional): weight applied to the mean
            value for x values in bounds. Defaults to None.

    Returns:
        float: the mean absolute error between y1 and y2
    """
    # Check parameters
    if y1.shape != y2.shape:
        raise ValueError("y1 and y2 don't have the same shape")
    if x is not None:
        if x.shape != y1.shape:
            raise ValueError("x doesn't have the same shape as y1 and y2")

    # if (bounds, weight) != (None, None):
    #     if None in [bounds, weights]:
    #         raise ValueError("bounds was set without weight (or the opposite)")
    #     if x is None:
    #         raise ValueError("if bounds are set, x array is needed")

    if bounds is None:
        bounds = []
    if weight is None:
        weight = []

    # create weights
    coefficients = np.ones(y1.shape)

    if isinstance(weight, list):
        weights = weight
    else:
        weights = [weight]

    for bound, w in zip(bounds, weights):
        indexes = np.where((x > bound[0]) & (x <= bound[1]))
        coefficients[indexes] = w

    # compute difference
    diff = np.abs(y1 - y2)
    diff = diff * coefficients
    err = diff.mean()

    return err


def error(p, norms=None, restart_data=None):
    """
    Compute average absolute error between simulation and reference
    """
    print("-" * 40)
    global j
    j += 1
    print("i = " + str(j))
    print("New simulation.")
    print("Point is:")
    print(p)

    # RUN FESTIM SIMULATION

    # scale parameters
    p_real = []
    for prm, norm in zip(p, norms):
        if norm == "linear":
            p_real.append(prm)
        elif norm == "log":
            p_real.append(10**prm)
        else:
            raise ValueError("Unknown {} norm".format(norm))

    print("Real parameters are:")
    print(
        "[{:.4f}, {:.4e}, {:.4f}, {:.4e}]".format(
            p_real[0], p_real[1], p_real[2], p_real[3]
        )
    )

    # if any parameter is negative, return a very high error
    # this is a way to artificially constrain Nelder-Mead
    if any([e < 0 for e in p_real]):
        return 1e30

    if restart_data is not None:
        # try to find point in database
        index_sim = np.where(np.all(np.isclose(restart_data[:, :-1], p_real), axis=1))
        if len(index_sim[0]) > 0:
            err = restart_data[index_sim][0][-1]
            return err

    # run FESTIM sim
    try:
        res = festim_sim(*p_real, initial_number_cells=500)
    except ValueError:
        print("Re-running sim with 4000 cells")
        res = festim_sim(*p_real, initial_number_cells=4000)

    # COMPUTE DIFFERENCE WITH REFERENCE

    # find the indexes of the columns based on the column name
    index_temperature = res[0].index("Average T volume 1")
    index_flux_1 = res[0].index("Flux surface 1: solute")
    index_flux_2 = res[0].index("Flux surface 2: solute")
    res.pop(0)  # remove header
    res = np.array(res)
    times = res[:, 0]
    tds_indexes = np.where(times > implantation_time + resting_time)

    # retrieve temperature and desorption flux
    T = res[:, index_temperature][tds_indexes]
    flux = -(res[:, index_flux_1] + res[:, index_flux_2])[tds_indexes]

    # interpolate simulated tds
    interp_tds = interp1d(T, flux, fill_value="extrapolate")
    # match to reference data
    simulated_desorption = interp_tds(T_ref)

    # compute error

    # desorptions are normalised
    normalised_desorption_ref = desorption_ref / desorption_ref.max()
    normalised_desorption_sim = simulated_desorption / desorption_ref.max()

    err = mean_absolute_error(
        normalised_desorption_ref,
        normalised_desorption_sim,
        T_ref,
        # for 0 dpa
        # bounds=[[485, 545]],
        # weight=[5],
        # for 0.023 dpa
        # bounds=[[460, 530], [750, 800]],
        # weight=[5, 5],
    )

    # uncomment to compute MSE
    # diff = normalised_desorption_ref - normalised_desorption_sim
    # err = (diff**2).mean()

    # print error
    print("Error: {:.2e}".format(err))
    print("Absolute tolerance: {:.2e}".format(fatol))
    print("Absolute tolerance: {:.2e}".format(xatol))

    # add parameters and error to csv file
    # with open("simulations_results_scaled.csv", "a") as f:
    #     writer = csv.writer(f, lineterminator="\n", delimiter=",")
    #     writer.writerow([*p, err])

    # with open("simulations_results.csv", "a") as f:
    #     writer = csv.writer(f, lineterminator="\n", delimiter=",")
    #     writer.writerow([*p_real, err])

    # RETURN ERROR
    return err


# READ REFERENCE DATA

data_ref = np.genfromtxt("tds_data/0.023_dpa.csv", delimiter=",")
T_ref = data_ref[:, 0]
# data in D/s, needs to convert to D/(m2 s)
desorption_ref = data_ref[:, 1] / (12e-03 * 15e-03)


# LOAD EARLIER RESULTS FOR RESTART
data_earlier = None  # np.genfromtxt('simulations_results.csv', delimiter=',')

if __name__ == "__main__":
    # initialise counter j
    j = 0

    # build initial guess
    E_p1 = 0.9134
    n1 = np.log10(1.5e24)
    E_p2 = 1.45
    n2 = np.log10(1.7e23)

    initial_guess = np.array([E_p1, n1, E_p2, n2])

    norms = ["linear", "log", "linear", "log"]

    # tolerances
    fatol = 1e-03
    xatol = 1e-03

    # recursive minimise function, useful for restart
    def minimise_with_neldermead(ftol, xtol, initial_guess):
        global fatol
        global xatol
        fatol = ftol
        xatol = xtol
        res = minimize(
            error,
            initial_guess,
            args=(norms, data_earlier),
            method="Nelder-Mead",
            options={"disp": True, "fatol": ftol, "xatol": xtol},
        )
        print("Solution is: " + str(res.x))
        goon = True
        while goon:
            a = input("Do you wish to restart ?")
            if a == "no" or a == "No":
                goon = False
            elif a == "Yes" or a == "yes":
                new_fatol = fatol
                new_xatol = xatol
                b = input("Choose fatol :")
                if b != "":
                    new_fatol = float(b)
                c = input("Choose xatol :")
                if c != "":
                    new_xatol = float(c)
                # FIXME I doubt that this will work with more that 2 parameters
                initial_guess = np.array([res.x[0], res.x[1]])
                minimise_with_neldermead(new_fatol, new_xatol, initial_guess)

    # start optimising!
    minimise_with_neldermead(fatol, xatol, initial_guess)
