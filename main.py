import pandas as pd
import numpy as np
from tqdm import tqdm

class NoShowPrediction:

	def __init__(self, dataframe):
		'''Entre com o caminho do dataset'''
		self.dataframe = pd.read_csv(dataframe, sep=',')

		self.dataframe = self.preProcess(self.dataframe)
		self.dataframe.to_csv("out.csv", sep=',')
		#...
		#...
		#...


	#pre processamento de algumas colunas, convertendo valores, removendo colunas, etc...
	def preProcess(self, dataframe):
		tqdm.pandas()
		#convertendo str para date
		dataframe["AppointmentDay"] = dataframe["AppointmentDay"].progress_map(lambda x: pd.to_datetime(x))
		dataframe["ScheduledDay"] = dataframe["ScheduledDay"].progress_map(lambda x: pd.to_datetime(x))
		
		#criando pares das datas para calcular a distancia de dias entre marcacao e consulta
		schedule = dataframe["ScheduledDay"]
		appointment = dataframe["AppointmentDay"]		
		distancesAppointment = list(zip(schedule,appointment))

		#criando novas variasveis a partir das datas
		dataframe["Day"] = dataframe["AppointmentDay"].progress_map(lambda x: x.strftime('%A'))
		dataframe["Month"] = dataframe["AppointmentDay"].progress_map(lambda x: x.strftime('%B'))
		dataframe["Week"] = dataframe["AppointmentDay"].progress_map(lambda x: x.strftime('%U'))
		dataframe["DistanceAppointment"] = list(map(lambda x: abs((x[0]-x[1]).days), distancesAppointment))

		#separando idades por grupos a cada 5 anos
		ages = [list(range(i*5,i*5+5)) for i in range(25)]
		dataframe["Age"] = dataframe["Age"].progress_map(lambda x: [ages.index(group) for group in ages if x in group][0])

		#removendo primary keys
		dataframe.drop(["PatientId","AppointmentID"], axis=1, inplace=True)
		return dataframe


instance = NoShowPrediction("./KaggleV2-May-2016.csv")