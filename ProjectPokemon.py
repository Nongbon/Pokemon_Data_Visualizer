import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pylab import get_cmap

def main():
    global df_init, cols, df
    
    # Read .csv file to initial DataFrame
    df_init = pd.read_csv('Pokemon.csv',encoding = "UTF-8")
    
    # Data Preprocessing
    df_init['Type 2'] = df_init['Type 2'].fillna('')
    cols = list(df_init)
    cols.remove('Type 1')
    cols.remove('Type 2')
    cols.insert(0, 'All')
    cols.insert(3, 'Type')
    df_init['All'] = ''
    df_init['Type'] = df_init['Type 1'] + ',' + df_init['Type 2']
    df_init = df_init[cols]
    
    # Create <Empty> DataFrame
    df = pd.DataFrame(columns=cols)
    
    while True:
        OptionMenu = {
            '1': "Create new Pokemon's DataFrame", 
            '2': "Edit Pokemon's DataFrame", 
            '3': "View DataFrame", 
            '4': "Plot Graph", 
            '5': "Save DataFrame as .csv File", 
            '0': "Exit Program"
        }
        
        # Display Option Menu
        BreakLine()
        print("Select a Program's Option")
        if df.empty:
            OptionMenu = {key: val for key,val in OptionMenu.items() if key in {'1', '0'}}
        for key,val in OptionMenu.items():
            print("{:>2}".format(key) + ' : ' + val)
            
        # Input Option
        OptionCode = InputLoop('Option', OptionMenu)
        BreakLine()
        
        # Determine and Do program with Option
        if OptionCode == '0':
            print("Exiting Program...")
            BreakLine()
            break
        elif OptionCode == '1':
            # Clear DataFrame
            df = pd.DataFrame(columns=cols)
            PokeSearch()
        elif OptionCode == '2':
            ModeMenu = {
                '1': 'Add new pokemons to DataFrame',
                '2': 'Filter pokemons in DataFrame',
                '3': 'Remove the specific pokemon from DataFrame'
            }
            
            for key,val in ModeMenu.items():
                print("{:>2}".format(key) + ' : ' + val)
            
            ModeCode = InputLoop('Mode', ModeMenu)
            BreakLine()
            
            if ModeCode == '1':
                PokeSearch()
            if ModeCode == '2':
                PokeSearch('Filter')
            if ModeCode == '3':
                PokeSearch('Remove')
        elif OptionCode == '3':
            PokeView()
        elif OptionCode == '4':
            PokePlot()
        elif OptionCode == '5':
            PokeSave()

def PokeSearch(mode='Add'):
    global df
    
    # Display Search Menu
    print("Select Searching field")
    for head in cols:
        print("{:>2}".format(cols.index(head)) + ' : ' + head)
    
    # Input SearchCode
    SearchCode = int(InputLoop("Searching Code", cols))
    
    # Add searched Pokemon to temporary DataFrame
    df_temp = df_init.copy()
    if SearchCode == 0:
        df_temp['Select'] = True  
    else:
        # Input keyword not All Search
        status, con = isNum(SearchCode)
        keyword = input("Enter <{}> keyword{} : ".format(cols[SearchCode], con))
        keyword = keyword.lower().replace(' ', '', -1)
        if status:
            if keyword.find('-') != -1:
                domain = list(map(int, keyword.split('-')))
                df_temp['Select'] = df_temp[cols[SearchCode]].between(domain[0], domain[1])
            else:
                df_temp['Select'] = df_temp[cols[SearchCode]].map(lambda x: int(x) == int(keyword))
        else:
            df_temp['Select'] = df_temp[cols[SearchCode]].map(lambda x: str(x).lower().find(keyword) != -1)
    df_temp.query('Select == True', inplace = True)
    BreakLine()
    
    # Add to DataFrame
    if mode == 'Add':
        df = pd.concat([df, df_temp[cols]])
        df.drop_duplicates(inplace=True)
        
    # or Filter from DataFrame
    elif mode == 'Filter':
        df = pd.concat([df, df_temp[cols]])
        df = df[df.duplicated(subset=cols, keep=False)]
        df.drop_duplicates(inplace=True)
        
    # or Remove from DataFrame
    elif mode == 'Remove':
        df = pd.concat([df, df_temp[cols]])
        df.drop_duplicates(keep=False, inplace=True)
        
    # Reset Index and Sort
    df.reset_index(drop=True, inplace=True)
    df.sort_values(by=['#', 'Name'])
    
    # Display the number of pokemons in DataFrame
    print("The DataFrame contains {} pokemon(s)".format(df.shape[0]))

