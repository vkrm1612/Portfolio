import numpy as np
import os
import pandas as pd
import shutil
import os
import time
import math

def check_convergence(file_path):
    data = pd.read_csv(file_path, delim_whitespace=True, usecols=[0, 1], skiprows=[0, 2])
    result = abs(((data.iloc[-1, 1]-data.iloc[-2, 1])/data.iloc[-1, 1])*100)
    return result

def last_value(file_path):
    data = pd.read_csv(file_path, delim_whitespace=True, usecols=[0, 1], skiprows=[0, 2])
    last_value = data.iloc[-1, 1]
    return last_value

def read_residuals(orig_folder, destination_folder):
    matching_files = [file for file in os.listdir(orig_folder) if file.startswith("fluent-2024")]
    if matching_files:
        source_file_path = os.path.join(orig_folder, matching_files[0])
        line = read_n_line(source_file_path,94)
        words = line.split()
        continuity = float(words[1])
        x_velocity = float(words[2])
        y_velocity = float(words[3]) 
        shutil.move(source_file_path, destination_folder)
        return continuity, x_velocity, y_velocity
    else:
        print("Transcript file not found.")
    
def read_n_line(filename, n = 1):
   # Returns the nth before last line of a file (n=1 gives last line)
    num_newlines = 0
    with open(filename, 'rb') as f:
        try:
            f.seek(-2, os.SEEK_END)    
            while num_newlines < n:
                f.seek(-2, os.SEEK_CUR)
                if f.read(1) == b'\n':
                    num_newlines += 1
        except OSError:
            f.seek(0)
        n_line = f.readline().decode()
    return n_line

