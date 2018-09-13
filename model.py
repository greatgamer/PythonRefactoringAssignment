import inspect
import sys
import os
import csv

##########################################
# Initial helper classes to store information while the parser
# parses the information


class ClassNode:
    """
    Class object containing attributes and functions
    Author: Braeden
    Contributor: Peter

    >>> ClassNode("Class One", []).name
    'Class One'
    >>> class_one = ClassNode("Class One", [])
    >>> class_one.add_attribute("Attribute One")
    >>> class_one.add_attribute("Attribute Two")
    >>> len(class_one.attributes)
    2
    """
    def __init__(self, name, super_classes=None):
        self.name = name
        self.attributes = []
        self.functions = []
        if super_classes is None:
            self.super_classes = []
        else:
            self.super_classes = super_classes

    def add_attribute(self, attribute_name, visibility):
        self.attributes.append(AttributeNode(attribute_name, visibility))

    def add_function(self, function_name, list_of_parameters, visibility):
        self.functions.append(FunctionNode(function_name, list_of_parameters,
                                           visibility))

    def add_super_class(self, super_class):
        self.super_classes.append(super_class)

    def get_name(self):
        return self.name


class AttributeNode:
    """
    Attribute object containing attribute name
    Author: Braeden

    >>> AttributeNode("Attribute One").name
    'Attribute One'
    """
    def __init__(self, name, visibility):
        self.name = name
        self.visibility = visibility


class FunctionNode:
    """
    Function object containing function name and parameters
    Author: Braeden

    >>> FunctionNode("Function One", []).get_name()
    'Function One'
    >>> len(FunctionNode("Funct One", ["Par One", "Par Two"]).parameters)
    2
    """
    def __init__(self, name, list_of_parameters, visibility):
        self.name = name
        self.parameters = list_of_parameters
        self.visibility = visibility

    def get_name(self):
        return self.name

    def get_parameters(self):
        return ",".join(self.parameters)


