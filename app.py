from flask import Flask, render_template, request, redirect, session
import random
from pypdf import PdfReader
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash


# ============================================================
# FLASK APP
# ============================================================

app = Flask(__name__)
app.secret_key = "prepai-secret-key-2026"


# ============================================================
# MYSQL DATABASE
# ============================================================

app.config["SQLALCHEMY_DATABASE_URI"] = (
    "mysql+pymysql://prepai_user:PrepAI%402026@localhost/prepai"
)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# ============================================================
# USER MODEL
# ============================================================

class User(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(100),
        nullable=False
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(255),
        nullable=False
    )


# ============================================================
# CREATE DATABASE TABLES
# ============================================================

with app.app_context():
    db.create_all()


# ============================================================
# PYTHON QUESTIONS
# ============================================================

python_questions = [

    {
        "id": 1,
        "question": "Which keyword is used to define a function in Python?",
        "option_a": "function",
        "option_b": "def",
        "option_c": "fun",
        "option_d": "define",
        "answer": "B",
        "explanation": "The def keyword is used to define a function in Python."
    },

    {
        "id": 2,
        "question": "Which of the following is a mutable data type?",
        "option_a": "Tuple",
        "option_b": "String",
        "option_c": "List",
        "option_d": "Integer",
        "answer": "C",
        "explanation": "A list is mutable, which means its elements can be changed after creation."
    },

    {
        "id": 3,
        "question": "What is the output of print(2 ** 3)?",
        "option_a": "6",
        "option_b": "8",
        "option_c": "9",
        "option_d": "5",
        "answer": "B",
        "explanation": "The ** operator performs exponentiation. 2 ** 3 = 8."
    },

    {
        "id": 4,
        "question": "Which symbol is used for a single-line comment in Python?",
        "option_a": "//",
        "option_b": "/*",
        "option_c": "#",
        "option_d": "--",
        "answer": "C",
        "explanation": "The # symbol is used to write a single-line comment in Python."
    },

    {
        "id": 5,
        "question": "Which function is used to get the length of a list?",
        "option_a": "size()",
        "option_b": "length()",
        "option_c": "count()",
        "option_d": "len()",
        "answer": "D",
        "explanation": "The len() function returns the number of elements in a list."
    },

    {
        "id": 6,
        "question": "Which collection stores key-value pairs?",
        "option_a": "List",
        "option_b": "Tuple",
        "option_c": "Dictionary",
        "option_d": "Set",
        "answer": "C",
        "explanation": "A dictionary stores data in key-value pairs."
    },

    {
        "id": 7,
        "question": "Which keyword is used to create a class in Python?",
        "option_a": "object",
        "option_b": "class",
        "option_c": "struct",
        "option_d": "define",
        "answer": "B",
        "explanation": "The class keyword is used to define a class in Python."
    },

    {
        "id": 8,
        "question": "What is the output of print(10 // 3)?",
        "option_a": "3",
        "option_b": "3.33",
        "option_c": "1",
        "option_d": "4",
        "answer": "A",
        "explanation": "The // operator performs floor division. 10 // 3 gives 3."
    },

    {
        "id": 9,
        "question": "Which keyword is used to handle exceptions?",
        "option_a": "catch",
        "option_b": "error",
        "option_c": "try",
        "option_d": "handle",
        "answer": "C",
        "explanation": "The try keyword starts a block where exceptions can be handled."
    },

    {
        "id": 10,
        "question": "Which loop is commonly used to iterate over a sequence?",
        "option_a": "for",
        "option_b": "repeat",
        "option_c": "loop",
        "option_d": "iterate",
        "answer": "A",
        "explanation": "A for loop is commonly used to iterate through a sequence."
    },

    {
        "id": 11,
        "question": "What is the output of print(type([]))?",
        "option_a": "<class 'tuple'>",
        "option_b": "<class 'list'>",
        "option_c": "<class 'set'>",
        "option_d": "<class 'dict'>",
        "answer": "B",
        "explanation": "[] creates an empty list."
    },

    {
        "id": 12,
        "question": "Which keyword is used to create an anonymous function in Python?",
        "option_a": "func",
        "option_b": "anonymous",
        "option_c": "lambda",
        "option_d": "def",
        "answer": "C",
        "explanation": "The lambda keyword creates a small anonymous function."
    },

    {
        "id": 13,
        "question": "What is the output of print(5 % 2)?",
        "option_a": "2",
        "option_b": "2.5",
        "option_c": "1",
        "option_d": "0",
        "answer": "C",
        "explanation": "The % operator returns the remainder. 5 % 2 = 1."
    },

    {
        "id": 14,
        "question": "Which of the following is NOT a valid Python data type?",
        "option_a": "List",
        "option_b": "Dictionary",
        "option_c": "Tuple",
        "option_d": "ArrayList",
        "answer": "D",
        "explanation": "ArrayList is a Java collection. Python commonly uses lists."
    },

    {
        "id": 15,
        "question": "What does the input() function return in Python?",
        "option_a": "Integer",
        "option_b": "String",
        "option_c": "Float",
        "option_d": "Boolean",
        "answer": "B",
        "explanation": "input() returns user input as a string unless explicitly converted."
    },

    {
        "id": 16,
        "question": "What is the output of print(len('Python'))?",
        "option_a": "5",
        "option_b": "6",
        "option_c": "7",
        "option_d": "Error",
        "answer": "B",
        "explanation": "The string Python contains 6 characters."
    },

    {
        "id": 17,
        "question": "What is the output of print('Python'[1:4])?",
        "option_a": "Pyt",
        "option_b": "yth",
        "option_c": "tho",
        "option_d": "ytho",
        "answer": "B",
        "explanation": "The slice [1:4] includes indexes 1, 2 and 3."
    },

    {
        "id": 18,
        "question": "Which collection is used to remove duplicate values?",
        "option_a": "List",
        "option_b": "Tuple",
        "option_c": "Set",
        "option_d": "String",
        "answer": "C",
        "explanation": "A set stores unique elements."
    },

    {
        "id": 19,
        "question": "What is the output of print({'a': 1, 'b': 2}['b'])?",
        "option_a": "1",
        "option_b": "2",
        "option_c": "b",
        "option_d": "Error",
        "answer": "B",
        "explanation": "The key b has the value 2."
    },

    {
        "id": 20,
        "question": "Which operator checks whether two variables refer to the same object?",
        "option_a": "==",
        "option_b": "=",
        "option_c": "is",
        "option_d": "!=",
        "answer": "C",
        "explanation": "The is operator checks object identity."
    },

    {
        "id": 21,
        "question": "What is the output of print(10 > 5 and 5 > 2)?",
        "option_a": "True",
        "option_b": "False",
        "option_c": "10",
        "option_d": "Error",
        "answer": "A",
        "explanation": "Both conditions are True."
    },

    {
        "id": 22,
        "question": "What is the output of print(3 * 'Python')?",
        "option_a": "PythonPythonPython",
        "option_b": "3Python",
        "option_c": "Python3",
        "option_d": "Error",
        "answer": "A",
        "explanation": "Multiplying a string by an integer repeats the string."
    },

    {
        "id": 23,
        "question": "What is the output of print(bool(0))?",
        "option_a": "True",
        "option_b": "False",
        "option_c": "0",
        "option_d": "Error",
        "answer": "B",
        "explanation": "0 is considered False when converted to boolean."
    },

    {
        "id": 24,
        "question": "What is the output of print([1, 2, 3][::-1])?",
        "option_a": "[1, 2, 3]",
        "option_b": "[3, 2, 1]",
        "option_c": "[2, 1, 3]",
        "option_d": "Error",
        "answer": "B",
        "explanation": "[::-1] reverses the list."
    },

    {
        "id": 25,
        "question": "Which keyword is used to define a function in Python?",
        "option_a": "function",
        "option_b": "define",
        "option_c": "def",
        "option_d": "fun",
        "answer": "C",
        "explanation": "The def keyword is used to define a function."
    },

    {
        "id": 26,
        "question": "What is the output of print(10 == 10.0)?",
        "option_a": "True",
        "option_b": "False",
        "option_c": "10.0",
        "option_d": "Error",
        "answer": "A",
        "explanation": "10 and 10.0 have the same numeric value."
    },

    {
        "id": 27,
        "question": "Which data structure follows the LIFO principle?",
        "option_a": "Queue",
        "option_b": "Stack",
        "option_c": "Array",
        "option_d": "Dictionary",
        "answer": "B",
        "explanation": "A stack follows Last In, First Out."
    },

    {
        "id": 28,
        "question": "What is the output of print(2 + 3 * 4)?",
        "option_a": "20",
        "option_b": "14",
        "option_c": "24",
        "option_d": "Error",
        "answer": "B",
        "explanation": "Multiplication has higher precedence, so 2 + 12 = 14."
    },

    {
        "id": 29,
        "question": "Which method adds an element to the end of a Python list?",
        "option_a": "add()",
        "option_b": "insert()",
        "option_c": "append()",
        "option_d": "push()",
        "answer": "C",
        "explanation": "append() adds an element to the end of a list."
    },

    {
        "id": 30,
        "question": "What is the output of print(type((1, 2, 3)))?",
        "option_a": "<class 'list'>",
        "option_b": "<class 'tuple'>",
        "option_c": "<class 'set'>",
        "option_d": "<class 'dict'>",
        "answer": "B",
        "explanation": "(1, 2, 3) is a tuple."
    }

]


# ============================================================
# SQL QUESTIONS
# ============================================================

