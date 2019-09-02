from single_comparasion  import *
##import json-----
import matplotlib.pyplot as mp

def compare( user_json):
	

	#second we read the input json data in numpy arrays
	score, score_partes, coordenadas_usuario  = transform_json(user_json)
	#now we separate the first 5 points of array are for head points, the 7 next are for torso, and left are for legs
	input_head, input_torso, input_legs = split_key_points(coordenadas_usuario)
	
	#we add [.., 1] a one to the inputs for resolver the AX=B
	input_head_1 = add_ones(input_head)
	input_torso_1 = add_ones(input_torso)
	input_legs_1 = add_ones(input_legs);

	#now have to read the model to compare
	modelo = read_model ("model_"+user_json["model"]+".json")

	#now i am gona split and add ones to the model
	score_model, score_partes_model, coordenadas_model  = transform_json(modelo)
	head_model, torso_model, legs_model = split_key_points(coordenadas_model)
	
	model_head_1 = add_ones(head_model)
	model_torso_1 = add_ones(torso_model)
	model_legs_1 = add_ones(legs_model);

		
	# Solve the least squares problem X * A = Y
	# and find the affine transformation matrix A. 
	A = find_a(input_head_1, model_head_1)
	#now we use A to get the best transformation of the input head to the head model
	input_head_transform = transform(input_head, A)

	# Solve the least squares problem X * A = Y
	# and find the affine transformation matrix A. 
	A = find_a(input_torso_1, model_torso_1)
	#now we use A to get the best transformation of the input torso to the torso model
	input_torso_transform = transform(input_torso, A)


	# Solve the least squares problem X * A = Y
	# and find the affine transformation matrix A. 
	A = find_a(input_legs_1, model_legs_1)
	#now we use A to get the best transformation of the input legs to the legs model
	input_legs_transform = transform(input_legs, A)

	#now we join all points in a single array
	all_points = np.append(np.append( input_head_transform, input_torso_transform,  axis=0), input_legs_transform, axis=0)
	
	distancias = [ round (x,2) for x in  decide_similarity (coordenadas_model, all_points) ]
	if (max(decide_similarity (coordenadas_model, all_points))>0.08):
		print("nokas")
	else:
		print("sikas")
        
    

	mp.subplot(1,3,1)
	mp.title(u' Pose 3', fontsize =11)  # Ponemos un título
	for i in range (0, len (all_points)):
		
		mp.scatter(coordenadas_usuario[i][0], -1*coordenadas_usuario[i][1],s=5,  c="#000000")
		#mp.scatter(all_points[i][0], -1*all_points[i][1], s = 11 , c="#FF0000")

	pasar_adyacentes(coordenadas_usuario, c=  'b')
	
	mp.subplot(1,3,2)
	mp.title(u'Pose 2', fontsize =11)  # Ponemo
	for i in range (0, len (coordenadas_model)):
		mp.scatter(coordenadas_model[i][0], -1*coordenadas_model[i][1], s = 5, c="#FF0000")
		#mp.scatter(coordenadas_usuario[i][0],-1*  coordenadas_usuario[i][1],s=5,  c="#000000")
	pasar_adyacentes(coordenadas_model, c= 'r')

	mp.subplot(1,3,3)

	mp.title(u'Pose 1 vs Pose 2', fontsize =11)  # Ponemo
	for i in range (0, len (all_points)):
		mp.annotate(str (distancias[i]), [all_points[i][0],-1*all_points[i][1]], size = 9)
		mp.scatter(all_points[i][0], -1*all_points[i][1], s = 5 , c="#000000")
	pasar_adyacentes(all_points, c= 'b')
	
	for i in range (0, len (coordenadas_model)):
		
		mp.scatter(coordenadas_model[i][0], -1*coordenadas_model[i][1], s=5,  c="#FF0000")
	
	pasar_adyacentes(coordenadas_model, c= 'r')
	mp.show()

def pasar_adyacentes(matriz, c):
	connect_points(matriz[5], matriz[7],c )
	connect_points(matriz[7], matriz[9], c)

	connect_points(matriz[6], matriz[8], c)
	connect_points(matriz[8], matriz[10], c)

	connect_points(matriz[5], matriz[6], c)
	connect_points(matriz[5], matriz[11], c)
	connect_points(matriz[6], matriz[12], c)
	connect_points(matriz[12], matriz[11], c)

	connect_points(matriz[11], matriz[13], c)
	connect_points(matriz[13], matriz[15], c )

	connect_points(matriz[12], matriz[14], c)
	connect_points(matriz[14], matriz[16], c)
def connect_points (x, y, c):
	mp.plot([x[0],  y[0]], [-x[1], -y[1]], c+'-')

