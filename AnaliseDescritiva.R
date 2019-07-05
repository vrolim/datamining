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

#variavel wait
summary(mydata$wait)
describe(mydata$wait)
ggplot(mydata, aes(x=wait,fill=Alvo)) + geom_histogram()
ggplot(mydata, aes(x=Age_Bin,y=wait)) + geom_boxplot()
ggplot(mydata, aes(x = "", y = wait)) + geom_boxplot()

#variavel gender
summary(mydata$Gender)
describe(mydata$Gender)
ggplot(mydata, aes(x=Gender, fill=Alvo))+ geom_bar()

#variavel envio de sms
summary(mydata$SMS_received)
describe(mydata$SMS_received)
ggplot(mydata, aes(x=SMS_received, fill=Alvo))+ geom_bar()
ggplot(mydata, aes(x=SMS_received,y=Age)) + geom_boxplot()

#variavel idades
summary(mydata$Age_Bin)
describe(mydata$Age_Bin)
ggplot(mydata, aes(x=Age_Bin, fill=Alvo)) + geom_bar()

summary(mydata$Age)
describe(mydata$Age)
ggplot(mydata, aes(x=Age, fill=Alvo)) + geom_histogram()
ggplot(mydata, aes(x = Alvo, y = Age)) + geom_boxplot()
ggplot(mydata, aes(x = Age_Bin, y = Age)) + geom_boxplot()

ggplot(mydata, aes(x=Age, y=Age_Bin, fill=Age_Bin)) +
  geom_density_ridges() +
  theme_ridges() + 
  theme(legend.position = "center")

#variavel de noshow passado
summary(mydata$n_noshow_passed)
describe(mydata$n_noshow_passed)
ggplot(mydata,aes(x=n_noshow_passed,fill=Alvo)) + geom_bar()
ggplot(mydata, aes(x="",y=n_noshow_passed)) + geom_boxplot()

#variavel no-show
summary(mydata$Alvo)
describe(mydata$Alvo)
ggplot(mydata,aes(x=Alvo,fill=Alvo)) + geom_bar()
