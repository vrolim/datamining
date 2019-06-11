# Datamining
Temos no nosso conjunto: 
  - 4 variáveis numéricas : 'wait','n_noshow_passed', "n_appoint_passed", "Age" 
  - 10 binarias: "Gender","Scholarship", "Hipertension","Diabetes","Alcoholism","handicap","SMS_received", 'stat_last_app_First','stat_last_app_ori',"Alvo"
  - 2 categoricas :'Adm_Zone','week_day'
  
  
### Conjunto 1 - RL_train.csv e RL_test.csv: 
transformações convencionais para a regressão. 
________
Variáveis numéricas ('wait','n_noshow_passed', "n_appoint_passed") nornalizadas. Apenas "Age" foi categorizada. 
Demais variáveis binárias/dummies.

### Conjunto 2 - DT_RI_train1.csv e DT_RI_test1.csv:
Sem nenhuma transformação, para Árvore e Regras. 
________
Variáveis numéricas ('wait','n_noshow_passed', "n_appoint_passed", "Age") sem normalização e categóricas('Adm_Zone','week_day) sem dummies. 
Demais variáveis binárias.

### Conjunto 3 - DT_RI_train2.csv e DT_RI_test2.csv:
Com categorização por frequência de algumas variáveis numéricas. Outra alternativa para Árvores e Regra:
_________
categorizadas('age_binned','n_noshow_passed_bin', 'n_appoint_passed_bin')
Apenas Wait, continua numérica. Demais binarias e categoricas.


[Detalhes](StoryTelling.ipynb)


## Resultados Regressao - Conjunto 1
**AUC: 0,59**
 
 **Variaveis importantes com significancia 5%:**
 

  
 
1. wait                         1.50     
2. n_noshow_passed              0.928    
3. stat_last_app_ori            0.602    
4. age_binned_5                 0.400    
_______
1. **n_appoint_passed             -1.15**    
2. **Hipertension                 -0.354** 
3. **Adm_Zone_VI.....Continente   -0.334**    
4. **week_day_2                   -0.138**    



