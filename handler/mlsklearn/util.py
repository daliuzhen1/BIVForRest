import json  
def regqeust_arg_to_sklearn_arg(reqeust_sklearn_arg, sklearn_arg_list):
	sklearn_arg = {}
	for regqeust_arg_key in reqeust_sklearn_arg:
		if regqeust_arg_key in sklearn_arg_list:
			argvalue = reqeust_sklearn_arg.get(regqeust_arg_key)
			sklearn_arg[regqeust_arg_key] = argvalue
	print(sklearn_arg)
	return sklearn_arg

def check_arg_valid(reqeust_sklearn_arg, sklearn_arg_list, clf):
	sklearn_arg = {}
	reqeust_sklearn_arg = reqeust_sklearn_arg.split(",")
	for regqeust_arg_key in reqeust_sklearn_arg:
		if regqeust_arg_key not in sklearn_arg_list:
			return False
	return True