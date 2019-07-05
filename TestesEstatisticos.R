#db<-read.csv(file = "~/phd/datamining/projetokdd/datamining/db_IN1119_consulta.csv", sep=",")
db<-read.csv(file = "C:/Users/Milton/Documents/Mestrado/Minera��o de Dados/Projeto/git/datamining/db_IN1119_consulta.csv", sep=",")
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
recem_nascido <- db$wait[db$Age_Bin=="Recem-Nascido"]
crianca <- db$wait[db$Age_Bin=="Crianca"]
adolescente <- db$wait[db$Age_Bin=="Adolescente"]
adulto_meia_idade <- db$wait[db$Age_Bin=="Adulto-Meia-Idade"]
adulto_jovem <- db$wait[db$Age_Bin=="Adulto-Jovem"]
idoso <- db$wait[db$Age_Bin=="Idoso"]


#Teste de aderencia da variavel Tempo de Espera 

ks.test(recem_nascido, "pnorm", mean(recem_nascido), sd(recem_nascido))
ks.test(crianca, "pnorm", mean(crianca), sd(crianca))
ks.test(adolescente, "pnorm", mean(adolescente), sd(adolescente))
ks.test(adulto_jovem, "pnorm", mean(adulto_jovem), sd(adulto_jovem))
ks.test(adulto_meia_idade, "pnorm", mean(adulto_meia_idade), sd(adulto_meia_idade))
ks.test(idoso, "pnorm", mean(idoso), sd(idoso))


#Checkpoints:  Não são normais, são independentes, maiores que 30
#Teste nao-parametrico para varias amostras
kruskal.test(list(RecemNascido, crianca, adolescente, Adultojovem, AdultoMeiaIdade, idoso))

#E adultos, tem o mesmo padrao?
#Teste nao-parametrico para duas amostras independetes
wilcox.test(AdultoMeiaIdade, Adultojovem, Paired=False)

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

#E para consultas com wait menor que 5?

x1<-length(db$Alvo[db$SMS_received==1 & db$wait< 5 & db$Alvo==1])
x2<-length(db$Alvo[db$SMS_received==0 & db$wait< 5 & db$Alvo==1])
n1<-length(db$Alvo[db$SMS_received==1 & db$wait< 5])
n2<-length(db$Alvo[db$SMS_received==0 & db$wait< 5])

prop.test(x = c(x1, x2), n = c(n1, n2))


##################Os genero tem influencia nos no-shows das consults?
#H0: Mulher e homens possuem mesmo comportamento em relacao ao no-show
#Ha: Mulher e homens possuem comportamentos diferentes em relacao ao no-show
#Checkpoints:  Não são normais,  duas amostras independentes, n*p > 5
#Teste Z (aproximação pela binomial)

n1<-length(db$Alvo[db$Gender==1])
n2<-length(db$Alvo[db$Gender==0])
#p = x/n

x1<-length(db$Alvo[db$Gender==1 & db$Alvo==1])
x2<-length(db$Alvo[db$Gender==0 & db$Alvo==1])

prop.test(x = c(x1, x2), n = c(n1, n2))



























