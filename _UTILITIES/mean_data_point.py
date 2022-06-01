import numpy as np

class MeanDataPoint:
    def __init__(self, mean_size_: int = None):
        # mean filter
        default_ = 5
        self._mean_size = mean_size_ if mean_size_ is not None else default_
        
        # data collection
        self._data_collect = np.empty(self._mean_size, dtype=object)
        self._total_index = 0
        self._cur_index = 0
    
    def set_mean_size(self, mean_size_: int):
        self._mean_size = mean_size_

    def push_raw_data(self, raw_dat_):
        # update data collection
        if self._data_collect.size < self._mean_size:
            np.append(self._data_collect, raw_dat_)
        else:
            self._data_collect[self._cur_index] = raw_dat_

        # update index
        self._total_index += 1
        self._cur_index = self._total_index % self._mean_size

    def get_filter_value(self) -> float:
        mean_ = None

        range_index_ = self._mean_size
        if self._total_index < self._mean_size:
            range_index_ = self._total_index

        if range_index_ > 0:
            mean_ = np.mean(self._data_collect[:range_index_])

        return mean_
    