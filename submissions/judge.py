import subprocess
import tempfile
import os
import time
from django.utils import timezone
from .models import Submission

class CodeJudge:
    def __init__(self, submission):
        self.submission = submission
        self.problem = submission.problem
        
    def execute_code(self):
        """Execute code and return result"""
        try:
            self.submission.status = "JUDGING"
            self.submission.save()
            
            # Get test cases
            test_cases = self.problem.testcases.all()
            if not test_cases:
                self.submission.status = "CE"
                self.submission.output = "No test cases found"
                self.submission.judged_at = timezone.now()
                self.submission.save()
                return
            
            passed_tests = 0
            total_tests = len(test_cases)
            
            for test_case in test_cases:
                result = self._run_single_test(test_case)
                if result['status'] != 'AC':
                    self.submission.status = result['status']
                    self.submission.output = result['output']
                    self.submission.execution_time = result.get('time', 0)
                    self.submission.judged_at = timezone.now()
                    self.submission.save()
                    return
                passed_tests += 1
            
            # All tests passed
            self.submission.status = "AC"
            self.submission.score = 100
            self.submission.output = f"All {total_tests} test cases passed!"
            self.submission.judged_at = timezone.now()
            self.submission.save()
            
        except Exception as e:
            self.submission.status = "RE"
            self.submission.output = f"Judge Error: {str(e)}"
            self.submission.judged_at = timezone.now()
            self.submission.save()
    
    def _run_single_test(self, test_case):
        """Run code against a single test case"""
        if self.submission.language == 'python':
            return self._run_python(test_case)
        elif self.submission.language == 'cpp':
            return self._run_cpp(test_case)
        else:
            return {'status': 'CE', 'output': 'Unsupported language'}
    
    def _run_python(self, test_case):
        """Execute Python code"""
        temp_file = None
        try:
            # Create temp file with unique name
            import uuid
            temp_dir = tempfile.gettempdir()
            temp_file = os.path.join(temp_dir, f"code_{uuid.uuid4().hex}.py")
            
            with open(temp_file, 'w') as f:
                f.write(self.submission.code)
            
            start_time = time.time()
            process = subprocess.run(
                ['python', temp_file],
                input=test_case.input_data,
                capture_output=True,
                text=True,
                timeout=self.problem.time_limit
            )
            execution_time = time.time() - start_time
            
            if process.returncode != 0:
                error_msg = process.stderr if process.stderr else "Unknown error"
                return {'status': 'RE', 'output': f"Runtime Error: {error_msg}", 'time': execution_time}
            
            output = process.stdout.strip()
            expected = test_case.expected_output.strip()
            
            if output == expected:
                return {'status': 'AC', 'output': 'Accepted', 'time': execution_time}
            else:
                return {
                    'status': 'WA', 
                    'output': f"Wrong Answer\nExpected: {expected}\nGot: {output}",
                    'time': execution_time
                }
                
        except subprocess.TimeoutExpired:
            return {'status': 'TLE', 'output': 'Time Limit Exceeded'}
        except Exception as e:
            return {'status': 'RE', 'output': f"System Error: {str(e)}"}
        finally:
            # Clean up temp file
            if temp_file and os.path.exists(temp_file):
                try:
                    os.unlink(temp_file)
                except:
                    pass
    
    def _run_cpp(self, test_case):
        """Execute C++ code"""
        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.cpp', delete=False) as f:
                f.write(self.submission.code)
                f.flush()
                
                # Compile
                exe_name = f.name.replace('.cpp', '.exe')
                compile_process = subprocess.run(
                    ['g++', f.name, '-o', exe_name],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                
                if compile_process.returncode != 0:
                    os.unlink(f.name)
                    return {'status': 'CE', 'output': compile_process.stderr}
                
                # Execute
                start_time = time.time()
                process = subprocess.run(
                    [exe_name],
                    input=test_case.input_data,
                    capture_output=True,
                    text=True,
                    timeout=self.problem.time_limit
                )
                execution_time = time.time() - start_time
                
                # Clean up
                os.unlink(f.name)
                if os.path.exists(exe_name):
                    os.unlink(exe_name)
                
                if process.returncode != 0:
                    return {'status': 'RE', 'output': process.stderr, 'time': execution_time}
                
                output = process.stdout.strip()
                expected = test_case.expected_output.strip()
                
                if output == expected:
                    return {'status': 'AC', 'output': 'Accepted', 'time': execution_time}
                else:
                    return {
                        'status': 'WA', 
                        'output': f"Wrong Answer\nExpected: {expected}\nGot: {output}",
                        'time': execution_time
                    }
                    
        except subprocess.TimeoutExpired:
            return {'status': 'TLE', 'output': 'Time Limit Exceeded'}
        except Exception as e:
            return {'status': 'RE', 'output': str(e)}

def judge_submission(submission_id):
    """Judge a submission by ID"""
    try:
        submission = Submission.objects.get(id=submission_id)
        judge = CodeJudge(submission)
        judge.execute_code()
    except Submission.DoesNotExist:
        pass