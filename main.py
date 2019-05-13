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
        
        #criando novas variaveis a partir das datas
        dataframe["Day"] = dataframe["AppointmentDay"].progress_map(lambda x: x.strftime('%A'))
        dataframe["Month"] = dataframe["AppointmentDay"].progress_map(lambda x: x.strftime('%B'))
        dataframe["Week"] = dataframe["AppointmentDay"].progress_map(lambda x: x.strftime('%U'))
        dataframe["DistanceAppointment"] = list(map(lambda x: abs((x[0]-x[1]).days), distancesAppointment))

        #separando idades por grupos a cada 5 anos
        ages = [list(range(i*5,i*5+5)) for i in range(25)]
        dataframe["Age"] = dataframe["Age"].progress_map(lambda x: [ages.index(group) for group in ages if x in group][0])

        #atribuindo Regiões administrativas
        dataframeZone=pd.read_csv( "regiao_adm.csv", delimiter="," )
        dataframeZone["Neighbourhood"]=dataframeZone["Neighbourhood"].apply(lambda x: x.upper().strip())
        dataframe['Neighbourhood']=dataframe['Neighbourhood'].apply(lambda x: x.upper().strip())
        dataframe=pd.merge(dataframe, dataframeZone, on='Neighbourhood', how='outer')
        
        # embutindo informacoes sobre as consultas ao grao paciente
        dataframe['NumberAppointments']=dataframe.groupby(['PatientId'])['PatientId'].transform('count')
        dataframe['LastScheduledDay']=dataframe.groupby(['PatientId'])['ScheduledDay'].transform('max')
        dataframe['LastAppointmentDay']=dataframe.groupby(['PatientId'])['AppointmentDay'].transform('max')
        dataframe['No-show'] = dataframe['No-show'].apply(lambda x: 1 if x == 'Yes' else 0)
        dataframe['Number_NoShow']=dataframe.groupby(['PatientId'])['No-show'].transform('sum')
        #distancia da ultima consulta
        lastschedule = dataframe["LastScheduledDay"]
        lastappointment = dataframe["LastAppointmentDay"]        
        lastdistanceAppointment = list(zip(lastschedule,lastappointment))
        dataframe['LastDistanceAppointment'] = list(map(lambda x: abs((x[0]-x[1]).days), lastdistanceAppointment)) 
        #media das distancias das consultas
        dataframe['MeanDistanceAppointment'] = dataframe.groupby(['PatientId'])['DistanceAppointment'].transform('mean')
        # transformando do grao consulta para o grao paciente 
        #dataframe=dataframe.drop_duplicates('PatientId')
        #removendo features do gao consultas ja descnessarias
        #dataframe.drop(['ScheduledDay','LastScheduledDay', 'AppointmentDay', 'LastAppointmentDay', 'DistanceAppointment'], axis=1, inplace=True)
        
        
        #removendo primary keys
        dataframe.drop(["PatientId","AppointmentID"], axis=1, inplace=True)
        
        return dataframe


instance = NoShowPrediction("./KaggleV2-May-2016.csv")
