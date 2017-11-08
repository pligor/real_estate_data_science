import numpy as np

def diff_in_vote_fraction(data_left, data_right):
    fraction_left = np.sum(data_left) / len(data_left)
    fraction_right = np.sum(data_right) / len(data_right)
    
    return np.abs(fraction_left - fraction_right)


def diff_of_means(data_1, data_2):
    """Difference in means of two arrays."""

    # The difference of means of data_1, data_2: diff
    diff = np.mean(data_1) - np.mean(data_2)

    return diff

def diff_of_stds(data_1, data_2):
    """Difference in means of two arrays."""

    # The difference of means of data_1, data_2: diff
    return np.std(data_1) - np.std (data_2)

