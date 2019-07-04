db<-read.csv(file = "~/phd/datamining/projetokdd/datamining/db_IN1119_consulta.csv", sep=",")

#pacotes necessarios
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

##################As diferentes faixas etarias, tendem a ter o mesmo padrao de agendamento?
#existe correlacao?
cor(db$Age,db$wait) 

#H0: Todas as idades tem mesmo padrão de agendamento 
#Ha: O padrao de agendamento muda com a Idade

#Filtros faixa etária
crianca<- filter(db, db$Age_Bin=="Crianca")
adolescente <- filter(db, db$Age_Bin=="Adolescente")
RecemNascido<- filter(db, db$Age_Bin=="Recem-Nascido")
AdultoMeiaIdade<-filter(db, db$Age_Bin=="Adulto-Meia-Idade")
Adultojovem<-filter(db, db$Age_Bin=="Adulto-Jovem")
idoso<-filter(db, db$Age_Bin=="Idoso")

#Medias amostrais para obsevação
mean(crianca$wait)
mean(adolescente$wait)

#Teste de aderencia da variavel Tempo de Espera
ggplot(db, aes(x=db$Age_Bin,y=wait)) + geom_boxplot() # para visulizar possibilidade de normalidade
wait_mean = mean(db$wait)
wait_sd = sd(db$wait)
ks.test(db$wait, "pnorm", wait_mean, wait_sd)

#Checkpoints:  Não são normais, são independentes, maiores que 30
#Teste nao-parametrico para varias amostras
kruskal.test(list(RecemNascido$wait, crianca$wait, adolescente$wait, Adultojovem$wait, AdultoMeiaIdade$wait, idoso$wait))

#E adultos, tem o mesmo padrao?
#Teste nao-parametrico para duas amostras independetes
wilcox.test(AdultoMeiaIdade$wait, Adultojovem$wait, Paired=False)

##################SMS causa efeito ou não no no-show das consultas?
#H0: Quem recebe SMS falta igual quem nao recebe
#Ha: Quem recebe SMS falta diferente
#Checkpoints: Não são normais,  duas amostras independentes, n*p > 5
#Teste Z (aproximação pela binomial)
x1<-length(db$Alvo[db$SMS_received==1 & db$Alvo==1])
x2<-length(db$Alvo[db$SMS_received==0 & db$Alvo==1])
n1<-length(db$Alvo[db$SMS_received==1])
n2<-length(db$Alvo[db$SMS_received==0])

prop.test(x = c(x1, x2), n = c(n1, n2))

##################Os genero tem influencia nos no-shows das consults?
#H0: Mulher e homens possuem mesmo comportamento em relacao ao no-show
#Ha: Mulher e homens possuem comportamentos diferentes em relacao ao no-show
#Checkpoints:  Não são normais,  duas amostras independentes, n*p > 5
#Teste Z (aproximação pela binomial)

n1<-length(db$Alvo[db$Gender==1])
n2<-length(db$Alvo[db$Gender==0])
p = x/n

x1<-length(db$Alvo[db$Gender==1 & db$Alvo==1])
x2<-length(db$Alvo[db$Gender==0 & db$Alvo==1])

prop.test(x = c(x1, x2), n = c(n1, n2))



























