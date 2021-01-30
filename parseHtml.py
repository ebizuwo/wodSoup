from bs4 import BeautifulSoup

def make_bs4_soup(fpath):
    with open(fpath, 'r') as f:
        contents = f.read()
        soup = BeautifulSoup(contents, 'lxml')
        return soup

def get_data(fpath):
    #extract necessary html
    data_description = {
        'col1': None,
        'col3': None,
    }
    workouts = []
    soup = make_bs4_soup(fpath)
    print(soup)
    print(soup.h2)
    print(soup.head)
    print(soup.li)
    return data

def make_dataframe(data):
    print(data)

def parser(fpath):
    """
    :param: None
    :return:
    The list of tags as map
    """
    print("I am a parser")
    data = get_data(fpath)
    dataframe = make_dataframe(data)