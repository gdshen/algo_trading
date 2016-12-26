import arrow
from datetime import timedelta


class WAP:
    def __init__(self):
        pass

    def load_data(self):
        pass

    @staticmethod
    def time_slice(time_intervals, n=10):
        """ slice the time_intervals to n slice

        :param time_intervals: [(start_time, end_time), (start_time, end_time), ...]
        :param n:
        :return:
        """
        time_format = 'HH:mm:ss'
        total_time = timedelta(0)
        for (start_time, end_time) in time_intervals:
            start = arrow.get(start_time, time_format)
            end = arrow.get(end_time, time_format)
            total_time += end - start
        delta_t = total_time / n

        l = list()
        for (start_time, end_time) in time_intervals:
            start = arrow.get(start_time, time_format)
            end = arrow.get(end_time, time_format)
            t = start
            while t < end:
                if t + delta_t <= end:
                    l.append((t.format(time_format), (t + delta_t).format(time_format),
                              (t + delta_t * np.random.random()).format(time_format)))
                else:
                    l.append((t.format(time_format), end.format(time_format),
                              (t + (end - t) * np.random.random()).format(time_format)))
                t += delta_t
        return l