sql_questions = [

    {
        "question": "Which SQL command is used to retrieve data from a database?",
        "options": ["INSERT", "SELECT", "UPDATE", "DELETE"],
        "answer": "SELECT",
        "explanation": "SELECT is used to retrieve data from one or more tables."
    },

    {
        "question": "Which SQL clause is used to filter records?",
        "options": ["ORDER BY", "WHERE", "GROUP BY", "SELECT"],
        "answer": "WHERE",
        "explanation": "WHERE filters rows based on a specified condition."
    },

    {
        "question": "Which command is used to remove all records from a table?",
        "options": ["DELETE", "DROP", "TRUNCATE", "REMOVE"],
        "answer": "TRUNCATE",
        "explanation": "TRUNCATE removes all rows while keeping the table structure."
    },

    {
        "question": "Which SQL function is used to count rows?",
        "options": ["SUM()", "COUNT()", "TOTAL()", "NUMBER()"],
        "answer": "COUNT()",
        "explanation": "COUNT() returns the number of rows."
    },

    {
        "question": "Which clause is used to sort query results?",
        "options": ["SORT BY", "ORDER BY", "GROUP BY", "ARRANGE BY"],
        "answer": "ORDER BY",
        "explanation": "ORDER BY sorts the result set."
    },

    {
        "question": "Which SQL keyword removes duplicate records from the result?",
        "options": ["UNIQUE", "DISTINCT", "REMOVE", "FILTER"],
        "answer": "DISTINCT",
        "explanation": "DISTINCT returns unique values."
    },

    {
        "question": "Which SQL command is used to add new records?",
        "options": ["ADD", "INSERT", "CREATE", "UPDATE"],
        "answer": "INSERT",
        "explanation": "INSERT INTO adds new rows to a table."
    },

    {
        "question": "Which SQL command modifies existing records?",
        "options": ["CHANGE", "MODIFY", "UPDATE", "ALTER"],
        "answer": "UPDATE",
        "explanation": "UPDATE modifies existing records."
    },

    {
        "question": "Which SQL command removes selected records?",
        "options": ["DELETE", "DROP", "REMOVE", "CLEAR"],
        "answer": "DELETE",
        "explanation": "DELETE removes rows based on a condition."
    },

    {
        "question": "Which SQL command removes a table completely?",
        "options": ["DELETE", "TRUNCATE", "DROP", "REMOVE"],
        "answer": "DROP",
        "explanation": "DROP TABLE removes the table and its structure."
    },

    {
        "question": "Which operator is used for pattern matching?",
        "options": ["MATCH", "LIKE", "SEARCH", "PATTERN"],
        "answer": "LIKE",
        "explanation": "LIKE is used with wildcard characters."
    },

    {
        "question": "Which wildcard represents zero or more characters?",
        "options": ["_", "%", "*", "#"],
        "answer": "%",
        "explanation": "% represents zero or more characters."
    },

    {
        "question": "Which wildcard represents exactly one character?",
        "options": ["%", "_", "*", "?"],
        "answer": "_",
        "explanation": "_ represents exactly one character."
    },

    {
        "question": "Which clause groups rows having the same values?",
        "options": ["GROUP BY", "ORDER BY", "WHERE", "HAVING"],
        "answer": "GROUP BY",
        "explanation": "GROUP BY groups rows for aggregate calculations."
    },

    {
        "question": "Which clause filters grouped records?",
        "options": ["WHERE", "FILTER", "HAVING", "GROUP"],
        "answer": "HAVING",
        "explanation": "HAVING filters groups after GROUP BY."
    },

    {
        "question": "Which function returns the total of numeric values?",
        "options": ["TOTAL()", "ADD()", "SUM()", "COUNT()"],
        "answer": "SUM()",
        "explanation": "SUM() calculates the total."
    },

    {
        "question": "Which function returns the average value?",
        "options": ["AVG()", "MEAN()", "AVERAGE()", "MID()"],
        "answer": "AVG()",
        "explanation": "AVG() returns the average value."
    },

    {
        "question": "Which function returns the largest value?",
        "options": ["HIGH()", "MAX()", "LARGE()", "TOP()"],
        "answer": "MAX()",
        "explanation": "MAX() returns the maximum value."
    },

    {
        "question": "Which function returns the smallest value?",
        "options": ["MIN()", "LOW()", "SMALL()", "BOTTOM()"],
        "answer": "MIN()",
        "explanation": "MIN() returns the minimum value."
    },

    {
        "question": "Which JOIN returns matching records from both tables?",
        "options": ["LEFT JOIN", "RIGHT JOIN", "INNER JOIN", "FULL JOIN"],
        "answer": "INNER JOIN",
        "explanation": "INNER JOIN returns matching rows from both tables."
    },

    {
        "question": "Which JOIN returns all records from the left table?",
        "options": ["INNER JOIN", "LEFT JOIN", "RIGHT JOIN", "CROSS JOIN"],
        "answer": "LEFT JOIN",
        "explanation": "LEFT JOIN returns all rows from the left table and matching rows from the right table."
    },

    {
        "question": "Which key uniquely identifies each record?",
        "options": ["Foreign Key", "Primary Key", "Candidate Key", "Alternate Key"],
        "answer": "Primary Key",
        "explanation": "A Primary Key uniquely identifies each row."
    },

    {
        "question": "Which key creates a relationship between tables?",
        "options": ["Primary Key", "Foreign Key", "Super Key", "Unique Key"],
        "answer": "Foreign Key",
        "explanation": "A Foreign Key references a key in another table."
    },

    {
        "question": "Which constraint prevents NULL values?",
        "options": ["UNIQUE", "NOT NULL", "DEFAULT", "CHECK"],
        "answer": "NOT NULL",
        "explanation": "NOT NULL prevents NULL values."
    },

    {
        "question": "Which constraint ensures values are different?",
        "options": ["UNIQUE", "CHECK", "DEFAULT", "NOT NULL"],
        "answer": "UNIQUE",
        "explanation": "UNIQUE prevents duplicate values."
    },

    {
        "question": "Which operator checks whether a value is within a range?",
        "options": ["IN", "BETWEEN", "RANGE", "WITHIN"],
        "answer": "BETWEEN",
        "explanation": "BETWEEN checks whether a value falls within an inclusive range."
    },

    {
        "question": "Which operator matches a value against multiple values?",
        "options": ["BETWEEN", "IN", "MATCH", "ANY"],
        "answer": "IN",
        "explanation": "IN checks whether a value matches any value in a specified list."
    },

    {
        "question": "Which keyword gives a temporary name to a column or table?",
        "options": ["NAME", "AS", "RENAME", "ALIAS"],
        "answer": "AS",
        "explanation": "AS is used to create an alias."
    },

    {
        "question": "Which SQL command changes the structure of an existing table?",
        "options": ["UPDATE", "ALTER", "MODIFY", "CHANGE"],
        "answer": "ALTER",
        "explanation": "ALTER TABLE changes the table structure."
    },

    {
        "question": "Which SQL statement creates a new table?",
        "options": ["MAKE TABLE", "NEW TABLE", "CREATE TABLE", "ADD TABLE"],
        "answer": "CREATE TABLE",
        "explanation": "CREATE TABLE creates a new table."
    }

]


# ============================================================
# JAVA QUESTIONS
# ============================================================

java_questions = [

    {
        "question": "Which keyword is used to create a class in Java?",
        "options": ["class", "Class", "create", "new"],
        "answer": "class",
        "explanation": "The class keyword is used to declare a class in Java."
    },

    {
        "question": "Which method is the entry point of a Java program?",
        "options": ["start()", "main()", "run()", "execute()"],
        "answer": "main()",
        "explanation": "The main() method is the entry point of a Java application."
    },

    {
        "question": "Which keyword is used to inherit a class in Java?",
        "options": ["implements", "inherits", "extends", "super"],
        "answer": "extends",
        "explanation": "The extends keyword is used for class inheritance."
    },

    {
        "question": "Which keyword is used to implement an interface?",
        "options": ["extends", "implements", "interface", "inherit"],
        "answer": "implements",
        "explanation": "A class uses implements to implement an interface."
    },

    {
        "question": "Which concept allows one interface to have multiple implementations?",
        "options": ["Inheritance", "Polymorphism", "Encapsulation", "Abstraction"],
        "answer": "Polymorphism",
        "explanation": "Polymorphism allows the same interface or method to have different implementations."
    },

    {
        "question": "Which OOP concept hides internal implementation details?",
        "options": ["Inheritance", "Polymorphism", "Abstraction", "Encapsulation"],
        "answer": "Abstraction",
        "explanation": "Abstraction hides implementation details and exposes only necessary functionality."
    },

    {
        "question": "Which OOP concept binds data and methods together?",
        "options": ["Encapsulation", "Inheritance", "Abstraction", "Polymorphism"],
        "answer": "Encapsulation",
        "explanation": "Encapsulation combines data and methods into a single unit such as a class."
    },

    {
        "question": "Which keyword is used to create an object in Java?",
        "options": ["object", "create", "new", "instance"],
        "answer": "new",
        "explanation": "The new keyword creates an object of a class."
    },

    {
        "question": "Which keyword refers to the current object?",
        "options": ["self", "this", "current", "object"],
        "answer": "this",
        "explanation": "this refers to the current object."
    },

    {
        "question": "Which keyword is used to refer to the parent class?",
        "options": ["parent", "base", "super", "this"],
        "answer": "super",
        "explanation": "super is used to access members of the parent class."
    },

    {
        "question": "Which access modifier provides the highest level of restriction?",
        "options": ["public", "protected", "private", "default"],
        "answer": "private",
        "explanation": "A private member can be accessed only within its own class."
    },

    {
        "question": "Which access modifier allows access from anywhere?",
        "options": ["private", "protected", "default", "public"],
        "answer": "public",
        "explanation": "Public members can be accessed from anywhere, subject to class/package rules."
    },

    {
        "question": "Which keyword is used to prevent method overriding?",
        "options": ["static", "final", "private", "const"],
        "answer": "final",
        "explanation": "A final method cannot be overridden by a subclass."
    },

    {
        "question": "Which keyword is used to define a constant variable?",
        "options": ["constant", "const", "final", "static"],
        "answer": "final",
        "explanation": "A final variable can be assigned only once."
    },

    {
        "question": "Which data type stores true or false values?",
        "options": ["boolean", "bool", "Boolean", "bit"],
        "answer": "boolean",
        "explanation": "boolean is the primitive data type used for true and false."
    },

    {
        "question": "What is the size of an int in Java?",
        "options": ["8 bits", "16 bits", "32 bits", "64 bits"],
        "answer": "32 bits",
        "explanation": "An int in Java is a signed 32-bit integer."
    },

    {
        "question": "Which keyword is used to handle an exception?",
        "options": ["catch", "error", "handle", "exception"],
        "answer": "catch",
        "explanation": "The catch block handles an exception thrown by the try block."
    },

    {
        "question": "Which block is always executed whether an exception occurs or not?",
        "options": ["try", "catch", "finally", "throw"],
        "answer": "finally",
        "explanation": "The finally block generally executes whether an exception occurs or not."
    },

    {
        "question": "Which keyword is used to explicitly throw an exception?",
        "options": ["throws", "throw", "exception", "catch"],
        "answer": "throw",
        "explanation": "The throw keyword is used to explicitly throw an exception."
    },

    {
        "question": "Which keyword declares that a method may throw exceptions?",
        "options": ["throw", "throws", "exception", "catch"],
        "answer": "throws",
        "explanation": "throws declares exceptions that a method may pass to its caller."
    },

    {
        "question": "Which collection does not allow duplicate elements?",
        "options": ["List", "Set", "Queue", "ArrayList"],
        "answer": "Set",
        "explanation": "A Set does not allow duplicate elements."
    },

    {
        "question": "Which collection maintains insertion order and allows duplicates?",
        "options": ["Set", "List", "Map", "HashSet"],
        "answer": "List",
        "explanation": "List allows duplicates and generally maintains insertion order."
    },

    {
        "question": "Which class implements a resizable array?",
        "options": ["LinkedList", "ArrayList", "HashSet", "TreeSet"],
        "answer": "ArrayList",
        "explanation": "ArrayList is a resizable-array implementation of the List interface."
    },

    {
        "question": "Which collection stores key-value pairs?",
        "options": ["List", "Set", "Map", "Queue"],
        "answer": "Map",
        "explanation": "Map stores data as key-value pairs."
    },

    {
        "question": "Which Map implementation generally does not maintain insertion order?",
        "options": ["LinkedHashMap", "TreeMap", "HashMap", "SortedMap"],
        "answer": "HashMap",
        "explanation": "HashMap does not guarantee insertion order."
    },

    {
        "question": "Which keyword is used for method overloading?",
        "options": ["There is no special keyword", "overload", "extends", "virtual"],
        "answer": "There is no special keyword",
        "explanation": "Method overloading is achieved by using the same method name with different parameter lists."
    },

    {
        "question": "Can Java support multiple inheritance using classes?",
        "options": ["Yes", "No", "Only with abstract classes", "Only with final classes"],
        "answer": "No",
        "explanation": "Java does not support multiple inheritance through classes, but it supports multiple interfaces."
    },

    {
        "question": "Which keyword is used to create an interface?",
        "options": ["Interface", "interface", "implements", "abstract"],
        "answer": "interface",
        "explanation": "The interface keyword is used to declare an interface."
    },

    {
        "question": "Which keyword is used to define an abstract class?",
        "options": ["abstract", "interface", "virtual", "base"],
        "answer": "abstract",
        "explanation": "The abstract keyword is used to declare an abstract class or method."
    },

    {
        "question": "Which feature automatically manages unused objects in Java?",
        "options": ["Destructor", "Garbage Collection", "Pointer", "Memory Reset"],
        "answer": "Garbage Collection",
        "explanation": "Java's garbage collector automatically reclaims memory from unreachable objects."
    },


]

