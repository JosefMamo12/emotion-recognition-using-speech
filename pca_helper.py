from kneed import KneeLocator
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import numpy as np
import matplotlib.pyplot as plt


class PcaHelper:
    """
    For pca algorithm,
    First I would like to find the best relation between the amount of features to the highest covariance value,
    using knee locator algorithm.
    """
    def __init__(self, x_train, x_test, num_of_samples=None):
        self.train_dataset = (np.append(x_train, x_test, axis=0))
        self.samples_after_pca = num_of_samples
        self.feature_len = len(x_train[0])
        self.train_samples_len = len(x_train)
        self.pca_test = PCA(num_of_samples)
        self.scaler = StandardScaler()
        self.min_feature_amount = None

    def find_knee_locator(self):
        self.scaler.fit(self.train_dataset)
        scaled_data = self.scaler.transform(self.train_dataset)
        self.pca_test.fit_transform(scaled_data)
        x = list(range(1, self.feature_len + 1))
        y = np.cumsum(self.pca_test.explained_variance_ratio_)
        kl = KneeLocator(x, y)
        kl.plot_knee()
        print(f"Features after pca: {kl.knee}")
        print("Saved covariance after pca: {:.3f}%".format(y[kl.knee] * 100))
        plt.show()
        return kl.knee

    def data_to_load(self):
        self.scaler.fit(self.train_dataset)
        scaled_data = self.scaler.transform(self.train_dataset)
        pca_train_test = self.pca_test.fit_transform(scaled_data)
        x_pca_train = pca_train_test[:self.train_samples_len]
        x_pca_test = pca_train_test[self.train_samples_len:]
        return x_pca_train, x_pca_test
