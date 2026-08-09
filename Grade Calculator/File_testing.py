"""
Author: Loggan April
"""

import unittest
import csv
import os
import tempfile
import shutil
from unittest.mock import patch, MagicMock

# ─────────────────────────────────────────────
#  File Testing
# ─────────────────────────────────────────────

from grade_module import validate_marks, overall_mark


class TestValidateMarks(unittest.TestCase):
    #Tests for validate_marks() in grade_module.py

    def test_valid_mark(self):
        # A normal mark within range should return True
        self.assertTrue(validate_marks("75"))

    def test_boundary_zero(self):
        # 0 is the lowest valid mark
        self.assertTrue(validate_marks("0"))

    def test_boundary_hundred(self):
        #100 is the highest valid mark
        self.assertTrue(validate_marks("100"))

    def test_above_range(self):
        #Anything above 100 should return False
        self.assertFalse(validate_marks("101"))

    def test_negative_mark(self):
        #Negative numbers should return False
        self.assertFalse(validate_marks("-1"))

    def test_non_numeric(self):
        #A non-numeric string should return False#
        self.assertFalse(validate_marks("abc"))

    def test_empty_string(self):
        #An empty string should return False#
        self.assertFalse(validate_marks(""))

    def test_decimal_mark(self):
        #Decimal marks within range should return True#
        self.assertTrue(validate_marks("85.5"))

    def test_decimal_out_of_range(self):
        #Decimal marks above 100 should return False#
        self.assertFalse(validate_marks("100.1"))

    def test_whitespace_string(self):
        #A whitespace-only string should return False#
        self.assertFalse(validate_marks("   "))


class TestOverallMark(unittest.TestCase):
    #Tests for overall_mark() in grade_module.py#

    def test_standard_calculation(self):
        #80*0.1 + 70*0.2 + 60*0.5 + 90*0.2 = 8+14+30+18 = 70.0#
        self.assertAlmostEqual(overall_mark(80, 70, 60, 90), 70.0)

    def test_all_zeros(self):
        #All zeros should produce an overall mark of 0#
        self.assertAlmostEqual(overall_mark(0, 0, 0, 0), 0.0)

    def test_all_hundreds(self):
        #All 100s should produce an overall mark of 100#
        self.assertAlmostEqual(overall_mark(100, 100, 100, 100), 100.0)

    def test_weights_sum_to_one(self):
        #Equal marks across all components should return that same mark#
        self.assertAlmostEqual(overall_mark(50, 50, 50, 50), 50.0)

    def test_exam_carries_most_weight(self):
        #Exam is 50% so a high exam mark should dominate the overall#
        result = overall_mark(0, 0, 100, 0)
        self.assertAlmostEqual(result, 50.0)

    def test_quiz_weight_only(self):
        #Quiz is 10% so 100 in quiz only = 10.0 overall#
        self.assertAlmostEqual(overall_mark(100, 0, 0, 0), 10.0)

    def test_project_weight_only(self):
        #Project is 20% so 100 in project only = 20.0 overall#
        self.assertAlmostEqual(overall_mark(0, 100, 0, 0), 20.0)

    def test_practical_weight_only(self):
        #Practical is 20% so 100 in practical only = 20.0 overall#
        self.assertAlmostEqual(overall_mark(0, 0, 0, 100), 20.0)

    def test_string_inputs(self):
        #overall_mark should handle string inputs (as used in gui.py)#
        self.assertAlmostEqual(overall_mark("80", "70", "60", "90"), 70.0)


# ─────────────────────────────────────────────
#  DATA MODULE TESTS
# ─────────────────────────────────────────────

import data_module


