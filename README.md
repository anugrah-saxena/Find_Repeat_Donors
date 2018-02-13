To run, just do ./run.sh and it will run the python file.

Approach:
I am using Python 3 for my implementation here.
I have written different method to validate the streaming transaction keeping in mind all the requirements to validate it. I have tested it using various data in person and it passes when desired.
Other major method is getPercentileValue that implements the nearest-neighbor algorithm.

My approach does the following tasks:
	Reads the percentile from the Input directory
	Reads the streaming data
	Creates a HashSet to identify if the donor already donated in the previous years
	Creates a list to maintain a sorted list of donation amounts for further calculations
	Goes through each transaction line by line and first verifies if valid
	Create a Unique Donor ID using Name and Zipcode
	Checks if donor (Unique ID) is already present in HashSet, adds if not
	Adds repeat donor information to List
	Calculates Percentile and other information
	Saves information in desired format in the Repeat_Donor file

To handle incoming streaming data, I would wish to implement a method to create a buffer that will save up the data and the program can read from it by calling some APIs.

The plan to deal with huge data if it is not a streaming data and just from a file will be to read parts of the file in a buffer by using SEEK method, such that if the file cannot be loaded into the memory as a whole, then just use some parts at a time and not load up the whole thing.

Note:
I was planning to use a List of Dictionaries	, but for some reason it was not working out as planned.
So i am submitting this not so correct result without consideration of different recipients.
Original plan was to have different data lists for each recipient and then next look for year.
I could have given it more time, or implemented a hashtable/dictionary of hashtable/dictionary to do a lookup and give the output based on each donor Unique ID and then based on the year. That would have been my ultimate solution.

Author: Anugrah Saxena# Find_Repeat_Donors
