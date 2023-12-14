# -*- coding: utf-8 -*-
"""
Created on Mon Jul 10 14:05:59 2017

@author: bbaruque
"""

import numpy as np
import global_def as gd

def load(file):

    #%% 
    
    in_file = open (file, "r")
    contentLines = in_file.readlines()
    in_file.close()
    
    #print(contentLines)

    #%% Load first line, describing the problem
    param = contentLines[0].split()
    gd.num_rows = int(param[0])
    gd.num_cols = int(param[1])
    gd.num_vehic = int(param[2])
    gd.num_rides = int(param[3])
    gd.bonus = int(param[4])
    gd.num_steps = int(param[5])
    
    print("num_rows",gd.num_rows)
    print("num_cols",gd.num_cols)
    print("num_vehic",gd.num_vehic)
    print("num_rides",gd.num_rides)
    print("bonus",gd.bonus)
    print("num_steps",gd.num_steps)
    
    #%%
    gd.rides = np.zeros((gd.num_rides, 7))
    #gd.fleet_pos = np.zeros((gd.num_vehic*2))

    for n_line in range(gd.num_rides):
        
        line = contentLines[n_line+1]
        for pos, d in enumerate(line.split()):
#            print(pos), print(d)
            gd.rides[n_line,pos] = d

    print(gd.rides)
    print("Data read correctly")

def load_mo(file):
    load(file)
    
    in_file = open (file, "r")
    contentLines = in_file.readlines()
    in_file.close()
    
    gd.adapted = [int(i) for i in contentLines[-1].split()]

def save(file_path, result):

    with open(file_path, "w+") as file:
        for r in result[1:]:
            r_str = str(r)[1:-1].replace(',','')
            file.write("{} {}\n".format(len(r), r_str))

if __name__ == "__main__":
#    file = "./qualification_round_2018.in/a_example.in"
#    load(file)    
    file = "./qualification_round_2018.in/b_should_be_easy_sp.in"
    load_mo(file)
    