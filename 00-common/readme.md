## Data Description

### Datasets
1. **YouseePlay\_stream\_data.zip:**
	* Original zipped CSV data from the YouseePlay streaming platform
<a name="dataset_2"></a>
* **10\_percent\_with\_time\_fields\_clean\_genres.csv:**
	* Top 80% - 90% of users with most transactions
	* Timestamps have been deserialized into two new fields: **DayOfWeek** and **HourOfDay**
	* Genres for adult movies have all been combined into one genre "**adult**"

### Training and Test sets
* **10\_percent\_clean\_v01\_< train | test >:**
	* Training and test sets in a 70/30 distribution based on dataset [2](#dataset_2)

### Bash Sorting of File
This sorts `<in_file>` based on the whole line:
`
head -n1 <in_file> > <out_file> ; tail -n+2 <in_file> | sort >> <out_file>
`