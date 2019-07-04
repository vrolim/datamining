db<-read.csv(file = "~/phd/datamining/projetokdd/datamining/db_IN1119_consulta.csv", sep=",")


library(Hmisc)
library(pastecs)
library(ggplot2)
library(ggridges)
library(dplyr)


#pre-processamento
db <-select(db,-c(X))
#db <-select(db,-c(PatientId))

db$Alvo<-as.factor(db$Alvo)
db$Gender<-as.factor(db$Gender)
db$SMS_received<-as.factor(db$SMS_received)

#descrevendo a base
summary(db)

##Plots para as consultas
#variavel wait
summary(db$wait)
describe(db$wait)
ggplot(db, aes(x=wait,fill=Alvo)) + geom_histogram()
ggplot(db, aes(x=Alvo,y=wait)) + geom_boxplot()
ggplot(db, aes(x = "", y = wait)) + geom_boxplot()

x<- (db$wait)
hist(x, prob=TRUE, ylim=c(0,0.2))
curve( dchisq(x, df=5), col='green', add=TRUE)
curve( dchisq(x, df=10), col='red', add=TRUE )
lines( density(x), col='orange')


#variavel envio de sms
summary(db$SMS_received)
describe(db$SMS_received)
ggplot(db, aes(x=SMS_received, fill=Alvo))+ geom_bar()

#variavel de noshow passado
summary(db$n_noshow_passed)
describe(db$n_noshow_passed)
ggplot(db,aes(x=n_noshow_passed,fill=Alvo)) + geom_bar()
ggplot(db, aes(x="",y=n_noshow_passed)) + geom_boxplot()

#variavel alvo
summary(db$Alvo)
describe(db$Alvo)
ggplot(db,aes(x=Alvo)) + geom_bar()

#Ideia de recorrencia
summary(db$n_noshow_passed)
ggplot(db,aes(x=PatientId)) + geom_bar()


#Plots para os Pacientes
db2<- distinct(db, PatientId)
#variavel gender
summary(db2$Gender)
describe(db2$Gender)
ggplot(db2, aes(x=Gender, fill=Alvo))+ geom_bar()


#variavel idades
summary(db2$Age_Bin)
describe(db2$Age_Bin)
ggplot(db2, aes(x=Age_Bin, fill=Alvo)) + geom_bar()

summary(db2$Age)
describe(db2$Age)
ggplot(db2, aes(x=Age, fill=Alvo)) + geom_bar()
ggplot(db2, aes(x = Alvo, y = Age)) + geom_boxplot()
ggplot(db2, aes(x = "", y = Age)) + geom_boxplot()

ggplot(db2, aes(x=Age, y=Age_Bin, fill=Age_Bin)) +
  geom_density_ridges() +
  theme_ridges() + 
  theme(legend.position = "center")
