from scipy.interpolate import interp1d
from scipy.optimize import minimize
import numpy as np

from neutron_trap_creation_models import annealing_sim, annealing_sim_beta
from annealing_effects import temperatures, trap_2, T_list, atom_density_W


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


def error(p, norms=None):
    '''
    Compute average absolute error between numerical model results and
    reference
    '''
    print('-' * 40)
    global j
    j += 1
    print('i = ' + str(j))
    print('New simulation.')
    print('Point is:')
    print(p)

    # RUN NUMERICAL MODEL
    # scale parameters
    p_real = []
    for prm, norm in zip(p, norms):
        if norm == "linear":
            p_real.append(prm)
        elif norm == "log":
            p_real.append(10**prm)
        else:
            raise ValueError("Unknown {} norm".format(norm))

    # if any parameter is negative, return a very high error
    # this is a way to artificially constrain Nelder-Mead

    print('Real parameters are:')
    print(p_real)

    for e in p:
        if e < 0:
            return 1e30

    # run numerical model
    # annealed_trap_densities = annealing_sim(*p_real)
    annealed_trap_densities = annealing_sim_beta(*p_real)

    # COMPUTE DIFFERENCE WITH REFERENCE

    # retrieve temperature
    T = T_list

    # normalised trap densities
    annealed_trap_densities = np.array(annealed_trap_densities)/atom_density_W
    annealed_trap_densities = annealed_trap_densities.tolist()

    # interpolate simulated tds
    interp_model = interp1d(T, annealed_trap_densities, fill_value='extrapolate')
    # match to reference data
    trap_densities_modelled = interp_model(T_ref)

    # compute error
    err = mean_absolute_error(
        trap_densities_ref, trap_densities_modelled, T_ref,
        bounds=[[590, 610]], weight=[5])

    # print error
    print('Error: {:.2e}'.format(err))
    print('Absolute tolerance: {:.2e}'.format(fatol))
    print('Absolute tolerance: {:.2e}'.format(xatol))

    # add parameters and error to csv file
    # with open('simulations_results_scaled.csv', 'a') as f:
    #     writer = csv.writer(f, lineterminator='\n', delimiter=',')
    #     writer.writerow([*p, err])

    # with open('simulations_results.csv', 'a') as f:
    #     writer = csv.writer(f, lineterminator='\n', delimiter=',')
    #     writer.writerow([*p_real, err])

    # RETURN ERROR
    return err


# READ REFERENCE DATA

T_ref = np.array(temperatures)
trap_densities_ref = np.array(trap_2)

if __name__ == "__main__":
    # initialise counter j
    j = 0

    # build initial guess
    # A_0 = np.log10(2.5858e-03)
    A_0 = 6.1838e-03
    beta = 1
    E_A = 0.2792

    initial_guess = np.array([A_0, beta, E_A])

    norms = ["linear", "linear", "linear"]

    # tolerances
    fatol = 1e-05
    xatol = 1e-05

    # recursive minimise function, useful for restart
    def minimise_with_neldermead(ftol, xtol, initial_guess):
        global fatol
        global xatol
        fatol = ftol
        xatol = xtol
        res = minimize(
            error, initial_guess, args=(norms),
            method='Nelder-Mead',
            options={'disp': True, 'fatol': ftol, 'xatol': xtol})
        print('Solution is: ' + str(res.x))

    # start optimising!
    minimise_with_neldermead(fatol, xatol, initial_guess)
