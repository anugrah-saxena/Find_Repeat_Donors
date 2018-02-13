##
# Author: Anugrah Saxena
# Version: 0.1v
# Date: February 12, 2018
# Task: This program finds out the Repeat Donors for the political candidates using the Federal Election Commission (FEC) data
# Submitted to: Insight Fellowship Coding Challenge
##

# Import required libraries
import sys
import re
import math
from datetime import datetime

# The method receives the percentile given by the program and a sorted list of contributions.
# It returns the percentile contribution based on nearest-rank algorithm

###################################################
# NOTE											  #
#    											  #
# I was planning to use a List of Dictionaries	  #
# But for some reason it was not working out      #
# So i am submitting this not so correct result   #
# without consideration of different recipients.  #
# Original plan was to have different data lists  #
# for each recipient and then next look for year. #
#    											  #
###################################################

def getPercentileValue(p,list):
	index = math.ceil(p*len(list)/100)
	return list[index-1]

# This method gives the cummulative amount of all the contributions made to the politician
def getSum(list):
	return sum(list)

# This method returns the total transactions received by the politician
def getTransactions(list):
	return len(list)

# This method checks if the name of the donor is valid or not.
# The name might be just a first or last name or both. In the later case it being separated by comma.
# Nothing apart from alphabets are assumed to be part of the name + ','
def isValidName(name):
	name_pattern=re.compile(r"[A-Za-z ]+(, )?[A-Za-z ]+")
	name_match=(name_pattern.match(name)).group(0)
	if name!=name_match:
  		return False
	else:
  		return True

# This method utilized the datetime library to check whether the date is correct or not
def isValidDate(date):
    try:
        if date != datetime.strptime(date, "%m%d%Y").strftime('%m%d%Y'):
            raise ValueError
        return True
    except ValueError:
        return False

# This method checks if the streaming transaction is valid or not. It finds different variables from the transition words.
# If the OTHER_ID is empty, and CMTE_ID, TRANS_AMT are not empty (assuming amount string is a number).
# It also checks for validity of TRANS_DT and NAME.
# If invalid it returns a dictionary with vaild field marked as False, otherwise True and sends other required variables to the main method.
def isValidRecord(words):
	dict = {}
	dict['valid'] = False

	dict['OTHER_ID'] = words[15]
	if dict['OTHER_ID']:
		return dict

	dict['CMTE_ID'] = words[0]
	dict['NAME'] = words[7]
	dict['ZIP_CODE'] = words[10]
	dict['TRANS_DT'] = words[13]
	dict['TRANS_AMT'] = words[14]

	if all([dict['CMTE_ID'], dict['NAME'], dict['ZIP_CODE'], dict['TRANS_DT'], dict['TRANS_AMT']]):
		if len(dict['ZIP_CODE']) < 5:
			dict['valid'] = False
			return dict

		if not isValidName(dict['NAME']):
		  dict['valid'] = False
		  return dict

		if len(dict['TRANS_DT']) > 8:
			dict['valid'] = False
			return dict

		if not isValidDate(dict['TRANS_DT']):
			dict['valid'] = False
			return dict

		dict['valid'] = True
	else:
		dict['valid'] = False
		return dict
	return dict

if __name__ == "__main__":
	#	Reads the percentile from the Input directory
	percentile = open(sys.argv[2],'r')
	percent=int(percentile.read())

	# Reads the streaming data
	with open(sys.argv[1],'r') as donations:
		data = donations.readlines()

	# File to write the repeat donors
	repeat = open(sys.argv[3],'w')
	# Set to identify if the donor already donated in the previous years
	donors = set()
	# To maintain a sorted list of donation amounts for further calculations
	l = []

	# Going through each transaction line by line
	for lines in data:
		# Identifying each component using Regular Expression
		words = lines.split("|")

		# Check for validity of Transaction
		if (isValidRecord(words))['valid']:
			CMTE_ID = words[0]
			NAME = words[7]
			ZIP_CODE = (words[10])[:5]
			TRANS_DT = words[13]
			TRANS_AMT = int(words[14])
			OTHER_ID = words[15]

			# Create a Unique Donor ID using Name and Zipcode
			UNIQUE_DONOR = NAME+ZIP_CODE

			# Check if donor already present in HashSet, add if not
			if UNIQUE_DONOR not in donors:
				donors.add(UNIQUE_DONOR)
			# Add repeat donor information to List and calculate Percentile and other information and save it in the Repeat_Donor file 
			else:
				l.append(TRANS_AMT)
				l.sort()
				new_rec = "{}|{}|{}|{}|{}|{}\n".format(CMTE_ID,ZIP_CODE,TRANS_DT[4:],getPercentileValue(percent,l),getSum(l),getTransactions(l))
				repeat.write(new_rec)

	# Close all files
	repeat.close()
	percentile.close()
	donations.close()
