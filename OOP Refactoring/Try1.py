import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
import random
from SubFunctions import calculate_weight, calc_ESI_param, SI_intsurf
from matplotlib.ticker import AutoMinorLocator
from matplotlib import gridspec

class exopsi:
    def calc_ESI(self, params, upper_lims=None, lower_lims=None,ref_val=None,threshold = 0.8,int_param = None,surf_param = None,p_index = None):
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
                ESI_param = calc_ESI_param(params.iloc[:,[i]], upper_lims[i], lower_lims[i],ref_val[i],threshold)
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
            if p_index.empty != True:
                ESI_df.insert(loc = 0, column = 'P.Name', value = p_index)
            
            return ESI_df
            
        
        
        except ValueError as e:
            print(e)




    #PLOTTING FUNCTIONS
    #1.Plot Interior vs Surface ESI
    def ESI_SI(self, df):  
        #sample = random.sample(sorted(df['ESI_Global']),200)
        data_x = df['ESI_Interior']
        data_y = df['ESI_Surface']
        
        fig,ax = plt.subplots(1)
        scatter = ax.scatter(data_x, data_y, cmap="viridis")
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
                    data_point_index = df.index[(df['ESI_Interior'] == data_point_location[0]) & (df['ESI_Surface'] == data_point_location[1])]
                    data_point_row = df.loc[data_point_index]

                    planet_name = data_point_row['P.Name'].values[0]
                    annotation.xy = data_point_location
                    

                    xlabel = planet_name
                    #ylabel = round(data_point_location[1],2)
                    text_label = f"{xlabel}"
                
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


    #Plot 2: Planetary bodies histogram
    def ESI_hist(self, df):

        facecolor = '#EAEAEA'
        color_bars = '#3475D0'
        txt_color1 = '#252525'
        txt_color2 = '#004C74'

        # df['bin'] = pd.cut(df['ESI_Global'], [0,0.2,0.4,0.6,0.8,1.0], labels=['0-0.2','0.2-0.4', '0.4-0.6', '0.6-0.8', '0.8-1.0'])
        # imd = df.groupby(['bin']).count()
        # y = imd['ESI_Global']
    
        # plot
        fig, ax = plt.subplots(facecolor=facecolor, figsize=(8,4))
        ax.set_facecolor(facecolor)
        n, bins, patches = ax.hist(df['ESI_Global'], bins=[0,0.2,0.4,0.6,0.8,1.0], color=color_bars)


        minor_locator = AutoMinorLocator(2)
        plt.gca().xaxis.set_minor_locator(minor_locator)
        plt.grid(which='minor', lw = 2.0, color=facecolor)

        # x ticks labels
        x_tickslabels = [ "{:.2f} - {:.2f}".format(value, bins[idx+1]) for idx, value in enumerate(bins[:-1])]
        # x ticks positions
        x_ticks = [(bins[idx+1] + value)/2 for idx, value in enumerate(bins[:-1])]

        plt.xticks(x_ticks, labels = x_tickslabels, c=txt_color1, fontsize=10)
        


        plt.xlabel('\nESI Values', c=txt_color2, fontsize=10)
        plt.ylabel('No. of Planets', c=txt_color2, fontsize=10)
        plt.tight_layout()
        plt.title('ESI Values Histogram', loc = 'center', fontsize = 12)
    
        # remove major and minor ticks from the x axis, but keep the labels
        ax.tick_params(axis='x', which='both',length=0)
        # Hide the right and top spines
        # remove major and minor ticks from the x axis, but keep the labels
        ax.tick_params(axis='x', which='both',length=0)
        
        # remove y ticks
        plt.yticks([])


        # Hide the right and top spines
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)

        # plot values on top of bars
        for idx, value in enumerate(n):
            if value > 0:
                plt.text(x_ticks[idx], value+5, int(value),ha='center', fontsize=8, c=txt_color1)
                
        plt.show()



exopsi = exopsi()
df = pd.read_excel(r"Aditya_Testing/Test Dataset.xlsx") 
upper_lims=[1.9, 1.5,1.4,323]
lower_lims = [0.5, 0.7,0.4,273]
ref_val = [1,1,1,288]

ESI_data = exopsi.calc_ESI(df.iloc[:,[5,6,7,9]],upper_lims,lower_lims,ref_val,0.8,surf_param=['P. Esc Vel (EU)','P. Ts Mean (K)'],int_param=['P. Radius (EU)','P. Density (EU)'],p_index=df.loc[:,'P. Name'])
print(ESI_data)

exopsi.ESI_SI(ESI_data)
exopsi.ESI_hist(ESI_data)