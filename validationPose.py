from single_comparasion import *
from log_test import print_result_pose

def validate(user_json):
	# we read the input json data in numpy arrays
	score, score_partes, coordenadas_usuario  = transform_json(user_json)
	#now we separate the first 5 points of array are for head points, the 7 next are for torso, and left are for legs
	input_head, input_torso, input_legs = split_key_points(coordenadas_usuario)
	
	#we add [.., 1] a one to the inputs for resolver the AX=B
	input_head_1 = add_ones(input_head)
	input_torso_1 = add_ones(input_torso)
	input_legs_1 = add_ones(input_legs)

	#now have to read the model to compare
	modelo = read_model ("model_"+user_json["model"]+".json")

	#now i am gona split and add ones to the model
	score_model, score_partes_model, coordenadas_model  = transform_json(modelo)
	head_model, torso_model, legs_model = split_key_points(coordenadas_model)
	
	model_head_1 = add_ones(head_model)
	model_torso_1 = add_ones(torso_model)
	model_legs_1 = add_ones(legs_model)
		
	# Solve the least squares problem X * A = Y and find the affine transformation matrix A. 
	A = find_a(input_head_1, model_head_1)
	#now we use A to get the best transformation of the input head to the head model
	input_head_transform = transform(input_head, A)

	# Solve the least squares problem X * A = Y  and find the affine transformation matrix A. 
	A = find_a(input_torso_1, model_torso_1)
	#now we use A to get the best transformation of the input torso to the torso model
	input_torso_transform = transform(input_torso, A)

	# Solve the least squares problem X * A = Y # and find the affine transformation matrix A. 
	A = find_a(input_legs_1, model_legs_1)
	#now we use A to get the best transformation of the input legs to the legs model
	input_legs_transform = transform(input_legs, A)

	#now we join all points in a single array
	all_points = np.append(np.append( input_head_transform, input_torso_transform,  axis=0), input_legs_transform, axis=0)
	#print( max(decide_similarity (coordenadas_model, all_points)))

	if (max(decide_similarity (coordenadas_model, all_points))>0.1):
		print_result_pose( str(max(decide_similarity (coordenadas_model, all_points))) ,"False",  user_json["model"])
		return "false"
	else:
		print_result_pose( str(max(decide_similarity (coordenadas_model, all_points))),"True", user_json["model"])
		return "true"
