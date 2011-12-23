
/*
 * find-words.js
 *
 */
 
var gameDict;


 $(document).ready(function() {
        
        // load our dictionary
        loadDict("dict.js");
        
    });

// ajax call to retrive our dictinary  
function loadDict( dictURL )
{
    $.ajax(
    {
        url: dictURL,
        dataType: "json",
        success: function(data)
        {
            
            // Let the rest of the game know
            // that the dictionary is ready
            dictReady(data);
        }
    });
    
} 

// prepere game dictinary
function dictReady(dict)
{
    gameDict = dict;
}

// take user provided letters and find all matching words
function findWords()
{
    cleanSearchResult();
    // get letters, remove none letter characters, and split them into an array
    var lettersArray = $('#letters').val().replace(/\W+/g,"").split("");
    
    $('#jmsg').append("<p>" + "Given letters: "+ lettersArray + "</p>");
    
    var words = findTrieWord(lettersArray, gameDict); 
    displayResult(words);
}

/*
 * Find Trie Word
 * 
 * @param letters
 * @param subTrie
 * @return listOfWords
 **/
function findTrieWord(letters, subTrie)
{
   var subWordList = new Array();
   // go through each node on the same level
   for(var curLetter in subTrie)
       {
           // check if any of our letters match current node letter 
           var matchedLetterPosition = jQuery.inArray(curLetter, letters);
           
           //if we found a match or the node is the end node continue
           //else go to the next node on the same level
           if(matchedLetterPosition != -1 || curLetter === "$")
               {
                   // if given node points to a number
                   if(typeof subTrie[curLetter] === "number")
                       {
                           //we riched the end node so we are done adding to it
                           if(curLetter === "$")
                               subWordList.push("");
                           else
                               subWordList.push(curLetter);
                       }
                   else // this is not the end node so we need to go deeper
                       {
                           //create a copy of our array
                           var lettersCopy = letters.slice();
                           //remove matched letter from the letter list
                           lettersCopy.splice(matchedLetterPosition, 1);
                           
                           // get the end portion of the word recursively
                           var wordListBelow = findTrieWord(lettersCopy, subTrie[curLetter]);
                           
                           // assamble all endings with our current letter 
                           for(var ii in wordListBelow)
                           {
                               //add them to our current letter
                               var tmp = curLetter+wordListBelow[ii];

                               //push all results to the current subWordList
                               subWordList.push(tmp);
                           }
                       }
               }
       }

   // return all available subwords/words
   return subWordList;
}

function displayResult( words )
{
    words.sort(sortByLength);
    for(var ii in words)
        {
            $('#jwords').append("<li><a href='http://www.google.com/search?q=define+"+words[ii] +"' target='_blank'>" + words[ii] + "</a></li>");
        }
}

function sortByLength(first, second)
{
    // longer words first
    return (second.length - first.length);
}

function cleanSearchResult()
{
    $('#jmsg').find('p').remove();
    $('#jwords').find('li').remove();
}