dsa_questions = [
        {
        "id": 1,
        "question": "What is the time complexity of accessing an element in an array by index?",
        "options": ["O(1)", "O(n)", "O(log n)", "O(n²)"],
        "answer": "O(1)",
        "explanation": "Array elements can be accessed directly using their index, so the time complexity is O(1)."
    },

    {
        "id": 2,
        "question": "Which data structure follows the LIFO principle?",
        "options": ["Queue", "Stack", "Array", "Linked List"],
        "answer": "Stack",
        "explanation": "Stack follows Last In, First Out (LIFO)."
    },

    {
        "id": 3,
        "question": "Which data structure follows the FIFO principle?",
        "options": ["Stack", "Queue", "Tree", "Graph"],
        "answer": "Queue",
        "explanation": "Queue follows First In, First Out (FIFO)."
    },

    {
        "id": 4,
        "question": "What is the time complexity of linear search in the worst case?",
        "options": ["O(1)", "O(log n)", "O(n)", "O(n²)"],
        "answer": "O(n)",
        "explanation": "Linear search may need to check every element, giving O(n) worst-case complexity."
    },

    {
        "id": 5,
        "question": "Binary search can be applied efficiently on which type of array?",
        "options": ["Unsorted array", "Sorted array", "Empty array only", "Circular array only"],
        "answer": "Sorted array",
        "explanation": "Binary search repeatedly divides a sorted search space into two halves."
    },

    {
        "id": 6,
        "question": "What is the worst-case time complexity of binary search?",
        "options": ["O(n)", "O(n²)", "O(log n)", "O(1)"],
        "answer": "O(log n)",
        "explanation": "Binary search eliminates half of the remaining elements at each step."
    },

    {
        "id": 7,
        "question": "Which sorting algorithm repeatedly selects the minimum element?",
        "options": ["Bubble Sort", "Selection Sort", "Merge Sort", "Quick Sort"],
        "answer": "Selection Sort",
        "explanation": "Selection Sort repeatedly selects the minimum element from the unsorted portion."
    },

    {
        "id": 8,
        "question": "Which sorting algorithm repeatedly swaps adjacent elements if they are in the wrong order?",
        "options": ["Selection Sort", "Merge Sort", "Bubble Sort", "Quick Sort"],
        "answer": "Bubble Sort",
        "explanation": "Bubble Sort compares adjacent elements and swaps them when necessary."
    },

    {
        "id": 9,
        "question": "What is the average time complexity of Merge Sort?",
        "options": ["O(n)", "O(log n)", "O(n log n)", "O(n²)"],
        "answer": "O(n log n)",
        "explanation": "Merge Sort divides the array into halves and merges them in O(n log n) time."
    },

    {
        "id": 10,
        "question": "Which technique is used by Merge Sort?",
        "options": ["Greedy", "Divide and Conquer", "Backtracking", "Dynamic Programming"],
        "answer": "Divide and Conquer",
        "explanation": "Merge Sort divides the problem into smaller subproblems and combines their results."
    },

    {
        "id": 11,
        "question": "Which data structure is commonly used to implement recursion internally?",
        "options": ["Queue", "Stack", "Heap", "Graph"],
        "answer": "Stack",
        "explanation": "Function calls and recursive calls are stored in the call stack."
    },

    {
        "id": 12,
        "question": "What is the main advantage of a linked list over an array?",
        "options": ["Constant-time random access", "Dynamic size", "Less memory usage always", "Faster binary search"],
        "answer": "Dynamic size",
        "explanation": "Linked lists can grow or shrink dynamically without requiring contiguous memory."
    },

    {
        "id": 13,
        "question": "In a singly linked list, each node normally contains data and what?",
        "options": ["Two previous pointers", "A pointer to the next node", "Only an index", "A stack"],
        "answer": "A pointer to the next node",
        "explanation": "A singly linked-list node stores data and a reference to the next node."
    },

    {
        "id": 14,
        "question": "Which data structure is best suited for implementing a priority queue?",
        "options": ["Heap", "Stack", "Linked List only", "String"],
        "answer": "Heap",
        "explanation": "A heap efficiently supports priority-based insertion and removal."
    },

    {
        "id": 15,
        "question": "Which tree traversal visits Root, Left, Right?",
        "options": ["Inorder", "Postorder", "Preorder", "Level Order"],
        "answer": "Preorder",
        "explanation": "Preorder traversal follows Root → Left → Right."
    },

    {
        "id": 16,
        "question": "Which tree traversal visits Left, Root, Right?",
        "options": ["Preorder", "Inorder", "Postorder", "Level Order"],
        "answer": "Inorder",
        "explanation": "Inorder traversal follows Left → Root → Right."
    },

    {
        "id": 17,
        "question": "Which tree traversal visits Left, Right, Root?",
        "options": ["Preorder", "Inorder", "Postorder", "Level Order"],
        "answer": "Postorder",
        "explanation": "Postorder traversal follows Left → Right → Root."
    },

    {
        "id": 18,
        "question": "Which data structure is commonly used for Breadth-First Search (BFS)?",
        "options": ["Stack", "Queue", "Heap", "Hash Table"],
        "answer": "Queue",
        "explanation": "BFS explores nodes level by level and uses a queue."
    },

    {
        "id": 19,
        "question": "Which data structure is commonly used for Depth-First Search (DFS)?",
        "options": ["Queue", "Stack", "Heap", "Array only"],
        "answer": "Stack",
        "explanation": "DFS uses a stack, either explicitly or through recursion."
    },

    {
        "id": 20,
        "question": "Which data structure stores elements as key-value pairs?",
        "options": ["Stack", "Queue", "Hash Map", "Array"],
        "answer": "Hash Map",
        "explanation": "A Hash Map stores data in key-value pairs and provides efficient average lookup."
    },

    {
        "id": 21,
        "question": "What is the average time complexity of searching in a Hash Map?",
        "options": ["O(1)", "O(n)", "O(log n)", "O(n²)"],
        "answer": "O(1)",
        "explanation": "Hash Maps provide average-case constant-time lookup using hashing."
    },

    {
        "id": 22,
        "question": "Which technique is commonly used to find a pair of elements with a given sum efficiently?",
        "options": ["Hashing", "Only recursion", "Bubble Sort only", "BFS"],
        "answer": "Hashing",
        "explanation": "A Hash Map or Hash Set can be used to check complements efficiently."
    },

    {
        "id": 23,
        "question": "What is the purpose of a base case in recursion?",
        "options": ["To increase memory usage", "To stop recursive calls", "To sort data", "To create a loop"],
        "answer": "To stop recursive calls",
        "explanation": "The base case provides the stopping condition for recursion."
    },

    {
        "id": 24,
        "question": "Which data structure is used to efficiently find the maximum or minimum element with priority operations?",
        "options": ["Heap", "Stack", "Queue only", "String"],
        "answer": "Heap",
        "explanation": "A min-heap or max-heap keeps the highest-priority element accessible."
    },

    {
        "id": 25,
        "question": "What is the worst-case time complexity of Quick Sort?",
        "options": ["O(n)", "O(log n)", "O(n log n)", "O(n²)"],
        "answer": "O(n²)",
        "explanation": "Quick Sort can degrade to O(n²) when partitions are highly unbalanced."
    },

    {
        "id": 26,
        "question": "Which technique is useful for finding the maximum sum subarray in linear time?",
        "options": ["Kadane's Algorithm", "Binary Search", "BFS", "Selection Sort"],
        "answer": "Kadane's Algorithm",
        "explanation": "Kadane's Algorithm finds the maximum subarray sum in O(n) time."
    },

    {
        "id": 27,
        "question": "Which technique is commonly used to solve problems involving a continuous range or subarray?",
        "options": ["Sliding Window", "Binary Tree", "DFS only", "Heap Sort"],
        "answer": "Sliding Window",
        "explanation": "Sliding Window efficiently processes contiguous ranges by maintaining a moving window."
    },

    {
        "id": 28,
        "question": "What is the main purpose of Big-O notation?",
        "options": ["To measure code length", "To describe algorithm efficiency", "To count variables", "To measure screen size"],
        "answer": "To describe algorithm efficiency",
        "explanation": "Big-O describes how an algorithm's time or space requirements grow with input size."
    },

    {
        "id": 29,
        "question": "Which data structure can be used to check balanced parentheses?",
        "options": ["Queue", "Stack", "Heap", "Graph"],
        "answer": "Stack",
        "explanation": "A stack keeps track of opening brackets so they can be matched with closing brackets."
    },

    {
        "id": 30,
        "question": "What is the space complexity of an array containing n elements?",
        "options": ["O(1)", "O(log n)", "O(n)", "O(n²)"],
        "answer": "O(n)",
        "explanation": "An array storing n elements requires space proportional to n."
    }



]

