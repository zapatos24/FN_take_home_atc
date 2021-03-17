# Parsing Awards for Legislative Districts

The goal is, given a list of legislators, and access to the NIH awards api, can we develop a database that connects
legislators to the scientific advancements that are happening in their congressional district.

There are two main files in use. The first is ```award_api.py``` which houses the NIHAwardAPI class. This is a
collection of functions that, given a dictionary of parameters, will iteratively call the API to assemble a list of
dictionaries in a variable associated with the instantiated class.

The ```main.py``` file instantiates the api object, and starts the calling process to assemble all awards that 
match the parameters of the passed dictionary. It then takes the list of dictionaries generated by the api object 
and turns it into a pandas dataframe. That dataframe is joined with the previously generated ```legislators.csv``` 
file (after some minor readability improvements) to create the full dataframe of all legislators alongside the NIH
projects in their district for the 2019 fiscal year.

To run the script, make sure you have Python installed (this was developed using 3.9, but should work fine for
previous versions) and navigate to the folder in your terminal. Run the following

```pip install -r requirements.txt```

to ensure you have all necessary libraries installed (though all you need are pandas and requests).

Next, run

```python main.py```

to begin the process. It can take around 10 minutes to parse through the 20K some awards that exist for this
instance of the script, but a progress bar should display in your terminal showing you how far along the process
is.

At the end, a new file labeled ```legislators_awards.csv``` will exist in the folder that can be used for further
analysis. The file contains information on:
* State
* Congressional District
* Name of the congressperson
* The congressperson's party affiliation
* Project Number
* Agency
* Title
* Department
* Financial Year
* Total Cost Amount
* Abstract

Caveats:
* A few of the awards pulled from the NIH api had no congressional district associated with them, and as none of them 
were in Vermont or Delaware (who each only have one congressional district) I opted to omit those from the joining
of legislators to awards
* The ```legislators.csv``` file had three repeat districts (though differing names) for individuals who left their
  position representing that district early, either through resignation or death. As such, I omitted those individuals
  from the final csv, as including them would have created ~2500 duplicate awards and could hamper easy data analysis
  down the road.
