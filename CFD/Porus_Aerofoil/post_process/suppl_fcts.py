import numpy as np
import os
import pandas as pd
import shutil
import os
import time
import math

def CV_force_comp(AoA, result_folder):
    # Read data
    air_prop = pd.read_csv(os.path.join(result_folder, 'air_properties'),sep=r'\s+')
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
        my_data = pd.read_csv(os.path.join(result_folder, my_file),sep=r'\s+')
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


