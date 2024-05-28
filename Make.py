import subprocess

# 파이썬 파일 실행
def execute_python_file(file_path):
    subprocess.run(['python', file_path])

# 실행할 파일들의 경로
file_paths = ['Prediction_Analyze.py', 'Corrcoef_Analyze.py']

# 파일들을 순차적으로 실행
for file_path in file_paths:
    execute_python_file('pythonFile/'+file_path)
