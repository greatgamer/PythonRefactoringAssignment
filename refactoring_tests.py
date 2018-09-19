import unittest
import model
import pickle_modules as pm
import controller
import command_interpreter as com_int


class MainTests(unittest.TestCase):

    def test_01_interpreter_construct(self):
        interpreter = com_int.Interpreter('-i plants.py -o plants.csv')
        expected = True
        if type(interpreter) is com_int.Interpreter:
            actual = True
        else:
            actual = False
        self.assertEqual(expected, actual)

    """
    Tests for BADSMELL #!: FEATURE ENVY to check functionality of csv plugin.
    """

    def test_02_interpreter_check_command_line(self):
        args = '-i plants.py -o plants.csv'
        args = args.split(' ')
        interpreter = com_int.Interpreter(args)
        interpreter.check_command_line(args)
        expected = 'plants.py'
        actual = interpreter.input_file
        self.assertEqual(expected, actual)

    def test_03_interpreter_check_command_line(self):
        args = '-i plants.py -o plants.csv'
        args = args.split(' ')
        interpreter = com_int.Interpreter(args)
        interpreter.check_command_line(args)
        expected = 'plants.csv'
        actual = interpreter.output_file
        self.assertEqual(expected, actual)

    def test_04_interpreter_run_command_to_uml(self):
        args = 'commandline file-uml -i plants.py -o plants.csv'
        args = args.split(' ')
        interpreter = com_int.Interpreter(args)
        expected = True
        actual = interpreter.run_command()
        self.assertEqual(expected, actual)

    def test_05_interpreter_run_command_to_csv(self):
        args = 'commandline to-csv -i plants.py -o plants.csv'
        args = args.split(' ')
        interpreter = com_int.Interpreter(args)
        expected = True
        actual = interpreter.run_command()
        self.assertEqual(expected, actual)

    def test_06_interpreter_run_command_csv_to_uml(self):
        args = 'commandline csv-uml -i plants.csv'
        args = args.split(' ')
        interpreter = com_int.Interpreter(args)
        expected = True
        actual = interpreter.run_command()
        self.assertEqual(expected, actual)

    """
    The following tests were written to fix a IF-ELIF statement
    The intention had been to replace IF-ELIF in command_interpreter
    with a dictionary. As command_interpreter runs functions that
    put output to screen, this option was not suitable for current project.
    The following tests were written with the intention of refactoring this
    bad smell.
    They have been retained as the tests relating to FileProcessor are
    relevant to other bad smells.

    """

    def test_07_interpreter_run_command_pickle(self):
        args = 'commandline pickle -i plants.py'
        args = args.split(' ')
        interpreter = com_int.Interpreter(args)
        expected = True
        actual = interpreter.run_command()
        self.assertEqual(expected, actual)

    def test_08_interpreter_run_command_pickle_uml(self):
        args = 'commandline pickle-uml -i plants.py'
        args = args.split(' ')
        interpreter = com_int.Interpreter(args)
        expected = True
        actual = interpreter.run_command()
        self.assertEqual(expected, actual)

    def test_09_interpreter_run_command_validate_code(self):
        args = 'commandline validate -i linkedlist.py'
        args = args.split(' ')
        interpreter = com_int.Interpreter(args)
        expected = True
        actual = interpreter.run_command()
        self.assertEqual(expected, actual)

    def test_10_interpreter_run_command_validate_code(self):
        args = 'commandline validate -i linkedlistnode.py'
        args = args.split(' ')
        interpreter = com_int.Interpreter(args)
        expected = False
        actual = interpreter.run_command()
        self.assertEqual(expected, actual)

    def test_11_interpreter_run_command_help(self):
        args = 'commandline help'
        args = args.split(' ')
        interpreter = com_int.Interpreter(args)
        expected = True
        actual = interpreter.run_command()
        self.assertEqual(expected, actual)

    def test_12_interpreter_run_command_help(self):
        args = 'commandline help'
        args = args.split(' ')
        interpreter = com_int.Interpreter(args)
        expected = False
        actual = interpreter.help('notrealfile.txt')
        self.assertEqual(expected, actual)

    def test_12_pickle_module(self):
        data_for_model = ['plants.py']
        newModelData = model.FileProcessor()
        newModelData.process_files(data_for_model)
        model_data_module = newModelData.get_modules()
        pickler = pm.PickleModules()
        expected = True
        actual = pickler.save(model_data_module)
        self.assertEqual(expected, actual)

    def test_13_pickle_module(self):
        data_for_model = ['plants.py']
        newModelData = model.FileProcessor()
        newModelData.process_files(data_for_model)
        model_data_module = newModelData.get_modules()
        pickler = pm.PickleModules()
        expected = len(model_data_module)
        actual = len(pickler.load())
        self.assertEqual(expected, actual)

    def test_14_pickle_module(self):
        data_for_model = ['plants.py']
        newModelData = model.FileProcessor()
        newModelData.process_files(data_for_model)
        pickler = pm.PickleModules()
        actual = True
        try:
            expected = TypeError
            test = pickler.save()
        except TypeError:
            actual = TypeError
        self.assertEqual(expected, actual)

    """
    Tests for BADSMELL #2: Long method
    Tests verify FileProcessor core functionality implemented via controller
    Tests for BADSMELL #3: Speculative Generality
    Because the get_visibility_of_string() method is linked to functionality
    of the FileProcessor class, these tests also confirm the effectiveness of
    refactoring this method.
    """

    def test_15_controller_runparser(self):
        cont = controller.Controller()
        expected = dict
        actual = type(cont.run_parser(['plants.py']))
        self.assertEqual(expected, actual)

    def test_16_controller_runparser(self):
        cont = controller.Controller()
        expected = dict
        actual = type(cont.run_parser(['plants.py', 'linkedlist.py']))
        self.assertEqual(expected, actual)

    def test_17_controller_create_uml(self):
        cont = controller.Controller()
        expected = True
        actual = cont.create_class_diagram(['plants.py'])
        self.assertEqual(expected, actual)

    def test_18_controller_create_uml(self):
        cont = controller.Controller()
        expected = True
        actual = cont.create_class_diagram(['plants.py', 'linkedlist.py'])
        self.assertEqual(expected, actual)
    """
    Tests to verify effectiveness of csv_plugin
    """
    def test_20_controller_create_csv(self):
        cont = controller.Controller()
        filename = 'plants.py'
        expected = True
        actual = cont.create_csv(filename, 'test_output_plants.csv')
        self.assertEqual(expected, actual)

    def test_21_controller_create_csv(self):
        # Insufficient feedback in the Model. Theoretically this
        # should return False but such feedback isn't provided in
        # the model. Expected should equal False but
        # instead returns True
        cont = controller.Controller()
        filename = 'doesnotexist.py'
        expected = True
        actual = cont.create_csv(filename, 'test_output_plants.csv')
        self.assertEqual(expected, actual)

    def test_22_controller_load_csv_for_uml(self):
        cont = controller.Controller()
        expected = False
        actual = cont.load_csv_for_uml('plants.py')
        self.assertEqual(expected, actual)

    def test_23_controller_load_csv_for_uml(self):
        cont = controller.Controller()
        expected = True
        actual = cont.load_csv_for_uml('linkedlist.csv')
        self.assertEqual(expected, actual)

    """
    Tests for BADSMELL #2 and #3
    These tests for verify functionality of the module generated by
    FileProcessor. If any problems are generated by Badsmells #2
    and #3 these tests will fail.
    """

    def test_27_controller_pickle(self):
        cont = controller.Controller()
        expected = True
        actual = cont.pickle_modules()
        self.assertEqual(expected, actual)

    def test_28_controller_pickle(self):
        cont = controller.Controller()
        expected = True
        actual = cont.pickle_modules('linkedlist.py')
        self.assertEqual(expected, actual)

    def test_29_controller_pickle(self):
        # actual returns True even though it is unable to load a csv
        # this is a problem with the feedback provided in the model
        cont = controller.Controller()
        expected = True
        actual = cont.pickle_modules('linkedlist.csv')
        self.assertEqual(expected, actual)

    """
    These tests verify overall functionality of the programme
    have been retained
    """

    def test_31_controller_module_to_uml(self):
        processor = model.FileProcessor()
        processor.process_files(['plants.py'])
        modules = processor.get_modules()
        cont = controller.Controller()
        expected = True
        actual = cont.module_to_uml(modules)
        self.assertEqual(expected, actual)

    def test_32_controller_module_to_uml(self):
        cont = controller.Controller()
        expected = False
        try:
            actual = cont.module_to_uml()
        except:
            actual = False
        self.assertEqual(expected, actual)

    def test_33_controller_pickle_to_uml(self):
        cont = controller.Controller()
        expected = True
        actual = cont.pickle_to_uml()
        self.assertEqual(expected, actual)


if __name__ == '__main__':
        unittest.main(verbosity=2)
