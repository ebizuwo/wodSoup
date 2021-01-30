import sys
import os
from parseHtml import parser




# function to make api call

# function to parse html

# function to manipulate and save dataframe

BASE_PATH = 'html'

def run_app(fname):
    fpath = os.path.join(BASE_PATH, fname)
    # returns soup object
    parser(fpath)


    return




if __name__ == '__main__':
    args = sys.argv
    print(args[1])
    fname = args[1]
    run_app(fname)


