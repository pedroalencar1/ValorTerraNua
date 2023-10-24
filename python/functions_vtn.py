
#%%
from math import trunc, ceil, exp
import pandas as pd
import numpy as np
import sidrapy

#%%
# get id values from dictionaries
IRRIGATION_ID = {'Não irrigavel':0, 
                 'Irrigavel': 1}
EXPLORATION_ID = {'Agricultura':0,
                  'Mista':1, 
                  "Sem exploração":2}
CLASS_USE_ID = {'Uso restrito': 0,
                "Baixa Prod.": 1, 
                "Média Prod.": 2, 
                "Alta Prod.": 3,  
                "Terras Arenosas": 4,
                "Aluvião": 5}

# equation coefficients
COEF_MEAN = {
    "constat": 6.048,
    "irrigation": [0, 0.584],
    "exploration": [0, -0.414, -0.669], #[agriculture, mix, none]
    "class_use": [0, 0.9, 1.512, 1.841, 2.135, 2.690], # [retrict, low, med., high, sandy, flood]
    "area": -0.001,
    "distance": -0.014
}

COEF_MIN = {
    "constat": 5.713,
    "irrigation": [0,0.399],
    "exploration": [0, -0.622, -0.899], #[agriculture, mix, none]
    "class_use": [0, 0.599, 1.209, 1.494, 1.821, 2.198], # [retrict, low, med., high, sandy, flood]
    "area": -0.002,
    "distance": -0.021
}

COEF_MAX = {
    "constat": 6.348,
    "irrigation": [0, 0.770], # [no_irrigation, irrigation]
    "exploration": [0, -0.205, -0.439], #[agriculture, mix, none]
    "class_use": [0, 1.201, 1.814, 2.189, 2.449, 3.182], # [retrict, low, med., high, sandy, flood]
    "area": -0.001,
    "distance": -0.014
}

#function to get price of empty land
def price_empty_land(irr_id, 
                     exp_id,
                     use_id,
                     area,
                     distance, 
                     ipca):
    
    """
    Calculates the price of empty land
    
        Parameters:
            irr_id (int): 0 or 1
            exp_id (int): 0, 1, or 2
            class_id (int):  0, 1, 2, 3, 4, or 5
            area (float): property area in hectares
            distance (float): distance of property to city center in kilometers
            ipca (float): interest readjustment provided  by IBGE (Brazil)
            
        Returns:
            pel_values: list of values with mean, min and max estimations    
    """
    
    pel_mean = exp(COEF_MEAN["constat"] + \
        COEF_MEAN["irrigation"][irr_id] + \
        COEF_MEAN["exploration"][exp_id] + \
        COEF_MEAN["class_use"][use_id] + \
        COEF_MEAN["area"]*area + \
        COEF_MEAN["distance"]*distance)*ipca
        
    pel_min = exp(COEF_MIN["constat"] + \
        COEF_MIN["irrigation"][irr_id] + \
        COEF_MIN["exploration"][exp_id] + \
        COEF_MIN["class_use"][use_id] + \
        COEF_MIN["area"]*area + \
        COEF_MIN["distance"]*distance)*ipca
        
    pel_max = exp(COEF_MAX["constat"] + \
        COEF_MAX["irrigation"][irr_id] + \
        COEF_MAX["exploration"][exp_id] + \
        COEF_MAX["class_use"][use_id] + \
        COEF_MAX["area"]*area + \
        COEF_MAX["distance"]*distance)*ipca
    
    pel_values = [pel_mean, pel_min, pel_max]
    
    return pel_values

def price_neat(pel_values):
    "round prices for display"
    
    pel_values = np.array(pel_values)
    
    pel_round = np.log10(pel_values)
    pel_round = np.ceil(pel_round) - 2
    pel_round[pel_round < 0] = 0
    pel_round = 10**pel_round
    
    pel_values = pel_values/pel_round
    pel_values = np.round(pel_values)
    pel_values = pel_values*pel_round
    
    pel_values_dict = {"Valor médio": pel_values[0],
                       "Valor mínimo": pel_values[1],
                       "Valor máximo": pel_values[2]}
    
    return pel_values_dict   


def price_neat_text(pel_neat):
    "get prices with comma as decimal separator "
    
    pel_str = [str(pel_neat["Valor médio"])[:-2],
               str(pel_neat["Valor mínimo"])[:-2],
               str(pel_neat["Valor máximo"])[:-2]]


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
            
    pel_values_dict = {"Valor médio": pel_str[0],
                       "Valor mínimo": pel_str[1],
                       "Valor máximo": pel_str[2]}
            
    return(pel_values_dict)
    
  
def price_neat_old(pel_values):
    "round price to thousands"
    
    pel_values = np.array(pel_values)/1000
    pel_values = pel_values.round()*1000
    
    pel_values_dict = {"Valor médio": pel_values[0],
                       "Valor mínimo": pel_values[1],
                       "Valor máximo": pel_values[2]}
    
    return pel_values_dict

def get_ipca():
    "calculate accumulated ipca since 01.2021 until current month "
    
    #retrieve data from ibge
    data = sidrapy.get_table(table_code = '1737',
                             territorial_level = '1',
                             ibge_territorial_code = 'all',
                             variable = '63,69,2263,2264,2265',
                             period = 'last%20472')
    
    #select period 
    ipca = data[data['D3N'] == 'IPCA - Variação mensal']
    ipca['D2C'] = [int(numeric_string) for numeric_string in ipca['D2C']]
    ipca['V'] = [float(numeric_string) for numeric_string in ipca['V']]
    ipca = ipca[ipca['D2C'] > 202100]

    # ref_month = list(ipca['D2C'])[-1]   

    #compute ipca
    ipca_list = ipca['V']/100 + 1
    ipca_val = np.prod(ipca_list)
    
    # return([ref_month, ipca_val])
    return(ipca_val)

def export_dataframe(irr_id, 
                     exp_id,
                     use_id,
                     area,
                     distance, 
                     ipca, 
                     pel_values):
    
    irr_key = [k for k, v in IRRIGATION_ID.items() if v == irr_id]
    exp_key = [k for k, v in EXPLORATION_ID.items() if v == exp_id]
    use_key = [k for k, v in CLASS_USE_ID.items() if v == use_id]

    arr = [irr_key[0],
        exp_key[0],
        use_key[0],
        area,
        distance, 
        round(ipca, 3), 
        pel_values["Valor médio"],
        pel_values["Valor mínimo"],
        pel_values["Valor máximo"]]

    arr_id = ["Irrigabilidade",
            "Tipo de exploração",
            "Classe de uso",
            "Área (hectares)",
            "Distância até a cidade (km)", 
            "Valor do IPCA",
            "Valor médio (R$/ha)",
            "Valor mínimo (R$/ha)",
            "Valor máximo (R$/ha)"]

    df = pd.DataFrame(arr, index = arr_id, columns = ["Valor"])
    
    return(df)

def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-16')
