# Analysis recipe README

This analysis recipe accompanies the following manuscript:

Mathôt, S., van der Linden, L., Grainger, J., & Vitu, F. (in preparation). *The Pupillary Light Response Reflects Eye-movement Preparation*.

Copyright 2013-2014 Sebastiaan Mathôt  
<s.mathot@cogsci.nl>  
<http://www.cogsci.nl/smathot>

## License

- Analysis code is released under a [GNU General Public License 3](https://www.gnu.org/copyleft/gpl.html).
- Data is released under a [Creative Commons Attribution-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-sa/4.0/).

## Usage note

This analysis recipe is provided so that the original analysis can be replicated, and so that further analyses can be performed by third parties with the required expertise. However, there is some fairly heavy scripting involved, which has been written for personal use, relies on custom libraries, and is not extensively documented. Therefore, this analysis recipe is provided *as is*.

## Dependencies

- python
- numpy
- scipy
- matplotlib
- exparser
- R

## Folder structure

- `analyze.py` is the main analysis script.
- `parse.py` is the main data-parsing script that pre-processes the data prior to further analysis.
- `analysis/*.py` is the Python package that contains the actual analysis scripts.
- `EDF/exp1/*.lzma` contains the original `.edf` per-participant data files as recorded by the EyeLink, compressed in `.lzma` format.

The following folders are filled with intermediate files by the analysis scripts, but are not necessary to run the analysis from scratch (and therefore not included in the repository).

- `data/exp1/` will contain the converted data files in `.asc` format.
- `data/` will contain a single parsed data matrix in `.npy` format.
- `output/exp1[.antiBias]/` will contain data summaries in `.csv` format.
- `plots/exp1[.antiBias]/png/` will contain data plots in `.png` format.
- `plots/exp1[.antiBias]/svg/` will contain data plots in `.svg` format.
- `stats/exp1[.antiBias]/` will contain the LME statistics array in `.npy` format.
- `traces/exp1/` will contain the eye-movement sample traces in `.npy` format.

## Analysis recipe

### Convert `.edf` data to `.asc` data

The EyeLink provides `.edf` files as output. These are not easily readable, but can be converted to a text-based `.asc` format, with the utility `edf2asc`.

Command:
	
	edf2asc EDF/exp1/*.edf
	
Input:
	
- Raw EyeLink data in `.edf` format, stored in `EDF/exp1/*.edf`

Output:
	
- Raw EyeLink data in `.asc` format, stored in `data/exp1/*.asc`

### Parse `.asc` data

The `.asc` data is first pre-processed for convenient analysis later on.

Command:

	python parse.py exp1
	
Input:
	
- Raw EyeLink data in `.asc` format, stored in `data/exp1/*.asc`

Output:
	
- Eye-position and pupil-size traces in `.npy` (Numpy) format, stored in `traces/exp1/*.npy`
- Data in spreadsheet form, stored in `data/exp1.data.npy`

### Perform full analysis

The actual analysis is performed by the script `analyze.py`, which takes various optional parameters. The commands below correspond to the analysis as reported in the manuscript. For further details, please refer to the source code of `analyze.py` and `helpers.py`. Note that this script assumes the existence of the folder `stats/exp1` to store intermediate data.
	
Command:

	python analyze.py exp1 checkMissing runStats mainPlots fit posTracePlots
	
Note that `checkMissing` is a required argument. To bypass this operation (debugging only), subsitute `checkMissing` for `-`.
	
Output:
	
- Various plots in `plots/exp1/` 
- Various output files in `output/exp1/`.
- Information printed to the standard output.

To analyze only the subset of trials in which the eyes deviated from the target side, execute the following command:
	
Command:

	python analyze.py exp1.antiBias checkMissing matchBias runStats mainPlots fit posTracePlots
	
This will generate analogous output to the regular analysis, but for only this subset of data and stored in folders called `exp1.antiBias`.
