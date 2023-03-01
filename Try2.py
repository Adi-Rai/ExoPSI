#Importing the library and initializing the class
from ExoPSI import exopsi
import pandas as pd
exopsi = exopsi()

#Loading the dataset
df = pd.read_excel(r"Test Dataset.xlsx") 
print(df)

#Weight Calculation
upper_lims=[1.9, 1.5,1.4,323]
lower_lims = [0.5, 0.7,0.4,273]
ref_val = [1,1,1,288]
weights = exopsi.calc_weight(ref_val,upper_lims,lower_lims)

#PSI Calculation
PSI_data = exopsi.calc_psi(df.iloc[:,[5,6,7,9]],upper_lims,lower_lims,ref_val,0.8,surf_param=['P. Esc Vel (EU)','P. Ts Mean (K)'],int_param=['P. Radius (EU)','P. Density (EU)'],p_index=df.loc[:,'P. Name'])
print(PSI_data)

#PSI Scale
exopsi.psi_scale(PSI_data)

#PSI Distribution
exopsi.psi_dist(PSI_data)

#Unit Conversion
mars_data = exopsi.unit_conv(df.iloc[:,[5,6,7]],[0.53,0.71,0.45],'MU')
print(mars_data)