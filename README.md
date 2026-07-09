# This is a work in progress. Compatibility has only been verified on a personal linux machine

## Question Bank Trimmer: Generate custom DSAT practice sets
## Current Version: 1.0.0

## Features
* Extracts questions and answers from PDF question banks
* Combines multiple PDFs into a single file and generates searchable JSON catalogs
* Separates catalogs by learning area
* Filters questions by:
  * Learning area
  * Difficulty
  * Skill
* Generates custom practice sets
* Supports command-line usage
  * GUI in development

## Known Issues
* RW cataloging functionality is unreliable

## Obtaining the necessary files
* All necessary files for generating custom question sets are included

### Basic usage:
1. Ensure *Python 3.10.9 or greater* is installed on your machine.
    * The Windows installer can be found [here](https://www.python.org/downloads/release/python-3109/)
    * When installing, ensure that you select the option to add Python to PATH on the initial splash screen.
2. Clone the repository to your machine using your preferred method
3. Install dependencies
    * _Windows Users skip to next_ A requirements.txt file *is* included. To install requirements, run the following in your terminal:
        * pip install -r requirements.txt
    * For Windows:
        * Open PowerShell. You can find it by using: Windows Key > PowerShell
        * Navigate to directory containing the scripts. This is done using the command 'cd'. Tab can be used to autocomplete directories, directories are separated by '\'.
        * Example usage for scripts saved to desktop directory DSAT_trimmer:
            * cd .\Desktop\qbank_trimmer
            * pip install -r requirements.txt\
4. Run the program

### Example usage:
* To generate a custom PDF of 10 math questions:
  * Windows:
    * .\main.py -s math -c 10 --questions-source bank\math_combined_questions.pdf --answers-source solns\math_combined_answers.pdf
  * Two PDFs will be generated in the generated directory, one containing only the questions and another with the relevant solution pages
