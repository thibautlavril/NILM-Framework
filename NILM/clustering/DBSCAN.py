from sklearn.cluster import DBSCAN


class DBSCAN(DBSCAN):

    pass


# def dbscan(events, eps, min_samples,
#            features=['delta P', 'delta Q'], viz=False,
#            standard_scaler=False):
#     try:
#         X = events[features].values
#     except TypeError:
#         features = pd.MultiIndex.from_tuples(features)
#         X = events[features].values
#     if standard_scaler is False:
#         Y = X
#     else:
#         Y = StandardScaler().fit_transform(X)
#     db = DBSCAN(eps=eps, min_samples=min_samples).fit(Y)
#     # events['cluster'] = db.labels_
#     labels = db.labels_
#     n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
#     print('Estimated number of clusters: %d' % n_clusters_)
#     if viz is True:
#         _viz_dbscan(db, X)
#     return db.labels_


# def _viz_dbscan(db, X):
#     labels = db.labels_
#     core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
#     core_samples_mask[db.core_sample_indices_] = True
#     # n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
#     unique_labels = set(labels)
#     colors = plt.cm.Spectral(np.linspace(0, 1, len(unique_labels)))
#     for k, col in zip(unique_labels, colors):
#         class_member_mask = (labels == k)
#         xy = X[class_member_mask & core_samples_mask]
#         plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=col,
#                  markeredgecolor='k', markersize=14)
#         xy = X[class_member_mask & ~core_samples_mask]
#         plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=col,
#                  markeredgecolor='k', markersize=6)
#     plt.show()