dbms_questions = [
        {
        "id": 1,
        "question": "What does DBMS stand for?",
        "options": [
            "Database Management System",
            "Data Backup Management System",
            "Database Monitoring System",
            "Data Management Software"
        ],
        "answer": "Database Management System",
        "explanation": "DBMS stands for Database Management System, which is software used to create, store, manage and retrieve data."
    },

    {
        "id": 2,
        "question": "Which key uniquely identifies each record in a table?",
        "options": [
            "Foreign Key",
            "Primary Key",
            "Candidate Key",
            "Composite Key"
        ],
        "answer": "Primary Key",
        "explanation": "A primary key uniquely identifies every record in a table and cannot contain NULL values."
    },

    {
        "id": 3,
        "question": "Which key establishes a relationship between two tables?",
        "options": [
            "Primary Key",
            "Foreign Key",
            "Super Key",
            "Alternate Key"
        ],
        "answer": "Foreign Key",
        "explanation": "A foreign key references a key in another table and helps maintain relationships between tables."
    },

    {
        "id": 4,
        "question": "Which constraint prevents NULL values in a column?",
        "options": [
            "UNIQUE",
            "CHECK",
            "NOT NULL",
            "DEFAULT"
        ],
        "answer": "NOT NULL",
        "explanation": "The NOT NULL constraint ensures that a column cannot contain NULL values."
    },

    {
        "id": 5,
        "question": "Which constraint ensures that all values in a column are different?",
        "options": [
            "NOT NULL",
            "UNIQUE",
            "DEFAULT",
            "CHECK"
        ],
        "answer": "UNIQUE",
        "explanation": "The UNIQUE constraint prevents duplicate values in a column."
    },

    {
        "id": 6,
        "question": "What is normalization used for?",
        "options": [
            "Increasing data redundancy",
            "Reducing data redundancy",
            "Deleting all duplicate databases",
            "Increasing storage space"
        ],
        "answer": "Reducing data redundancy",
        "explanation": "Normalization organizes data to reduce redundancy and improve data integrity."
    },

    {
        "id": 7,
        "question": "Which normal form removes repeating groups and ensures atomic values?",
        "options": [
            "1NF",
            "2NF",
            "3NF",
            "BCNF"
        ],
        "answer": "1NF",
        "explanation": "First Normal Form requires atomic values and removes repeating groups."
    },

    {
        "id": 8,
        "question": "Which normal form removes partial dependency?",
        "options": [
            "1NF",
            "2NF",
            "3NF",
            "BCNF"
        ],
        "answer": "2NF",
        "explanation": "Second Normal Form removes partial dependency on a composite key."
    },

    {
        "id": 9,
        "question": "Which normal form removes transitive dependency?",
        "options": [
            "1NF",
            "2NF",
            "3NF",
            "4NF"
        ],
        "answer": "3NF",
        "explanation": "Third Normal Form removes transitive dependencies."
    },

    {
        "id": 10,
        "question": "What does SQL stand for?",
        "options": [
            "Structured Query Language",
            "Simple Query Language",
            "System Query Language",
            "Structured Question Language"
        ],
        "answer": "Structured Query Language",
        "explanation": "SQL stands for Structured Query Language and is used to interact with relational databases."
    },

    {
        "id": 11,
        "question": "Which SQL command is used to retrieve data?",
        "options": [
            "INSERT",
            "UPDATE",
            "SELECT",
            "DELETE"
        ],
        "answer": "SELECT",
        "explanation": "SELECT is used to retrieve data from one or more tables."
    },

    {
        "id": 12,
        "question": "Which SQL command is used to add new records?",
        "options": [
            "INSERT",
            "ADD",
            "CREATE",
            "APPEND"
        ],
        "answer": "INSERT",
        "explanation": "INSERT is used to add new rows to a table."
    },

    {
        "id": 13,
        "question": "Which SQL command is used to modify existing records?",
        "options": [
            "CHANGE",
            "MODIFY",
            "UPDATE",
            "ALTER"
        ],
        "answer": "UPDATE",
        "explanation": "UPDATE modifies existing records in a table."
    },

    {
        "id": 14,
        "question": "Which SQL command removes selected rows from a table?",
        "options": [
            "DROP",
            "DELETE",
            "REMOVE",
            "TRUNCATE"
        ],
        "answer": "DELETE",
        "explanation": "DELETE removes rows from a table and can use a WHERE condition."
    },

    {
        "id": 15,
        "question": "Which SQL command removes all rows from a table while keeping its structure?",
        "options": [
            "DROP",
            "DELETE",
            "TRUNCATE",
            "REMOVE"
        ],
        "answer": "TRUNCATE",
        "explanation": "TRUNCATE removes all rows while keeping the table structure."
    },

    {
        "id": 16,
        "question": "Which SQL command removes the table structure itself?",
        "options": [
            "DELETE",
            "TRUNCATE",
            "DROP",
            "CLEAR"
        ],
        "answer": "DROP",
        "explanation": "DROP removes the table and its structure from the database."
    },

    {
        "id": 17,
        "question": "Which clause is used to filter rows?",
        "options": [
            "GROUP BY",
            "WHERE",
            "ORDER BY",
            "HAVING"
        ],
        "answer": "WHERE",
        "explanation": "WHERE filters individual rows based on a specified condition."
    },

    {
        "id": 18,
        "question": "Which clause is used to group rows having the same values?",
        "options": [
            "ORDER BY",
            "WHERE",
            "GROUP BY",
            "HAVING"
        ],
        "answer": "GROUP BY",
        "explanation": "GROUP BY groups rows with the same values for aggregate calculations."
    },

    {
        "id": 19,
        "question": "Which clause is used to filter grouped records?",
        "options": [
            "WHERE",
            "HAVING",
            "GROUP BY",
            "ORDER BY"
        ],
        "answer": "HAVING",
        "explanation": "HAVING filters groups after GROUP BY has been applied."
    },

    {
        "id": 20,
        "question": "Which function returns the number of rows?",
        "options": [
            "SUM()",
            "COUNT()",
            "TOTAL()",
            "NUMBER()"
        ],
        "answer": "COUNT()",
        "explanation": "COUNT() returns the number of rows or non-NULL values depending on its usage."
    },

    {
        "id": 21,
        "question": "Which function calculates the average value?",
        "options": [
            "AVG()",
            "MEAN()",
            "AVERAGE()",
            "MID()"
        ],
        "answer": "AVG()",
        "explanation": "AVG() calculates the average of numeric values."
    },

    {
        "id": 22,
        "question": "Which function returns the highest value?",
        "options": [
            "HIGH()",
            "MAX()",
            "TOP()",
            "UPPER()"
        ],
        "answer": "MAX()",
        "explanation": "MAX() returns the maximum value from a set of values."
    },

    {
        "id": 23,
        "question": "Which JOIN returns only matching rows from both tables?",
        "options": [
            "LEFT JOIN",
            "RIGHT JOIN",
            "INNER JOIN",
            "FULL JOIN"
        ],
        "answer": "INNER JOIN",
        "explanation": "INNER JOIN returns rows where the join condition matches in both tables."
    },

    {
        "id": 24,
        "question": "Which JOIN returns all rows from the left table and matching rows from the right table?",
        "options": [
            "INNER JOIN",
            "LEFT JOIN",
            "RIGHT JOIN",
            "CROSS JOIN"
        ],
        "answer": "LEFT JOIN",
        "explanation": "LEFT JOIN returns all rows from the left table and matching rows from the right table."
    },

    {
        "id": 25,
        "question": "What is a transaction in DBMS?",
        "options": [
            "A database table",
            "A logical unit of database operations",
            "A type of key",
            "A database user"
        ],
        "answer": "A logical unit of database operations",
        "explanation": "A transaction is a logical unit of work containing one or more database operations."
    },

    {
        "id": 26,
        "question": "Which ACID property ensures that a transaction is completed fully or not at all?",
        "options": [
            "Consistency",
            "Isolation",
            "Atomicity",
            "Durability"
        ],
        "answer": "Atomicity",
        "explanation": "Atomicity ensures that all operations of a transaction happen completely or none happen."
    },

    {
        "id": 27,
        "question": "Which ACID property ensures that committed data remains saved after a system failure?",
        "options": [
            "Atomicity",
            "Consistency",
            "Isolation",
            "Durability"
        ],
        "answer": "Durability",
        "explanation": "Durability ensures that committed changes persist even after system failures."
    },

    {
        "id": 28,
        "question": "What is an index used for in a database?",
        "options": [
            "To increase data redundancy",
            "To speed up data retrieval",
            "To delete tables",
            "To create users"
        ],
        "answer": "To speed up data retrieval",
        "explanation": "Indexes can improve the speed of data retrieval operations."
    },

    {
        "id": 29,
        "question": "What is a view in DBMS?",
        "options": [
            "A physical copy of the database",
            "A virtual table based on a query",
            "A primary key",
            "A database backup"
        ],
        "answer": "A virtual table based on a query",
        "explanation": "A view is a virtual table whose data is derived from one or more tables using a query."
    },

    {
        "id": 30,
        "question": "Which command is commonly used to save a transaction permanently?",
        "options": [
            "SAVE",
            "COMMIT",
            "STORE",
            "PERSIST"
        ],
        "answer": "COMMIT",
        "explanation": "COMMIT permanently saves the changes made by the current transaction."
    }

]

cn_questions = [

    {
        "id": 1,
        "question": "What does LAN stand for?",
        "options": [
            "Local Area Network",
            "Large Area Network",
            "Long Area Network",
            "Linked Area Network"
        ],
        "answer": "Local Area Network",
        "explanation": "LAN stands for Local Area Network and connects devices within a limited geographical area."
    },

    {
        "id": 2,
        "question": "Which layer of the OSI model is responsible for routing?",
        "options": [
            "Physical Layer",
            "Data Link Layer",
            "Network Layer",
            "Transport Layer"
        ],
        "answer": "Network Layer",
        "explanation": "The Network Layer is responsible for logical addressing and routing packets between networks."
    },

    {
        "id": 3,
        "question": "Which protocol is used to reliably transfer data over the Internet?",
        "options": [
            "UDP",
            "TCP",
            "IP",
            "ARP"
        ],
        "answer": "TCP",
        "explanation": "TCP provides reliable, connection-oriented data transmission."
    },

    {
        "id": 4,
        "question": "Which protocol is connectionless?",
        "options": [
            "TCP",
            "UDP",
            "HTTP",
            "FTP"
        ],
        "answer": "UDP",
        "explanation": "UDP is connectionless and does not guarantee delivery or ordering of packets."
    },

    {
        "id": 5,
        "question": "What does IP stand for?",
        "options": [
            "Internet Protocol",
            "Internal Protocol",
            "Internet Process",
            "Internal Process"
        ],
        "answer": "Internet Protocol",
        "explanation": "IP stands for Internet Protocol and is responsible for addressing and routing packets."
    },

    {
        "id": 6,
        "question": "Which device connects different networks?",
        "options": [
            "Switch",
            "Router",
            "Hub",
            "Repeater"
        ],
        "answer": "Router",
        "explanation": "A router connects different networks and forwards packets between them."
    },

    {
        "id": 7,
        "question": "Which device primarily operates at the Data Link Layer?",
        "options": [
            "Router",
            "Switch",
            "Modem",
            "Repeater"
        ],
        "answer": "Switch",
        "explanation": "A traditional network switch primarily operates at Layer 2, the Data Link Layer."
    },

    {
        "id": 8,
        "question": "How many layers are there in the OSI model?",
        "options": [
            "5",
            "6",
            "7",
            "8"
        ],
        "answer": "7",
        "explanation": "The OSI model consists of seven layers."
    },

    {
        "id": 9,
        "question": "Which is the lowest layer of the OSI model?",
        "options": [
            "Data Link Layer",
            "Physical Layer",
            "Network Layer",
            "Transport Layer"
        ],
        "answer": "Physical Layer",
        "explanation": "The Physical Layer is Layer 1 and is responsible for transmitting raw bits."
    },

    {
        "id": 10,
        "question": "Which OSI layer is responsible for end-to-end communication?",
        "options": [
            "Network Layer",
            "Transport Layer",
            "Session Layer",
            "Application Layer"
        ],
        "answer": "Transport Layer",
        "explanation": "The Transport Layer provides end-to-end communication between applications."
    },

    {
        "id": 11,
        "question": "Which protocol translates domain names into IP addresses?",
        "options": [
            "HTTP",
            "DNS",
            "FTP",
            "SMTP"
        ],
        "answer": "DNS",
        "explanation": "DNS translates human-readable domain names into IP addresses."
    },

    {
        "id": 12,
        "question": "Which protocol is mainly used to transfer web pages?",
        "options": [
            "HTTP",
            "FTP",
            "SMTP",
            "SNMP"
        ],
        "answer": "HTTP",
        "explanation": "HTTP is the main protocol used for communication between web browsers and web servers."
    },

    {
        "id": 13,
        "question": "Which protocol is the secure version of HTTP?",
        "options": [
            "FTP",
            "HTTPS",
            "SSH",
            "SMTP"
        ],
        "answer": "HTTPS",
        "explanation": "HTTPS uses TLS encryption to secure HTTP communication."
    },

    {
        "id": 14,
        "question": "Which protocol is commonly used for sending emails?",
        "options": [
            "SMTP",
            "FTP",
            "HTTP",
            "DNS"
        ],
        "answer": "SMTP",
        "explanation": "SMTP stands for Simple Mail Transfer Protocol and is used for sending email."
    },

    {
        "id": 15,
        "question": "Which protocol is commonly used for transferring files?",
        "options": [
            "FTP",
            "SMTP",
            "DNS",
            "ARP"
        ],
        "answer": "FTP",
        "explanation": "FTP stands for File Transfer Protocol and is used to transfer files between systems."
    },

    {
        "id": 16,
        "question": "Which protocol maps an IP address to a MAC address?",
        "options": [
            "DNS",
            "ARP",
            "HTTP",
            "DHCP"
        ],
        "answer": "ARP",
        "explanation": "ARP resolves an IPv4 address to the corresponding MAC address on a local network."
    },

    {
        "id": 17,
        "question": "Which protocol automatically assigns IP addresses to devices?",
        "options": [
            "DNS",
            "DHCP",
            "ARP",
            "FTP"
        ],
        "answer": "DHCP",
        "explanation": "DHCP automatically provides devices with IP configuration such as IP address and gateway."
    },

    {
        "id": 18,
        "question": "Which type of address is associated with a network interface card?",
        "options": [
            "IP Address",
            "MAC Address",
            "Port Number",
            "Domain Name"
        ],
        "answer": "MAC Address",
        "explanation": "A MAC address is a hardware-level address associated with a network interface."
    },

    {
        "id": 19,
        "question": "Which topology connects all devices to a central device?",
        "options": [
            "Bus",
            "Ring",
            "Star",
            "Mesh"
        ],
        "answer": "Star",
        "explanation": "In a star topology, devices are connected to a central device such as a switch."
    },

    {
        "id": 20,
        "question": "What is the main purpose of a firewall?",
        "options": [
            "Increase CPU speed",
            "Filter network traffic",
            "Store files",
            "Assign MAC addresses"
        ],
        "answer": "Filter network traffic",
        "explanation": "A firewall monitors and filters incoming and outgoing network traffic based on security rules."
    },

    {
        "id": 21,
        "question": "Which protocol is used for secure remote login?",
        "options": [
            "SSH",
            "FTP",
            "HTTP",
            "SMTP"
        ],
        "answer": "SSH",
        "explanation": "SSH provides secure remote access to another computer over a network."
    },

    {
        "id": 22,
        "question": "What is the default port number of HTTP?",
        "options": [
            "21",
            "25",
            "80",
            "443"
        ],
        "answer": "80",
        "explanation": "HTTP commonly uses TCP port 80."
    },

    {
        "id": 23,
        "question": "What is the default port number of HTTPS?",
        "options": [
            "22",
            "53",
            "80",
            "443"
        ],
        "answer": "443",
        "explanation": "HTTPS commonly uses TCP port 443."
    },

    {
        "id": 24,
        "question": "Which protocol is used to resolve a domain name?",
        "options": [
            "DNS",
            "TCP",
            "UDP",
            "ICMP"
        ],
        "answer": "DNS",
        "explanation": "DNS resolves domain names such as example.com into IP addresses."
    },

    {
        "id": 25,
        "question": "Which protocol is commonly used by the ping command?",
        "options": [
            "TCP",
            "UDP",
            "ICMP",
            "HTTP"
        ],
        "answer": "ICMP",
        "explanation": "Ping commonly uses ICMP Echo Request and Echo Reply messages."
    },

    {
        "id": 26,
        "question": "What is bandwidth?",
        "options": [
            "Delay in a network",
            "Maximum data transfer capacity",
            "Number of routers",
            "IP address range"
        ],
        "answer": "Maximum data transfer capacity",
        "explanation": "Bandwidth represents the maximum amount of data that can be transmitted over a network connection per unit of time."
    },

    {
        "id": 27,
        "question": "What is network latency?",
        "options": [
            "Data storage capacity",
            "Time taken for data to travel",
            "Number of devices",
            "Network bandwidth"
        ],
        "answer": "Time taken for data to travel",
        "explanation": "Latency is the delay involved in transmitting data from one point to another."
    },

    {
        "id": 28,
        "question": "Which addressing system uses 32-bit addresses?",
        "options": [
            "IPv4",
            "IPv6",
            "MAC",
            "DNS"
        ],
        "answer": "IPv4",
        "explanation": "IPv4 uses 32-bit addresses, while IPv6 uses 128-bit addresses."
    },

    {
        "id": 29,
        "question": "Which addressing system uses 128-bit addresses?",
        "options": [
            "IPv4",
            "IPv6",
            "MAC",
            "ARP"
        ],
        "answer": "IPv6",
        "explanation": "IPv6 uses 128-bit addresses to provide a much larger address space."
    },

    {
        "id": 30,
        "question": "Which transport layer protocol is faster but does not guarantee delivery?",
        "options": [
            "TCP",
            "UDP",
            "HTTP",
            "FTP"
        ],
        "answer": "UDP",
        "explanation": "UDP has lower overhead than TCP but does not guarantee delivery, ordering, or retransmission."
    }

]