def CV_force_comp(AoA, result_folder):
    # Read data
    air_prop = pd.read_csv(os.path.join(result_folder,'air_properties'), delim_whitespace= True)
    density = np.array( air_prop['density'] )
    viscosity = np.array( air_prop['viscosity-lam'] )

    # read data files
    # inlet - outlet - top - bottom
    data_files = ['NP_CVinlet_data','NP_CVoutlet_data','NP_CVtop_data','NP_CVbottom_data']

    # normal vectors
    n = [np.array([-1,0]), np.array([1,0]), np.array([0,1]), np.array([0,-1])]

    cter = 0

    # volumetric flow rate
    Q = np.zeros(4)
    Fx1, Fx2, Fx3 = np.zeros(4), np.zeros(4), np.zeros(4)
    Fy1, Fy2, Fy3 = np.zeros(4), np.zeros(4), np.zeros(4)

    for my_file in data_files:
        my_data = pd.read_csv(os.path.join(result_folder,my_file), delim_whitespace= True)
        x = np.array( my_data['x-coordinate'] )
        y = np.array( my_data['y-coordinate'] )
        u = np.array( my_data['x-velocity'] )
        v = np.array( my_data['y-velocity'] )
        p = np.array( my_data['pressure'] )
        dudx = np.array( my_data['dx-velocity-dx'] )
        dudy = np.array( my_data['dx-velocity-dy'] )
        dvdx = np.array( my_data['dy-velocity-dx'] )
        dvdy = np.array( my_data['dy-velocity-dy'] )

        if np.array_equal( abs(n[cter]), np.array([1,0]) ):
            idx = np.argsort(y)
            x, y, u, v, p, dudx, dudy, dvdx, dvdy= x[idx], y[idx], u[idx], v[idx], p[idx], dudx[idx], dudy[idx], dvdx[idx], dvdy[idx]
        else:
            idx = np.argsort(x)
            x, y, u, v, p, dudx, dudy, dvdx, dvdy = x[idx], y[idx], u[idx], v[idx], p[idx], dudx[idx], dudy[idx], dvdx[idx], dvdy[idx]

        # central collocation
        dx = abs( x[0:-1]-x[1::] )
        dy = abs( y[0:-1]-y[1::] )
        
        coords = np.zeros([len(dx),2])
        vel = np.zeros([len(dx),2])
        u_dot_n = np.zeros(len(dx))
        dev_tensor = np.zeros([len(dx),2,2])

        coords[:,0] = 0.5*(x[0:-1]+x[1::])
        coords[:,1] = 0.5*(y[0:-1]+y[1::])
        vel[:,0] = 0.5*(u[0:-1]+u[1::])
        vel[:,1] = 0.5*(v[0:-1]+v[1::])
        dev_tensor[:,0,0] = 2 * viscosity*0.5*(dudx[0:-1]+dudx[1::]) #2 mu dudx
        dev_tensor[:,0,1] = viscosity*0.5*(dudy[0:-1]+dudy[1::]) + viscosity*0.5*(dvdx[0:-1]+dvdx[1::]) # mu dudy + mu dvdx
        dev_tensor[:,1,0] = viscosity*0.5*(dudy[0:-1]+dudy[1::]) + 0.5*(dvdx[0:-1]+dvdx[1::]) # mu dudy + mu dvdx
        dev_tensor[:,1,1] = 2 * viscosity*0.5*(dvdy[0:-1]+dvdy[1::]) #2 mu dvdy

        pc = 0.5*(p[0:-1]+p[1::])

        # mass conservation term
        for i in range(len(dx)):
            u_dot_n[i] = np.dot(vel[i,:],n[cter])
        # integral
        if np.array_equal( abs(n[cter]), np.array([1,0]) ):
            Q[cter] = np.sum(u_dot_n*dy)
        else:
            Q[cter] = np.sum(u_dot_n*dx)

        # momentum conservation term 1 - convective acceleration
        uu_dot_n_x = vel[:,0] * u_dot_n
        uu_dot_n_y = vel[:,1] * u_dot_n
        # integral
        if np.array_equal( abs(n[cter]), np.array([1,0]) ):
            Fx1[cter] = -density*np.sum(uu_dot_n_x*dy)
            Fy1[cter] = -density*np.sum(uu_dot_n_y*dy)
        else:
            Fx1[cter] = -density*np.sum(uu_dot_n_x*dx)
            Fy1[cter] = -density*np.sum(uu_dot_n_y*dx)

        # momentum conservation term 2 - hydrostatic force from pressure
        p_n_x = pc*n[cter][0]
        p_n_y = pc*n[cter][1]

        if np.array_equal( abs(n[cter]), np.array([1,0]) ):
            Fx2[cter] = -np.sum(p_n_x*dy)
            Fy2[cter] = -np.sum(p_n_y*dy)
        else:
            Fx2[cter] = -np.sum(p_n_x*dx)
            Fy2[cter] = -np.sum(p_n_y*dx)
        
        # TODO implementing the third force term
        # momentum conservation term 3 - force from deviatoric stress tensor
        tau_n_x = dev_tensor[:,0,0]*n[cter][0] + dev_tensor[:,0,1]*n[cter][1]
        tau_n_y = dev_tensor[:,0,1]*n[cter][0] + dev_tensor[:,1,1]*n[cter][1]
        
        if np.array_equal( abs(n[cter]), np.array([1,0]) ):
            Fx3[cter] = np.sum(tau_n_x*dy)
            Fy3[cter] = np.sum(tau_n_y*dy)
        else:
            Fx3[cter] = np.sum(tau_n_x*dx)
            Fy3[cter] = np.sum(tau_n_y*dx)

        cter = cter+1
    
    Fx = np.sum(Fx1+Fx2+Fx3)
    Fy = np.sum(Fy1+Fy2+Fy3)
    lift_force = Fy*math.cos(math.radians(AoA))-Fx*math.sin(math.radians(AoA))
    drag_force = Fy*math.sin(math.radians(AoA))+Fx*math.cos(math.radians(AoA))
    aero_eff = lift_force/drag_force
    imbalance_perc = 100*np.sum(Q)/np.sum(Q[Q<0])

    print("Total inflow:\t\t\t", np.sum(Q[Q<0]))
    print("Total outflow:\t\t\t", np.sum(Q[Q>0]))
    print("vol flow imbalance:\t\t", np.sum(Q))
    print("vol flow imbalance [%]:\t\t", imbalance_perc)
    print('\n')
    print("Fx (Drag):\t\t\t", drag_force)
    print("Fy (Lift):\t\t\t", lift_force)
    print("Efficiency:\t\t\t", aero_eff)
    print("-------------------------------------------")
    print('\n\n\n')

    return lift_force, drag_force, aero_eff, imbalance_perc

