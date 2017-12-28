import os
import re

def remove_tex_comments(line):
    return line.split('%')[0]

def remove_tex_commands(line):
    return line.split('\\')[0]

def skip_inline_equations(line):
    return ' '.join(line.split('$')[::2])


def count_words(line):
    """Counts words in a line """
    r = re.findall("[a-zA-Z_]+", line)
    return len(r)


def file_word_count(filename, 
                    skip_inline=True, 
                    skip_commands=False, 
                    skip_comments=True,
                   **kwargs):
    """
    Counts the words intside the given .tex file
    
    Parameters
    ----------
    filename : string
        Path to filename to open
    skip_inline : boolean
        Skips inline equations
    skip_commands : boolean
        Skips commands, buggy when dealing with inline commands
    skip_comments : boolean
        Skips comments lines
    """
    
    count = 0
    with open(filename) as f:
        for line in f:
            if skip_inline:
                line = skip_inline_equations(line)
            if skip_commands:
                line = remove_tex_commands(line)
            if skip_comments:
                line = remove_tex_comments(line)
            line_count = count_words(line)
            count += line_count
    return count

def list_files(path='.', extension='.tex',**kwargs): 
    """ Returns list of files in path with the given extension"""
    files = os.listdir(path)
    file_list = []
    for name in files:
        if name.endswith(extension):
            file_list.append(os.path.join(path,name))
    return file_list

def tex_word_count(filename=None, path='.',**kwargs):
    
    if filename is None:
        l = list_files(path=path,**kwargs)
        count = 0
        for filename in l:
            count += file_word_count(filename,**kwargs)
        return count
    else:
        count = file_word_count(filename,**kwargs)

        
if __name__ == "__main__":
    import sys
    path = sys.argv[0]
    path = '.'
    if len(sys.argv) >1:
        path = sys.argv[1]

    count = tex_word_count( path=path)
    print(count)
    