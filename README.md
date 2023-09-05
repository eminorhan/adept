## ADEPT data & evaluation tools 

The [videos](https://github.com/eminorhan/adept/tree/master/videos) directory contains the ADEPT training and test data in video format (`.mp4`). You can use the [measure_accuracy.py]() to calculate the absolute and relative accuracies of a model. Example usage:
```python
python -u measure_accuracy.py \
	--summary_file 'demo_scores.json' \
	--output_folder OUTPUT_FOLDER
```
where `summary_file` is a `json` file that should contain the scores assigned by the model to each test trial. An example `summary_file` is provided in [`demo_scores.json`](https://github.com/eminorhan/adept/blob/master/demo_scores.json).

The code here is mostly recycled from the original [ADEPT dataset](https://github.com/JerryLingjieMei/ADEPT-Dataset-Release) repository.