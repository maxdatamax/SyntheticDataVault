from scipy import stats

def GaussianCopula(row, metadata):

    # This function takes in a row of data. It also takes in a list of metadata.
    # The metadata should identify the feature distribution, its associated parameters,
    # and whether or not the feature is continuous.

    # the purpose of this function is to convert a dataset of varying distributions
    # into solely gaussian normal variables. An unbiased estimation of covariance
    # can then be found from this "gaussian copula".


    # 1) Take the column's CDf of the specific point
    # This is done using a for loop for each point in the row and
    # an if statement for each of the four distributions
    x = 0

    for point in row:

        feature = metadata[x]

        # this function doesnt currently account for categorical variables.
        # skips that until later
        if feature[2] == 1:
            print("This feature is categorical. Create a function for this later")
            continue


        # identifies the distribution needing to be used
        distribution = feature[0]
        param = feature[1]

        # finds the CDF of each distribution individually
        if distribution == 'beta':
            a = param[0]
            b = param[1]
            loc = param[2]
            scale = param[3]
            cdf = stats.beta.cdf(point, a, b, loc=loc, scale=scale)

        # Im having some serious problems with this distribution
        elif distribution == 'truncnorm':
            # im given four parameters but im not sure what they actually mean.
            cdf = stats.truncnorm.cdf(point)

        elif distribution == 'expon':
            loc = param[0]
            scale = param[1]
            cdf = stats.expon.cdf(point, loc=loc, scale=scale)


        elif distribution == 'uniform':
            loc = param[0]
            scale = param[1]
            cdf = stats.uniform.cdf(point, loc=loc, scale=scale)

        # I'm only dealing with the 4 distributions listed. If you want to use others,
        # go for it.
        else:
            print("Distribution not recognized.")


        # 2) Apply the inverse gaussian CDF of the point
        #
        # now that step one has been completed, the cdf of the individualized
        # distribution has to be fed back into a standard normal distribution
        # to create a gaussian copula

        row[x] = stats.norm.ppf(cdf)
        x = x + 1

    return row


def findCovariance():
    stopYellingAtMe = 1