# ============================================================
# HOME PAGE
# ============================================================

@app.route("/")
def home():

    return render_template(
        "index.html"
    )


# ============================================================
# REGISTER
# ============================================================

@app.route(
    "/register",
    methods=["GET", "POST"]
)
def register():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        if password != confirm_password:

            return (
                "Passwords do not match. "
                "Please go back and try again."
            )

        existing_user = User.query.filter_by(
            email=email
        ).first()

        if existing_user:

            return (
                "An account with this email "
                "already exists."
            )

        hashed_password = generate_password_hash(
            password
        )

        new_user = User(
            name=name,
            email=email,
            password=hashed_password
        )

        db.session.add(new_user)
        db.session.commit()

        return redirect("/login")

    return render_template(
        "register.html"
    )


# ============================================================
# LOGIN
# ============================================================

@app.route(
    "/login",
    methods=["GET", "POST"]
)
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(
            email=email
        ).first()

        if user and check_password_hash(
            user.password,
            password
        ):

            session["user_id"] = user.id
            session["user_name"] = user.name
            session["user_email"] = user.email

            return redirect(
                "/dashboard"
            )

        return (
            "Invalid email or password. "
            "Please try again."
        )

    return render_template(
        "login.html"
    )


@app.route("/resume-analyzer", methods=["GET", "POST"])
def resume_analyzer():

    if "user_id" not in session:
        return redirect("/login")

    if request.method == "POST":

        resume = request.files.get("resume")

        if not resume:
            return render_template(
                "resume_analyzer.html",
                error="Please select a PDF resume."
            )

        if resume.filename == "":
            return render_template(
                "resume_analyzer.html",
                error="Please select a PDF resume."
            )

        if not resume.filename.lower().endswith(".pdf"):
            return render_template(
                "resume_analyzer.html",
                error="Only PDF files are allowed."
            )

        resume_text = ""

        reader = PdfReader(resume)

        for page in reader.pages:
            text = page.extract_text()

            if text:
                resume_text += text + "\n"

        text_lower = resume_text.lower()

        sections = {
            "Contact Information": (
                "@" in text_lower
                or any(char.isdigit() for char in text_lower)
            ),

            "Professional Summary": any(
                phrase in text_lower
                for phrase in [
                    "professional summary",
                    "about me",
                    "summary",
                    "profile"
                ]
            ),

            "Technical Skills": "technical skills" in text_lower,

            "Projects": "projects" in text_lower,

            "Education": "education" in text_lower,

            "Experience": any(
                phrase in text_lower
                for phrase in [
                    "work experience",
                    "professional experience",
                    "employment history",
                    "work history"
                ]
            ),

            "Certifications": "certifications" in text_lower
        }


        skill_keywords = [
            "html",
            "css",
            "javascript",
            "react",
            "python",
            "java",
            "mysql",
            "sql",
            "git",
            "flask",
            "mongodb",
            "node.js"
        ]

        detected_skills = []

        for skill in skill_keywords:
            if skill in text_lower:
                detected_skills.append(skill.upper())

        suggestions = []        

        if not sections["Contact Information"]:
            suggestions.append(
                "Add your phone number, professional email address and location so recruiters can easily contact you."
            )

        if not sections["Professional Summary"]:
            suggestions.append(
                "Add a concise professional summary describing your technical strengths, career goal and the type of role you are targeting."
            )

        if not sections["Technical Skills"]:
            suggestions.append(
                "Add a dedicated Technical Skills section and organize technologies by categories such as programming languages, frontend, database and tools."
            )

        if not sections["Projects"]:
            suggestions.append(
                "Add 2–3 relevant projects with technologies used, your contribution, key features and measurable outcomes."
            )

        if not sections["Education"]:
            suggestions.append(
                "Add your degree, college name, graduation year and other relevant academic details."
            )

        if not sections["Experience"]:
            suggestions.append(
                "If you have internships, training or relevant experience, include the role, organization, responsibilities and achievements."
            )

        if not sections["Certifications"]:
            suggestions.append(
                "Add relevant certifications, courses or technical training that support your target job role."
            )

        if sections["Projects"]:
            suggestions.append(
                "Strengthen project descriptions by highlighting your specific contribution, technical implementation and measurable results."
            )

        if detected_skills:
            suggestions.append(
                "Your resume includes technical skills. Keep the skills section focused on technologies relevant to the job you are applying for."
            )

        if len(detected_skills) < 5:
            suggestions.append(
                "Consider adding relevant technical skills that you can confidently discuss during technical interviews."
            )

        if len(suggestions) > 5:
            suggestions = suggestions[:5]

        skill_keywords = [
            "html",
            "css",
            "javascript",
            "react",
            "python",
            "java",
            "mysql",
            "sql",
            "git",
            "flask",
            "mongodb",
            "node.js"
        ]

        detected_skills = []

        for skill in skill_keywords:
            if skill in text_lower:
                detected_skills.append(skill.upper())

        completed_sections = sum(sections.values())

        analysis_score = int(
            (completed_sections / len(sections)) * 100
        )

        return render_template(
            "resume_analyzer.html",
            success="Resume uploaded and analyzed successfully!",
            resume_text=resume_text,
            sections=sections,
            analysis_score=analysis_score,
            suggestions=suggestions,
            detected_skills=detected_skills
        )

    return render_template("resume_analyzer.html")


# ============================================================
# DASHBOARD
# ============================================================

@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect("/login")

    questions_attempted = session.get("questions_attempted", 0)
    progress = min(int((questions_attempted / 30) * 100), 100)
    
    interviews_completed = session.get("interview_sessions", 0)

    return render_template(
        "dashboard.html",
        progress=progress,
        questions_attempted=questions_attempted,
        interviews_completed=interviews_completed
    )


@app.route("/analytics")
def analytics():

    if "user_id" not in session:
        return redirect("/login")

    questions_attempted = session.get(
        "questions_attempted",
        0
    )

    interviews_completed = session.get(
        "interview_sessions",
        0
    )

    # =========================
    # TECHNICAL SCORES
    # =========================

    python_score = session.get("python_score", 0)
    sql_score = session.get("sql_score", 0)
    java_score = session.get("java_score", 0)
    dsa_score = session.get("dsa_score", 0)
    dbms_score = session.get("dbms_score", 0)
    cn_score = session.get("cn_score", 0)

    # =========================
    # PERCENTAGES
    # =========================

    python_percentage = round(
        (python_score / 30) * 100
    )

    sql_percentage = round(
        (sql_score / 30) * 100
    )

    java_percentage = round(
        (java_score / 30) * 100
    )

    dsa_percentage = round(
        (dsa_score / 30) * 100
    )

    dbms_percentage = round(
        (dbms_score / 30) * 100
    )

    cn_percentage = round(
        (cn_score / 30) * 100
    )

    # =========================
    # TOTAL SCORE
    # =========================

    total_score = (
        python_score
        + sql_score
        + java_score
        + dsa_score
        + dbms_score
        + cn_score
    )

    total_questions = 180

    overall_percentage = round(
        (total_score / total_questions) * 100
    )

    if overall_percentage >= 80:
        readiness_status = "Good Progress"
    elif overall_percentage >= 60:
        readiness_status = "Needs More Practice"
    else:
        readiness_status = "Keep Practicing"

    # =========================
    # SUBJECT PERFORMANCE
    # =========================

    subject_scores = {
        "Python": python_percentage,
        "SQL": sql_percentage,
        "Java": java_percentage,
        "DSA": dsa_percentage,
        "DBMS": dbms_percentage,
        "Computer Networks": cn_percentage
    }

    # Highest score

    highest_subject = max(
        subject_scores,
        key=subject_scores.get
    )

    highest_percentage = subject_scores[
        highest_subject
    ]

    # Lowest non-zero score

    non_zero_subjects = {
        subject: percentage
        for subject, percentage
        in subject_scores.items()
        if percentage > 0
    }

    if non_zero_subjects:

        lowest_subject = min(
            non_zero_subjects,
            key=non_zero_subjects.get
        )

        lowest_percentage = non_zero_subjects[
            lowest_subject
        ]

    else:

        lowest_subject = "None"
        lowest_percentage = 0


    # =========================
    # DYNAMIC INSIGHTS
    # =========================

    strong_area_message = (
        f"{highest_subject} shows your highest "
        f"recorded technical score at "
        f"{highest_percentage}%."
    )

    improvement_message = (
        f"{lowest_subject} currently has your "
        f"lowest non-zero technical score at "
        f"{lowest_percentage}%."
    )


    return render_template(
        "analytics.html",

        questions_attempted=questions_attempted,

        interviews_completed=interviews_completed,

        python_score=python_score,
        sql_score=sql_score,
        java_score=java_score,
        dsa_score=dsa_score,
        dbms_score=dbms_score,
        cn_score=cn_score,

        python_percentage=python_percentage,
        sql_percentage=sql_percentage,
        java_percentage=java_percentage,
        dsa_percentage=dsa_percentage,
        dbms_percentage=dbms_percentage,
        cn_percentage=cn_percentage,

        total_score=total_score,

        overall_percentage=overall_percentage,
        readiness_status=readiness_status,

        highest_subject=highest_subject,
        highest_percentage=highest_percentage,

        lowest_subject=lowest_subject,
        lowest_percentage=lowest_percentage,

        strong_area_message=strong_area_message,
        improvement_message=improvement_message
    )


