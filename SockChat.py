import os

def choice():


	print ("would you like to CREATE or JOIN a chat room?")
	print ("1. Create")
	print ("2. Join")
	print ("")
	answer = input(">> ")

	if answer == "Join" or answer == "join" or answer == "2":
		os.system("python client.py")

	elif answer == "Create" or answer == "create" or answer == "1":
		os.system("python server.py")

	else:
		print ("That is not a valid answer, please try again")
		print ("")
		print ("")
		choice()


choice()
