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


def error(p, scaling_factors=None, restart_data=None):
    '''
    Compute average absolute error between simulation and reference
    '''
    print('-' * 40)
    global j
    j += 1
    print('i = ' + str(j))
    print('New simulation.')
    print('Point is:')
    print(p)

    # if any parameter is negative, return a very high error
    # this is a way to artificially constrain Nelder-Mead
    for e in p:
        if e < 0:
            return 1e30

    # RUN FESTIM SIMULATION

    # scale parameters
    if scaling_factors is None:
        scaling_factors = np.ones(len(p))

    if len(scaling_factors) != len(p):
        raise ValueError("scaling_factors doesn't have the same length as p")
    p_real = [prm*factor for prm, factor in zip(p, scaling_factors)]

    if restart_data is not None:
        # try to find point in database
        index_sim = np.where(
            np.all(
                np.isclose(restart_data[:, :-1], p_real),
                axis=1
                )
            )
        if len(index_sim[0]) > 0:
            err = restart_data[index_sim][0][-1]
            return err

    # run FESTIM sim
    try:
        res = festim_sim(*p_real, initial_number_cells=1500)
    except ValueError:
        print("Re-running sim with 4000 cells")
        res = festim_sim(*p_real, initial_number_cells=4000)

    # COMPUTE DIFFERENCE WITH REFERENCE

    # find the indexes of the columns based on the column name
    index_temperature = res[0].index('Average T volume 1')
    index_flux_1 = res[0].index('Flux surface 1: solute')
    index_flux_2 = res[0].index('Flux surface 2: solute')
    res.pop(0)  # remove header
    res = np.array(res)
    times = res[:, 0]
    tds_indexes = np.where(times > implantation_time + resting_time)

    # retrieve temperature and desorption flux
    T = res[:, index_temperature][tds_indexes]
    flux = -(res[:, index_flux_1] + res[:, index_flux_2])[tds_indexes]

    # interpolate simulated tds
    interp_tds = interp1d(T, flux, fill_value='extrapolate')
    # match to reference data
    simulated_desorption = interp_tds(T_ref)

    # compute error

    # desorptions are normalised
    normalised_desorption_ref = desorption_ref/desorption_ref.max()
    normalised_desorption_sim = simulated_desorption/desorption_ref.max()

    err = mean_absolute_error(
        normalised_desorption_ref, normalised_desorption_sim, T_ref,
        bounds=[[550, 600], [770, 810]], weight=[5, 10]
    )
    # uncomment to compute MSE
    # diff = normalised_desorption_ref - normalised_desorption_sim
    # err = (diff**2).mean()

    # print error
    print('Error: {:.2e}'.format(err))
    print('Absolute tolerance: {:.2e}'.format(fatol))
    print('Absolute tolerance: {:.2e}'.format(xatol))

    # add parameters and error to csv file
    with open('simulations_results_scaled.csv', 'a') as f:
        writer = csv.writer(f, lineterminator='\n', delimiter=',')
        writer.writerow([*p, err])

    with open('simulations_results.csv', 'a') as f:
        writer = csv.writer(f, lineterminator='\n', delimiter=',')
        writer.writerow([*p_real, err])

    # RETURN ERROR
    return err


# READ REFERENCE DATA

data_to_use = 'single'
# data_to_use = 'double'
# data_to_use = 'triple'

data_ref = np.genfromtxt('Results/{}_damaged/{}_damaged.csv'.format(data_to_use,
                         data_to_use), delimiter=',')
T_ref = data_ref[:, 0]
desorption_ref = data_ref[:, 1]


# LOAD EARLIER RESULTS FOR RESTART
data_earlier = None  # np.genfromtxt('simulations_results.csv', delimiter=',')

if __name__ == "__main__":
    # initialise counter j
    j = 0

    # build initial guess
    # k_01 = 1
    E_p1 = 1
    n1 = 1
    n1_2 = 1
    # k_02 = 1
    E_p2 = 1
    n2 = 1
    n2_2 = 1

    initial_guess = np.array([E_p1, n1, n1_2, E_p2, n2, n2_2])

    scaling_factors = [
        1.23,
        1.31e+26,
        8.22e+25,
        1.61,
        4.72e+25,
        2.53e+25
    ]

    # tolerances
    fatol = 1e-02
    xatol = 1e-02

    # recursive minimise function, useful for restart
    def minimise_with_neldermead(ftol, xtol, initial_guess):
        global fatol
        global xatol
        fatol = ftol
        xatol = xtol
        res = minimize(
            error, initial_guess, args=(scaling_factors, data_earlier),
            method='Nelder-Mead',
            options={'disp': True, 'fatol': ftol, 'xatol': xtol})
        print('Solution is: ' + str(res.x))
        goon = True
        while goon:
            a = input('Do you wish to restart ?')
            if a == 'no' or a == 'No':
                goon = False
            elif a == 'Yes' or a == 'yes':
                new_fatol = fatol
                new_xatol = xatol
                b = input('Choose fatol :')
                if b != '':
                    new_fatol = float(b)
                c = input('Choose xatol :')
                if c != '':
                    new_xatol = float(c)
                # FIXME I doubt that this will work with more that 2 parameters
                initial_guess = np.array([res.x[0], res.x[1]])
                minimise_with_neldermead(new_fatol, new_xatol, initial_guess)

    # start optimising!
    minimise_with_neldermead(fatol, xatol, initial_guess)