def cost_fct(AoA, param_values, configs, ID):
    for i in range(len(configs['optim_space'])):
        configs['prmtrs'][configs['optim_space'][i]] = param_values[i]
    
    #TODO: ugly solution -> replace so that x is not introduced
    x=np.zeros(len(configs['prmtrs']))
    my_param_mapper = ['a1','b1','c1','d1','e1','a2','b2','c2','d2','e2']
    for i in range(len(configs['prmtrs'])):
        x[i] = configs['prmtrs'][my_param_mapper[i]]

    myID = (len(ID))
    ID.append(myID)
    # PREPARE DIRECTORIES AND SETTINGS
    # iteration coefficients
    coefficients = str("{:.3e}".format(x[0]))+'_'+str("{:.3e}".format(x[1]))+'_'+str("{:.3e}".format(x[2]))+'_'+str("{:.3e}".format(x[3]))+'_'+str("{:.3e}".format(x[4]))+"_"+str("{:.3e}".format(x[5]))+"_"+str("{:.3e}".format(x[6]))+"_"+str("{:.3e}".format(x[7]))+"_"+str("{:.3e}".format(x[8]))+"_"+str("{:.3e}".format(x[9]))
    # Create simulation folder where computations happen
    simulation_folder_orig = os.path.join(configs['data_folder'],"AoA_ID" + "{:0d}".format(myID))
    # renamed simulation folder with the results
    simulation_folder_renamed = os.path.join(configs['data_folder'],'AoA_' + "{:0d}".format(myID))
    # local directory to store results
    result_folder = os.path.join(configs['data_folder'],'AoA_' + "{:0d}".format(myID))

    # check if case already exists
    iteration_forces = os.path.join(result_folder, 'Forces.txt')
    if os.path.exists(simulation_folder_renamed):
        solution = pd.read_csv(iteration_forces, delim_whitespace=True)
        if configs['cost_type'].lower() == 'lift':
            return -solution["Lift"][0]
        elif configs['cost_type'].lower() == 'efficiency':
            return -solution["Efficiency"][0]
        else:
            raise Exception("the following cost function type is unknown: " + configs['cost_type'])
    
    # DEFINE FLUENT SETTINGS
    # Define the dimension and precision of the simulation
    dimension_precision = "2ddp"
    # Define the path to the journal file
    journal_file_path = '"' + os.path.join(simulation_folder_orig,'template.jou') + '"'

    # copy template folder before running simulation
    shutil.copytree(configs['initial_case_folder'], simulation_folder_orig)

    # Read the initial journal file
    with open(os.path.join(simulation_folder_orig,'template.jou'), 'r') as file:
        lines = file.readlines()
    # Modify the desired lines
    modified_lines = []
    for i, line in enumerate(lines):
        words = line.split()
        if i == 1 and len(words) >= 2:  
            words[1] = simulation_folder_orig
        elif i == 5 and len(words) >= 8:  
            words[8] = str(math.cos(math.radians(AoA)))
            words[10] = str(math.sin(math.radians(AoA)))
        elif i == 6 and len(words) >= 8:  
            words[8] = str(math.cos(math.radians(AoA)))
            words[10] = str(math.sin(math.radians(AoA)))
        modified_line = ' '.join(words) + '\n'
        modified_lines.append(modified_line)
    # Write the modified content to the same file
    with open(os.path.join(simulation_folder_orig,'template.jou'), 'w') as file:
        file.writelines(modified_lines)


    # RUN SIMULATION
    # change directory to the location of fluent.exe
    os.chdir(configs['fluent_path'])

    # Create the command string running Fluent with a journal file and run simulation
    command = 'start fluent.exe ' + dimension_precision + ' -g -i ' + journal_file_path
    os.system(command)

    # wait for Fluent to finish
    
    flag_file = os.path.join(simulation_folder_orig, 'flag_file')
    while True:
        time.sleep(5)
        if os.path.exists(flag_file):
            with open(flag_file, 'r') as file:
                content = file.read()
            if 'pressure' in content: 
                time.sleep(5)
                break
    os.remove(flag_file)

    continuity_res, xMomentum_res, yMomentum_res = read_residuals(configs['transcript_folder'], simulation_folder_orig)

     # rename simulation folder and move it back to original work directory
    shutil.move(simulation_folder_orig, simulation_folder_renamed)
    shutil.move(simulation_folder_renamed, result_folder)

    # CHECK COVERGENCE
    lift_report = os.path.join(result_folder,'lift-rfile.out')
    solution_file = os.path.join(configs['data_folder'], 'non_porous_AoA_sweep.txt')
    if check_convergence(lift_report) > 5:
        with open(solution_file , 'a') as file:
            # file.write(coefficients + " Case does not converge\n")
            file.write("{:04d}".format(myID)+
                       " "+coefficients.replace('_',' ')+
                       " "+str("{:.3e}".format(avg_K11))+
                       " "+str("{:.3e}".format(avg_K22))+
                       " "+str("{:.3e}".format(min_K11))+
                       " "+str("{:.3e}".format(min_K22))+
                       " "+str("{:.3e}".format(max_K11))+
                       " "+str("{:.3e}".format(max_K22))+
                       " "+str("{:.3e}".format(continuity_res))+
                       " "+str("{:.3e}".format(xMomentum_res))+
                       " "+str("{:.3e}".format(yMomentum_res))+
                       " "+str("{:.3e}".format(imbalance_perc))+
                       " "+str("{:.3e}".format(0))+
                       " "+str("{:.3e}".format(0))+
                       " "+str("{:.3f}".format(0))+"\n")
        print("Case: \t\t\t Does not converge")
        my_cost = 20
        return my_cost
    
    # FORCE CALCULATION
    lift_force, drag_force, aero_eff, imbalance_perc = CV_force_comp(AoA, result_folder)

    # Read surface reports and residuals
    avg_K11 = last_value(os.path.join(result_folder,'avg_k11-rfile.out'))
    avg_K22 = last_value(os.path.join(result_folder,'avg_k22-rfile.out'))
    max_K11 = last_value(os.path.join(result_folder,'max_k11-rfile.out'))
    max_K22 = last_value(os.path.join(result_folder,'max_k22-rfile.out'))
    min_K11 = last_value(os.path.join(result_folder,'min_k11-rfile.out'))
    min_K22 = last_value(os.path.join(result_folder,'min_k22-rfile.out'))
   
    # Write iteration results
    with open(iteration_forces , 'a') as file:
            file.write(str("{:.3f}".format(drag_force))+" "+str("{:.3f}".format(lift_force))+" "+str("{:.3f}".format(aero_eff)))

    with open(solution_file , 'a') as file:
        file.write("{:04d}".format(myID)+
                   " "+coefficients.replace('_',' ')+
                   " "+str("{:.3e}".format(avg_K11))+
                   " "+str("{:.3e}".format(avg_K22))+
                   " "+str("{:.3e}".format(min_K11))+
                   " "+str("{:.3e}".format(min_K22))+
                   " "+str("{:.3e}".format(max_K11))+
                   " "+str("{:.3e}".format(max_K22))+
                   " "+str("{:.3e}".format(continuity_res))+
                   " "+str("{:.3e}".format(xMomentum_res))+
                   " "+str("{:.3e}".format(yMomentum_res))+
                   " "+str("{:.3e}".format(imbalance_perc))+
                   " "+str("{:.3e}".format(drag_force))+
                   " "+str("{:.3e}".format(lift_force))+
                   " "+str("{:.3f}".format(aero_eff))+"\n")
    
    if configs['cost_type'].lower() == 'lift':
        my_cost = -lift_force
    elif configs['cost_type'].lower() == 'efficiency':
        my_cost = -aero_eff
    else:
        raise Exception("the following cost function type is unknown: " + configs['cost_type'])
    
    # check simulation quality also based on imbalance
    if abs(imbalance_perc)>0.3 or lift_force<0 or drag_force<0 or max_K11<1e-10 or max_K22<1e-10 or min_K11>1e-5 or min_K22>1e-5 or continuity_res>1e-4 or xMomentum_res>1e-4 or yMomentum_res>1e-4:
        my_cost = 20
    
    return my_cost