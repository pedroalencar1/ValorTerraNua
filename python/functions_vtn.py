from math import trunc, ceil
import numpy as np

# get id values from dictionaries
IRRIGATION_ID = {'Não irrigavel':0, 
                 'Irrigavel': 1}
EXPLORATION_ID = {'Agricultura':0,
                  'Mista':1, 
                  "Sem exploração":2}
CLASS_USE_ID = {'Uso retrito': 0,
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
                     distance):
    
    """
    Calculates the price of empty land
    
        Parameters:
            irr_id (int): 0 or 1
            exp_id (int): 0, 1, or 2
            class_id (int):  0, 1, 2, 3, 4, or 5
            area (float): property area in hectares
            distance (float): distance of property to city center in kilometers
            
        Returns:
            pel_values: list of values with mean, min and max estimations    
    """
    
    pel_mean = 10**(COEF_MEAN["constat"] + \
        COEF_MEAN["irrigation"][irr_id] + \
        COEF_MEAN["exploration"][exp_id] + \
        COEF_MEAN["class_use"][use_id] + \
        COEF_MEAN["area"]*area + \
        COEF_MEAN["distance"]*distance)
        
    pel_min = 10**(COEF_MIN["constat"] + \
        COEF_MIN["irrigation"][irr_id] + \
        COEF_MIN["exploration"][exp_id] + \
        COEF_MIN["class_use"][use_id] + \
        COEF_MIN["area"]*area + \
        COEF_MIN["distance"]*distance)
        
    pel_max = 10**(COEF_MAX["constat"] + \
        COEF_MAX["irrigation"][irr_id] + \
        COEF_MAX["exploration"][exp_id] + \
        COEF_MAX["class_use"][use_id] + \
        COEF_MAX["area"]*area + \
        COEF_MAX["distance"]*distance)
    
    pel_values = [pel_mean, pel_min, pel_max]
    
    return pel_values
        
def price_neat(pel_values):
    "round price to thousands"
    
    pel_values = np.array(pel_values)/1000
    pel_values = pel_values.round()*1000
    
    pel_values_dict = {"Valor médio": pel_values[0],
                       "Valor mínimo": pel_values[1],
                       "Valor máximo": pel_values[2]}
    
    return pel_values_dict
