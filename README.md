# Question Bank Trimmer

Generate custom DSAT practice sets from official question banks

Current Version: eMFgenV1.0.2

## Features
* Extracts questions and answers from PDF question banks
* Combines multiple PDFs into a single file and generates searchable JSON catalogs
* Separates catalogs by learning area
* Filters questions by:
  * Learning area
  * Difficulty
  * Skill
* Generates custom practice sets
* Provides both graphical and command line interfaces
  * Some advanced features like catalog generation and PDF consolidation are CLI only. Do not attempt to use these unless you're familiar and comfortable programming

## Known Issues
* RW cataloging functionality is unreliable

## Download

Prebuilt versions are available in the Releases section.

Download the archive matching your operating system:
- Windows
- Linux
- macOS

## Installation (Prebuilt Application)
1. Download the latest release for your operating system.
2. Extract the archive.
3. Run SATQuestionBankTrimmer.

The included resources folder contains required question banks and catalogs. Do not move or rename this folder.

No Python installation is required.

## Usage (GUI)
1. Select the desired question category.
2. Apply filters.
3. Generate a practice set.
4. Review the generated PDF output.

## Troubleshooting
If the application fails to start:
- Make sure the entire folder was extracted.
- Do not move the executable away from the _internal folder.
- Ensure the resources folder is present.

### CLI Usage
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
        * Example usage for scripts saved to desktop directory qbank_trimmer:
            * cd .\Desktop\qbank_trimmer
            * pip install -r requirements.txt\
4. Run the program

### Example usage (CLI Only):
* To generate a custom PDF of 10 math questions:
  * Windows:
    * .\main.py -s math -c 10 --questions-source bank\math_combined_questions.pdf --answers-source solns\math_combined_answers.pdf
  * Two PDFs will be generated in the generated directory, one containing only the questions and another with the relevant solution pages

### Planned updates
* Add mac support
  * If you would like to use the program and you're on mac, contact me or submit a pull request
* Add support for generating sets from multiple learning areas/skills
* Add support for generating practice 'tests' following the same learning area distributions