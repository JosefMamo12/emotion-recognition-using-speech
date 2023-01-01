from kneed import KneeLocator
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import numpy as np


class PcaHelper:
    def __init__(self, x_train, x_test, num_of_samples=None):
        self.train_dataset = (np.append(x_train, x_test, axis=0))
        self.samples_after_pca = num_of_samples
        self.feature_len = len(x_train[0])
        self.train_samples_len = len(x_train)
        self.pca_test = PCA(num_of_samples)
        self.scaler = StandardScaler()

    def find_knee_locator(self):
        self.scaler.fit(self.train_dataset)
        scaled_data = self.scaler.transform(self.train_dataset)
        self.pca_test.fit_transform(scaled_data)
        x = list(range(0, self.feature_len))
        y = np.cumsum(self.pca_test.explained_variance_ratio_)
        kl = KneeLocator(x, y)
        kl.plot_knee()
        return kl.knee

    def data_to_load(self):
        self.scaler.fit(self.train_dataset)
        scaled_data = self.scaler.transform(self.train_dataset)
        pca_train_test = self.pca_test.fit_transform(scaled_data)
        x_pca_train = pca_train_test[:self.train_samples_len]
        x_pca_test = pca_train_test[self.train_samples_len:]
        return x_pca_train, x_pca_test
