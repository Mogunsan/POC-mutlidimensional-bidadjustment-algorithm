from multiprocessing import Pool
import numpy as np
from scipy import optimize
from timeit import default_timer as timer
import pandas as pd
from pathlib import Path

mod_path = Path(__file__).parent
csv_path = 'data.csv'


# import data from bidadjdata.csv and make it usuable
raw_data = []
loaded_data = pd.read_csv((mod_path / csv_path).resolve())
loaded_data = loaded_data.values.tolist()
[raw_data.append(x[0]) for x in loaded_data]
raw_data[13] = int(raw_data[13])
raw_data[14] = int(raw_data[14])

# Assign values from loaded csv
total_conv = raw_data[0]
total_cost = raw_data[1]
phon_conv = raw_data[2]*total_conv
tabl_conv = raw_data[3]*total_conv
desk_conv = raw_data[4]*total_conv
germ_conv = raw_data[5]*total_conv
neth_conv = raw_data[6]*total_conv
phon_orig_total_cost = raw_data[7]*total_cost
tabl_orig_total_cost = raw_data[8]*total_cost
desk_orig_total_cost = raw_data[9]*total_cost
germ_orig_total_cost = raw_data[10]*total_cost
neth_orig_total_cost = raw_data[11]*total_cost

#Declare idenpendently calculable var
total_cpa = total_cost / total_conv
total_icpa = total_conv / total_cost
phon_cpa = phon_orig_total_cost / phon_conv
phon_icpa = phon_conv / phon_orig_total_cost
phon_orig_adj = phon_icpa / total_icpa
phon_new_cost = phon_orig_adj * phon_orig_total_cost
tabl_cpa = tabl_orig_total_cost / tabl_conv
tabl_icpa = tabl_conv / tabl_orig_total_cost
tabl_orig_adj = tabl_icpa / total_icpa
tabl_new_cost = tabl_orig_adj * tabl_orig_total_cost
desk_cpa = desk_orig_total_cost / desk_conv
desk_icpa = desk_conv / desk_orig_total_cost
desk_orig_adj = desk_icpa / total_icpa
desk_new_cost = desk_orig_adj * desk_orig_total_cost
germ_cpa = germ_orig_total_cost / germ_conv
germ_icpa = germ_conv / germ_orig_total_cost
germ_orig_adj = germ_icpa / total_icpa
germ_new_cost = germ_orig_adj * germ_orig_total_cost
neth_cpa = neth_orig_total_cost / neth_conv
neth_icpa = neth_conv / neth_orig_total_cost
neth_orig_adj = neth_icpa / total_icpa
neth_new_cost = neth_orig_adj * neth_orig_total_cost
total_new_cost_device_dimension = phon_new_cost + tabl_new_cost + desk_new_cost
total_new_cost_location_dimension = germ_new_cost + neth_new_cost
weighting_factor_device_dimension = (total_new_cost_device_dimension) / ((phon_orig_adj * phon_new_cost) + (tabl_orig_adj * tabl_new_cost) + (desk_orig_adj * desk_new_cost))
weighting_factor_location_dimension = (total_new_cost_location_dimension) / ((germ_orig_adj * germ_new_cost) + (neth_orig_adj * neth_new_cost))
phon_wei_adj =  phon_orig_adj * weighting_factor_device_dimension
phon_wei_adj_cost = phon_wei_adj * phon_orig_total_cost
tabl_wei_adj =  tabl_orig_adj * weighting_factor_device_dimension
tabl_wei_adj_cost = tabl_wei_adj * tabl_orig_total_cost
desk_wei_adj =  desk_orig_adj * weighting_factor_device_dimension
desk_wei_adj_cost = desk_wei_adj * desk_orig_total_cost
germ_wei_adj =  germ_orig_adj * weighting_factor_location_dimension
germ_wei_adj_cost = germ_wei_adj * germ_orig_total_cost
neth_wei_adj =  neth_orig_adj * weighting_factor_location_dimension
neth_wei_adj_cost = neth_wei_adj * neth_orig_total_cost
total_wei_adj_cost = phon_wei_adj_cost + tabl_wei_adj_cost + desk_wei_adj_cost + germ_wei_adj_cost + neth_wei_adj_cost

