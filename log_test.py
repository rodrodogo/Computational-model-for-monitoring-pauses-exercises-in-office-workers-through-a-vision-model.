
def print_name(name):
	f= open("log_prueba.txt","a+")
	f.write(("\nname {0}\n\n").format(name))
	f.close()

	f= open("log_sqrt.txt","a+")
	f.write(("\nname {0}\n\n").format(name))
	f.close()

	f= open("log_max","a+")
	f.write(("\nname {0}\n\n").format(name))
	f.close()


def print_error(sqrt_error, error_between_points):
	f= open("log_prueba.txt","a+")
	f.write("mean_squared_error : " + sqrt_error +"\n")
	f.close()

	f= open("log_sqrt.txt","a+")
	f.write(("{0}\n").format(sqrt_error))
	f.close()


def print_result_pose( valor ,result, exercise):
	f= open("log_prueba.txt","a+")
	f.write("\nPose done : " + result+ "; with value: "+valor +" ; In excercise:  " + exercise + "\n\n")
	f.close()

	f= open("log_max.txt","a+")
	f.write(("{0}\n").format(valor))
	f.close()


