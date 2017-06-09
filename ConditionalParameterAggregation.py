from scipy import stats
import random
import numpy as np
import pandas as pd
import CleanData

# Conditional Parameter Aggregation (CPA) is one of the most important parts
# of the entire SDV paper. It is what allows the user to synthesize an entire
# database instead of a single table. there are a couple steps that will be taken
# in this paper in accordance with the SDV paper. Keep in mind that the end result
# is to create a series of extended tables that include each original table's data
# and metrics from all the associated children tables

# 1) Start the extended table by saving all the data from the original table.
# 2) Iteratively go through each value in the original table's primary key
#   2a) Go iteratively through each child table
#       2ai) Find all primary key value instances in all children tables
#       2aj) Perform Gaussian Copula and find feature covariance
#       2ak) find alpha and beta values for distribution
#       2al) save all covariance and alpha beta values into the extended table

def MakeFakeData(Continuous):
    # I'm making fake data to debug this with. It's a temporary funcution

    if Continuous == 1:
        primaryKey = np.linspace(1,100, num=100)
        data1 = stats.norm.rvs(loc=10, scale=1, size=100)
        data2 = stats.norm.rvs(loc=20, scale=1, size=100)
        data3 = stats.norm.rvs(loc=5, scale=2, size=100)
        data4 = stats.norm.rvs(loc=100, scale=10, size=100)
        df = np.concatenate([primaryKey, data1, data2, data3, data4])
        df = df.reshape([5, 100])
        df = pd.DataFrame(df.T)
        df.columns = ['df_id', 'data1', 'data2', 'data3', 'data4']

        foreignKey = [random.sample(primaryKey.tolist(), 1) for _ in range(500)]
        foreignKey = np.array([item[0] for item in foreignKey])
        data1 = stats.norm.rvs(loc=60, scale=1.5, size=500)
        data2 = stats.norm.rvs(loc=30, scale=3, size=500)
        data3 = stats.norm.rvs(loc=5, scale=4, size=500)
        data4 = stats.norm.rvs(loc=100, scale=1, size=500)
        child1 = np.concatenate([foreignKey, data1, data2, data3, data4])
        child1 = child1.reshape([5, 500])
        child1 = pd.DataFrame(child1.T)
        child1.columns = ['df_id', 'data1', 'data2', 'data3', 'data4']

        foreignKey = [random.sample(primaryKey.tolist(), 1) for _ in range(500)]
        foreignKey = np.array([item[0] for item in foreignKey])
        data1 = stats.norm.rvs(loc=6, scale=5, size=500)
        data2 = stats.norm.rvs(loc=35, scale=3.5, size=500)
        data3 = stats.norm.rvs(loc=2, scale=.5, size=500)
        data4 = stats.norm.rvs(loc=10, scale=2, size=500)
        child2 = np.concatenate([foreignKey, data1, data2, data3, data4])
        child2 = child2.reshape([5, 500])
        child2 = pd.DataFrame(child2.T)
        child2.columns = ['df_id', 'data1', 'data2', 'data3', 'data4']
    else:

        primaryKey = np.linspace(1,100, num=100)
        data1 = [i[0] for i in [random.sample([1, 2, 3, 4, 5], 1) for _ in range(100)]]
        data2 = [i[0] for i in [random.sample([1, 2, 3, 4, 5], 1) for _ in range(100)]]
        data3 = [i[0] for i in [random.sample([1, 2, 3, 4, 5], 1) for _ in range(100)]]
        data4 = [i[0] for i in [random.sample([1, 2, 3, 4, 5], 1) for _ in range(100)]]
        df = np.concatenate([primaryKey, data1, data2, data3, data4])
        df = df.reshape([5, 100])
        df = pd.DataFrame(df.T)
        df.columns = ['df_id', 'data1', 'data2', 'data3', 'data4']

        foreignKey = [random.sample(primaryKey.tolist(), 1) for _ in range(500)]
        foreignKey = np.array([item[0] for item in foreignKey])
        data1 = [i[0] for i in [random.sample([1, 2, 3, 4, 5], 1) for _ in range(500)]]
        data2 = [i[0] for i in [random.sample([1, 2, 3, 4, 5], 1) for _ in range(500)]]
        data3 = [i[0] for i in [random.sample([1, 2, 3, 4, 5], 1) for _ in range(500)]]
        data4 = [i[0] for i in [random.sample([1, 2, 3, 4, 5], 1) for _ in range(500)]]
        child1 = np.concatenate([foreignKey, data1, data2, data3, data4])
        child1 = child1.reshape([5, 500])
        child1 = pd.DataFrame(child1.T)
        child1.columns = ['df_id', 'data1', 'data2', 'data3', 'data4']

        foreignKey = [random.sample(primaryKey.tolist(), 1) for _ in range(500)]
        foreignKey = np.array([item[0] for item in foreignKey])
        data1 = [i[0] for i in [random.sample([10, 20, 30, 40, 50], 1) for _ in range(500)]]
        data2 = [i[0] for i in [random.sample([10, 20, 30, 40, 50], 1) for _ in range(500)]]
        data3 = [i[0] for i in [random.sample([10, 20, 30, 40, 50], 1) for _ in range(500)]]
        data4 = [i[0] for i in [random.sample([10, 20, 30, 40, 50], 1) for _ in range(500)]]
        child2 = np.concatenate([foreignKey, data1, data2, data3, data4])
        child2 = child2.reshape([5, 500])
        child2 = pd.DataFrame(child2.T)
        child2.columns = ['df_id', 'data1', 'data2', 'data3', 'data4']

    return df, child1, child2



