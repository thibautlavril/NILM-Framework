***************************************
Non Intrusive Load Monitoring Framework
***************************************

:Date: April 2015
:Authors: Thibaut Lavril
:Version: 2.0


Purpose
=======

Framework to implement Non Intrusive Load Monitoring (NILM) based on event
detection. This framework implements algorithms and methods developped by 
Hart in [1]. 

The goal of NILM is to breakdown a total consumption of an household
into applliances consumptions (fridge, aircon, etc). To do so machine learning
techniques (mainly unsupervised learning) are used.

Algorithm Overview
==================

The algorithm is composed of different steps:

- *Data Loading and Preprocessing*: the meter data, e.g. powers measured by a smart meter on the different phases is load into memory and preprocessed (sampling rate, missing values, outliers).
- *Detection of events*: events are variations of total consumption which can be caused by the change of state of an appliance. Events are detected by different signal processing algorithms.
- *Clustering of events*: events detected are clustered, e.g. we try to group together events which are likely to come from the same appliance's change of state. Unsupervised machine learning algorithms are emplyed there.
- *Modeling of appliances*: with the clusters obtained and time serie analysis, appliance models are built. An appliance model regroups clusters. Each cluster representing a change of state of the appliance.
- *Tracking of appliance's consumptions*: Once appliance models built, it is possible to track the behaviour of each appliance to compute the consumption of this appliance at each time.

The total consumption is therefore breakdown into different appliances. Theses appliances are not lablelled. The ultimate part consits of using a supervised machine learning algorithm to label each appliance disaggregated (not implemented here).





