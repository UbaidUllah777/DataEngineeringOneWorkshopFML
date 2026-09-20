import pandas as pd


class StreamingSimulator:

    def __init__(self, csv_path):
        self.data = pd.read_csv(csv_path)
        self.current_index = 0

    def nextDataPoint(self):
        if self.current_index < len(self.data):
            data_point = self.data.iloc[[self.current_index]]
            self.current_index += 1
            return data_point

        return None