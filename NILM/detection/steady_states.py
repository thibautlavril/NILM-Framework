from __future__ import print_function, division
import pandas as pd
import numpy as np
import sys


def steady_states(dataframe, state_threshold=15,
                  edge_threshold=70):
    """
    Finds steady states given a datafram of power
    
    Taken from nilmtk. Quote while using


    Parameters
    ----------

    dataframe: pd.DataFrame with DateTimeIndex
    min_n_samples(int): number of samples to consider constituting a
             steady state.
    state_threshold: maximum difference between highest and lowest
        value in steady state.
    edge_threshold: the level used to define significant
        appliances, transitions below this level will be ignored.
        See Hart 1985. p27.


    Returns
    -------

    """


# Tells whether we have both real and reactive power or only real power
    num_measurements = len(dataframe.columns)
    estimatedSteadyPower = np.array([0] * num_measurements)
    lastSteadyPower = np.array([0] * num_measurements)
    previousMeasurement = np.array([0] * num_measurements)

    # These flags store state of power

    instantaneousChange = False  # power changing this second
    ongoingChange = False  # power change in progress over multiple seconds

    index_transitions = []  # Indices to use in returned Dataframe
    index_steadystates = []
    transitions = []  # holds information on transitions
    steadyStates = []  # steadyStates to store in returned Dataframe
    N = 0  # N stores the number of samples in state
    time = dataframe.iloc[0].name  # first state starts at beginning

    # Iterate over the rows performing algorithm
    # print ("Finding Edges, please wait ...", end="\n")
    # sys.stdout.flush()

    for row in dataframe.itertuples():

        # test if either active or reactive moved more than threshold
        # http://stackoverflow.com/questions/17418108/elegant-way-to-perform-tuple-arithmetic
        # http://stackoverflow.com/questions/13168943/expression-for-elements-greater-than-x-and-less-than-y-in-python-all-in-one-ret

        # Step 2: this does the threshold test and then we sum the boolean
        # array.
        thisMeasurement = row[1:]
        # logging.debug('The current measurement is: %s' % (thisMeasurement,))
        # logging.debug('The previous measurement is: %s' %
        # (previousMeasurement,))

        stateChange = np.fabs(
            np.subtract(thisMeasurement, previousMeasurement))
        # logging.debug('The State Change is: %s' % (stateChange,))

        if np.sum(stateChange > state_threshold):
            instantaneousChange = True
        else:
            instantaneousChange = False

        # Step 3: Identify if transition is just starting, if so, process it
        if (instantaneousChange and (not ongoingChange)):

            # Calculate transition size
            lastTransition = np.subtract(estimatedSteadyPower, lastSteadyPower)
            # logging.debug('The steady state transition is: %s' %
            # (lastTransition,))

            # Sum Boolean array to verify if transition is above noise level
            if np.sum(np.fabs(lastTransition) > edge_threshold):
                if not time == dataframe.iloc[0].name:

                    # 3A, C: if so add the index of the transition start and the
                    # power information

                    # Avoid outputting first transition from zero
                    index_transitions.append(time)
                    # logging.debug('The current row time is: %s' % (time))
                    transitions.append(lastTransition)

                    # I think we want this, though not specifically in Hart's algo notes
                    # We don't want to append a steady state if it's less than min samples in length.
                    # if N > min_n_samples:
                    index_steadystates.append(time)
                    # logging.debug('The ''time'' stored is: %s' % (time))
                    # last states steady power
                    steadyStates.append(estimatedSteadyPower)

        

            # 3B
            lastSteadyPower = estimatedSteadyPower
            # 3C
            time = row[0]

        # Step 4: if a new steady state is starting, zero counter
        if instantaneousChange:
            N = 0

        # Hart step 5: update our estimate for steady state's energy
        estimatedSteadyPower = np.divide(
            np.add(np.multiply(N, estimatedSteadyPower),
                   thisMeasurement), (N + 1))
        # logging.debug('The steady power estimate is: %s' %
        #    (estimatedSteadyPower,))
        # Step 6: increment counter
        N = N + 1

        # Step 7
        ongoingChange = instantaneousChange

        # Step 8
        previousMeasurement = thisMeasurement

    lastTransition = np.subtract(estimatedSteadyPower, lastSteadyPower)
    if np.sum(np.fabs(lastTransition) > edge_threshold):
        index_transitions.append(time)
        # logging.debug('The current row time is: %s' % (time))
        transitions.append(lastTransition)

        # I think we want this, though not specifically in Hart's algo notes
        # We don't want to append a steady state if it's less than min samples in length.
        # if N > min_n_samples:
        index_steadystates.append(time)
        # logging.debug('The ''time'' stored is: %s' % (time))
        # last states steady power
        steadyStates.append(estimatedSteadyPower)



    # print("Edge detection complete.")

    # print("Creating transition frame ...")
    # sys.stdout.flush()
    
    columns = dataframe.columns


    if len(index_transitions)==0:
        # No events
        return pd.DataFrame(), pd.DataFrame()
    else:
        transitions = pd.DataFrame(data=transitions, index=index_transitions,
                                   columns=columns)
        transitions.index.name = dataframe.index.name
        # print("Transition frame created.")

        # print("Creating states frame ...")
        # sys.stdout.flush()
        steadyStates = pd.DataFrame(data=steadyStates, index=index_steadystates,
                                    columns=columns)
        # print("States frame created.")
        # print("Finished.")
        return transitions