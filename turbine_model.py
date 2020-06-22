#IMPORT MODULES
import tkinter, csv
from matplotlib import colors
import turbine_class

#SET UP EACH MAP'S LIST
ocean_dtm, rowlist_ocean_dtm = [], []
ocean_blank, rowlist_ocean_blank = [], []
ocean_depth, rowlist_ocean_depth = [], []
ocean_slope, rowlist_ocean_slope = [], []
ocean_slope_reclass, rowlist_ocean_slope_reclass = [], []
mce, rowlist_mce = [], []

#SET UP THE EXTERNAL AGENT-BASED TURBINE CLASS
turbines = turbine_class.Turbine()
turbines = []



#CREATE BLANK LISTS
def function_create_blank_array(a, b):

    #Create the row list
    for i in range(300):
       a = []
       b.append(a)
       
       #Create a nested column list for every row 
       for j in range(300):
           a.append(0)



#READ IN DATA FROM EXTERNAL SOURCE
def function_read_data():
        
    #Import variables
    global ocean_dtm, rowlist_ocean_dtm

    #Import digital terrain model (DTM)
    r = open('data_in.txt', newline='')
    reader = csv.reader(r, quoting=csv.QUOTE_NONNUMERIC)
    
    #Create major list
    ocean_dtm = []
    for row in reader:
        #Create minor row list
        rowlist_ocean_dtm = []
        #Append the major list with the minor list
        ocean_dtm.append(rowlist_ocean_dtm)
        #Append the minor list with values
        for value in row:
            rowlist_ocean_dtm.append(value)
            
    #Close the file
    r.close()



#OBTAIN SLOPES FROM HIGHEST HEIGHT DIFFERENCES FROM ADJACENT CELLS
def function_obtain_slope():
    
    #Select every cell
    for i in range(len(ocean_dtm)):
        for j in range(len(ocean_dtm)):
            #Exclude edge cells (those with < 8 adjacent cells)
            if i > 1 and j > 1 and i < 299 and j < 299:
                
                #Create empty list for slope data
                slopedata = []
                
                #Retrieve the height differences for adjacent cells
                #and append them to the list
                slopedata.append(ocean_dtm[i][j] - ocean_dtm[i-1][j])
                slopedata.append(ocean_dtm[i][j] - ocean_dtm[i-1][j-1])
                slopedata.append(ocean_dtm[i][j] - ocean_dtm[i][j-1])
                slopedata.append(ocean_dtm[i][j] - ocean_dtm[i+1][j-1])
                slopedata.append(ocean_dtm[i][j] - ocean_dtm[i+1][j])
                slopedata.append(ocean_dtm[i][j] - ocean_dtm[i+1][j+1])
                slopedata.append(ocean_dtm[i][j] - ocean_dtm[i][j+1])
                slopedata.append(ocean_dtm[i][j] - ocean_dtm[i-1][j+1])
                
                #Turn negative height differences positive
                for k in range(len(slopedata)):
                    if slopedata[k] < 0:
                        slopedata[k] = slopedata[k] * -1
                
                #Find the maximum height difference and append it to the
                    #slope map
                l = max(slopedata)
                ocean_slope[i][j] = l