@app.route("/coding")
def coding():
    if "user_id" not in session:
        return redirect("/login")

    return render_template("coding.html")

@app.route("/coding/easy")
def coding_easy():
    if "user_id" not in session:
        return redirect("/login")

    return render_template("coding_easy.html")

@app.route("/coding/easy/1", methods=["GET", "POST"])
def coding_easy_1():
    if "user_id" not in session:
        return redirect("/login")

    result = None

    if request.method == "POST":
        code = request.form.get("code")

        if code:
            result = "Code submitted successfully!"

            questions_attempted = session.get(
                "questions_attempted",
                0
            )

            questions_attempted += 1

            session["questions_attempted"] = questions_attempted

            print(
                "QUESTIONS ATTEMPTED:",
                session["questions_attempted"]
            )


    return render_template(
        "coding_easy_1.html",
        result=result
    )

@app.route("/coding/easy/2", methods=["GET", "POST"])
def coding_easy_2():
    if "user_id" not in session:
        return redirect("/login")

    result = None

    if request.method == "POST":
        code = request.form.get("code")

        if code:
            result = "Code submitted successfully!"

            questions_attempted = session.get(
                "questions_attempted",
                0
            )

            questions_attempted += 1

            session["questions_attempted"] = questions_attempted

            print(
                "QUESTIONS ATTEMPTED:",
                session["questions_attempted"]
            )

    return render_template(
        "coding_easy_2.html",
        result=result
    )

@app.route("/coding/easy/3", methods=["GET", "POST"])
def coding_easy_3():
    if "user_id" not in session:
        return redirect("/login")

    result = None

    if request.method == "POST":
        code = request.form.get("code")

        if code:
            result = "Code submitted successfully!"

            questions_attempted = session.get(
                "questions_attempted",
                0
            )

            questions_attempted += 1

            session["questions_attempted"] = questions_attempted

            print(
                "QUESTIONS ATTEMPTED:",
                session["questions_attempted"]
            )

    return render_template(
        "coding_easy_3.html",
        result=result
    )

@app.route("/coding/medium")
def coding_medium():
    if "user_id" not in session:
        return redirect("/login")

    return render_template("coding_medium.html")

@app.route("/coding/medium/1", methods=["GET", "POST"])
def coding_medium_1():
    if "user_id" not in session:
        return redirect("/login")

    result = None

    if request.method == "POST":
        code = request.form.get("code")

        if code:
            result = "Code submitted successfully!"

            questions_attempted = session.get(
                "questions_attempted",
                0
            )

            questions_attempted += 1

            session["questions_attempted"] = questions_attempted

            print(
                "QUESTIONS ATTEMPTED:",
                session["questions_attempted"]
            )

    return render_template(
        "coding_medium_1.html",
        result=result
    )

@app.route("/coding/medium/2", methods=["GET", "POST"])
def coding_medium_2():
    if "user_id" not in session:
        return redirect("/login")

    result = None

    if request.method == "POST":
        code = request.form.get("code")

        if code:
            result = "Code submitted successfully!"

            questions_attempted = session.get(
                "questions_attempted",
                0
            )

            questions_attempted += 1

            session["questions_attempted"] = questions_attempted

            print(
                "QUESTIONS ATTEMPTED:",
                session["questions_attempted"]
            )

    return render_template(
        "coding_medium_2.html",
        result=result
    )


@app.route("/coding/medium/3", methods=["GET", "POST"])
def coding_medium_3():
    if "user_id" not in session:
        return redirect("/login")

    result = None

    if request.method == "POST":
        code = request.form.get("code")

        if code:
            result = "Code submitted successfully!"

            questions_attempted = session.get(
                "questions_attempted",
                0
            )

            questions_attempted += 1

            session["questions_attempted"] = questions_attempted

            print(
                "QUESTIONS ATTEMPTED:",
                session["questions_attempted"]
            )

    return render_template(
        "coding_medium_3.html",
        result=result
    )

@app.route("/coding/placement")
def coding_placement():
    if "user_id" not in session:
        return redirect("/login")

    return render_template("coding_placement.html")


@app.route("/coding/placement/1", methods=["GET", "POST"])
def coding_placement_1():
    if "user_id" not in session:
        return redirect("/login")

    result = None

    if request.method == "POST":
        code = request.form.get("code")

        if code:
            result = "Code submitted successfully!"

            questions_attempted = session.get(
                "questions_attempted",
                0
            )

            questions_attempted += 1

            session["questions_attempted"] = questions_attempted

            print(
                "QUESTIONS ATTEMPTED:",
                session["questions_attempted"]
            )

    return render_template(
        "coding_placement_1.html",
        result=result
    )

@app.route("/coding/placement/2", methods=["GET", "POST"])
def coding_placement_2():
    if "user_id" not in session:
        return redirect("/login")

    result = None

    if request.method == "POST":
        code = request.form.get("code")

        if code:
            result = "Code submitted successfully!"

            questions_attempted = session.get(
                "questions_attempted",
                0
            )

            questions_attempted += 1

            session["questions_attempted"] = questions_attempted

            print(
                "QUESTIONS ATTEMPTED:",
                session["questions_attempted"]
            )

    return render_template(
        "coding_placement_2.html",
        result=result
    )

@app.route("/coding/placement/3", methods=["GET", "POST"])
def coding_placement_3():
    if "user_id" not in session:
        return redirect("/login")

    result = None

    if request.method == "POST":
        code = request.form.get("code")

        if code:
            result = "Code submitted successfully!"

            questions_attempted = session.get(
                "questions_attempted",
                0
            )

            questions_attempted += 1

            session["questions_attempted"] = questions_attempted

            print(
                "QUESTIONS ATTEMPTED:",
                session["questions_attempted"]
            )

    return render_template(
        "coding_placement_3.html",
        result=result
    )


# ============================================================
# LOGOUT
# ============================================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")


# ============================================================
# TECHNICAL PRACTICE
# ============================================================

@app.route("/technical")
def technical():

    if "user_id" not in session:
        return redirect("/login")

    return render_template(
        "technical.html"
    )

@app.route("/aptitude")
def aptitude():

    if "user_id" not in session:
        return redirect("/login")

    return render_template("aptitude.html")

@app.route("/aptitude/quantitative")
def quantitative_aptitude():

    if "user_id" not in session:
        return redirect("/login")

    return render_template("quantitative.html")

@app.route("/aptitude/quantitative/percentages")
def percentages():
    if "user_id" not in session:
        return redirect("/login")

    return render_template("percentages.html")

@app.route("/aptitude/quantitative/profit-loss")
def profit_loss():
    if "user_id" not in session:
        return redirect("/login")

    return render_template("profit_loss.html")


@app.route("/aptitude/quantitative/ratio")
def ratio_aptitude():
    if "user_id" not in session:
        return redirect("/login")

    return render_template("ratio.html")

@app.route("/aptitude/quantitative/average")
def average_aptitude():
    if "user_id" not in session:
        return redirect("/login")

    return render_template("average.html")

@app.route("/aptitude/reasoning")
def reasoning_aptitude():
    if "user_id" not in session:
        return redirect("/login")

    return render_template("reasoning.html")

@app.route("/aptitude/reasoning/series")
def reasoning_series():
    if "user_id" not in session:
        return redirect("/login")

    return render_template("reasoning_series.html")

@app.route("/aptitude/reasoning/coding-decoding")
def coding_decoding():
    if "user_id" not in session:
        return redirect("/login")

    return render_template("coding_decoding.html")

@app.route("/aptitude/reasoning/blood-relations")
def blood_relations():
    if "user_id" not in session:
        return redirect("/login")

    return render_template("blood_relations.html")

@app.route("/aptitude/verbal")
def verbal_aptitude():
    if "user_id" not in session:
        return redirect("/login")

    return render_template("verbal.html")

@app.route("/aptitude/verbal/grammar")
def verbal_grammar():
    if "user_id" not in session:
        return redirect("/login")

    return render_template("grammar.html")

@app.route("/aptitude/verbal/vocabulary")
def verbal_vocabulary():
    if "user_id" not in session:
        return redirect("/login")

    return render_template("vocabulary.html")

@app.route("/aptitude/verbal/sentence-correction")
def sentence_correction():
    if "user_id" not in session:
        return redirect("/login")

    return render_template("sentence_correction.html")

@app.route("/track-question", methods=["POST"])
def track_question():

    if "user_id" not in session:
        return {"success": False}, 401

    questions_attempted = session.get(
        "questions_attempted",
        0
    )

    questions_attempted += 1

    session["questions_attempted"] = questions_attempted

    print(
        "QUESTIONS ATTEMPTED:",
        session["questions_attempted"]
    )

    return {"success": True}

# ============================================================
# PYTHON QUIZ
# ============================================================

@app.route(
    "/python",
    methods=["GET", "POST"]
)
def python():

    if "user_id" not in session:
        return redirect("/login")

    if request.method == "GET":

        session["python_question"] = 0
        session["python_score"] = 0

        question_order = list(
            range(len(python_questions))
        )

        random.shuffle(question_order)

        session["python_order"] = question_order

        question = python_questions[
            question_order[0]
        ]

        return render_template(
            "python.html",
            question=question,
            question_number=1,
            total_questions=len(python_questions),
            score=0,
            submitted=False,
            progress=3
        )

    # =========================
    # GET CURRENT QUESTION
    # =========================

    question_number = session.get(
        "python_question",
        0
    )

    score = session.get(
        "python_score",
        0
    )

    question_order = session.get(
        "python_order",
        list(range(len(python_questions)))
    )

    current_question = python_questions[
        question_order[question_number]
    ]

    # =========================
    # GET USER ANSWER
    # =========================

    selected_answer = request.form.get(
        "answer"
    )

    if not selected_answer:

        return render_template(
            "python.html",
            question=current_question,
            question_number=question_number + 1,
            total_questions=len(python_questions),
            score=score,
            submitted=False,
            progress=int(
                ((question_number + 1) /
                 len(python_questions)) * 100
            ),
            error="Please select an answer."
        )

    # =========================
    # TRACK QUESTION
    # =========================

    questions_attempted = session.get(
        "questions_attempted",
        0
    )

    questions_attempted += 1

    session["questions_attempted"] = (
        questions_attempted
    )

    print(
        "QUESTIONS ATTEMPTED:",
        session["questions_attempted"]
    )

    # =========================
    # CHECK ANSWER
    # =========================

    is_correct = (
        selected_answer ==
        current_question["answer"]
    )

    if is_correct:

        score += 1

        session["python_score"] = score

    return render_template(
        "python.html",
        question=current_question,
        question_number=question_number + 1,
        total_questions=len(python_questions),
        score=score,
        submitted=True,
        selected_answer=selected_answer,
        correct_answer=current_question["answer"],
        explanation=current_question["explanation"],
        is_correct=is_correct,
        progress=int(
            ((question_number + 1) /
             len(python_questions)) * 100
        )
    )


