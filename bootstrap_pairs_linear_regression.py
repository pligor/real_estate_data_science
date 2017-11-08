import numpy as np
from bootstrap_replicates import draw_bootstrap_replicates
from matplotlib import pyplot as plt

def draw_bs_pairs_linreg_OLD(x, y, size=1, random_state=np.random):
    """Perform pairs bootstrap for linear regression."""

    # Set up array of indices to sample from: inds
    inds = np.arange(len(x))

    # Initialize replicates: bs_slope_reps, bs_intercept_reps
    bs_slope_reps = np.empty(size)
    bs_intercept_reps = np.empty(size)

    # Generate replicates
    for i in range(size):
        bs_inds = random_state.choice(inds, size=len(inds))
        bs_x, bs_y = x[bs_inds], y[bs_inds]
        bs_slope_reps[i], bs_intercept_reps[i] = np.polyfit(bs_x, bs_y, deg=1)

    return bs_slope_reps, bs_intercept_reps


def draw_bs_pairs_linreg(x, y, size=1, random_state=np.random):
    """Perform pairs bootstrap for linear regression."""

    # Set up array of indices to sample from: inds
    inds = np.arange(len(x))

    # Initialize replicates: bs_slope_reps, bs_intercept_reps
    bs_slope_reps = np.empty(size)
    bs_intercept_reps = np.empty(size)

    arr = draw_bootstrap_replicates(lambda bs_x, bs_y : np.polyfit(bs_x, bs_y, deg=1),
                                    size, random_state, *[x, y])

    #bs_slope_reps = list(map(lambda xx: xx[0], arr))
    #bs_intercept_reps = list(map(lambda xx: xx[1], arr))
    bs_slope_reps, bs_intercept_reps = zip(*arr)

    return bs_slope_reps, bs_intercept_reps

def plot_bs_pairs_linreg(x_data, y_data, slopes, intercepts, xlabel, ylabel):
    xx = np.array([min(x_data), max(x_data)])

    # Plot the bootstrap lines
    assert len(slopes) == len(intercepts)
    for ii in range(len(slopes)):
        plt.plot(xx, slopes[ii]*xx + intercepts[ii],
                 linewidth=0.5, alpha=0.01, color='gray')

    plt.plot(xx, np.mean(slopes)*xx + np.mean(intercepts),
             linewidth=0.5, alpha=1., color='red')

    observeds = np.polyfit(x_data, y_data, deg=1)
    plt.plot(xx, observeds[0]*xx + observeds[1], linewidth=0.5, alpha=1., color='green')

    # Plot the data
    plt.plot(x_data, y_data, marker='.', linestyle='none', color='blue')

    # Label axes, set the margins, and show the plot
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.margins(0.02)