#Assemble the GUI for the user to navigate
def function_create_gui():
    
    #Create a root display for the menu
    root = tkinter.Tk()
    root.title('Offshore Wind Turbines')



    #Run the model
    def function_run_model():
        
        #Test the model for any errors
        try:
        
            #Redefine the slope map according to the user's inputs
            def function_redefine_slope():
        
                #Import minimum slope from the GUI
                a = int(min_slope.get())       
                
                #Import maximum slope from the GUI
                b = int(max_slope.get())       
                
                #Bring in all cells
                for i in range(len(ocean_slope)):
                    for j in range(len(ocean_slope)):
                        
                        #If land is too shallow, rate 0
                        if ocean_slope[i][j] < a:
                            ocean_slope_reclass[i][j] = 0
                        
                        #If land is within slope preference, rate 1
                        if ocean_slope[i][j] >= a:
                            ocean_slope_reclass[i][j] = 1
            
                        #If land is too deep, rate 0
                        if ocean_slope[i][j] > b:
                            ocean_slope_reclass[i][j] = 0
                
                
    
            #Redefine the depth map according to the user's input
            def function_redefine_depth():
        
                #Import minimum depth from the GUI
                c = int(min_depth.get())        
                
                #Import maximum depth from the GUI
                d = int(max_depth.get()) 
                
                #Bring in all cells and recalculate depth
                for i in range(len(ocean_dtm)):
                    for j in range(len(ocean_dtm)):
                        
                        #If land is above minimum depth / above sea level, rate 0
                        if ocean_dtm[i][j] < c + 127:
                            ocean_depth[i][j] = 0
                        
                        #If ocean is above maximum depth . below minimum depth, rate 1
                        if ocean_dtm[i][j] >= c + 127:
                            ocean_depth[i][j] = 1
            
                        #If ocean is below maximum depth, rate 0
                        if ocean_dtm[i][j] > d + 127:
                            ocean_depth[i][j] = 0
                            
                            
            
            #Perform the multi-criteria analysis
            def function_perform_mce():
                
                #Bring in every cell
                for i in range(len(mce)):
                    for j in range(len(mce)):
                        
                        #Multiply the depth and slope layers together
                        mce[i][j] = ocean_depth[i][j] * ocean_slope_reclass[i][j]   
                        
                        #Remove any land (DTM value < 127) from the MCE to leave just the ocean
                        if ocean_dtm[i][j] <= 127:
                            mce[i][j] = 2
                                
                            
            #Locate a wind turbine
            def function_locate_turbine():
                
                #Import minimum distance between turbines from GUI
                e = int(min_dist.get()/10)
                
                #Send this information to the turbine agent
                turbines.append(turbine_class.Turbine(mce, turbines, e))

            
            
                
            #Plot the data's figure
            def function_draw_plot():
            
                #Import modules and create figure window
                from matplotlib import pyplot as plt
                plt.figure(figsize=(4, 4))
                
                #Import the number of turbines from the GUI
                f = int(num_of_turbines.get()) 
                
                #Plot as many turbines as required on the map
                for i in range(f):
                    
                    #Plot the shadow to aid visibility
                    plt.scatter(turbines[i]._x + 1, turbines[i]._y - 1, \
                    color = 'black', marker = '1')
                    
                    #Plot the turbine
                    plt.scatter(turbines[i]._x, turbines[i]._y, \
                    color = 'white', marker = '1')
                
                #Import the choice of backdrop map from the GUI
                g = str(maptype.get())
                
                #Create mapping parameters for the MCE
                if g == 'Multi-Criteria Evaluation':
                    map_a = mce
                    map_b = 2
                    map_c = colors.ListedColormap(['#175FD4', '#82B1FD', 'Black'])
                
                #Create mapping parameters for the slope map      
                if g == 'Slope Map':
                    map_a, map_b, map_c  = ocean_slope, 14, 'gist_gray'
                    
                #Create mapping parameters for the depth map   
                if g == 'Depth Map':
                    map_a, map_b, map_c = ocean_dtm, 255, 'Greys'
                    
                #Display the map, using the parameters from the chosen backdrop map
                plt.imshow(map_a, vmin = 0, vmax = map_b, cmap = map_c)
                plt.gca().invert_yaxis()
                plt.show()
        
        
            #Trigger the events for performing the MCE
            function_redefine_slope()
            function_redefine_depth()
            function_perform_mce()
            
            #Remove all turbines should the model have already been run
            del turbines[:]
            
            #Retrieve the number of turbines from the GUI
            e = int(num_of_turbines.get())
            #Locate as many turbines as required
            for i in range(e):
                function_locate_turbine()
            
            #Close the map so as to avoid overlaying previous data underneath current data
            from matplotlib import pyplot as plt
            plt.close()

            #Create an empty line of text should no error have occurred
            emptylabel = tkinter.Label(root, text = "                                                                                                                       ")
            emptylabel.grid(columnspan = 4, row = 11, column = 0, padx = 10, pady = 10 )     
            function_draw_plot()

            
        
        #If maths error has been found, print an error message on the GUI
        except RecursionError:

            errorlabel = tkinter.Label(root, foreground = "red", text = "Cannot plot all turbines under current conditions.  Please try again.")
            errorlabel.grid(columnspan = 4, row = 11, column = 0, padx = 10)



    #Print the results
    def function_print_results():
        
        #Check if the model has been run for results to be printed
        if turbines != []:
            
            a = int(min_slope.get())       
            b = int(max_slope.get())       
            c = int(min_depth.get())        
            d = int(max_depth.get()) 
            e = int(num_of_turbines.get())
    
            #Open 'out.txt'
            with open('data_out.txt', mode='w') as out:
                
                #Create / overwrite 'out.txt'
                writer = csv.writer(out, delimiter=',', quotechar='"',\
                quoting=csv.QUOTE_MINIMAL)
                
                #Write the model parameters to the file
                writer.writerow(['*MODEL PARAMETERS*'])
                writer.writerow(['Minimum depth = ' + format(c)])
                writer.writerow(['maximum depth = ' + format(d)])
                writer.writerow(['Minimum slope = ' + format(a)])
                writer.writerow(['Maximum slope = ' + format(b)])
                writer.writerow([])
                
                #Write out the turbines' details
                writer.writerow(['*TURBINE LOCATIONS*'])
                writer.writerow(['Number of turbines = ' + format(e)])
                
                #Write out the turbines' coordinates for each turbine
                for i in range(e):
                    writer.writerow(['Turbine ' + format(i + 1) +': (' + format(turbines[i]._x) + ', ' + format(turbines[i]._y) + ')'])

        #If no model has been run, print error message to the GUI
        else:
            
            errorlabel = tkinter.Label(root, foreground = "red", text = "No results to print.  Please run model and try again.")
            errorlabel.grid(columnspan = 4, row = 11, column = 0, padx = 10)
        
        
        
    label_title = tkinter.Label(root, text = "OFFSHORE WIND TURBINES")
    label_title.grid(columnspan = 4, row = 1, column = 0, padx = 10, pady = 15)
    label_title.config(font = ("Courier", 19))   

    tkinter.Label(root, text = "ELEVATION SETTINGS").grid(columnspan = 2, row = 2, column = 2, padx = 10, pady = 10)
    
    #Create the minimum depth variable in the GUI
    tkinter.Label(root, text = "Min. Depth (m)").grid(row = 3, column = 2, padx = 10)
    min_depth = tkinter.IntVar(root)
    min_depth.set("10")
    #Create the spinbox for the variable
    spin1 = tkinter.Spinbox(root, from_= 0, to = 127, width = 5, textvariable = min_depth)
    spin1.grid(row = 3, column = 3, padx = 10)
    
    #Create the maximum depth variable in the GUI
    tkinter.Label(root, text = "Max. Depth (m)").grid(row = 4, column = 2, padx = 10)
    max_depth = tkinter.IntVar(root)
    max_depth.set("40")
    #Create the spinbox for the variable
    spin2 = tkinter.Spinbox(root, from_= 0, to = 127, width = 5, textvariable = max_depth)
    spin2.grid(row = 4, column = 3, padx = 10, pady = 5)

    tkinter.Label(root, text = "SLOPE SETTINGS").grid(columnspan = 2, row = 5, column = 2, padx = 10, pady = 10)
    
    #Create the minimum slope variable in the GUI
    tkinter.Label(root, text = "Min. Slope (°)    ").grid(row = 6, column = 2, padx = 10)
    min_slope = tkinter.IntVar(root)
    min_slope.set("0")
    #Create the spinbox for the variable
    spin3 = tkinter.Spinbox(root, from_= 0, to = 13, width = 5, textvariable = min_slope)
    spin3.grid(row = 6, column = 3, padx = 10, pady = 5)
    
    #Create the maximum slope variable in the GUI
    tkinter.Label(root, text = "Max. Slope (°)    ").grid(row = 7, column = 2, padx = 10)
    max_slope = tkinter.IntVar(root)
    max_slope.set("3")
    #Create the spinbox for the variable
    spin4 = tkinter.Spinbox(root, from_= 0, to = 13, width = 5, textvariable = max_slope)
    spin4.grid(row = 7, column = 3, padx = 10, pady = 5)
    
    tkinter.Label(root, text = "TURBINE SETTINGS").grid(columnspan = 2, row = 2, column = 0, padx = 10, pady = 10)
    
    #Create the number of turbines variable in the GUI
    tkinter.Label(root, text = "# of Turbines        ").grid(row = 3, column = 0, padx = 10)
    num_of_turbines = tkinter.IntVar(root)
    num_of_turbines.set("10")
    #Create the spinbox for the variable
    spin5 = tkinter.Spinbox(root, from_= 1, to = 100, width = 5, textvariable = num_of_turbines)
    spin5.grid(row = 3, column = 1, padx = 10)    

    #Create the minimum distance variable in the GUI
    tkinter.Label(root, text ="Max. distance (m)").grid(row = 4, column = 0, padx = 10)
    min_dist = tkinter.IntVar(root)
    min_dist.set("500")
    #Create the spinbox for the variable
    spin6 = tkinter.Spinbox(root, from_= 0, to = 1000, width = 5, textvariable = min_dist, increment = 10)
    spin6.grid(row = 4, column = 1, padx = 10)

    #Create the map background variable in the GUI
    tkinter.Label(root, text = "MAP BACKGROUND").grid(columnspan = 2, row = 5, column = 0, padx = 10, pady = 10)
    maptype = tkinter.StringVar(root)
    maptype.set('Multi-Criteria Evaluation')
    choices = {'Depth Map','Slope Map','Multi-Criteria Evaluation'}
    #Create the popup box for the variable
    popup1 = tkinter.OptionMenu(root, maptype, *choices)
    popup1.grid(columnspan = 2, row = 6, column = 0, padx = 10)

    #Create the buttons for running the model
    tkinter.Label(root, text = " ").grid(columnspan = 4, row = 11, column = 0, padx = 10, pady = 10 ) 
    tkinter.Button(root, text ="Run Model", width = 24, command = function_run_model).grid(columnspan = 2, row = 9, column = 0, padx = 15, pady = 10)
    tkinter.Button(root, text ="Export Current Results", width = 22, command = function_print_results).grid(columnspan = 2, row = 9, column = 2, padx = 15)

    #Loop the GUI
    root.mainloop()



#Run the model's processes
function_create_blank_array(rowlist_ocean_depth, ocean_depth)
function_create_blank_array(rowlist_ocean_slope, ocean_slope)
function_create_blank_array(rowlist_ocean_slope_reclass, ocean_slope_reclass)
function_create_blank_array(rowlist_mce, mce)
function_read_data()
function_obtain_slope()
function_create_gui()