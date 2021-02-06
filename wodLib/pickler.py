class Picklable:
    def __init__(self, force_build=False, **pickle_kwargs):
        self.pickler = Pickler()
        self.force_build = False
        self.pickle_kwargs = pickle_kwargs
        if self.__check_for_pickle():
            try:
                self.load()
                self.is_pickled = True
            except Exception as e:
                print(e)
                pass
        else:
            print(f'no pickle exists for class {self.__class__.__name__}')
            print(f'object should implement super().save() to save')

    def check_if_force_build(self):
        if self.force_build:
            print(f'{self.__class__.__name__} force_build set to true executing pipeline')
            return True
        else:
            print(f'{self.__class__.__name__} force_build set to false checking for pickle')
            if self.__check_for_pickle():
                print(f'{self.__class__.__name__} pickle is present load pickle and use methods/attributes')
                return False
            else:
                print(f'{self.__class__.__name__} no pickle is present executing pipeline')
                return True

    def __check_for_pickle(self):
        print(f'{self.__class__.__name__} checking for pickle')
        return self.pickler.check_pickle(**self.pickle_kwargs)

    def save(self, obj=None):
        if obj:
            self.pickle_kwargs['obj'] = obj
        else:
            self.pickle_kwargs['obj'] = self.__dict__
        self.pickler.add_pickle(**self.pickle_kwargs)

    def load(self):
        print(f'{self.pickle_kwargs["name"]} loading from existing pickle')
        obj = self.pickler.get_pickle(**self.pickle_kwargs)
        if obj == False:
            print(f'{self.pickle_kwargs["name"]} obj not loaded from file')
        else:
            print(f'loading {self.pickle_kwargs["name"]} from file')
            # return obj
            self.__dict__ = obj


# TODO: Use this to make pickles classes and test picklability
class Child(Picklable):
    def __init__(self, force_build=False):
        pd = PickleDef(self)
        self.pickle_kwargs = pd()
        super().__init__(force_build, **self.pickle_kwargs)

    def pipeline(self):
        if super().check_if_force_build():
            print('build pipeline')
            pass
        else:
            print('not building pipeline')

    def save(self):
        super().save()

    def load(self):
        self.__dict__.update(super(Child, self).load())


class Pickler:
    """
    On Init looks for files in the pickles directory
    Saves file names and creates a pickles definition file
    This allows you to recall your object by name
    """
    def __init__(self):
        self.pickle_def_fname = 'pickledef.json'
        self.pickle_def_path = os.path.join(PICKLE_DIR, self.pickle_def_fname)
        if self.__def_exists():
            self.pickle_defs = self.__get_defs()
        else:
            self.pickle_defs = None
        # self.pickles stores pickles
        self.pickles = {}
        # has the names of the pickle files in the dir
        self.__pickle_files = self.__get_pickle_files()

    def __get_pickle_files(self):
        """
        gets a list of files in the pickles dir
        """
        filenames = []
        for file in os.listdir(PICKLE_DIR):
            if file.endswith('.pkl'):
                filenames.extend(file)
        # make some logic as this will not throw errors if files are empty
        if len(filenames) == 0:
            return None
        else:
            return filenames

    def __def_exists(self):
        """
        checks if there is a definition file in the pickles dir
        """
        def_file = Path(self.pickle_def_path)
        if def_file.exists():
            return True
        else:
            return False

    def __get_defs(self):
        """
        gets the definitions from the pickles files
        """
        if self.__def_exists():
            try:
                with open(self.pickle_def_path, 'r') as f:
                    defs_ = json.load(f)
                    self.pickle_defs = defs_
                    return defs_
            except Exception as e:
                print(e)

    def __dump_defs(self):
        """
        dumps pickle defs to a json file in the pickles dir
        """
        with open(self.pickle_def_path, 'w') as f:
            json.dump(self.pickle_defs, f, indent=4)

    def __save_pickle(self, name, fname, obj):
        file = os.path.join(PICKLE_DIR, fname)
        try:
            with open(file, 'wb') as f:
                pickle.dump(obj, f)
        except Exception as e:
            raise e

    def __update_def(self, pickle_obj):
        """
        if pickle definitions exists it updates the class attribute
        then will dump to file to save it
        else
        creates pickle definition dict attribute
        """
        if self.pickle_defs:
            self.pickle_defs[pickle_obj['name']] = pickle_obj['def_']
            self.__dump_defs()
        else:
            self.pickle_defs = {}
            self.pickle_defs[pickle_obj['name']] = pickle_obj['def_']
            self.__dump_defs()

    def __rollback_def(self, pickle_obj):
        if self.pickle_defs:
            del self.pickle_defs[pickle_obj['name']]
            self.__dump_defs()

    #TODO: make a namespace or class for defining a pickle
    def add_pickle(self, name, fname, obj):
        """
        provides method to add a pickle to the pickle objects
        """
        definition = {
            'name': name,
            'def_': {
                'fname': fname,
                'obj_type': str(type(obj))
            }
        }
        # update pickle def before writing to file
        self.__update_def(definition)
        # write pickle!
        try:
            self.__save_pickle(name, fname, obj)
        except Exception as e:
            # rollback def update if adding pickle fails
            print(e)
            print('rolling back pickle def update')
            self.__rollback_def(definition)

    # TODO: Rework getting all the pickles files
    def get_all_pickles(self):
        """
        loops through pickles files in pickles dir and gets them all
        returns a list of pickle objects
        """
        if self.__pickle_files:
            # self.pickles = {pickle.load(file) for file in self.__pickle_files]
            return self.pickles
        else:
            raise FileNotFoundError

    def check_pickle(self, **kwargs):
        """
        get a named pickle by name or by file name
        kwargs
        use fname
        name
        """
        if self.pickle_defs:
            if kwargs['name'] in self.pickle_defs:
                return True
            else:
                return False

    def get_pickle(self, **kwargs):
        if self.check_pickle(**kwargs):
            fname = os.path.join(PICKLE_DIR, kwargs['fname'])
            try:
                if os.path.getsize(fname) > 0:
                    with open(fname, 'rb') as f:
                        return pickle.load(file=f)
                else:
                    print('pickle file is empty')
                    return False
            except FileNotFoundError as e:
                print(f'pickle file not found for {kwargs["name"]} at {fname}')
                self.__rollback_def(**kwargs)
                return False
        else:
            print(f'Pickle not found by name {kwargs["name"]}')

    def __repr__(self):
        pass

    def __call__(self):
        pass

if __name__ == '__main__':
    pass
else:
    pass