# Function to calculate Errorvalue
def optmin (coefficients):
    phon_coef, tabl_coef, desk_coef, germ_coef, neth_coef = coefficients
    return (((phon_orig_total_cost*raw_data[10])*total_icpa*phon_wei_adj*phon_coef*germ_wei_adj*germ_coef)-(phon_conv*raw_data[5]))**2+(((phon_orig_total_cost*raw_data[11])*total_icpa*phon_wei_adj*phon_coef*neth_wei_adj*neth_coef)-(phon_conv*raw_data[6]))**2+(((tabl_orig_total_cost*raw_data[10])*total_icpa*tabl_wei_adj*tabl_coef*germ_wei_adj*germ_coef)-(tabl_conv*raw_data[5]))**2+(((tabl_orig_total_cost*raw_data[11])*total_icpa*tabl_wei_adj*tabl_coef*neth_wei_adj*neth_coef)-(tabl_conv*raw_data[6]))**2+(((desk_orig_total_cost*raw_data[10])*total_icpa*desk_wei_adj*desk_coef*germ_wei_adj*germ_coef)-(desk_conv*raw_data[5]))**2+(((desk_orig_total_cost*raw_data[11])*total_icpa*desk_wei_adj*desk_coef*neth_wei_adj*neth_coef)-(desk_conv*raw_data[6]))**2

# Function to calculate Costdifferencevalue
def findminchange (result):
    sum_of_total_icpa_method_cost = ((phon_new_cost+tabl_new_cost+desk_new_cost+germ_new_cost+neth_new_cost))
    change = abs((((float(result.x[0])*phon_wei_adj*phon_orig_total_cost)+(float(result.x[1])*tabl_wei_adj*tabl_orig_total_cost)+(float(result.x[2])*desk_wei_adj*desk_orig_total_cost)+(float(result.x[3])*germ_wei_adj*germ_orig_total_cost)+(float(result.x[4])*neth_wei_adj*neth_orig_total_cost))/(sum_of_total_icpa_method_cost))-1)
    return change

