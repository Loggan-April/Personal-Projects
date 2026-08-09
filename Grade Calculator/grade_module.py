import threading
from concurrent.futures import ThreadPoolExecutor

"""
Author: Loggan April
"""
_execute = ThreadPoolExecutor(max_workers=4)

_lock = threading.Lock()

""" validates the marks entered by the user is a whole and positive number"""
def validate_marks(mark, callback = None):
    def run():
        with _lock:
            try:
                value = float(mark)
                result = 0 <= value <= 100
            
            except ValueError:
                result = False
        if callback:
            callback(result)
        return result
    if callback:
        _execute.submit(run)
    else:
        return run()

""" calculates the overall mark and returns it to the user"""
def overall_mark(quiz, project, exam, practical, callback=None):
    """
    Calculates the overall weighted mark
    - If callback is provided it will run in a background thread and passes result to callback
    - If callback is not called then it runs normally and returns the result directly
    """
    def run():
        with _lock:
            result = (
                float(quiz) * 0.1 +
                float(project) * 0.2 +
                float(exam) * 0.5 +
                float(practical) * 0.2 
            )
        if callback:
            callback(result)
        return result
    if callback:
        _execute.submit(run)
    else:
        return run()

""" Validates all the numbers entered by the user in a batch in a separate thread"""
def validate_batch(marks, callback=None):
    """ Validates each mark"""
    def validate_single(mark):
        try: 
            value = float(marks)
            return mark, 0 <= value <= 100
        except ValueError:
            return mark, False
    def run():
        futures = {_execute.submit(validate_single, m): m for m in marks}
        results = {}
        for future in futures:
            mark, is_valid = future.result()
            results[mark]= is_valid

        if callback:
            callback(results)
        return results
    
    if callback:
        thread = threading.Thread(target = run, daemon=True)
        thread.start()
    else:
        return run()
    
""" Validates that the overall mark is a positive number/float"""
def overall_mark_batch(students, callback=None):
    def calc_single(student):
        with _lock:
            result = (
                float(student["Quiz(10%)"]) * 0.1 +
                float(student["Project(20%)"]) * 0.2 +
                float(student["Final_Exam(50%)"]) * 0.5 +
                float(student["Practical(20%)"]) * 0.2 
            )
        return student["student_No"], result
    
    def run():
        futures = [_execute.submit(calc_single, s) for s in students]
        results = [f.result() for f in futures]

        if callback:
            callback(results)
        return results 
    if callback:
        thread = threading.Thread(target=run, daemon=True)
        thread.start()
    else:
        return run()