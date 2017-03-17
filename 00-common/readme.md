## Data Description

### Datasets
1. **YouseePlay\_stream\_data:**
	* Original data from the YouseePlay streaming platform
<a name="dataset_2"></a>
2. **10\_percent\_with\_time\_fields\_clean\_genres:**
	* Several columns have been removed
	* 80 to 90 percentile of users with most movie transactions
	* Timestamps have been deserialized into two new fields: **DayOfWeek** and **HourOfDay**
	* For all movies with no defined genre, a genre "**unknown**" has been added
	* Genres for adult movies have all been combined into one genre "**adult**"
	* Scripts to run to produce this set:
		1. `python prune-columns-and-series.py YouseePlay_stream_data.< zip | csv >`
		2. `python prune_80_90.py no_serier_pruned_columns_10_percent. < zip | csv >`
		3. `python add_time_fields.py no_serier_pruned_columns_10_percent.< zip |csv >`
		4. `python genres-clean.py 10_percent_with_time_fields.< zip |csv >`

### Training and Test sets
1. **10\_percent\_clean\_v01\_< train | test >:**
	* Training and test sets in a 70/30 distribution based on dataset [2](#dataset_2)

### Bash Sorting of File
This sorts `in_file` based on the whole line and outputs the result to `out_file`:
`
export in_file="some_input.csv" ; export out_file="some_output.csv" ; head -n1 $in_file > $out_file ; tail -n+2 $in_file | sort >> $out_file
`
