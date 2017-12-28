#!/usr/bin/env python3
from __future__ import print_function

import os
import sys
import re
import click
import subprocess
import time
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl

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


def progress_bar(i, total, size=30, char1='#', char2='-'):
    progress = float(i)/total
    filled = int(progress*size)
    str = ''.join([char1]*filled)
    str += ''.join([char2]*(size-filled))
    return str
    
        
@click.command()
@click.option('--output', '-o', default='wordcount.csv', help="Save word count data")
@click.option('--plot', is_flag=True, default=False, help="Plot figure")
@click.option('--count', is_flag=True, default=False, help="Count current folder")
@click.option('--save_fig', '-s', default='wordcount.png', help="Save figure")
@click.option('--path', '-p', default='./', help="Path to git repository")
def main(output, plot, save_fig, path, count):
    FNULL = open(os.devnull, 'w')

    
    if count:
        count = tex_word_count(path=path, skip_commands=True)
        print (count)
        return
    
    cwd = os.path.dirname(path)
    isRepo = False
    # Verifies if it is a git repository to iterate over commits
    try:
        data = subprocess.call(["git", "stash",], stdout=FNULL, stderr=subprocess.STDOUT)
        data = subprocess.call(["git", "checkout", "master"], stdout=FNULL, stderr=subprocess.STDOUT)

        isRepo = True
        #print('Is repo')
    except subprocess.CalledProcessError as e:
        #print e.output
        data = -1
        isRepo = False
        return

    # Gets commit hashes
    data = subprocess.check_output(["git", "log", "--pretty=%H"], cwd=cwd, ).decode("utf-8") 
    commit_list = str(data).split('\n')

    # Gets commit timestamps
    data = subprocess.check_output(["git", "log", "--pretty=%ct"], cwd=cwd, ).decode("utf-8") 
    date_list = str(data).split('\n')
    valididx = [d != '' for d in date_list]
    date_list = [date_list[i] for i in range(len(date_list)) if valididx[i] ]
    commit_list = [commit_list[i] for i in range(len(commit_list)) if valididx[i] ]
    
    datestr_list = []
    for i in range(len(date_list)):
        datestr_list.append(datetime.datetime.fromtimestamp(float(date_list[i])))

        
    total = len(date_list)
    print("Total commits: %d"%(total))

    count_list = []
    for i, (commit, date) in enumerate(zip(commit_list,date_list)):

        #p = subprocess.Popen(["git", "checkout", commit], cwd=cwd, stdout=subprocess.PIPE)
        p = subprocess.Popen(["git", "checkout", commit], cwd=cwd, 
                             stdout=FNULL, stderr=subprocess.STDOUT)
        path = cwd

        # Waits 100 ms for checkout to finish
        time.sleep(0.1)
        count = tex_word_count(path=path, skip_commands=True)
        count_list.append(count)
        progress = progress_bar(i, total)
        #strdate = datetime.datetime.fromtimestamp(float(date) )
        print("\r Commit %4d of %4d [%s] %s Word count: %d"%( i, total,progress,datestr_list[i],count), 
              end="")
        sys.stdout.flush()

    data = subprocess.call(["git", "checkout", "master"], stdout=FNULL, stderr=subprocess.STDOUT)

    print("")

    data_list = {'commit':commit_list,
                    'date':datestr_list,
                    'timestamp':date_list,
                    'wordcount':count_list}
    df = pd.DataFrame(data=data_list, ).set_index('date')
    
    df.to_csv(output)
    print("Saved data to %s"%(output))
    

    plt.plot(df['wordcount'])
    plt.gca().yaxis.set_major_formatter(mpl.ticker.StrMethodFormatter('{x:,.0f}'))
    plt.ylabel('Word count')
    plt.savefig(save_fig)    
    plt.show()
    
    return data_list


if __name__ == "__main__":

    
    main()
    
    
#    path = sys.argv[0]
#    path = '.'
#    
#    if len(sys.argv) >1:
#        path = sys.argv[1]

#    count = tex_word_count( path=path)
#    print(count)
    
#    date_list2 = date_list.copy()
#    for i in range(len(date_list)-1):
#        date_list2[i] = datetime.strptime(date_list2[i], "%c %z")
#        pass

#    plt.plot(date_list2[:],count_list[:])
#    plt.gca().yaxis.set_major_formatter(mpl.ticker.StrMethodFormatter('{x:,.0f}'))

#    plt.ylabel('Word count')
#    plt.savefig('word-count.png')
    