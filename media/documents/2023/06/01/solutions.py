
import re
def names():
    simple_string = """Amy is 5 years old, and her sister Mary is 2 years old. 
    Ruth and Peter, their parents, have 3 kids."""

    names = re.findall(r'\b[A-Z]\w+', simple_string)
    return names


def grades():
    with open("assets/grades.txt", 'r') as file:
        grades = file.read()
        b_grades = re.findall(r'(\w+ \w+): B', grades)
        print(b_grades)

        return b_grades

def logs():

    with open('assets/logs.txt', 'r') as file:
        text = file.read()
        pattern = r'(?P<host>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) - (?P<user_name>\w+|-) \[(?P<time>.+)\] "(?P<request>.+)"'
        logsDict = [match.groupdict() for match in re.finditer(pattern, text)]

        print(logsDict)

        return logsDict


# names()
grades()
