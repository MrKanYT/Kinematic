import pandas as pd
from config import cfg

class CSVTools:
    def __init__(self, csv_path):
        self.data = pd.read_csv(csv_path, sep=",")  # загружаем файл с точками

    def BakeData(self):
        rowsDict = {}
        colsDict = {}
        counter = 0
        for i in sorted(self.data["X_pos"].unique()):
            colsDict[i] = counter
            counter += 1
        counter = 0

        self.min_X = min(self.data["X_pos"])
        self.max_X = max(self.data["X_pos"])

        self.min_Y = min(self.data["Y_pos"])
        self.max_Y = max(self.data["Y_pos"])

        for i in sorted(self.data["Y_pos"].unique()):
            rowsDict[i] = counter
            counter += 1

        self.pointsArray = []
        for i in range(len(self.data["Y_pos"].unique())):  # получаем из файла двумерный массив точек в нужном порядке
            self.pointsArray.append([])
            for i2 in range(len(self.data["X_pos"].unique())):
                self.pointsArray[i].append([])

        for i in range(len(self.data["X_pos"])):
            self.pointsArray[rowsDict[self.data["Y_pos"][i]]][colsDict[self.data["X_pos"][i]]] = [self.data["X_pos"][i], self.data["Y_pos"][i],
                                                                                   [self.data["Rot1"][i], self.data["Rot2"][i]]]
