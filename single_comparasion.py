import numpy as np 
import json
from log_test import print_error
from sklearn.metrics import mean_squared_error

def transform_json(diccionario ):
	score= diccionario["score"]
	score_partes=[]
	puntos=[]
	for i in range (0, len(diccionario["keypoints"])):
	    score_partes.append( diccionario["keypoints"][i]["score"])
	    puntos.append ([diccionario["keypoints"][i]["position"]["x"], diccionario["keypoints"][i]["position"]["y"]])
	return (np.array(score), np.array(score_partes), feature_scaling(np.array(puntos) ))


def split_key_points(set_keypoints):
	return (set_keypoints[0:5], set_keypoints[5:11], set_keypoints[11:17])


def add_ones (vec_keypoints):
	vector = vec_keypoints.copy()
	return np.hstack([vector,  np.ones((vector.shape[0], 1))]) 


def remove_ones (vec_keypoints):
	vector = vec_keypoints.copy()
	return vector[:, :-1]


def transform (vec_keypoints, A):
	vector = vec_keypoints.copy()
	return  remove_ones(np.dot(add_ones(vector), A))
	


def find_a(X,Y):
	A, res, rank, s = np.linalg.lstsq(X, Y , rcond=-1)
	A[np.abs(A) < 1e-10] = 0  # set really small values to zero
	return (A)

def read_model (ruta ):
	
	#corregir por que deberia ser una ruta
	with open(ruta) as file:
		data = json.load(file)
		
	return data

def decide_similarity (model, user_pose):
	subtraction = np.abs(model - user_pose)
	distance_btween_points = ((subtraction[:, 0] )**2+ (subtraction[:, 1]) ** 2)**0.5
    #dP = (sum(subtraction)**2)**0.5
    #print(dP)
    #res =sum(x)**1/2
	print_error(str(mean_squared_error(model, user_pose)),distance_btween_points)
	#print ("mean mean_squared_error :" + str(mean_squared_error(model, user_pose)  ))
	#print (distance_btween_points)
	return distance_btween_points
        


def feature_scaling(input):
        xmax = max(input[:, 0])
        ymax = max(input[:, 1])
        xmin = np.min(input[np.nonzero(input[:,0])]) #np.nanmin(input[:, 0])
        ymin = np.min(input[np.nonzero(input[:,1])]) #np.nanmin(input[:, 1])
        sec_x = (input[:, 0]-xmin)/(xmax-xmin)
        sec_y = (input[:, 1]-ymin)/(ymax-ymin)
        output = np.vstack(np.array([sec_x, sec_y]).T)
        output[output<0] = 0
        return output
