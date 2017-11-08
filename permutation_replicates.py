import numpy as np

def permutation_sample(data, data_1_len, random_state=np.random):
    """Generate a permutation sample from two data sets."""

    # Permute the concatenated array: permuted_data
    permuted_data = random_state.permutation(data)

    # Split the permuted array into two: perm_sample_1, perm_sample_2
    perm_sample_1 = permuted_data[:data_1_len]
    perm_sample_2 = permuted_data[data_1_len:]

    return perm_sample_1, perm_sample_2


def draw_perm_reps(data_1, data_2, func, size=1, random_state=np.random):
    """Generate multiple permutation replicates."""
    # Initialize array of replicates: perm_replicates
    perm_replicates = np.empty(size)
    
    #np.concatenate((data_1, data_2))

    # Concatenate the data sets: data
    data = np.concatenate((data_1, data_2))
    data_1_len = len(data_1)

    return [func(*permutation_sample(data, data_1_len, random_state)) for ii in range(size)]
    #for ii in range(size):
        # Generate permutation sample
        #perm_sample_1, perm_sample_2 = permutation_sample(data_1, data_2, random_state)
        # Compute the test statistic
        #perm_replicates[i] = func(perm_sample_1, perm_sample_2)
    #return perm_replicates

