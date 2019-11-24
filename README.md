# TapSearchAPI

Task done for TapChief Intern SDE.  
Tools used:  
Programming Language - Python  
Web Framework - Flask  
Deployed at : [https://tap-search-api-py.herokuapp.com](https://tap-search-api-py.herokuapp.com)
  
## Features  
- Accepts Text with two new lines character (\n\n) as breaking/distinguishing character.
- Takes multiple PDF files and indexes them. Same rule as above.
- Takes multiple images of format (.png, .jpg, .jpeg) and indexes them.
- Search. Enter a keyword to look at the top results. Sorted by frequency of keyword occurrence. Also Frequency is displayed at result page.
- Clear. Allows you to clear the both the files stored and also the InvertedIndex. Basically a restart.
- View Index. Displays a table of terms and document sources, along with the paragraph ID of occurence.
    - However, indexes are generally huge. And in my case, the index is a HashMap of terms, so displaying this on HTML can be hard on the browser if number of terms if huge. It will load the whole index currently, with no temporary breaks.

## Results
- **The time delays between the redirections of each webpage is bit higher than the messaeg passing in the cloud deployment. So, due to this reason there maybe no results in "Search" or "ViewIndex" calls sometimes. Reiterating the search or request can help. I tried fixing this in different ways, but it broke the app more.**
- Inverted Indexer built for indexing and fast searching of text keywords.
- Currently supports search for only one keyword. But that search in itself is almost instantaneous.
- A few test runs - 
    * Text Only input ~1100 words split in 6 paragraphs. (Is randomly generated online)
        * Indexing Duration - 0.11173829999998475 sec
        * Search for keyword 'can' Duration - 0.00036920000002282904 sec  
        
    * PDF plain only text no other visual elements included.
        * File total size: 452 KB (113, 145, 194) KB
        * Indexing Duration - 0.18611084643316556 sec
        * Search for keyword 'many' - 0.00034557435080165 sec
        * Search for keyword 'thoughts' - 0.0006357463503780 sec  
        
    * PDF with visual elements, code blocks, embeds, etc present.
        * File  sizes: total 30,149 KB (852, 22492, 6805) KB
        * Indexing Duration: 58 sec (0.85, 45.19, 12.55)
        * InvertedIndex contains ~30k terms and 5172 documents/paragraphs
        * Search for keyword 'two' - 0.000360399999923611 sec
        * Search for keyword 'machine' - 0.0003675000000384898 sec
        * Search for keyword 'recursion' - 0.0003510000000233049 sec  
        
    * Images with multiple text blocks (3, 5, 2) and are of Times New Roman font and varying font sizes.
        * Images are PNG format, and sized total 153 KB (76, 29, 48)
        * Time taken for upload + GCP API Call + Indexing - 0.0037941398099064827 sec‬(0.002126180101186037, 0.0017215709667652845, 0.0018599508330225945)
        * Search similar and no different to others as, well it uses the same InvertedIndex and methods to search.  
          
## Project Structure & Code:
- Code is split into Frontend and some mini-processing and "backend" or the core of the project.   

config -- GCP Auth Key  
files -- contains the uploaded content (pdf + images)  
templates -- HTML documents  
app.py -- Entry point to the project. Runs from here.
IndexClass.py -- InvertedIndex and its overlying methods are implemented here.  

- IndexClass where methods are implemented are commented and for most parts modularity is maintained.
- Overall, the project seems to be running well, with almost no bugs (except for missing features mentioned below)

  
## Key Notes:
- PDF parsing heavily depends on the pdf content. If a plain PDF is given, it is guaranteed to be quick on lines of (0.1 sec/page)
- Images are decoded to Base64 string format and sent to GoogleCloud for processing. 
- Previous attempts of deploying self-trained ML model failed due to the core trained model being very big size (~1.2 GB). Training samples were MNIST as standard training set, with additional normal training set. This was slow and chunky. Further prospects would be deploying a custom made lightweight ML model maybe through Tensorflow.JS
- Visual elements were not focused upon, so the whole project might look as if it were from 90's.
-Images even if they were to have paragraphs in them, GCP Vision API doesn't return same text composition rather a complex of words possible for each word. This makes this part of the API a bit hard to process.
        
## Futher Improvements:
- To improve image processing in the task. The problem with GCP Vision is that it returns a rough estimated map of where the text could have been. Also it doesn't consider the composure of paragraphs. For that improvement look at [This Discussion](https://stackoverflow.com/questions/42325484/how-to-split-an-image-into-clean-paragraphs-in-python-opencv)
- I also consider the PDF Parser to be very slow and is a generic purposed text praser maybe (?). So, implementing a parser  for PDF would also take top priority.
- Change the language of implementation. Most of the code should scale down by factor of 10 if used functional programming.
