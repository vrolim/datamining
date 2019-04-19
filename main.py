import pandas as pd
import numpy as np
from tqdm._tqdm_notebook import tqdm_notebook

class NoShowPrediction:

    def __init__(self, dataframe):
        '''Entre com o caminho do dataset'''
        self.dataframe = pd.read_csv(dataframe, sep=',', index_col='AppointmentID')
        self.dataframe = self.preProcess(self.dataframe)

        #...
        #...
        #...


    #pre processamento de algumas colunas, convertendo valores, removendo colunas, etc...
    def preProcess(self, dataframe):
        tqdm_notebook.pandas()

        #...
        #...
        #...

        dataframe.drop(['PatientId','AppointmentID'], axis=1, inplace=True)
        return dataframe


instance = NoShowPrediction('./KaggleV2-May-2016.csv')