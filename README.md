## Requirements: 
	Python - Version(3.5.4 or higher)
	Libraries - os,pandas,dedupe

## Steps To Follows:
	1. Go to the project directory and then open the terminal and run -
		"python innovacer_task.py"
	2. Intermediate_Output.csv will be generated which shows the records which are matching with the same cluster_Id.
	3. Now run the command -
		"python Final_output.py"
	4. Final output file will be generated

## Sample Input:

	ln				dob			gn	fn 
	Frometa Garo	14/03/1997	M	Vladimir Antonio
	Frometa Garo	14/03/1997	M	Vladimir A
	Frometa			14/03/1997	M	Vladimir
	Frometa G		14/03/1997	M	Vladimir
	Frometa			14/03/1997	M	Vladimir A 
	Frometa G		14/03/1997	M	Vladimir A 

## Sample Output:
	
	ln			dob			gn	fn
	Frometa	G	14/03/1997	F	Vladimir A

### FOR RETRAINING DELETE THE FILE NAMED: 
	csv_example_learned_settings
	csv_example_training.json