class FileProcessor:
    """
    Process multiple files into class objects ready to be converted into DOT
    Author: Braeden
    """
    filter_out_attributes = ["__doc__", "__module__",
                             "__dict__", "__weakref__"]

    def __init__(self):
        self.modules = dict()

    def process_files(self, file_names):
        """
        Loop through a list of files, and process each file as an individual
        Author: Braeden

        >>> fp.process_files(["plants.py"])
        1
        >>> fp.process_files(["plants.py", "plants2.py"])
        2
        """
        for file in file_names:
            self.process_file(file)
        return len(self.modules)

    def process_file(self, file_name):
        # Import specified file_name and store as module
        path, file = os.path.split(file_name)
        module_name = file.replace("./", "").replace(".py", "")\
            .replace("/", ".")

        # change path for import to directory of file
        sys.path.append(path)

        try:
            __import__(module_name, locals(), globals())
            self.process_module(sys.modules[module_name])
        except ImportError:
            print("A file with this name could not be found, "
                  "please try again.")
        except OSError:
            print("The provided python file contains invalid syntax,"
                  " please fix the provided code before running")

    def process_module(self, module):
        # Find any classes that exists within this module
        for (name, something) in inspect.getmembers(module):
            if inspect.isclass(something):
                self.process_class(something)

    def process_class(self, some_class):
        # Process the found class, and store in global modules
        # Find any functions with-in the class
        name = some_class.__name__

        module_name = some_class.__module__

        # create module for current file in global modules list
        if module_name not in self.modules:
            self.modules[module_name] = list()

        super_classes = []
        super_classes_names = []

        # Only creates class_nodes that have unique name,
        # stops duplicate class_nodes
        # Strips any random objects, only leaves proper class names
        for class_object in some_class.__bases__:
            if class_object.__name__ != 'object':
                if class_object.__name__ not in super_classes_names:
                    super_classes.append(class_object)
                    super_classes_names.append(class_object.__name__)

        # create class node and append to current module
        class_node = ClassNode(name, super_classes)
        self.modules[module_name].append(class_node)

        # create list of functions in class
        for (name, something) in inspect.getmembers(some_class):
            if inspect.ismethod(something) or inspect.isfunction(something):
                # get the class from the functions element
                function_class = something.__qualname__.split('.')[0]

                # only add function if the current class is the same as the
                # selected functions class
                if some_class.__name__ == function_class:
                    # create list of attributes in class with constructor
                    if something.__name__ == "__init__":
                        attributes = something.__code__.co_names

                        for attribute in attributes:
                            self.process_attribute(attribute, class_node,
                                                   self.get_visibility_of_string
                                                   (attribute))

                    self.process_function(something, class_node,
                                          self.get_visibility_of_string
                                          (something.__name__))

    def process_function(self, some_function, class_node, visibility):
        # Functions are added to the class node with just their title
        class_node.add_function(some_function.__name__,
                                inspect.getfullargspec(some_function)[0],
                                visibility)

    def process_attribute(self, attribute_name, class_node, visibility):
        # Attributes are added to the class node with just their name
        # filter out __module__, __doc__
        if attribute_name not in self.filter_out_attributes:
            class_node.add_attribute(attribute_name, visibility)

    def get_modules(self):
        return self.modules

    def get_visibility_of_string(self, string):
        # get visibility of function (public = +, protected = #, private = -)
        visibility = "+"
        if string[:2] == "__":
            visibility = "-"
        elif string[0] == "_":
            visibility = "#"
        return visibility


    def write_csv_file(self, modules, filename='myclass.csv'):
        """
        Refactored code
        The code in the following methods has been refactored from csv_plugin.
        Smell: Feature Envy
        Fix: relocated methods from csv_plugin class to FileProcessor
        """

        # Writes module as received from model or from self.open_file
        # to specified csv file.
        output = ''
        for (name, module) in modules.items():
            output += 'module,{}\n'.format(name)
            for c in module:
                output += 'class,{}'.format(c.name)
                if len(c.attributes) > 0:
                    output += '\nattributes'
                for attr in c.attributes:
                    output += ',{}'.format(attr.name)
                if len(c.functions) > 0:
                    output += '\nmethods'
                for func in c.functions:
                    output += ',{}'.format(func.name)
                if c.super_classes is not None:
                    if len(c.super_classes) > 0:
                        output += '\nsuper_classes'
                        for super_class in c.super_classes:
                            output += ',{}'.format(super_class)
                output += '\n'
        try:
            with open(filename, "wt") as f:
                f.write(output)
            return True
        except IOError:
            print("Cannot write csv file. Try again another day")
            return False
        except PermissionError:
            print('You do not have appropriate permissions on '
                  'this system to save the file')
            return False
        except:
            print('The system encountered a problem here. '
                  'Please turn off your computer,')
            print('jump up and down three times, flap your arms '
                  'and quack like a duck and then try again.')
            return False

    def open_csv_file(self, filename='myclass.csv'):
        # Opens csv file and loads each line of the file into list
        # Then load_data_to_module for parsing
        result = []
        try:
            with open(filename) as File:
                reader = csv.reader(File)
                for row in reader:
                    result.append(row)
            return self.load_data_to_module(result)
        except FileNotFoundError:
            print('File cannot be found. Please check path and '
                  'file name or check that file exists')
            return False
        except IndexError:
            print('File cannot be found. Please check path and '
                  'file name or check that file exists')
            return False
        except:
            print('An error has occurred. Could not load '
                  'information from csv file.')
            return False

    def load_data_to_module(self, module_list):
        """
        This is used to parse list and reconsruct the class structure
        current version will only work with a single file. Extenstion
        should be easy
        Module is loaded into dictionary which can then be used by by
        the uml output to generate UML diagram
        """
        module_name = ''
        modules = dict()
        newClass = None
        for aline in module_list:
            if aline[0] == 'module':
                module_name = aline[1]
                modules[module_name] = list()
            elif aline[0] == 'class':
                if newClass is None:
                    newClass = ClassNode(aline[1].strip())
                else:
                    modules[module_name].append(newClass)
                    newClass = ClassNode(aline[1].strip())
            elif aline[0] == 'attributes':
                loop_counter = 1
                while loop_counter < len(aline):
                    newClass.add_attribute(aline[loop_counter].strip(), False)
                    loop_counter += 1
            elif aline[0] == 'methods':
                loop_counter = 1
                while loop_counter < len(aline):
                    newClass.add_function(aline[loop_counter].strip(),
                                          'params', False)
                    loop_counter += 1
            elif aline[0] == 'super_classes':
                pass
        modules[module_name].append(newClass)
        return modules

if __name__ == "__main__":
    import doctest
    doctest.testmod(extraglobs={'fp': FileProcessor()})
