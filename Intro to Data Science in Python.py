#---------------------------------------Assignment 1---------------------------------------

# Part A
# Find a list of all of the names in the following string using regex.

import re
def names():
    simple_string = """Amy is 5 years old, and her sister Mary is 2 years old. 
    Ruth and Peter, their parents, have 3 kids."""
    
    # YOUR CODE HERE
    return re.findall('Amy|Mary|Ruth|Peter',simple_string)

    raise NotImplementedError()

# Part B
# The dataset file in assets/grades.txt contains a line separated list of people with their grade in a class. Create a regex to generate a list of just those students who received a B in the course.

import re
def grades():
    with open ("assets/grades.txt", "r") as file:
        grades = file.read()

    # YOUR CODE HERE
    return re.findall("(\w*\s\w*)(?=:\sB)", grades)
    
    raise NotImplementedError()

# Part C
# Consider the standard web log file in assets/logdata.txt. This file records the access a user makes when visiting a web page (like this one!). Each line of the log has the following items:
  # a host (e.g., '146.204.224.152')
  # a user_name (e.g., 'feest6811' note: sometimes the user name is missing! In this case, use '-' as the value for the username.)
  # the time a request was made (e.g., '21/Jun/2019:15:45:24 -0700')
  # the post request type (e.g., 'POST /incentivize HTTP/1.1' note: not everything is a POST!)
  # Your task is to convert this into a list of dictionaries, where each dictionary looks like the following:
  #example_dict = {"host":"146.204.224.152", 
                # "user_name":"feest6811", 
                # "time":"21/Jun/2019:15:45:24 -0700",
                # "request":"POST /incentivize HTTP/1.1"}
        
 import re
def logs():
    with open("assets/logdata.txt", "r") as file:
        logdata = file.read()
    
    # YOUR CODE HERE
    pattern = """
        (?P<host>\d{1,3}[.]\d{1,3}[.]\d{1,3}[.]\d{1,3})
        (.\W*)
        (?P<user_name>[\w-]+(?=\s\[))
        (.*)
        (?P<time>\d{2}\/\w*\/[\d\s\-:]*(?=\]\s))
        (.*)
        (?P<request>(?<=\]\s\").*?(?=\")) """
    
    result = []
    for item in re.finditer(pattern, logdata, re.VERBOSE):
        result.append(item.groupdict())
    return result
    
    raise NotImplementedError()    
