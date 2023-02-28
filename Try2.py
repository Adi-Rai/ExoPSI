from ExoPSI import exopsi
import pandas as pd
exopsi = exopsi()
df = pd.read_excel(r"Aditya_Testing/Test Dataset.xlsx") 
upper_lims=[1.9, 1.5,1.4,323]
lower_lims = [0.5, 0.7,0.4,273]
ref_val = [1,1,1,288]
ESI_data = exopsi.calc_psi(df.iloc[:,[5,6,7,9]],upper_lims,lower_lims,ref_val,0.8,surf_param=['P. Esc Vel (EU)','P. Ts Mean (K)'],int_param=['P. Radius (EU)','P. Density (EU)'],p_index=df.loc[:,'P. Name'])
print(ESI_data)