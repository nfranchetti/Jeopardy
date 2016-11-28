# Part 2: Problem Statement + EDA

### Articulate “Specific aim”

### Outline proposed methods and models

### Define risks & assumptions

### Revise initial goals & success criteria, as needed

### Create local database
A database isn't necessary for this project, my data .csv is stored in the data folder.

### Describe data cleaning/munging techniques

### Create a data dictionary
Show Number - The show number on the j-archive.com website, not necessarily the overall show number (there are some episodes missing from the archive)
Air Date - Original air date of the question
Round - Round the question was asked in (ie: Jeopardy!, Double Jeopardy!, Final Jeopardy!, or (rarely) Tiebreaker)
Category - The category of the question
Value - The amount the question is worth. For Daily Doubles, this number can vary, depending on what value the contestant chose to wager. For Final Jeopardy!, this field is 'None'.
Question - The text of the question. I'm defining the "Question" as what was asked by the host, not the answer given in the form of a question.
Answer - The correct answer to the question.

### Perform & summarize EDA
EDA is in the data_exploring.ipynb file.