# Function to iterate different startingvalues to find the best startingvalues
def xiter(x_xiter):
    # Set up values to iterate over
    teilergebnis_xiter = [0,1,2,3]
    min_value_xiter = float(1.7976931348623157e+308320)
    startingiteration_xiter = raw_data[14]
    iterations_xiter = raw_data[13]
    step_xiter = raw_data[12]
    starttime_xiter = timer()
    x_start_xiter = x_xiter*step_xiter
    # bnds = [(0.8,1.40),(0.8,1.40),(0.8,1.40),(0.8,1.40),(0.8,1.40)]    
    for y_xiter in range(startingiteration_xiter,iterations_xiter):
        # Print the progress so far
        print("Process "+str(x_xiter)+" at "+str(round((((3**iterations_xiter)/iterations_xiter)/(3**iterations_xiter)*y_xiter*100),0))+"%")
        y_start_xiter = y_xiter*step_xiter
        for z_xiter in range(startingiteration_xiter,iterations_xiter):
            # print("Inbetween of inbetween: "+str(round((((2**iterations)/iterations)/(2**iterations)*z*100),0))+"%")
            z_start_xiter = z_xiter*step_xiter
            for w_xiter in range(startingiteration_xiter,iterations_xiter):
                w_start_xiter = w_xiter*step_xiter
                for v_xiter in range(startingiteration_xiter,iterations_xiter):
                    v_start_xiter = v_xiter*step_xiter
                    # Apply curent startvalues to function
                    ergebnis_xiter = optimize.minimize(optmin, (x_start_xiter,y_start_xiter,z_start_xiter,w_start_xiter,v_start_xiter))
                    # Check if best startvalues so far
                    if(ergebnis_xiter.fun < min_value_xiter):
                        min_value_xiter = ergebnis_xiter.fun
                        teilergebnis_xiter[0] = ergebnis_xiter.fun
                        teilergebnis_xiter[1] = ergebnis_xiter.x
                        teilergebnis_xiter[2] = findminchange(ergebnis_xiter)
                        teilergebnis_xiter[3] = [x_start_xiter,y_start_xiter,z_start_xiter,w_start_xiter,v_start_xiter]  
                                            
    endergebnis_xiter = optimize.minimize(optmin, teilergebnis_xiter[3])
    endtime_xiter = timer()
    
    # valuepair =[1,1,1,1,1,1,1]
    # valuepair[0] = (((phon_orig_total_cost*raw_data[10])*total_icpa*phon_wei_adj*ergebnis_xiter.x[0]*germ_wei_adj*ergebnis_xiter.x[3])-(phon_conv*raw_data[5]))**2
    # valuepair[1] = (((phon_orig_total_cost*raw_data[11])*total_icpa*phon_wei_adj*ergebnis_xiter.x[0]*neth_wei_adj*ergebnis_xiter.x[4])-(phon_conv*raw_data[6]))**2
    # valuepair[2] = (((tabl_orig_total_cost*raw_data[10])*total_icpa*tabl_wei_adj*ergebnis_xiter.x[1]*germ_wei_adj*ergebnis_xiter.x[3])-(tabl_conv*raw_data[5]))**2
    # valuepair[3] = (((tabl_orig_total_cost*raw_data[11])*total_icpa*tabl_wei_adj*ergebnis_xiter.x[1]*neth_wei_adj*ergebnis_xiter.x[4])-(tabl_conv*raw_data[6]))**2
    # valuepair[4] = (((desk_orig_total_cost*raw_data[10])*total_icpa*desk_wei_adj*ergebnis_xiter.x[2]*germ_wei_adj*ergebnis_xiter.x[3])-(desk_conv*raw_data[5]))**2
    # valuepair[5] = (((desk_orig_total_cost*raw_data[11])*total_icpa*desk_wei_adj*ergebnis_xiter.x[2]*neth_wei_adj*ergebnis_xiter.x[4])-(desk_conv*raw_data[6]))**2
    # valuepair[6] = valuepair[0]+valuepair[1]+valuepair[2]+valuepair[3]+valuepair[4]+valuepair[5]
    
    # endvaluepair =[1,1,1,1,1,1,1]
    # endvaluepair[0] = (((phon_orig_total_cost*raw_data[10])*total_icpa*phon_wei_adj*endergebnis_xiter.x[0]*germ_wei_adj*endergebnis_xiter.x[3])-(phon_conv*raw_data[5]))**2
    # endvaluepair[1] = (((phon_orig_total_cost*raw_data[11])*total_icpa*phon_wei_adj*endergebnis_xiter.x[0]*neth_wei_adj*endergebnis_xiter.x[4])-(phon_conv*raw_data[6]))**2
    # endvaluepair[2] = (((tabl_orig_total_cost*raw_data[10])*total_icpa*tabl_wei_adj*endergebnis_xiter.x[1]*germ_wei_adj*endergebnis_xiter.x[3])-(tabl_conv*raw_data[5]))**2
    # endvaluepair[3] = (((tabl_orig_total_cost*raw_data[11])*total_icpa*tabl_wei_adj*endergebnis_xiter.x[1]*neth_wei_adj*endergebnis_xiter.x[4])-(tabl_conv*raw_data[6]))**2
    # endvaluepair[4] = (((desk_orig_total_cost*raw_data[10])*total_icpa*desk_wei_adj*endergebnis_xiter.x[2]*germ_wei_adj*endergebnis_xiter.x[3])-(desk_conv*raw_data[5]))**2
    # endvaluepair[5] = (((desk_orig_total_cost*raw_data[11])*total_icpa*desk_wei_adj*endergebnis_xiter.x[2]*neth_wei_adj*endergebnis_xiter.x[4])-(desk_conv*raw_data[6]))**2
    # endvaluepair[6] = endvaluepair[0]+endvaluepair[1]+endvaluepair[2]+endvaluepair[3]+endvaluepair[4]+endvaluepair[5]

    # print("Value sum: "+str(valuepair[6]))
    # print("Endvalue sum: "+str(endvaluepair[6]))
    # print("Teilergebnis fun: "+str(teilergebnis_xiter[0]))
    # print("Endergebnis fun: "+str(endergebnis_xiter.fun))
    
    print("Time: "+str(endtime_xiter - starttime_xiter))
    print("Startvalues: "+str(teilergebnis_xiter[3]))
    print("Errorvalue: "+str(endergebnis_xiter.fun))
    print("Costdifferencevalue: "+str(findminchange(endergebnis_xiter)))
    print("Coefficients: "+str(endergebnis_xiter.x))
    return endergebnis_xiter

# Part of the code that finds the best result of the parallel run iterations and runs them to begin with
if __name__ == '__main__':
    with Pool(processes=(raw_data[13])) as pool:
        results = pool.map(xiter, range(raw_data[13]))
        bestpoolresult = float(1.7976931348623157e+308320)
        for current_attempt in range(len(results)):
            attempt_at_best_result = results[current_attempt].fun
            if(attempt_at_best_result < bestpoolresult):
                best_attempt_number = current_attempt
                bestpoolresult = attempt_at_best_result
        print(results[best_attempt_number])
        print("Anfang")
        print(results[best_attempt_number].fun)
        #Build results[best_attempt_number].x but by accessing the values directly thus getting more decimals to work with
        print("["+str(results[best_attempt_number].x[0])+" "+str(results[best_attempt_number].x[1])+" "+str(results[best_attempt_number].x[2])+" "+str(results[best_attempt_number].x[3])+" "+str(results[best_attempt_number].x[4])+"]")
        print(findminchange(results[best_attempt_number]))
        print("Startingiteration: "+str(raw_data[14]))
        print("Iterations: "+str(raw_data[13]))
        print("Iterationstep: "+str(raw_data[12]))