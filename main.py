import pandas as pd
import numpy as np
from tqdm import tqdm
from sklearn.linear_model import LogisticRegression
from sklearn import metrics 
import pickle

class NoShowPrediction:

    def __init__(self, dataframe):
        '''Entre com o caminho do dataset'''
        self.dataframe = pd.read_csv(dataframe, sep=',')

        self.dataframe = self.preProcess(self.dataframe)
        self.dataframe.to_csv("out.csv", sep=',')
        self.train_set = self.dataframe[(self.dataframe.AppointmentDay < pd.to_datetime('2016-05-29')) & (self.dataframe.AppointmentDay >= pd.to_datetime('2016-04-29'))]
        self.test_set = self.dataframe[self.dataframe.AppointmentDay >= pd.to_datetime('2016-05-29')]

        self.model = None

        self.train_set.to_csv('noshow_train.csv')
        self.test_set.to_csv('noshow_test.csv')

        self.train_set.drop(['AppointmentDay'], axis=1, inplace=True)
        self.test_set.drop(['AppointmentDay'], axis=1, inplace=True)
        
        self.distColumns()
        
        self.createModel()

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
        # dataframe["Month"] = dataframe["AppointmentDay"].progress_map(lambda x: x.strftime('%B'))
        # dataframe["Week"] = dataframe["AppointmentDay"].progress_map(lambda x: x.strftime('%U'))
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
        # dataframe['Number_NoShow']=dataframe.groupby(['PatientId'])['No-show'].transform('sum')
        # #distancia da ultima consulta
        lastschedule = dataframe["LastScheduledDay"]
        lastappointment = dataframe["LastAppointmentDay"]        
        lastdistanceAppointment = list(zip(lastschedule,lastappointment))
        dataframe['LastDistanceAppointment'] = list(map(lambda x: abs((x[0]-x[1]).days), lastdistanceAppointment)) 
        # #media das distancias das consultas
        dataframe['MeanDistanceAppointment'] = dataframe.groupby(['PatientId'])['DistanceAppointment'].transform('mean')
        # transformando do grao consulta para o grao paciente 
        #dataframe=dataframe.drop_duplicates('PatientId')
        #removendo features do gao consultas ja descnessarias
        #dataframe.drop(['ScheduledDay','LastScheduledDay', 'AppointmentDay', 'LastAppointmentDay', 'DistanceAppointment'], axis=1, inplace=True)
        
        
        #removendo primary keys
        dataframe.drop(["PatientId","AppointmentID","ScheduledDay","LastAppointmentDay","LastScheduledDay","Neighbourhood"], axis=1, inplace=True)
        
        return dataframe

    def distColumns(self):
        all_data = pd.concat([self.train_set,self.test_set])

        for column in all_data.select_dtypes(include=[np.object]).columns:
            #print( '\n\n', 5*'--')
            #print('processing column: ', column)
            all_data[column].fillna(0, inplace=True)

            #print(all_data[column].value_counts())

            self.train_set[column]  = self.train_set[column].fillna(0).astype(
                pd.api.types.CategoricalDtype(categories =  all_data[column].unique()))
            self.test_set[column]   = self.test_set[column].fillna(0).astype(
                pd.api.types.CategoricalDtype(categories =  all_data[column].unique()))
        print(len(self.test_set))
        print(len(self.train_set))

    def labelRemotion(self):
        train_df = self.train_set
        test_df = self.test_set

        y_train = train_df["No-show"]
        train_df.drop(['No-show'], axis=1, inplace=True)

        y_test = test_df["No-show"]
        test_df.drop(['No-show'], axis=1, inplace=True)
        return train_df, y_train, test_df, y_test

    def createModel(self,eval=True):
        train_df, y_train, test_df, y_test = self.labelRemotion()

        dummy_train_df = pd.get_dummies(train_df)
        dummy_test_df = pd.get_dummies(test_df)

        model = LogisticRegression()

        print(10*'=', 'Training')
        model.fit(dummy_train_df, y_train)

        if(eval):
            self.evaluation(model, dummy_test_df, y_test)
        pickle.dump(model,open("model.pickle",'wb'))
        return model

    def evaluation(self,model, test, y_valid):
        print(10*'=', 'evaluating on test set... ')
        y_pred = model.predict(test)
        print(metrics.classification_report(y_valid, y_pred))

        auc = metrics.roc_auc_score(y_valid, y_pred)
        print('\t, auc=',auc )

        # Compute confusion matrix
        print(10*'=', 'confusion matrix (test set)... ')
        cnf_matrix = metrics.confusion_matrix(y_valid, y_pred)
        print(cnf_matrix,"\n")

instance = NoShowPrediction("./KaggleV2-May-2016.csv")
