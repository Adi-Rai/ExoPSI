import math
import pandas as pd
import numpy as np

#Calculate Weight for each parameter in the similarity index
def calculate_weight(ref_val, upper_lim, lower_lim, threshold=0.8):
  
  wa = math.log(threshold)/math.log(1-((ref_val - upper_lim)/(ref_val + upper_lim)))
  wb = math.log(threshold)/math.log(1-((lower_lim - ref_val)/(lower_lim + ref_val)))
  weight = round(math.sqrt(wa*wb), 2)
  
  return weight


#Calculate Earth Similarity Index for Individual Params

def calc_ESI_param(param, lower_lim, upper_lim, threshold = 0.8):

#   w = {'radius': 0.57, 'density': 1.07, 'escape_velocity': 0.70, 'revolution': 0.70, 'surface_gravity': 0.13, 'surface_temperature': 5.58
#      ,'self': self_defined_weight}
  ref_values = {'radius': 1, 'density': 1, 'escape_velocity': 1, 'revolution': 1, 'surface_gravity': 1, 'surface_temperature': 288}
  
  ESI_P = []

  if param in ref_values:
    ref_val = ref_values[param]
    weight = calculate_weight(ref_val, lower_lim,  upper_lim,  threshold)
#   for i in range(len(param)):
#     V = round(math.pow(1-abs((param[i] - ref_val)/(ref_val + param[i])), weight), 6)
#     ESI_P.append(V)
  
#   return np.array(ESI_P)
  return weight 


#Pass an array of Params to calculate 
#Pass an array of upper lims for respective Params 
#Pass an array of lower lims for respective Params

def calc_ESI(params, upper_lims=None, lower_lims=None):

    #Default Upper Lims
    if upper_lims is None:
        upper_lims = []
    upper_lims = [2]*len(params)

    #Default Lower Lims 
    if lower_lims is None:
        lower_lims = []
    lower_lims = [0.5]*len(params)
        
    try:
        #Perform sanity checks 
        len(params) == len(upper_lims) == len(lower_lims)
        
        for i in range(0, len(upper_lims)):
            upper_lims[i]>=lower_lims[i]

        #Calculate Weights    
        weights = []
        for i in range(0, len(params)):
            weight = calc_ESI_param(params[i], upper_lims[i], lower_lims[i])
            weights.append(weight)

        return weights
    
    except ValueError as e:
        print(e)

    
def readData(csv):

    #1. Read Column Names 
    df = pd.read_csv(csv, index_col=0) 
    cols = list(df.columns)
    
    cols_lower = [col.lower() for col in cols]
    

    #2. Browse column names and select columns which are in the ESI Formula
    columns = ['radius', 'density', 'escape_velocity', 'revolution']
    
    common_cols = []

    for i in range(0, len(columns)):     
        for j in range(0, len(cols_lower)):
            if columns[i] in cols_lower[j]:
                common_cols.append(cols[j])

    new_df = df[common_cols].copy()   

    return new_df      




new_df = readData(r"C:\Users\raiad\Downloads\Rock NESI.csv")
#4. Calculate weights for each parameters based on default limits
new_cols = list(new_df.columns)
print(new_cols)
#OPTIONAL - Pass upper and lower lims or will take default values 
calc_ESI(new_cols)