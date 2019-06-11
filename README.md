# Datamining
Temos no nosso conjunto: 
  * 4 variáveis numéricas : 'wait','n_noshow_passed', "n_appoint_passed", "Age" 
  * 10 binarias: "Gender","Scholarship", "Hipertension","Diabetes","Alcoholism","handicap","SMS_received", 'stat_last_app_First','stat_last_app_ori',"Alvo"
  * 2 categoricas :'Adm_Zone','week_day'
  
  
### Conjunto 1 - RL_train.csv e RL_test.csv:
transformações convencionais para a regressão. 
Variáveis numéricas ('wait','n_noshow_passed', "n_appoint_passed") nornalizadas. Apenas "Age" foi categorizada. 
Demais variáveis binárias.

### Conjunto 2 - DT_RI_train1.csv e DT_RI_test1.csv:
Arvore e Regras.
Variáveis numéricas ('wait','n_noshow_passed', "n_appoint_passed", "Age") sem normalização e categóricas('Adm_Zone','week_day) sem dummies. 
Demais variáveis binárias.

### Conjunto 3 - DT_RI_train2.csv e DT_RI_test2.csv:
Outra alternativa para Árvores e Regras, com categorização por frequência de algumas variáveis numéricas:
('age_binned','n_noshow_passed_bin', 'n_appoint_passed_bin')
Apenas Wait, continua numérica. Demais binarias e categoricas.


[Detalhes](StoryTelling.ipynb)


## Resultados Regressao
**AUC: 0,59**
 
 **Variaveis importantes com significancia 5%:
 

   term                       estimate std.error statistic  p.value
 
 **1. wait                          1.50     0.159       9.45 3.30e-21**
 **2. n_noshow_passed               0.928    0.275       3.38 7.26e- 4**
 **3. stat_last_app_ori             0.602    0.0574     10.5  1.04e-25**
 **4. age_binned_5                  0.400    0.119       3.37 7.44e- 4**
 5 Alcoholism                    0.355    0.0901      3.94 8.22e- 5
 6 age_binned_15                 0.350    0.106       3.31 9.43e- 4
 7 age_binned_15ormore           0.244    0.0987      2.47 1.35e- 2
 8 Scholarship                   0.234    0.0508      4.61 3.99e- 6
 9 stat_last_app_First           0.113    0.0413      2.74 6.15e- 3
10 week_day_1                   -0.101    0.0374     -2.69 7.25e- 3
11 SMS_received                 -0.114    0.0344     -3.32 9.01e- 4
**12 week_day_2                   -0.138    0.0375     -3.69 2.28e- 4
13 Adm_Zone_VI.....Continente   -0.334    0.0389     -8.57 1.01e-17 
14 Hipertension                 -0.354    0.0407     -8.71 3.00e-18
15 n_appoint_passed             -1.15     0.273      -4.20 2.63e- 5