# ============================================================
# NEXT PYTHON QUESTION
# ============================================================

@app.route(
    "/python/next",
    strict_slashes=False
)
def python_next():

    if "user_id" not in session:
        return redirect("/login")

    question_number = session.get(
        "python_question",
        0
    )

    score = session.get(
        "python_score",
        0
    )

    question_number += 1

    session["python_question"] = question_number

    if question_number >= len(python_questions):

        return render_template(
            "python_result.html",
            score=score,
            total_questions=len(python_questions)
        )

    question_order = session.get(
        "python_order",
        list(range(len(python_questions)))
    )

    question = python_questions[
        question_order[question_number]
    ]

    return render_template(
        "python.html",
        question=question,
        question_number=question_number + 1,
        total_questions=len(python_questions),
        score=score,
        submitted=False,
        progress=int(
            ((question_number + 1) / len(python_questions)) * 100
        )
    )


# ============================================================
# SQL PRACTICE
# ============================================================

@app.route("/sql")
def sql():

    if "user_id" not in session:
        return redirect("/login")

    return render_template(
        "sql.html"
    )


# ============================================================
# SQL QUIZ
# ============================================================

@app.route(
    "/sql/quiz",
    methods=["GET", "POST"]
)
def sql_quiz():

    if "user_id" not in session:
        return redirect("/login")

    if "sql_order" not in session:

        session["sql_order"] = list(
            range(len(sql_questions))
        )

        random.shuffle(
            session["sql_order"]
        )

        session["sql_question"] = 0
        session["sql_score"] = 0

    question_number = session.get(
        "sql_question",
        0
    )

    if question_number >= len(sql_questions):

        return redirect(
            "/sql/result"
        )

    question_order = session.get(
        "sql_order",
        list(range(len(sql_questions)))
    )

    question_index = question_order[
        question_number
    ]

    question = sql_questions[
        question_index
    ]

    feedback = None
    selected_answer = None

    if request.method == "POST":
        selected_answer = request.form.get(
            "answer"
        )

        questions_attempted = session.get(
            "questions_attempted",
            0
        )

        questions_attempted += 1

        session["questions_attempted"] = questions_attempted

        print(
            "QUESTIONS ATTEMPTED:",
            session["questions_attempted"]
        )

        if selected_answer == question["answer"]:
            session["sql_score"] = session.get(
                "sql_score",
                0
            ) + 1
            feedback = "correct"
        else:
            feedback = "wrong"

    return render_template(
        "sql_quiz.html",
        question=question,
        question_number=question_number + 1,
        total_questions=len(sql_questions),
        score=session.get(
            "sql_score",
            0
        ),
        feedback=feedback,
        selected_answer=selected_answer
    )


# ============================================================
# NEXT SQL QUESTION
# ============================================================

@app.route("/sql/next")
def sql_next():

    if "user_id" not in session:
        return redirect("/login")

    question_number = session.get(
        "sql_question",
        0
    )

    question_number += 1

    session["sql_question"] = question_number

    if question_number >= len(sql_questions):

        return redirect(
            "/sql/result"
        )

    return redirect(
        "/sql/quiz"
    )


# ============================================================
# SQL RESULT
# ============================================================

@app.route("/sql/result")
def sql_result():

    if "user_id" not in session:
        return redirect("/login")

    score = session.get(
        "sql_score",
        0
    )

    total = len(sql_questions)

    return render_template(
        "sql_result.html",
        score=score,
        total=total
    )


# ============================================================
# SQL RESTART
# ============================================================

@app.route("/sql/restart")
def sql_restart():

    if "user_id" not in session:
        return redirect("/login")

    session.pop(
        "sql_order",
        None
    )

    session.pop(
        "sql_question",
        None
    )

    session.pop(
        "sql_score",
        None
    )

    return redirect(
        "/sql/quiz"
    )


# ============================================================
# JAVA PRACTICE
# ============================================================

@app.route("/java")
def java():

    if "user_id" not in session:
        return redirect("/login")

    return render_template(
        "java.html"
    )


# ============================================================
# JAVA QUIZ
# ============================================================

@app.route(
    "/java/quiz",
    methods=["GET", "POST"]
)
def java_quiz():

    if "user_id" not in session:
        return redirect("/login")

    if "java_order" not in session:

        session["java_order"] = list(
            range(len(java_questions))
        )

        random.shuffle(
            session["java_order"]
        )

        session["java_question"] = 0
        session["java_score"] = 0

    question_number = session.get(
        "java_question",
        0
    )

    if question_number >= len(java_questions):

        return redirect(
            "/java/result"
        )

    question_order = session.get(
        "java_order",
        list(range(len(java_questions)))
    )

    question_index = question_order[
        question_number
    ]

    question = java_questions[
        question_index
    ]

    feedback = None
    selected_answer = None

    if request.method == "POST":

        selected_answer = request.form.get(
            "answer"
        )

        questions_attempted = session.get(
            "questions_attempted",
            0
        )

        questions_attempted += 1

        session["questions_attempted"] = questions_attempted

        print(
            "QUESTIONS ATTEMPTED:",
            session["questions_attempted"]
        )

        

        if selected_answer == question["answer"]:

            session["java_score"] = session.get(
                "java_score",
                0
            ) + 1

            feedback = "correct"

        else:

            feedback = "wrong"

    return render_template(
        "java_quiz.html",
        question=question,
        question_number=question_number + 1,
        total_questions=len(java_questions),
        score=session.get(
            "java_score",
            0
        ),
        feedback=feedback,
        selected_answer=selected_answer
    )


# ============================================================
# NEXT JAVA QUESTION
# ============================================================

@app.route("/java/next")
def java_next():

    if "user_id" not in session:
        return redirect("/login")

    question_number = session.get(
        "java_question",
        0
    )

    question_number += 1

    session["java_question"] = question_number

    if question_number >= len(java_questions):

        return redirect(
            "/java/result"
        )

    return redirect(
        "/java/quiz"
    )


# ============================================================
# JAVA RESULT
# ============================================================

@app.route("/java/result")
def java_result():
    if "user_id" not in session:
        return redirect("/login")

    score = session.get("java_score", 0)
    total = len(java_questions)

    percentage = round((score / total) * 100)

    return render_template(
        "java_result.html",
        score=score,
        total=total,
        percentage=percentage
    )


# ============================================================
# JAVA RESTART
# ============================================================

@app.route("/java/restart")
def java_restart():

    if "user_id" not in session:
        return redirect("/login")

    session.pop(
        "java_order",
        None
    )

    session.pop(
        "java_question",
        None
    )

    session.pop(
        "java_score",
        None
    )

    return redirect(
        "/java/quiz"
    )


@app.route("/dsa")
def dsa():
    if "user_id" not in session:
        return redirect("/login")

    return render_template("dsa.html")


@app.route("/dsa/quiz", methods=["GET", "POST"])
def dsa_quiz():
    if "user_id" not in session:
        return redirect("/login")

    if "dsa_order" not in session:
        session["dsa_order"] = list(range(len(dsa_questions)))
        random.shuffle(session["dsa_order"])

        session["dsa_question"] = 0
        session["dsa_score"] = 0

    question_number = session.get("dsa_question", 0)

    if question_number >= len(dsa_questions):
        return redirect("/dsa/result")

    question_order = session.get(
        "dsa_order",
        list(range(len(dsa_questions)))
    )

    question_index = question_order[question_number]
    question = dsa_questions[question_index]

    feedback = None
    selected_answer = None

    if request.method == "POST":
        selected_answer = request.form.get("answer")

        questions_attempted = session.get(
            "questions_attempted",
            0
        )

        questions_attempted += 1

        session["questions_attempted"] = questions_attempted

        print(
            "QUESTIONS ATTEMPTED:",
            session["questions_attempted"]
        )

        if selected_answer == question["answer"]:
            session["dsa_score"] = session.get("dsa_score", 0) + 1
            feedback = "correct"
        else:
            feedback = "wrong"

    return render_template(
        "dsa_quiz.html",
        question=question,
        question_number=question_number + 1,
        total_questions=len(dsa_questions),
        score=session.get("dsa_score", 0),
        feedback=feedback,
        selected_answer=selected_answer
    )

@app.route("/dsa/next")
def dsa_next():
    if "user_id" not in session:
        return redirect("/login")

    question_number = session.get("dsa_question", 0)
    question_number += 1
    session["dsa_question"] = question_number

    if question_number >= len(dsa_questions):
        return redirect("/dsa/result")

    return redirect("/dsa/quiz")

@app.route("/dsa/result")
def dsa_result():
    if "user_id" not in session:
        return redirect("/login")

    score = session.get("dsa_score", 0)
    total = len(dsa_questions)

    percentage = round((score / total) * 100)

    return render_template(
        "dsa_result.html",
        score=score,
        total=total,
        percentage=percentage
    )

@app.route("/dsa/restart")
def dsa_restart():
    if "user_id" not in session:
        return redirect("/login")

    session.pop("dsa_order", None)
    session.pop("dsa_question", None)
    session.pop("dsa_score", None)

    session.modified = True

    return redirect("/dsa/quiz")

@app.route("/dbms")
def dbms():
    if "user_id" not in session:
        return redirect("/login")

    return render_template("dbms.html")

@app.route("/dbms/quiz", methods=["GET", "POST"])
def dbms_quiz():
    if "user_id" not in session:
        return redirect("/login")

    if "dbms_order" not in session:
        session["dbms_order"] = list(range(len(dbms_questions)))
        random.shuffle(session["dbms_order"])
        session["dbms_question"] = 0
        session["dbms_score"] = 0

    question_number = session.get("dbms_question", 0)

    if question_number >= len(dbms_questions):
        return redirect("/dbms/result")

    question_order = session.get(
        "dbms_order",
        list(range(len(dbms_questions)))
    )

    question_index = question_order[question_number]
    question = dbms_questions[question_index]

    feedback = None
    selected_answer = None

    if request.method == "POST":
        selected_answer = request.form.get("answer")

        questions_attempted = session.get(
            "questions_attempted",
            0
        )

        questions_attempted += 1

        session["questions_attempted"] = questions_attempted

        print(
            "QUESTIONS ATTEMPTED:",
            session["questions_attempted"]
        )

        if selected_answer == question["answer"]:
            session["dbms_score"] = session.get("dbms_score", 0) + 1
            feedback = "correct"
        else:
            feedback = "wrong"

    return render_template(
        "dbms_quiz.html",
        question=question,
        question_number=question_number + 1,
        total_questions=len(dbms_questions),
        score=session.get("dbms_score", 0),
        feedback=feedback,
        selected_answer=selected_answer
    )

@app.route("/dbms/next")
def dbms_next():
    if "user_id" not in session:
        return redirect("/login")

    question_number = session.get("dbms_question", 0)
    question_number += 1
    session["dbms_question"] = question_number

    if question_number >= len(dbms_questions):
        return redirect("/dbms/result")

    return redirect("/dbms/quiz")

