#TapSearchAPI

Task done for TapChief Intern SDE.  
Tools used:  
Programming Language - Python  
Web Framework - Flask  
Deployed at :
  
## Features  
- Accepts Text with two new lines character (\n\n) as breaking/distinguishing character.
- Takes multiple PDF files and indexes them. Same rule as above.
- Takes images of format (.png, .jpg, .jpeg) and indexes them.
- Search. Enter a keyword to look at the top results. Sorted by frequency of keyword occurrence. Also Frequency is displayed at result page.
- Clear. Allows you to clear the both the files stored and also the InvertedIndex. Basically a restart.
- View Index. Displays a table of terms and document sources, along with the paragraph ID of occurence.
    - However, indexes are generally huge. And in my case, the index is a HashMap of terms, so displaying this on HTML can be hard on the browser if number of terms if huge. It will load the whole index currently, with no temporary breaks.

##Results
- Inverted Indexer built for indexing and fast searching of text keywords.
- Currently supports search for only one keyword. But that search in itself is almost instantaneous.
- A few test runs - 
    * Text ~1100 words split in 6 paragraphs. (Is randomly generated online)
        * Indexing Duration - 0.11173829999998475 sec
        * Search for keyword 'can' Duration - 0.00036920000002282904 sec
    * PDF plain only text no other visual elements included.
        * 
    * PDF with visual elements, code blocks, embeds, etc present.
        * File  sizes: total 30,149 KB (852, 22492, 6805)
        * Indexing Duration: 58 sec (0.85, 45.19, 12.55)
        * InvertedIndex contains ~30k terms and 5172 documents/paragraphs
        * Search for keyword 'two' - 0.000360399999923611 sec
        * Search for keyword 'machine' - 0.0003675000000384898 sec
        * Search for keyword 'recursion' - 0.0003510000000233049 sec

##Key Notes:
- PDF parsing heavily depends on the pdf content. If a plain PDF is given, it is guaranteed to be quick on lines of (0.1 sec/page)
- Images are decoded to Base64 string format and sent to GoogleCloud for processing. 
- Previous attempts of deploying self-trained ML model failed due to the core trained model being very big size (~1.2 GB). Training samples were MNIST as standard training set, with additional normal training set. This was slow and chunky. Further prospects would be deploying a custom made lightweight ML model maybe through Tensorflow.JS
- Visual elements were not focused upon, so the whole project might look as if it were from 90's.
 
        
        