class TestDataModule(unittest.TestCase):
    """Tests for all functions in data_module.py.
    Uses a temporary CSV file so real data is never touched."""

    def setUp(self):
        #Create a temp folder and point data_module at a test CSV before each test#
        self.test_dir = tempfile.mkdtemp()
        self.test_file = os.path.join(self.test_dir, "test_grades.csv")
        # Redirect data_module to use the temp file
        self._original_file = data_module.FILE_NAME
        data_module.FILE_NAME = self.test_file

        # Write a header + one student row to start with
        with open(self.test_file, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                "Student_No", "Name", "Surname", "Module",
                "Quiz(10%)", "Project(20%)", "Final_Exam(50%)",
                "Practical(20%)", "Overall Grade"
            ])
            writer.writerow(["S001", "John", "Doe", "Python Programming",
                            "80", "70", "60", "90", "70.0"])

    def tearDown(self):
        #Restore original file name and delete temp folder after each test#
        data_module.FILE_NAME = self._original_file
        shutil.rmtree(self.test_dir)

    # --- initialize_file ---

    def test_initialize_file_creates_file(self):
        #initialize_file() should create the CSV if it doesn't exist#
        new_file = os.path.join(self.test_dir, "new_grades.csv")
        data_module.FILE_NAME = new_file
        data_module.initialize_file()
        self.assertTrue(os.path.exists(new_file))

    def test_initialize_file_writes_header(self):
        #initialize_file() should write the correct column headers#
        new_file = os.path.join(self.test_dir, "new_grades.csv")
        data_module.FILE_NAME = new_file
        data_module.initialize_file()
        with open(new_file, "r") as f:
            reader = csv.reader(f)
            header = next(reader)
        self.assertIn("Student_No", header)
        self.assertIn("Overall Grade", header)

    def test_initialize_file_does_not_overwrite(self):
        #initialize_file() should not touch a file that already exists#
        data_module.initialize_file()
        with open(self.test_file, "r") as f:
            rows = list(csv.reader(f))
        # Should still have header + 1 student row
        self.assertEqual(len(rows), 2)

    # --- save_student ---

    def test_save_student_adds_row(self):
        #save_student() should append a new row to the CSV#
        student = {
            "student_No": "S002", "name": "Jane", "surname": "Smith",
            "module": "Java Programming", "Quiz(10%)": "90",
            "Project(20%)": "85", "Final_Exam(50%)": "75",
            "Practical(20%)": "80", "Overall_Grade": "80.5"
        }
        data_module.save_student(student)
        with open(self.test_file, "r") as f:
            rows = list(csv.reader(f))
        # Header + original student + new student = 3 rows
        self.assertEqual(len(rows), 3)
        self.assertEqual(rows[2][0], "S002")

    def test_save_student_correct_values(self):
        #save_student() should store all fields in the correct order#
        student = {
            "student_No": "S003", "name": "Alice", "surname": "Brown",
            "module": "Networking", "Quiz(10%)": "60",
            "Project(20%)": "65", "Final_Exam(50%)": "70",
            "Practical(20%)": "75", "Overall_Grade": "69.0"
        }
        data_module.save_student(student)
        result = data_module.search_student("S003")
        self.assertEqual(result[1], "Alice")
        self.assertEqual(result[3], "Networking")

    # --- search_student ---

    def test_search_student_found(self):
        #search_student() should return the correct row for a valid student number#
        result = data_module.search_student("S001")
        self.assertIsNotNone(result)
        self.assertEqual(result[0], "S001")
        self.assertEqual(result[1], "John")

    def test_search_student_not_found(self):
        #search_student() should return None if the student number doesn't exist#
        result = data_module.search_student("S999")
        self.assertIsNone(result)

    def test_search_student_returns_correct_fields(self):
        #search_student() should return all 9 fields for the matched student#
        result = data_module.search_student("S001")
        self.assertEqual(len(result), 9)

    # --- delete_student ---

    def test_delete_student_removes_row(self):
        #delete_student() should remove the student from the CSV#
        data_module.delete_student("S001")
        result = data_module.search_student("S001")
        self.assertIsNone(result)

    def test_delete_student_keeps_others(self):
        #delete_student() should not remove other students#
        student = {
            "student_No": "S002", "name": "Jane", "surname": "Smith",
            "module": "Java Programming", "Quiz(10%)": "90",
            "Project(20%)": "85", "Final_Exam(50%)": "75",
            "Practical(20%)": "80", "Overall_Grade": "80.5"
        }
        data_module.save_student(student)
        data_module.delete_student("S001")
        result = data_module.search_student("S002")
        self.assertIsNotNone(result)

    def test_delete_nonexistent_student(self):
        #delete_student() on a student that doesn't exist should not crash#
        try:
            data_module.delete_student("S999")
        except Exception as e:
            self.fail(f"delete_student raised an exception unexpectedly: {e}")

    def test_delete_student_preserves_header(self):
        #delete_student() should keep the header row intact#
        data_module.delete_student("S001")
        with open(self.test_file, "r") as f:
            reader = csv.reader(f)
            header = next(reader)
        self.assertEqual(header[0], "Student_No")


# ─────────────────────────────────────────────
#  GUI TESTS  (no window opens)
# ─────────────────────────────────────────────

class TestGuiFunctions(unittest.TestCase):
    """Tests for logic functions in gui.py.
    tkinter is mocked so no window ever opens."""

    @classmethod
    def setUpClass(cls):
        #Mock tkinter before importing gui so no window is created#
        cls.tk_patcher = patch.dict("sys.modules", {
            "tkinter": MagicMock(),
            "tkinter.ttk": MagicMock(),
            "tkinter.messagebox": MagicMock(),
            "pywinstyles": MagicMock(),
        })
        cls.tk_patcher.start()

        # Also mock the data/grade imports gui.py uses
        import sys
        sys.modules["data_module"] = MagicMock()
        sys.modules["grade_module"] = MagicMock()

    @classmethod
    def tearDownClass(cls):
        cls.tk_patcher.stop()

    def test_overall_mark_logic(self):
        #overall_mark() calculation used by save_data() is correct#
        result = overall_mark(80, 70, 60, 90)
        self.assertAlmostEqual(result, 70.0)

    def test_validate_marks_used_in_save(self):
        #validate_marks() correctly rejects non-numeric input that save_data would receive#
        self.assertFalse(validate_marks("abc"))
        self.assertFalse(validate_marks(""))
        self.assertTrue(validate_marks("85"))

    def test_validate_marks_boundary_in_gui_context(self):
        #Boundary values that a user might type into the entry fields#
        self.assertTrue(validate_marks("0"))
        self.assertTrue(validate_marks("100"))
        self.assertFalse(validate_marks("-0.1"))
        self.assertFalse(validate_marks("100.1"))


if __name__ == "__main__":
    unittest.main(verbosity=2)