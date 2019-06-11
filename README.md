# datamining
Temos no nosso conjunto: 
  * 4 variáveis numéricas : 'wait','n_noshow_passed', "n_appoint_passed", "Age" 
  * 10 binarias: "Gender","Scholarship", "Hipertension","Diabetes","Alcoholism","handicap","SMS_received", 'stat_last_app_First','stat_last_app_ori',"Alvo"
  * 2 categoricas :'Adm_Zone','week_day'
  
  
##Conjunto 1 - RL_train.csv e RL_test.csv:
transformações convencionais para a regressão. 
Variáveis numéricas ('wait','n_noshow_passed', "n_appoint_passed") nornalizadas. Apenas "Age" foi categorizada. 
Demais variáveis binárias.

##Conjunto 2 - DT_RI_train1.csv e DT_RI_test1.csv:
Arvore e Regras.
Variáveis numéricas ('wait','n_noshow_passed', "n_appoint_passed", "Age") sem normalização e categóricas('Adm_Zone','week_day) sem dummies. 
Demais variáveis binárias.

##Conjunto 3 - DT_RI_train2.csv e DT_RI_test2.csv:
Outra alternativa para Árvores e Regras, com categorização por frequência de algumas variáveis numéricas:
('age_binned', "Adm_Zone", "week_day", 'n_noshow_passed_bin', 'n_appoint_passed_bin')
Apenas Wait, continua numérica. Demais binarias.


##Detalhes: 




