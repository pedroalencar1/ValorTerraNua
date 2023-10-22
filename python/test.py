
#%% import functions
# import functions_resed as rsd
import numpy as np

#%%
# Importa as variações do IPCA
data = sidrapy.get_table(table_code = '1737',
                             territorial_level = '1',
                             ibge_territorial_code = 'all',
                             variable = '63,69,2263,2264,2265',
                             period = 'last%20472')

# %%
ipca = data[data['D3N'] == 'IPCA - Variação mensal']
ipca['D2C'] = [int(numeric_string) for numeric_string in ipca['D2C']]
ipca['V'] = [float(numeric_string) for numeric_string in ipca['V']]
ipca = ipca[ipca['D2C'] > 202100]

ref_month = list(ipca['D2C'])[-1]

ipca_list = ipca['V']/100 + 1
ipca_val = np.prod(ipca_list)
ipca_val
# %%
import functions_vtn as vtn
# %%
price_empty = vtn.price_empty_land(1,1,1,1000,1, 1.2)
price_neat = vtn.price_neat(price_empty)
# %%

def price_neat_text(pel_neat):
    
    pel_str = [str(pel_neat)[:-2],
               str(pel_neat[1])[:-2],
               str(pel_neat[2])[:-2]]


    for i in range(3):
        if (len(pel_str[i]) > 6):
            aux1 = pel_str[i][:-6]
            aux2 = pel_str[i][-6:-3]
            aux3 = pel_str[i][-3:]
            
            pel_str[i] = aux1+'.'+aux2+'.'+aux3+",00"
            
        elif (len(pel_str[i]) > 3):
            aux1 = pel_str[i][:-3]
            aux2 = pel_str[i][-3:]
            
            pel_str[i] = aux1+'.'+aux2+",00"
        else:
            pel_str[i] = pel_str[i]+",00"
            
    return(pel_str)
