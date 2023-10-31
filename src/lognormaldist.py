import numpy as np

def scale_to_range(value, target_max=600):
    # Generate a large number of samples to approximate the true max of the distribution
    samples = np.random.lognormal(mean, sigma, 100000)
    actual_max = max(samples)
    return min(target_max, value/target_max * actual_max)

mean = 3
sigma = 1.5
lognorm_value = np.random.lognormal(mean, sigma)
scaled_value = scale_to_range(lognorm_value)

print(scaled_value)