def ConditionalParameterAggregaation(df, children, cur):

    # df is the information from the original table. This includes missing value indices
    # and has all datetime values converted to EPOCH
    #
    # children is a list of all child tables
    #
    # cur is a database cursor object that will be used to pull data in the future

    # makes fake data so I dont have to clean just yet
    df, child1, child2 = MakeFakeData(0)
    children = ['child1', 'child2']


    # now that we have a parent table and two child tables all containing continuous data,
    # I can work on the CPA algorithm
    x = 0
    extendedTable = [0]*len(children)
    for child in children:

        child = eval(child)

        # saves all data as categorical or not. ignores the primary key
        logicalCategorical = CleanData.IdentifyCategorical(child)
        logicalCategorical = logicalCategorical[1:]

        # find all possible options for categorical variables and saves them
        uniqueCategories = [0] * (len(child.columns))
        for y in range(1,len(child.columns)):
            if logicalCategorical[y-1]:
                uniqueCategories[y] = child[child.columns[y]].unique().tolist()
        uniqueCategories = uniqueCategories[1:]

        # iterate over all IDs in the primary key
        y = 0
        extendedTable[x] = [0]*len(df)
        for ID in df[df.columns[0]]:

            # pulls all data in the child table corresponding to the specific ID
            data = pd.DataFrame(child[child[df.columns[0]] == ID])

            # iterates over every column in the dataset
            z = 0
            extendedTable[x][y] = [0]*len(child.columns)
            for column in data.columns[1:]:

                # if the column is continuous
                if logicalCategorical[z] == 0:
                    # fit the data to a beta distribution and append it to the extended table
                    if len(data) == 0:
                        extendedTable[x][y][z] = tuple( [None]*4 )
                        continue
                    else:
                        extendedTable[x][y][z] = stats.beta.fit(data[column])

                else:

                    # initial dataframe to make sure that numbers aren't left out
                    d1 = pd.DataFrame([0] * len(uniqueCategories[z])).T
                    d1.columns = uniqueCategories[z]
                    # finds the percentage of each variable in the column of the temporary
                    # dataset. then saves that
                    if len(data) == 0:
                        extendedTable[x][y][z] = tuple( [None]*(len(uniqueCategories[z])) )
                    else:
                        count = data[column].value_counts()
                        count = (count + d1) / sum(count)
                        count[count.isnull()] = 0
                        extendedTable[x][y][z] = tuple(map(tuple, count.as_matrix()))[0]

                # move onto next column
                z = z+1

            # move onto next ID
            y = y+1

        # save data and move on to next table
        x = x+1


    # reshapes the table
    for x in range(len(extendedTable)):
        #colnames = ['alpha_%s'% children[x], 'beta_%s'% children[x],
        #            'loc_%s' % children[x], 'scale_%s'% children[x]]
        df = pd.concat([df, pd.DataFrame(extendedTable[x])], axis=1)



    return extendedTable

ConditionalParameterAggregaation(1,1,1)