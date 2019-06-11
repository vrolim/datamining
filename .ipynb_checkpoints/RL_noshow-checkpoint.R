library(broom)
library(tidyr)
library(dplyr)
library(pscl)
library(ROCR)
#library(car)
library(foreign)
library(plyr)
options(tibble.print_max = Inf)

#Ler Base de Dados
test <- read.csv(file = "~/phd/datamining/projetokdd/datamining/RL_train.csv", sep=",")
train <- read.csv(file = "~/phd/datamining/projetokdd/datamining/RL_test.csv", sep=",")
#drop extra column
test<-select (test,-c(X))
train<-select (train,-c(X))

#Regressao Logistica - Modelo Vazio e Cheio
#StepForward
ConjVazio = glm(Alvo ~1, family = binomial(logit), data = train)
ConjCheio = glm(Alvo ~., family = binomial(logit), data = train) 
StepModel <- step(ConjVazio, scope =list(lower=ConjVazio, upper=ConjCheio),direction = "both") 

#Coeficientes e p-values para data frame
df<- tidy(StepModel)

#Ordena coeficientes e filtra p-value nivel 0.05
df<-arrange(df, desc(estimate))
df<-filter(df, p.value < 0.05)
#Coleta 6 principais negativos e 6 principais positivos
main_positivas<-head(df, n=6)
main_negativas<-tail(df, n=6)

#Preparacao base de Testes para avaliação
#filtro teste apenas com variáveis selecionadas pelo Step
df1<-tidy(anova(StepModel))
#extrai a coluna com nomes das colunas importantes para um vetor
df1<-df1 %>% pull(term)
#Retira primeira linha com valor NULL
df1<-df1[-(1)]
#Separa alvo dos demais
Alvo<-select(test, Alvo)
#Cria nova base testes apenas com colunas importantes (Alvo fica fora, porem foi guardado no passo anterior)
test2<-test %>% select(df1)
#Combina novamente Alvo ao teste filtrado
test2<- cbind(test2, Alvo)


#Avaliacao
PredicaoResp <- predict(StepModel, newdata = test2, type = "response")
PredicaoClass <- ifelse(PredicaoResp > 0.5,1,0)
MisClasificError <- mean(PredicaoClass !=test2$Alvo)
acc<- 1-MisClasificError
pr <- prediction(PredicaoResp, test2$Alvo)
prf <- performance(pr, measure = "tpr", x.measure = "fpr") 
#Area under Roc Curve
auc <- performance(pr, measure = "auc")
auc <- auc@y.values[[1]] 
#Plota Grafico ROC
#plot(prf, main = "ROC Curve", colorize=T)
#abline(a=0, b=1, col = "gray60")


