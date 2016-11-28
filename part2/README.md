# Part 2: Problem Statement + EDA

### Articulate “Specific aim”
The end goal of this project is to perform text-based clustering on ~217,000 Jeopardy questions and answers, in order to break them down into more broadly defined "categories", rather than the hundreds of individual categories given on the show.

I've taken some inspiration for this project from [this talk](https://vimeo.com/29001512) by former Jeopardy! champion Roger Craig, a data scientist who used clustering to create a web app to help himself prepare for the show, and then became hugely successful on the show, including setting the single game record for most money won.


### Outline proposed methods and models
I

There are a variety of resources on text-based clustering in Python that I've looked at, [here](http://brandonrose.org/clustering) is one very thorough example that I think will be very useful.


### Define risks & assumptions
The dataset is not a complete record of every single Jeopardy question asked. The j-archive.com website is missing some shows.


### Revise initial goals & success criteria, as needed
I'm not sure what specific success criteria are for an unstructured learning problem like clusting.


### Create local database
A database isn't necessary for this project, my data .csv is stored in the data folder.


### Describe data cleaning/munging techniques
The data was fairly clean to start out with. All I really did was clean up the "Value" column by removing commas and $'s, fill in NaNs for the Final Jeopardy! questions, and convert to a numeric type.


### Create a data dictionary
Show Number - The show number on the j-archive.com website, not necessarily the overall show number (there are some episodes missing from the archive)

Air Date - Original air date of the question

Round - Round the question was asked in (ie: Jeopardy!, Double Jeopardy!, Final Jeopardy!, or (rarely) Tiebreaker)

Category - The category of the question

Value - The amount the question is worth. For Daily Doubles, this number can vary, depending on what value the contestant chose to wager. For Final Jeopardy!, this field is 'None'.

Question - The text of the question. I'm defining the "Question" as what was asked by the host, not the answer given in the form of a question.

Answer - The correct answer to the question.


### Perform & summarize EDA
EDA is in the data_exploring.ipynb file. I created some basic graphs histograms, did some simple word counting of the text columns of my dataset, and started messing with the CountVectorizer function.