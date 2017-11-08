# -*- coding: UTF-8 -*-
from __future__ import division
import numpy as np
import pandas as pd
import sys
import math
import re
from scipy import stats


class ConfidenceInterval(object):
    """https://www.youtube.com/watch?v=bekNKJoxYbQ"""

    def getPercentageForConfidenceInterval(self,  # three things we can measure
                                           N_sample=36, sample_mean=112, sample_std=40,
                                           min_mean=100, max_mean=124  # we are asking for these boundaries
                                           ):
        assert min_mean < sample_mean < max_mean

        # N_total = 200e3 <-- we consider population to be very large

        # there is the population distribution that we do NOT know

        # the sample mean itself as a distribution (under the law of big numbers) will be Gaussian
        means_mean = sample_mean  # the mean of the mean is same as the sample mean
        # means_std = population_std / math.sqrt(N_sample) # but population std is unknown so..
        approx_population_std = sample_std
        # so..
        means_std = approx_population_std / math.sqrt(N_sample)

        left_distance = abs(min_mean - sample_mean)
        right_distance = abs(max_mean - sample_mean)

        # print left_distance, right_distance

        total_percentage = self.getPercentageOfSide(distance=left_distance, means_std=means_std) + \
                           self.getPercentageOfSide(distance=right_distance, means_std=means_std)

        return total_percentage

    @staticmethod
    def getPercentageOfSide(distance, means_std):
        # now we want to convert the distance of the mean from the boundaries to standard deviations
        how_many_stds = distance / means_std
        # print how_many_stds

        minus_inf_to_zero = 0.5  # stats.norm.cdf(0) = 0.5 # this is standard
        # this gives all the area from minus infinity to the std
        minus_inf_to_std = stats.norm.cdf(how_many_stds)
        return minus_inf_to_std - minus_inf_to_zero

    @staticmethod
    def getConfidenceInterval(percentage=0.928139, sample_mean=112, sample_std=40, N_sample=36):
        return stats.norm.interval(percentage, loc=sample_mean, scale=sample_std / math.sqrt(N_sample))


if __name__ == "__main__":
    N_sample = 36
    sample_mean = 112
    sample_std = 40

    cf = ConfidenceInterval()

    # if you know the end points
    min_mean = 100
    max_mean = 124
    # and you want to know the percentage
    percentage = cf.getPercentageForConfidenceInterval(N_sample=N_sample, sample_mean=sample_mean,
                                                       sample_std=sample_std, min_mean=min_mean, max_mean=max_mean)
    print percentage

    # if you know the percentage
    # but you want to get the end points
    bounds = cf.getConfidenceInterval(percentage=percentage, sample_mean=sample_mean,
                                      sample_std=sample_std, N_sample=N_sample)
    print bounds

    assert np.allclose(bounds, (min_mean, max_mean))
