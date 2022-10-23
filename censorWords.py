"""
This program defines the following methods:

replace_with_char,
censor_word_in_line,
censor_whole_word_in_line,
cleanse_file

#####################################
replace_with_char is a simple method that replaces characters in a string with your supplied character

#####################################
censor_word_in_line searches a string for a given word and then calls replace_with_char

#####################################
censor_whole_word_in_line is just like censor_word_in_line but calls from a defined list of delimiters to
prevent replacing partial words.

## For example ##

censor_word_in_line("sun", "You are my sunshine", "*") would return "You are my ***shine" -- partial word censored
censor_whole_word_in_line("sun", "You are my sunshine", "*") would return "You are my sunshine" -- no censorship

#####################################
case_insensitive_mode is an input for either censor method that enables checking for different capitalizations of the censored word.

## For example ##

censor_word_in_line("friend", "I hate the show Friends", "*", case_insensitive_mode=False) would return "I hate the show Friends"
censor_word_in_line("friend", "I hate the show Friends", "*", case_insensitive_mode=True) would return "I hate the show ******s"

#####################################
cleanse_file takes:

    a file path and name as a string for:
        input text file,
        a list of censored words text file,
        an output text file to write to,
    
    and whether to run as case_insensitive_mode and whole_word_mode

    whole_word_mode just selects whether to censor each word with censor_word_in_line or censor_whole_word_in_line

#####################################
this project includes an inputText that was found on reddit.com/r/nosleep.
I honestly haven't read it, so I apologize if there's anything in the story that is triggering.

At the end of this program is a call to cleanse_file with the local input / censor list references

Try playing with different input combinations and censored words in the censoredWords.txt file!

"""

def replace_with_char(source: str, start_index: int, length: int, char: str) -> str:

    # all characters before replace word
    rv = source[:start_index]

    # insert char for length times
    for _ in range(length):
        rv += char

    # all characters after replaced word
    rv += source[(start_index + length):]

    return rv

# scans line for censored word and replaces with something else
# returns: bool, int, str: whether the word was found, the index in the line where the word was found, and the new string
# if the word isn't found, bool is false, the index returned is None, and the string is unchanged
# set case_insensitive_mode if you want to search for the censored word with any capitalization
def censor_word_in_line(
    cword : str,
    line : str,
    censor_char: str,
    case_insensitive_mode: bool = False
) -> tuple[bool, int, str]:

    (check_word, check_line) = (cword.lower(), line.lower()) if case_insensitive_mode else (cword, line)

    # check if the cword is in the line
    if check_word in check_line:

        # if it is, get the position in the line where the censored word starts
        cIndex = check_line.index(check_word)

        # replace the letters for the censored word with "*"
        line = replace_with_char(line, cIndex, len(cword), censor_char)
        
        # the word has been replaced
        return True, cIndex, line
    
    # if the word wasn't found, return
    else:
        return False, None, line

# It's only a whole word if the character before and after the censwored word is in this list
WHOLE_WORD_DELIMIETERS = [
    " ",
    "\"",
    "\/",
    "\\",
    ".",
    ","
]

# works just like censor_word_in_line but only replaces the censored word if it's the WHOLE word
def censor_whole_word_in_line(
    cword : str,
    line : str,
    censor_char: str,
    case_insensitive_mode: bool = False
) -> tuple[bool, int, str]:

    # check every combination of delimiter before and after censored word
    for i in WHOLE_WORD_DELIMIETERS:
        for j in WHOLE_WORD_DELIMIETERS:   

            (check_word, check_line) = (cword.lower(), line.lower()) if case_insensitive_mode else (cword, line)

            whole_cword = i + check_word + j

            if whole_cword in check_line:

                cIndex = check_line.index(whole_cword) + 1 # Plus one because the first character is " ", "/", "/", etc.

                line = replace_with_char(line, cIndex, len(cword), censor_char)

                return True, cIndex, line
        
    return False, None, line

def cleanse_file(
    cwordFile : str,
    inputFile : str,
    outputFile : str,
    whole_word_mode : bool = False,
    case_insensitive_mode : bool = False
) -> int:

    censored_count = 0

    cwords = []

    print("parsing c words from censoredWords.txt...\n")
    with open(cwordFile, 'r') as f_cword:
        for line in f_cword:
            cwords.append(line.split('\n')[0]) # splitting on new line and getting index 0 removes the newline from the cword
            print(cwords[-1]) # print the most recently appended
    print()
    
    print(f"opening input file...\n")
    with open(inputFile, 'r') as f_in:
        input_lines = f_in.readlines()

    output_lines = []

    for i, line in enumerate(input_lines):

        # Remove all instances of each cword, one cword at a time, one line at a time
        for cword in cwords:
            
            filthy = True
            while filthy:
                
                if whole_word_mode:
                    filthy, index, line = censor_whole_word_in_line(
                        cword= cword,
                        line= line,
                        censor_char= "*",
                        case_insensitive_mode=case_insensitive_mode
                    )
                else:
                    filthy, index, line = censor_word_in_line(
                        cword= cword,
                        line= line,
                        censor_char= "*",
                        case_insensitive_mode=case_insensitive_mode
                    )
                if filthy:
                    print(f"{cword} found on line {i + 1} at index {index}") # plus one because inputText starts lines at 1
                    censored_count += 1
        
        output_lines.append(line)
    
    with open(outputFile, 'w') as f_out:
        for line in output_lines:
            f_out.write(line)
    
    return censored_count


if __name__ == "__main__":
    naughty_count = cleanse_file(
        cwordFile= "censoredWords.txt",
        inputFile= "inputText.txt",
        outputFile= "outputText.txt",
        whole_word_mode=True,
        case_insensitive_mode=True
    )

    print(f"\n\n\nFound this many naughty words: {naughty_count}")