import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
import random



#Calculate Weight for each parameter in the similarity index
def calculate_weight(ref_val, upper_lim, lower_lim, threshold=0.8):
  
  w_lower = math.log(threshold)/math.log(1-((ref_val - lower_lim)/(ref_val + lower_lim)))
  w_upper = math.log(threshold)/math.log(1-((upper_lim - ref_val)/(upper_lim + ref_val)))
  weight = round(math.sqrt(w_lower*w_upper), 2)
  return weight






#Calculate Earth Similarity Index for Individual Params
def calc_ESI_param(param, upper_lim, lower_lim,ref_val, threshold = 0.8):
  w = {'radius': 0.57, 'density': 1.07, 'escape_velocity': 0.70, 'revolution': 0.70, 'surface_gravity': 0.13, 'surface_temperature': 5.58}

  ref_values = {'radius': 1, 'density': 1, 'escape_velocity': 1, 'revolution': 1, 'surface_gravity': 1, 'surface_temperature': 288}
  # print(param.columns[0])
  # col_lower = param.columns[0].lower()
  # print(col_lower)
  if (param.columns[0] in ref_values):
    if pd.isna(ref_val):
        ref_val = ref_values[param.columns[0]]
    if pd.isna(upper_lim) or pd.isna(lower_lim):
        weight = w[param.columns[0]]
    else:
        weight = calculate_weight(ref_val, upper_lim,  lower_lim,  threshold)
  else:
    weight = calculate_weight(ref_val, upper_lim,  lower_lim,  threshold)  
    
  ESI_P = [] 
  
  for i in range(len(param)):
    V = round(math.pow(1-abs((param.iat[i,0] - ref_val)/(ref_val + param.iat[i,0])), weight), 6)
    ESI_P.append(V)
  
  return ESI_P
# return weight 






#function to calculate combined ESI
def SI_intsurf(data):
    SI_intsurf_df = pd.DataFrame()
    n = len(data.columns)
    data.loc[:,'new'] = 1
    for i in range(0,n):
        data.loc[:,'new'] = data.loc[:,'new']*data.iloc[:,i]
    
    data.loc[:,'new'] = pow(data.loc[:,'new'],1/n)
    return data.loc[:,'new']
    





#Pass an array of Params to calculate 
#Pass an array of upper lims for respective Params 
#Pass an array of lower lims for respective Params

def calc_ESI(params, upper_lims=None, lower_lims=None,ref_val=None,int_param = None,surf_param = None):
    colnames = list(params.columns)
    
    #Default Upper Lims
    if upper_lims is None:
        upper_lims = [float("NaN")]*len(colnames)

    #Default Lower Lims 
    if lower_lims is None:
        lower_lims = [float("NaN")]*len(colnames)
   
    if ref_val is None:
        ref_val = [float("NaN")]*len(colnames)
        
    try:
        #Perform sanity checks 
        len(colnames) == len(upper_lims) == len(lower_lims) == len(ref_val)
        
        for i in range(0, len(upper_lims)):
            upper_lims[i]>=lower_lims[i]

        #Calculate Weights    
        ESI_df = pd.DataFrame()
        for i in range(0, len(colnames)):
            ESI_param = calc_ESI_param(params.iloc[:,[i]], upper_lims[i], lower_lims[i],ref_val[i])
            ESI_colname = "ESI_{}".format(colnames[i])
            ESI_df[ESI_colname] = ESI_param
        ESI_df.index = params.index
        if int_param != None:
            ESI_int_param = list('ESI_{}'.format(col) for col in int_param)
            ESI_df['ESI_Interior'] = SI_intsurf(ESI_df.loc[:,ESI_int_param])
        if surf_param != None:
            ESI_surf_param = list('ESI_{}'.format(col) for col in surf_param)
            ESI_df['ESI_Surface'] = SI_intsurf(ESI_df.loc[:,ESI_surf_param])
        if int_param != None and surf_param != None:
            ESI_df['ESI_Global'] = SI_intsurf(ESI_df.loc[:,['ESI_Interior','ESI_Surface']])
        return ESI_df
        
        
    
    except ValueError as e:
        print(e)


#PLOTTING FUNCTIONS
#1.Plot Interior vs Surface ESI
def plot1(df):  
    sample = random.sample(sorted(df['ESI_Global']),200)
    data_x = df['ESI_Interior'].head(200)
    data_y = df['ESI_Surface'].head(200)
    
    fig,ax = plt.subplots(1)
    scatter = ax.scatter(data_x, data_y, cmap="viridis", c=sample)
    plt.xlabel("ESI_Interior")
    plt.ylabel("ESI_Surface")
    plt.title("Interior VS Surface ESI")
    
    #Create Annotation Object
    annotation = ax.annotate(
        text='',
        xy=(0, 0),
        xytext=(15, 15), # distance from x, y
        textcoords='offset points',
        bbox={'boxstyle': 'round', 'fc': 'w'},
        arrowprops={'arrowstyle': '->'}
    )
    annotation.set_visible(False)


    def mouse_hover(event):
        annotation_visbility = annotation.get_visible()
        if event.inaxes == ax:
            is_contained, annotation_index = scatter.contains(event)

            if is_contained:
                data_point_location = scatter.get_offsets()[annotation_index['ind'][0]]
                
                annotation.xy = data_point_location
                print(data_point_location)

                xlabel = round(data_point_location[0],2)
                ylabel = round(data_point_location[1],2)
                text_label = f"{xlabel},{ylabel}"
                #text_label = '({0:.2f}, {0:.2f})'.format(data_point_location[0], data_point_location[1])
                annotation.set_text(text_label)
                annotation.set_visible(True)
                fig.canvas.draw_idle()
                
            else:
                if annotation_visbility:
                    annotation.set_visible(False)
                    fig.canvas.draw_idle()


    fig.canvas.mpl_connect('motion_notify_event', mouse_hover)
    plt.show()




params = ['radius', 'density']
df = pd.read_csv(r"C:\Users\raiad\Downloads\Rock NESI.csv") 
upper_lims=[1.9, 1.5,1.4,323]
lower_lims = [0.5, 0.7,0.4,273]
ref_val = [1,1,1,288]
#surf_param=['P. Esc Vel (EU)','P. Teq Mean (K)']
#int_param=['P. Radius (EU)','P. Density (EU)']
ESI_data2 = calc_ESI(df.iloc[:,[5,6,8,9]],upper_lims,lower_lims,ref_val,surf_param=['P. Esc Vel (EU)','P. Teq Mean (K)'],int_param=['P. Radius (EU)','P. Density (EU)'])
ESI_data2  
plot1(ESI_data2)