def PokeView():
    
    # Display Display Menu
    print("Select Displaying field <separate ','>")
    for head in cols:
        print("{:>2}".format(cols.index(head)) + ' : ' + head)

    # Input Display
    while True:
        temp = True
        DisplayCode = input("Displaying Code : ")
        DisplayCode = DisplayCode.replace(' ', '', -1).split(',')
        for item in DisplayCode:
            if not item.isnumeric():
                temp = False
                break
        if temp:
            DisplayCode = list(map(int, DisplayCode))
            break
        print("Invalid Displaying Code")
    BreakLine()
    
    # Create "For displayed" DataFrame
    if 0 in DisplayCode:
        cols_disp = cols.copy()   
    else:
        cols_disp = [cols[i] for i in DisplayCode]
    
    # Data Deprocessing
    df_disp = Deprocess(df[cols_disp])
    
    # Display DataFrame
    pd.set_option("display.max_rows", None, "display.max_columns", None)
    print(df_disp)

def PokePlot():
    cols_plot = [item for item in cols]
    cols_plot[0] = 'Amount'
    cols_plot.pop(2)
    cols_plot.pop(1)
    PlotMenu = {str(cols_plot.index(item)): item for item in cols_plot if item not in {'#', 'Name'}}
    cols_plot.insert(1, '#')
    cols_plot.insert(2, 'Name')
    
    # Display Plot Menu in x-axis
    print("Select a Label in x-axis") 
    for key,val in PlotMenu.items():
        print("{:>2}".format(key) + ' : ' + val)
        
    # Input x-axis' field
    xlabelCode = InputLoop("x-axis' Label", PlotMenu)
    xlabel = PlotMenu[xlabelCode]
    xlabelCode = cols_plot.index(xlabel)
    BreakLine()

    # Display Plot Menu in y-axis
    if xlabel == 'Amount':
        PlotMenu.pop('0')
    elif isStat(xlabelCode):
        temp = {key: val for key,val in PlotMenu.items()}
        for key in temp:
            if not isStat(key, Range=range(2, 9)):
                PlotMenu.pop(key)
    else:
        temp = {key: val for key,val in PlotMenu.items()}
        for key in temp:
            if isStat(key, return0=False, Range=range(2, 9)):
                PlotMenu.pop(key)
    print("Select a Label in y-axis") 
    for key,val in PlotMenu.items():
        print("{:>2}".format(key) + ' : ' + val)
        
    # Input y-axis' field
    ylabelCode = InputLoop("y-axis' Label", PlotMenu)
    ylabel = PlotMenu[ylabelCode]
    ylabelCode = cols_plot.index(ylabel)
    BreakLine()
    
    # Set Graph Option
    fig = plt.figure(facecolor='#111111', dpi=100)
    ax = fig.gca(facecolor='#111111')
    plt.setp([ax.spines[x] for x in ax.spines],
             alpha=0.5, color='#EEEEEE', lw=2)
    plt.xticks(color='#EEEEEE', alpha=0.5)
    plt.yticks(color='#EEEEEE', alpha=0.5)
    ax.tick_params(colors='#EEEEEE')
    cmap = 'gist_rainbow'
    
    if isStat(xlabelCode, return0=False) or isStat(ylabelCode, return0=False):
        if not isStat(ylabelCode, return0=False): # --- Histogram
            titlename = 'Histogram'
            x = df[xlabel]
            
            # Plot Graph from x
            n, bins, patches = ax.hist(x, lw=2, alpha=0.5)
            
            # Add Color to each patches
            color = get_cmap(cmap, len(patches))
            for i in range(len(patches)):
                patches[i].set_facecolor(color(i))
            
        elif not isStat(xlabelCode, return0=False): # --- Horizontal Histogram
            titlename = 'Horizontal Histogram'
            y = df[ylabel]
            
            # Plot Graph from x
            n, bins, patches = ax.hist(y, lw=2, alpha=0.5,
                                       orientation="horizontal")
            
            # Add Color to each patches
            color = get_cmap(cmap, len(patches))
            for i in range(len(patches)):
                patches[i].set_facecolor(color(i))
                
        else: # --- Scatter Plot
            titlename = 'Scatter Plot'
            y = df[ylabel]
            x = df[xlabel]
            
            # Plot Graph from y and x
            ax.scatter(x, y, lw=2, alpha=0.3, c=y, cmap=cmap)
    else:
        df_temp = Deprocess(df)
        if xlabel == 'Type':
            if ylabel == 'Type':
                xCols = ['Type 2']
                yCols = ['Type 1']
            else:
                xCols = ['Type 1', 'Type 2']
                yCols = [ylabel]
        else:
            xCols = [xlabel]
            if ylabel == 'Type':
                yCols = ['Type 1', 'Type 2']
            else:
                yCols = [ylabel]
                
        if isStat(ylabelCode): # --- Bar Chart
            titlename = 'Bar Chart'
            xlabels = set()
            xdict = dict()
            
            # Create y and xlabels
            for col in xCols:
                xlabels.update([item for item in df_temp[col]])
            xlabels = sorted(list(xlabels))
            if '' in xlabels:
                xlabels.remove('')
            
            for col in xCols:
                for label in xlabels:
                    df_temp['Select'] = df_temp[col].map(lambda x: x == label)
                    xdict.setdefault(label, 0)
                    xdict[label] += df_temp['Select'].astype(int).sum()
            
            y = [xdict[label] for label in xlabels]
            
            # Plot Graph from y and xlabels
            i = range(len(xlabels))
            patches = ax.bar(i, y, align='center', alpha=0.5, lw=2)
            
            # Add color to each patches
            color = get_cmap(cmap, len(patches))
            for j in range(len(patches)):
                patches[j].set_facecolor(color(j))
            
            # Add labels
            if len(xlabels) < 9:
                plt.xticks(i, xlabels)
            else:
                plt.xticks(i, xlabels, rotation='vertical')
            
        elif isStat(xlabelCode): # --- Horizontal Bar Chart
            titlename = 'Horizontal Bar Chart'
            ylabels = set()
            ydict = dict()
            
            # Create x and ylabels
            for col in yCols:
                ylabels.update([item for item in df_temp[col]])
            ylabels = sorted(list(ylabels), reverse=True)
            for col in yCols:
                for label in ylabels:
                    df_temp['Select'] = df_temp[col].map(lambda y: y == label)
                    ydict.setdefault(label, 0)
                    ydict[label] += df_temp['Select'].astype(int).sum()
            if '' in ylabels:
                ylabels.remove('')
            x = [ydict[label] for label in ylabels]
            
            # Plot Graph from x and ylabels
            i = range(len(ylabels))
            patches = ax.barh(i, x, align='center', alpha=0.5, lw=2)
            
            # Add color to each patches
            color = get_cmap(cmap, len(patches))
            for j in range(len(patches)):
                patches[j].set_facecolor(color(j))
            
            # Add labels
            if len(ylabels) < 9:
                plt.yticks(i, ylabels)
            else:
                plt.yticks(i, ylabels, rotation='horizontal')
            
        else: # --- Heat Map
            titlename = 'Heat Map'
            xlabels = set()
            ylabels = set()
            alldict = dict()
            
            for xcol in xCols:
                xlabels.update([item for item in df_temp[xcol]])
            xlabels = sorted(list(xlabels))
            
            for ycol in yCols:
                ylabels.update([item for item in df_temp[ycol]])
            ylabels = sorted(list(ylabels))
            
            if xlabel == ylabel == 'Type':
                act = True
            else:
                act = False
            for xcol in xCols:
                for label_x in xlabels:
                    for ycol in yCols:
                        for label_y in ylabels:
                            df_temp['Select'] = df_temp[xcol].map(lambda x: x == label_x) & df_temp[ycol].map(lambda y: y == label_y)
                            alldict.setdefault(sort_cood([label_y, label_x], xlabels, act), 0)
                            alldict[sort_cood([label_y, label_x], xlabels, act)] += df_temp['Select'].astype(int).sum()
            
            
            if '' in xlabels and not act:
                xlabels.remove('')
            if '' in ylabels:
                ylabels.remove('')
            
            array = [[alldict[sort_cood([j,i], xlabels, act)] for i in xlabels] for j in ylabels]
            array = np.array(array)
            
            ax = sns.heatmap(array, cmap='gist_heat', annot=True, cbar=False, fmt='d')
            
            # Add labels
            j, i = array.shape
            i = np.arange(i) + 0.5
            j = np.arange(j) + 0.5
            plt.yticks(j, ylabels, rotation=0)
            if '' in xlabels:
                xlabels[xlabels.index('')] = 'Null'
                
            
            if len(xlabels) < 9:
                plt.xticks(i, xlabels)
            else:
                plt.xticks(i, xlabels, rotation='vertical')
            if xlabel == ylabel == 'Type':
                ylabel = 'Type1'
                xlabel = 'Type2'
                
    plt.title(titlename, color='#EEEEEE', alpha=0.5)    
    plt.xlabel(xlabel, color='#EEEEEE', alpha=0.5)
    plt.ylabel(ylabel, color='#EEEEEE', alpha=0.5)
    plt.show()
     