#json = {"model":"1","score": 0.9291614258990568, "keypoints": [{ "score": 0.9954102635383606, "part": "nose", "position": { "x": 176.10376748407862, "y": 139.78416469588817 } }, { "score": 0.972926139831543, "part": "leftEye", "position": { "x": 185.4536709915339, "y": 128.9459554768722 } }, { "score": 0.9934205412864685, "part": "rightEye", "position": { "x": 174.63481929793898, "y": 127.13654521838237 } }, { "score": 0.49820947647094727, "part": "leftEar", "position": { "x": 200.74710035509634, "y": 136.04749562304306 } }, { "score": 0.8525473475456238, "part": "rightEar", "position": { "x": 154.6648159398179, "y": 120.9593956053025 } }, { "score": 0.9786084294319153, "part": "leftShoulder", "position": { "x": 177.68802236119132, "y": 180.14656717025815 } }, { "score": 0.9955539107322693, "part": "rightShoulder", "position": { "x": 109.19484541481108, "y": 154.71562767770968 } }, { "score": 0.9835679531097412, "part": "leftElbow", "position": { "x": 238.8376796143528, "y": 115.60053460978348 } }, { "score": 0.8045794367790222, "part": "rightElbow", "position": { "x": 142.2954665603341, "y": 76.65121384260719 } }, { "score": 0.9803146123886108, "part": "leftWrist", "position": { "x": 209.91079248806847, "y": 60.72453472864767 } }, { "score": 0.7472712397575378, "part": "rightWrist", "position": { "x": 173.19718582806422, "y": 54.14958254743643 } }, { "score": 0.9985266327857971, "part": "leftHip", "position": { "x": 143.41368263333686, "y": 319.12144203037604 } }, { "score": 0.9983755350112915, "part": "rightHip", "position": { "x": 84.35611454707637, "y": 312.19399965041345 } }, { "score": 0.9997187256813049, "part": "leftKnee", "position": { "x": 151.14604798550732, "y": 439.5862867897123 } }, { "score": 0.9998410940170288, "part": "rightKnee", "position": { "x": 79.88215660956118, "y": 444.99632892534424 } }, { "score": 0.9984532594680786, "part": "leftAnkle", "position": { "x": 157.34811163876304, "y": 551.3518481421563 } }, { "score": 0.9984196424484253, "part": "rightAnkle", "position": { "x": 77.18475288361427, "y": 551.2231173385442 } }] }
#json = {"model":"1","score": 0.9628403958152322, "keypoints": [{ "score": 0.9800685048103333, "part": "nose", "position": { "x": 137.15254134241246, "y": 76.57080936060805 } }, { "score": 0.9949072599411011, "part": "leftEye", "position": { "x": 149.18543715421328, "y": 70.98348709581427 } }, { "score": 0.9621239900588989, "part": "rightEye", "position": { "x": 133.81230098264228, "y": 65.3566830705576 } }, { "score": 0.9367852807044983, "part": "leftEar", "position": { "x": 173.26975544139106, "y": 80.02791274846295 } }, { "score": 0.7877744436264038, "part": "rightEar", "position": { "x": 114.01916088297207, "y": 76.64172011497884 } }, { "score": 0.9916576743125916, "part": "leftShoulder", "position": { "x": 183.86463091067304, "y": 122.3773862786794 } }, { "score": 0.9978892207145691, "part": "rightShoulder", "position": { "x": 92.3802416612202, "y": 116.28903067622203 } }, { "score": 0.9971256852149963, "part": "leftElbow", "position": { "x": 250.29587445092108, "y": 79.5474797111541 } }, { "score": 0.9650275707244873, "part": "rightElbow", "position": { "x": 42.490088911835784, "y": 78.49894418976186 } }, { "score": 0.860549807548523, "part": "leftWrist", "position": { "x": 178.05858805021887, "y": 89.47678151112122 } }, { "score": 0.9022080898284912, "part": "rightWrist", "position": { "x": 54.4505482239482, "y": 68.28528175650868 } }, { "score": 0.997552216053009, "part": "leftHip", "position": { "x": 172.48908729404792, "y": 286.2570297300584 } }, { "score": 0.9994643330574036, "part": "rightHip", "position": { "x": 118.39534477501064, "y": 286.5138416512931 } }, { "score": 0.9986269474029541, "part": "leftKnee", "position": { "x": 175.56616638421082, "y": 407.1507990499415 } }, { "score": 0.9996596574783325, "part": "rightKnee", "position": { "x": 113.39867261597152, "y": 406.29512599841166 } }, { "score": 0.9979526400566101, "part": "leftAnkle", "position": { "x": 183.5339402966926, "y": 517.0956247530095 } }, { "score": 0.9989134073257446, "part": "rightAnkle", "position": { "x": 103.80172313883148, "y": 516.5233197045234 } }] }
#json = {"model":"1", "score":0.9651684901293587,"keypoints":[{"score":0.9989815354347229,"part":"nose","position":{"x":110.26819144519851,"y":66.18558445793182}},{"score":0.9976053833961487,"part":"leftEye","position":{"x":115.04511459884941,"y":59.95203634180448}},{"score":0.9956823587417603,"part":"rightEye","position":{"x":104.24424007430616,"y":60.79343862570678}},{"score":0.8633224964141846,"part":"leftEar","position":{"x":125.63798896997355,"y":64.26785123951241}},{"score":0.7712759375572205,"part":"rightEar","position":{"x":96.1001801249582,"y":62.76588944609527}},{"score":0.9967202544212341,"part":"leftShoulder","position":{"x":135.30378663771813,"y":101.42524867670082}},{"score":0.9984403252601624,"part":"rightShoulder","position":{"x":85.70169937193162,"y":104.06242162800949}},{"score":0.994921863079071,"part":"leftElbow","position":{"x":146.062450364406,"y":145.2717982191984}},{"score":0.9985347986221313,"part":"rightElbow","position":{"x":76.54049718240819,"y":149.61009578482188}},{"score":0.9949861764907837,"part":"leftWrist","position":{"x":150.3816600755031,"y":186.56654803205558}},{"score":0.9973738193511963,"part":"rightWrist","position":{"x":67.2278812868586,"y":190.73575743441452}},{"score":0.9992551207542419,"part":"leftHip","position":{"x":128.6021099164792,"y":191.75976230012768}},{"score":0.9982981085777283,"part":"rightHip","position":{"x":92.41951618120365,"y":187.4563224584676}},{"score":0.9959250688552856,"part":"leftKnee","position":{"x":123.16779769719344,"y":262.5170162215771}},{"score":0.9952794313430786,"part":"rightKnee","position":{"x":102.66160660680632,"y":264.5591373666251}},{"score":0.8869891166687012,"part":"leftAnkle","position":{"x":115.6972555910103,"y":332.80900413424126}},{"score":0.9242725372314453,"part":"rightAnkle","position":{"x":112.24784619520611,"y":335.2228056317638}}]}
#json = {"model":"1","score":0.9489200676188749,"keypoints":[{"score":0.9972324967384338,"part":"nose","position":{"x":243.53218001428746,"y":79.18095780903262}},{"score":0.9939756989479065,"part":"leftEye","position":{"x":258.2240304316065,"y":73.09263441627591}},{"score":0.995942234992981,"part":"rightEye","position":{"x":236.10193634033203,"y":66.60427448257862}},{"score":0.846885085105896,"part":"leftEar","position":{"x":270.1638229310745,"y":76.80955253037033}},{"score":0.8253374695777893,"part":"rightEar","position":{"x":215.4971279040385,"y":79.85051783699005}},{"score":0.9972171783447266,"part":"leftShoulder","position":{"x":294.22987644774446,"y":134.0850380626634}},{"score":0.9947142004966736,"part":"rightShoulder","position":{"x":198.18224729545386,"y":136.42862360022875}},{"score":0.9901853799819946,"part":"leftElbow","position":{"x":351.56475764768135,"y":205.76526775434323}},{"score":0.9863618612289429,"part":"rightElbow","position":{"x":141.72703291006127,"y":211.0006754240637}},{"score":0.9126535058021545,"part":"leftWrist","position":{"x":399.3205027895679,"y":187.70925226471303}},{"score":0.8435911536216736,"part":"rightWrist","position":{"x":78.16554947493142,"y":188.59593450049016}},{"score":0.9968180060386658,"part":"leftHip","position":{"x":277.9178830157922,"y":301.5186794889576}},{"score":0.9963420629501343,"part":"rightHip","position":{"x":210.51658692712454,"y":302.11120094863355}},{"score":0.9731559753417969,"part":"leftKnee","position":{"x":259.8009160260746,"y":436.2018326933745}},{"score":0.9834533333778381,"part":"rightKnee","position":{"x":213.72068860836998,"y":437.815080338415}},{"score":0.8875550627708435,"part":"leftAnkle","position":{"x":241.32726145347272,"y":534.7006273084113}},{"score":0.9102204442024231,"part":"rightAnkle","position":{"x":220.18303819945817,"y":531.4041459495455}}]}
#json = {"model":"2","score": 0.8103751681525918, "keypoints": [{ "score": 0.9538564682006836, "part": "nose", "position": { "x": 252.08697052595681, "y": 89.82591204513372 } }, { "score": 0.0284572746604681, "part": "leftEye", "position": { "x": 251.43362438632357, "y": 82.88001945881528 } }, { "score": 0.960119366645813, "part": "rightEye", "position": { "x": 249.37345245005093, "y": 79.72328665469871 } }, { "score": 0.01722041890025139, "part": "leftEar", "position": { "x": 210.78634993853734, "y": 84.18502706683563 } }, { "score": 0.992445170879364, "part": "rightEar", "position": { "x": 229.78838345420036, "y": 86.8001380653233 } }, { "score": 0.9743292331695557, "part": "leftShoulder", "position": { "x": 214.6863499504119, "y": 137.31467123068722 } }, { "score": 0.9913697838783264, "part": "rightShoulder", "position": { "x": 200.35650848507416, "y": 144.291925155699 } }, { "score": 0.5800746083259583, "part": "leftElbow", "position": { "x": 251.78372970165447, "y": 199.48550043959563 } }, { "score": 0.9921643733978271, "part": "rightElbow", "position": { "x": 209.17026291190416, "y": 230.90635954266855 } }, { "score": 0.3508157432079315, "part": "leftWrist", "position": { "x": 232.5461206695913, "y": 302.3669672272085 } }, { "score": 0.9940073490142822, "part": "rightWrist", "position": { "x": 213.3907403018224, "y": 311.6935300121975 } }, { "score": 0.9860791563987732, "part": "leftHip", "position": { "x": 238.1198763717473, "y": 274.6938611932302 } }, { "score": 0.9974567294120789, "part": "rightHip", "position": { "x": 199.60804107309778, "y": 283.4536782943785 } }, { "score": 0.9782775044441223, "part": "leftKnee", "position": { "x": 317.7167778757296, "y": 326.2723965180987 } }, { "score": 0.9887549877166748, "part": "rightKnee", "position": { "x": 156.3756455595855, "y": 379.63384309167526 } }, { "score": 0.9960874319076538, "part": "leftAnkle", "position": { "x": 261.5093228826263, "y": 433.172862368335 } }, { "score": 0.9948622584342957, "part": "rightAnkle", "position": { "x": 49.28123367250197, "y": 390.13385597555555 } }] }
json = {"model":"2","score": 0.9937738951514749, "keypoints": [{ "score": 0.9991373419761658, "part": "nose", "position": { "x": 118.29286526334886, "y": 54.76203839788177 } }, { "score": 0.9984309077262878, "part": "leftEye", "position": { "x": 126.33321775443818, "y": 45.61005009751375 } }, { "score": 0.9994140863418579, "part": "rightEye", "position": { "x": 106.82093306367034, "y": 45.87777614222426 } }, { "score": 0.9675434827804565, "part": "leftEar", "position": { "x": 141.50473366822712, "y": 55.57304092140049 } }, { "score": 0.9882251024246216, "part": "rightEar", "position": { "x": 90.34374810007293, "y": 59.55319495887608 } }, { "score": 0.9890862703323364, "part": "leftShoulder", "position": { "x": 162.71684413568516, "y": 110.78463322086556 } }, { "score": 0.9985117316246033, "part": "rightShoulder", "position": { "x": 65.36846312289106, "y": 109.88876967671315 } }, { "score": 0.9990621209144592, "part": "leftElbow", "position": { "x": 197.81159527849127, "y": 144.3189953458912 } }, { "score": 0.9994192123413086, "part": "rightElbow", "position": { "x": 36.11400880331195, "y": 158.61749858336688 } }, { "score": 0.982377290725708, "part": "leftWrist", "position": { "x": 142.7559058044671, "y": 151.4089044058833 } }, { "score": 0.98646080493927, "part": "rightWrist", "position": { "x": 97.02103055961396, "y": 154.84164574174102 } }, { "score": 0.9971152544021606, "part": "leftHip", "position": { "x": 144.47033489539, "y": 257.8663349967986 } }, { "score": 0.9970376491546631, "part": "rightHip", "position": { "x": 89.03736547922807, "y": 254.4988439240808 } }, { "score": 0.9985045194625854, "part": "leftKnee", "position": { "x": 147.4423748565555, "y": 380.52951144801034 } }, { "score": 0.9959707260131836, "part": "rightKnee", "position": { "x": 84.49819076478713, "y": 383.21137691750135 } }, { "score": 0.9990654587745667, "part": "leftAnkle", "position": { "x": 149.99576435014893, "y": 496.2777033111928 } }, { "score": 0.9987942576408386, "part": "rightAnkle", "position": { "x": 71.63306919795528, "y": 496.65954678902824 } }] }
compare(json)
