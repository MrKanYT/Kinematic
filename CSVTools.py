import pandas as pd

class CSVTools:

    data = None

    min_X = None
    max_X = None

    min_Y = None
    max_Y = None

    pointsArray = None

    def BakeDB(self, csv_path):
        rowsDict = {}
        colsDict = {}
        pointsArray = []

        self.data = pd.read_csv(csv_path, sep=",")

        # get points cols
        for num, i in enumerate(sorted(self.data["X_pos"].unique())):
            colsDict[i] = num

        # get points rows
        for num, i in enumerate(sorted(self.data["Y_pos"].unique())):
            rowsDict[i] = num

        # get empty 2D array
        for num, i in enumerate(self.data["Y_pos"].unique()):
            pointsArray.append([])
            for i in self.data["X_pos"].unique():
                pointsArray[num].append([])

        # fill array
        for num, i in enumerate(self.data["X_pos"]):
            pointsArray[rowsDict[self.data["Y_pos"][num]]][colsDict[self.data["X_pos"][num]]] = [self.data["X_pos"][num], self.data["Y_pos"][num],
                                                                                   [self.data["Rot1"][num], self.data["Rot2"][num]]]
        self.pointsArray = pointsArray


        # find min and max points
        self.min_X = min(self.data["X_pos"])
        self.max_X = max(self.data["X_pos"])

        self.min_Y = min(self.data["Y_pos"])
        self.max_Y = max(self.data["Y_pos"])