@app.route("/dbms/result")
def dbms_result():
    if "user_id" not in session:
        return redirect("/login")

    score = session.get("dbms_score", 0)
    total = len(dbms_questions)

    percentage = round((score / total) * 100)

    return render_template(
        "dbms_result.html",
        score=score,
        total=total,
        percentage=percentage
    )

@app.route("/dbms/restart")
def dbms_restart():
    if "user_id" not in session:
        return redirect("/login")

    session.pop("dbms_order", None)
    session.pop("dbms_question", None)
    session.pop("dbms_score", None)

    return redirect("/dbms/quiz")

@app.route("/cn")
def cn():
    if "user_id" not in session:
        return redirect("/login")

    return render_template("cn.html")

@app.route("/cn/quiz", methods=["GET", "POST"])
def cn_quiz():
    if "user_id" not in session:
        return redirect("/login")

    if "cn_order" not in session:
        session["cn_order"] = list(range(len(cn_questions)))
        random.shuffle(session["cn_order"])
        session["cn_question"] = 0
        session["cn_score"] = 0

    question_number = session.get("cn_question", 0)

    if question_number >= len(cn_questions):
        return redirect("/cn/result")

    question_order = session.get(
        "cn_order",
        list(range(len(cn_questions)))
    )

    question_index = question_order[question_number]
    question = cn_questions[question_index]

    feedback = None
    selected_answer = None

    if request.method == "POST":
        selected_answer = request.form.get("answer")

        questions_attempted = session.get(
            "questions_attempted",
            0
        )

        questions_attempted += 1

        session["questions_attempted"] = questions_attempted

        print(
            "QUESTIONS ATTEMPTED:",
            session["questions_attempted"]
        )

        if selected_answer == question["answer"]:
            session["cn_score"] = session.get("cn_score", 0) + 1
            feedback = "correct"
        else:
            feedback = "wrong"

    return render_template(
        "cn_quiz.html",
        question=question,
        
        question_number=question_number + 1,
        total_questions=len(cn_questions),
        score=session.get("cn_score", 0),
        feedback=feedback,
        selected_answer=selected_answer
    )

@app.route("/cn/next")
def cn_next():
    if "user_id" not in session:
        return redirect("/login")

    question_number = session.get("cn_question", 0)
    question_number += 1
    session["cn_question"] = question_number

    if question_number >= len(cn_questions):
        return redirect("/cn/result")

    return redirect("/cn/quiz")

@app.route("/cn/result")
def cn_result():
    if "user_id" not in session:
        return redirect("/login")

    score = session.get("cn_score", 0)
    total = len(cn_questions)

    percentage = round((score / total) * 100)

    return render_template(
        "cn_result.html",
        score=score,
        total=total,
        percentage=percentage
    )

@app.route("/cn/restart")
def cn_restart():
    if "user_id" not in session:
        return redirect("/login")

    session.pop("cn_order", None)
    session.pop("cn_question", None)
    session.pop("cn_score", None)

    return redirect("/cn/quiz")

@app.route("/mock-interview")
def mock_interview():
    if "user_id" not in session:
        return redirect("/login")

    return render_template("mock_interview.html")

@app.route("/mock-interview/technical")
def technical_interview():
    if "user_id" not in session:
        return redirect("/login")

    return render_template("technical_interview.html")

technical_interview_questions = [
    {
        "question": "What are the four main pillars of OOP?",
        "answer": "The four main pillars are Encapsulation, Inheritance, Polymorphism and Abstraction."
    },
    {
        "question": "What is the difference between an array and a linked list?",
        "answer": "An array stores elements in contiguous memory and provides fast index access, while a linked list stores nodes connected through pointers and allows easier insertion and deletion."
    },
    {
        "question": "What is a primary key in DBMS?",
        "answer": "A primary key uniquely identifies each record in a table and cannot contain NULL values."
    },
    {
        "question": "What is the difference between DELETE, TRUNCATE and DROP?",
        "answer": "DELETE removes selected rows, TRUNCATE removes all rows while keeping the table structure, and DROP removes the table itself."
    },
    {
        "question": "What is the difference between TCP and UDP?",
        "answer": "TCP is connection-oriented and provides reliable ordered delivery, while UDP is connectionless and faster but does not guarantee delivery."
    },
    {
        "question": "What is a Python list?",
        "answer": "A Python list is an ordered, mutable collection that can store multiple values and allows duplicate elements."
    },
    {
        "question": "What is inheritance in Java?",
        "answer": "Inheritance allows one class to acquire the properties and methods of another class using the extends keyword."
    },
    {
        "question": "What is binary search?",
        "answer": "Binary search is an efficient searching algorithm that works on sorted data by repeatedly dividing the search space into two halves."
    },
    {
        "question": "What is normalization in DBMS?",
        "answer": "Normalization is the process of organizing database tables to reduce data redundancy and improve data integrity."
    },
    {
        "question": "What is the difference between HTTP and HTTPS?",
        "answer": "HTTP transfers data without encryption, while HTTPS uses TLS encryption to secure communication."
    }
]

@app.route("/mock-interview/technical/start")
def technical_interview_start():
    if "user_id" not in session:
        return redirect("/login")

    session["technical_interview_question"] = 0
    session["technical_interview_score"] = 0
    session["technical_session_counted"] = False

    return redirect("/mock-interview/technical/question")

@app.route("/mock-interview/technical/question", methods=["GET", "POST"])
def technical_interview_question():
    if "user_id" not in session:
        return redirect("/login")

    question_number = session.get(
        "technical_interview_question", 0
    )

    if question_number >= len(technical_interview_questions):
        return redirect("/mock-interview/technical/result")

    question = technical_interview_questions[question_number]

    feedback = None
    user_answer = None

    if request.method == "POST":
        user_answer = request.form.get("answer")

        if user_answer:
            expected_answer = question["answer"].lower()
            user_answer_lower = user_answer.lower()

            keywords = expected_answer.split()

            matched_keywords = 0

            for keyword in keywords:
                if keyword in user_answer_lower:
                    matched_keywords += 1

            if matched_keywords >= len(keywords) * 0.4:
                session["technical_interview_score"] = (
                    session.get("technical_interview_score", 0) + 1
                )

            feedback = "Your answer has been recorded."

    return render_template(
        "technical_interview_question.html",
        question=question,
        question_number=question_number + 1,
        total_questions=len(technical_interview_questions),
        feedback=feedback,
        user_answer=user_answer
    )

@app.route("/mock-interview/technical/next")
def technical_interview_next():
    if "user_id" not in session:
        return redirect("/login")

    question_number = session.get(
        "technical_interview_question", 0
    )

    question_number += 1

    session["technical_interview_question"] = question_number

    if question_number >= len(technical_interview_questions):
        return redirect("/mock-interview/technical/result")

    return redirect("/mock-interview/technical/question")

@app.route("/mock-interview/technical/result")
def technical_interview_result():
    if "user_id" not in session:
        return redirect("/login")

    score = session.get("technical_interview_score", 0)

    if not session.get("technical_session_counted"):
        session["interview_sessions"] = session.get(
            "interview_sessions", 0
        ) + 1

        session["technical_session_counted"] = True

    total = len(technical_interview_questions)
    percentage = round((score / total) * 100)

    return render_template(
        "technical_interview_result.html",
        score=score,
        total=total,
        percentage=percentage
    )

hr_interview_questions = [
    {
        "question": "Tell me about yourself.",
        "answer": "A concise introduction covering education, skills, projects, strengths and career goals."
    },
    {
        "question": "Why should we hire you?",
        "answer": "I have relevant technical skills, project experience, willingness to learn and the ability to adapt."
    },
    {
        "question": "What are your strengths?",
        "answer": "Good learning ability, problem-solving, teamwork, adaptability and consistency."
    },
    {
        "question": "What is your biggest weakness?",
        "answer": "A genuine weakness along with the steps being taken to improve it."
    },
    {
        "question": "Why do you want to join our company?",
        "answer": "Interest in the company's work, learning opportunities, growth and the ability to contribute."
    },
    {
        "question": "Where do you see yourself in five years?",
        "answer": "Growing into a skilled professional, taking more responsibility and contributing to meaningful projects."
    },
    {
        "question": "Describe a challenging situation you faced.",
        "answer": "Explain the situation, the action taken to solve it and the result."
    },
    {
        "question": "How do you handle pressure?",
        "answer": "By prioritizing tasks, staying organized, remaining calm and focusing on solutions."
    },
    {
        "question": "Are you comfortable working in a team?",
        "answer": "Yes, with effective communication, collaboration and willingness to support team members."
    },
    {
        "question": "Why should we select you as a fresher?",
        "answer": "I have a strong learning attitude, relevant technical knowledge, project experience and willingness to grow."
    }
]


@app.route("/mock-interview/hr/start")
def hr_interview_start():
    if "user_id" not in session:
        return redirect("/login")

    session["hr_interview_question"] = 0
    session["hr_interview_score"] = 0

    return redirect("/mock-interview/hr/question")

@app.route("/mock-interview/hr/question", methods=["GET", "POST"])
def hr_interview_question():
    if "user_id" not in session:
        return redirect("/login")

    question_number = session.get(
        "hr_interview_question", 0
    )

    if question_number >= len(hr_interview_questions):
        return redirect("/mock-interview/hr/result")

    question = hr_interview_questions[question_number]

    feedback = None
    user_answer = None

    if request.method == "POST":
        user_answer = request.form.get("answer")

        if user_answer:
            user_answer_lower = user_answer.lower()

            hr_keywords = {
                0: ["education", "skills", "project", "career", "btech"],
                1: ["skills", "experience", "learn", "adapt", "contribute"],
                2: ["learning", "problem", "teamwork", "adaptability", "consistent"],
                3: ["improve", "learning", "practice", "weakness"],
                4: ["company", "learning", "growth", "opportunity", "contribute"],
                5: ["career", "professional", "responsibility", "skills", "growth"],
                6: ["challenge", "situation", "action", "solve", "result"],
                7: ["pressure", "priority", "organized", "calm", "solution"],
                8: ["team", "communication", "collaboration", "support"],
                9: ["fresher", "learning", "technical", "project", "grow"]
            }

            current_keywords = hr_keywords.get(
                question_number, []
            )

            matched_keywords = 0

            for keyword in current_keywords:
                if keyword in user_answer_lower:
                    matched_keywords += 1

            if matched_keywords >= 2:
                session["hr_interview_score"] = (
                    session.get("hr_interview_score", 0) + 1
                )

            feedback = "Your answer has been recorded."

    return render_template(
        "hr_interview_question.html",
        question=question,
        question_number=question_number + 1,
        total_questions=len(hr_interview_questions),
        feedback=feedback,
        user_answer=user_answer
    )

@app.route("/mock-interview/hr/next")
def hr_interview_next():
    if "user_id" not in session:
        return redirect("/login")

    question_number = session.get(
        "hr_interview_question", 0
    )

    question_number += 1

    session["hr_interview_question"] = question_number

    if question_number >= len(hr_interview_questions):
        return redirect("/mock-interview/hr/result")

    return redirect("/mock-interview/hr/question")

@app.route("/mock-interview/hr/result")
def hr_interview_result():
    if "user_id" not in session:
        return redirect("/login")

    score = session.get("hr_interview_score", 0)
    total = len(hr_interview_questions)

    percentage = round((score / total) * 100)

    return render_template(
        "hr_interview_result.html",
        score=score,
        total=total,
        percentage=percentage
    )




# ============================================================
# RUN APPLICATION
# ============================================================

if __name__ == "__main__":

    app.run(
        debug=True
    )