def PokeSave():
    df_temp = Deprocess(df)
    FileName = input("File Name <.csv> : ")
    if FileName[-4:] != '.csv':
        FileName += '.csv'
    df_temp.to_csv(FileName)
    print("Completely Save {}".format(FileName))
            
def BreakLine():
    # Display Break Line
    print("-" * 40)
    
def InputLoop(VarName, Checklist):
    # Input Variable which must in Checklist
    temp = [str(i) for i in range(len(Checklist))]
    while True:
        Var = input(VarName + ' : ').lower()
        if isinstance(Checklist, dict):
            if Var in Checklist:
                break
        elif Var in temp:
            break
        print("Invalid", VarName)
    return Var

def isNum(Code):
    if int(Code) in range(4, 11):
        return True, " <range '-'>"
    elif int(Code) in {1, 11}:
        return True, " <range '-'>"
    else:
        return False, ''
    
def isStat(Code, return0=True, Range=range(4,11)):
    if int(Code) == 0:
        return return0
    elif int(Code) in Range:
        return True
    else:
        return False
    
def Deprocess(df_input):
    df_var = df_input.copy()
    cols_temp = list(df_var)
    if 'Type' in cols_temp:
        loc = cols_temp.index('Type')
        df_var['Type 1'] = df_var['Type'].map(lambda x: x.split(',')[0])
        df_var['Type 2'] = df_var['Type'].map(lambda x: x.split(',')[1])
        cols_temp.remove('Type')
        cols_temp.insert(loc, 'Type 2')
        cols_temp.insert(loc, 'Type 1')
    if 'All' in cols_temp:
        cols_temp.remove('All')
    return df_var[cols_temp]

def sort_cood(list, main, activate=False):
    if activate:
        if list[0] in main:
            return tuple(sorted(list, reverse=True))
        else:
            return tuple(sorted(list))
    else:
        return tuple(list)

main()