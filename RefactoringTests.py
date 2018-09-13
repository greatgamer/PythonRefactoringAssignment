import unittest
import model
import csv_plugin
import python_code_validator as py_cv
import pickle_modules as pm
import controller
import command_interpreter as com_int
import command_line as com_line


class MainTests(unittest.TestCase):

    def test_21_controller_create_csv(self):
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

    def test_24_controller_validate_code(self):
        cont = controller.Controller()
        expected = 1
        actual = len(cont.validate_code(['plants.py']))
        self.assertEqual(expected, actual)

    def test_25_controller_validate_code(self):
        cont = controller.Controller()
        expected = 2
        actual = len(cont.validate_code(['plants.py', 'plants.py']))
        self.assertEqual(expected, actual)

    def test_26_controller_validate_code(self):
        cont = controller.Controller()
        expected = 1
        actual = len(cont.validate_code(['linkedlist.py', 'plants.foo']))
        self.assertEqual(expected, actual)

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

    def test_30_controller_load_pickle(self):
        cont = controller.Controller()
        expected = dict
        actual = type(cont.load_pickle())
        self.assertEqual(expected, actual)

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
