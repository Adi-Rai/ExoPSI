#Importing the libraries
from ExoPSI import exopsi
import pandas as pd
#Initializing the class
exopsi = exopsi()

#Loading the dataset
P_df = pd.read_csv(r"phl_exoplanet_catalog.csv") 
new_df = P_df.loc[P_df['P_TEMP_SURF'].isna()==False]
new_df = new_df.loc[new_df['P_RADIUS'].isna()==False]
new_df = new_df.loc[new_df['P_MASS'].isna()==False]
new_df = new_df.loc[new_df['P_ESCAPE'].isna()==False]
new_df = new_df.loc[new_df['P_NAME'].isna()==False]
P_df = new_df
red_df = P_df.loc[:,['P_NAME','P_RADIUS','P_MASS','P_ESCAPE','P_TEMP_SURF']]
red_df.to_csv("reduced phl3.csv")
print(P_df)

O_df = pd.read_csv(r"S1_spreadsheet_REVISION.csv")
new_df = O_df.loc[O_df['Min. Temp. (°C)'].isna()==False]
new_df = new_df.loc[new_df['Max. Temp. (°C)'].isna()==False]
new_df = new_df.loc[new_df['Name'].isna()==False]
O_df = new_df
red_df = O_df.loc[:,['Name','Min. Temp. (°C)','Max. Temp. (°C)']]
red_df.to_csv("reduced thermobase.csv")
print(O_df)


#Weight Calculation
upper_lims=[1.9,1.5,1.4,395]
lower_lims = [0.5,0.7,0.4,258]
ref_val = [1,1,1,288]
weights = exopsi.calc_weight(ref_val,upper_lims,lower_lims)

#PSI Calculation
PSI_data = exopsi.calc_psi(P_df[['P_RADIUS','P_MASS','P_ESCAPE','P_TEMP_SURF']],
                           upper_lims,lower_lims,ref_val,0.8,
                           surf_param=['P_ESCAPE','P_TEMP_SURF'],
                           int_param=['P_RADIUS','P_MASS'],
                           p_index=P_df.loc[:,'P_NAME'])
print(PSI_data)


#PSI Scale
exopsi.psi_scale(PSI_data)

#PSI Distribution
exopsi.psi_dist(PSI_data)
sim_candidates = PSI_data.loc[PSI_data['PSI_Global']>0.8]
sim_candidates = sim_candidates.sort_values(by = ['PSI_Global'],ascending = False)
print(sim_candidates)
sim_candidates.to_csv("sim cand.csv")