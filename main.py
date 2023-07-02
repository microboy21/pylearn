from kivy.base import stopTouchApp
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.screenmanager import SlideTransition
from kivy.uix.relativelayout import RelativeLayout
from kivy.core.text import LabelBase
from kivy.uix.image import Image
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout

image_path = './pythonbg2.jpg'
font1_path = './font1.ttf'
font2_path = './font2.ttf'

LabelBase.register("font2", fn_regular='./font2.ttf')
LabelBase.register("font1", fn_regular='./font1.ttf')


class LessonScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        self.text_input = TextInput(text='', font_size=20, readonly=True, multiline=True)

        back_button = Button(text='Back', on_press=self.go_to_main_screen, size_hint=(None, None), size=(100, 50))

        layout.add_widget(self.text_input)
        layout.add_widget(back_button)

        # Create a ScrollView and add the layout to it
        scroll_view = ScrollView()
        scroll_view.add_widget(layout)

        self.add_widget(scroll_view)


    def go_to_main_screen(self, instance):
        self.manager.current = 'main'

    def show_topics(self, instance):
        topics_layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        topics_label = Label(text='Select a Topic:', font_size=30)
        topics_layout.add_widget(topics_label)

        scroll_view = ScrollView()

        # Create a grid layout for the buttons
        grid = GridLayout(cols=1, spacing=10, size_hint_y=None)

        # Calculate the height of the grid based on the number of topics
        grid.bind(minimum_height=grid.setter('height'))

        # Add buttons for the topics
        topics = self.get_selected_lesson_topics()
        for topic in topics:
            topic_button = Button(text=topic['title'], size_hint_y=None, height=40)
            grid.add_widget(topic_button)

            scroll_view = ScrollView()
            scroll_view.add_widget(grid)

            scroll_view.add_widget(grid)
            topics_layout.add_widget(scroll_view)

        # Add back button
        back_button = Button(text='Back', on_press=self.go_to_lesson_screen, size_hint=(None, None), size=(100, 50))
        topics_layout.add_widget(back_button)

        self.clear_widgets()  # Clear the existing widgets
        self.add_widget(topics_layout)

    def go_to_topic_screen(self, instance, topic):
        topic_title = topic['title']
        topic_content = topic['content']
        topic_screen = self.manager.get_screen('topics')
        topic_screen.label.text = topic_title
        topic_screen.text_input.text = topic_content

        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = 'topics'


class MainScreen(Screen):
    def __init__(self, lessons, **kwargs):
        super().__init__(**kwargs)
        self.lessons = lessons

        layout = RelativeLayout()

        background_image = Image(source=image_path,
                                 allow_stretch=True, keep_ratio=False)
        layout.add_widget(background_image)

        label = Label(text='PyLearn', font_name='font2', font_size=80,
                      color=(1, 1, 1, 1))  # Set the label text color to white
        layout.add_widget(label)

        lessons_button = Button(text='Lessons', font_name='font2', on_press=self.show_lessons,
                                size_hint=(None, None), size=(150, 50),
                                pos_hint={'center_x': 0.5, 'center_y': 0.4}, background_color=(
            0.3, 0.3, 0.3, 1))  # Set the button's background color to a darker shade (e.g., dark gray)
        exit_button = Button(text='Exit', on_press=self.exit_app, size_hint=(None, None), size=(100, 50),
                             pos_hint={'right': 0.95, 'top': 0.95}, background_color=(
            0.3, 0.3, 0.3, 1))  # Set the button's background color to a darker shade (e.g., dark gray)

        layout.add_widget(lessons_button)
        layout.add_widget(exit_button)

        self.add_widget(layout)

    def show_lessons(self, instance):
        lessons_layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        lessons_label = Label(text='Select a Lesson:', font_name='font2', font_size=30)
        lessons_layout.add_widget(lessons_label)

        for i, lesson in enumerate(self.lessons):
            lesson_button = Button(text=lesson['title'], size_hint=(0.8, None), size=(200, 50),
                                   pos_hint={'center_x': 0.5, 'y': 0.6}, background_color=(0.3, 0.3, 0.3, 1))
            lesson_button.bind(
                on_press=lambda instance, lesson_index=i: self.go_to_lesson_screen(instance, lesson_index))
            lessons_layout.add_widget(lesson_button)

        back_button = Button(text='Back', on_press=self.go_to_main_screen, size_hint=(None, None), size=(100, 50))
        lessons_layout.add_widget(back_button)

        self.manager.get_screen('lessons').clear_widgets()
        self.manager.get_screen('lessons').add_widget(lessons_layout)
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = 'lessons'

    def go_to_lesson_screen(self, instance, lesson_index):
        lesson_screen = self.manager.get_screen('lessons')
        lesson_screen.lesson_index = lesson_index

        topics_layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        topics_label = Label(text='Select a Topic:', font_name='font2', font_size=30, )
        topics_layout.add_widget(topics_label)

        selected_lesson = self.lessons[lesson_index]
        topics = selected_lesson['topics']

        for topic in topics:
            topic_button = Button(text=topic['title'], size_hint=(0.8, None), size=(200, 50),
                                  pos_hint={'center_x': 0.5, 'y': 0.7}, background_color=(0.3, 0.3, 0.3, 1))
            topic_button.bind(on_press=lambda instance, topic=topic: self.go_to_topic_screen(instance, topic))
            topics_layout.add_widget(topic_button)

        back_button = Button(text='Back', on_press=self.go_to_main_screen, size_hint=(None, None), size=(100, 50))
        topics_layout.add_widget(back_button)

        lesson_screen.clear_widgets()
        lesson_screen.add_widget(topics_layout)

        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = 'lessons'

    def go_to_topic_screen(self, instance, topic):
        topic_title = topic['title']
        topic_content = topic['content']
        topic_screen = self.manager.get_screen('topics')
        topic_screen.label.text = topic_title
        topic_screen.text_input.text = topic_content

        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = 'topics'

    def go_to_main_screen(self, instance):
        self.manager.current = 'main'

    def exit_app(self, instance):
        stopTouchApp()


class CustomTextInput(TextInput):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.foreground_color = (1, 1, 1, 1)  # Set text color to red (RGBA format)


class TopicScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        self.label = Label(text='', font_name='font2', font_size=30, size_hint=(0.4, 0.4))
        self.text_input = CustomTextInput(text='', font_name='font1', background_color=(0.1, 0.1, 0.1, 1),
                                          font_size=20, readonly=True, multiline=True)
        back_button = Button(text='Back', on_press=self.go_to_lesson_screen, size_hint=(None, None), size=(100, 50))
        background_image = Image(source=image_path,
                                 allow_stretch=True, keep_ratio=False)

        self.add_widget(background_image)
        layout.add_widget(self.label)
        layout.add_widget(self.text_input)
        layout.add_widget(back_button)
        self.add_widget(layout)

    def go_to_lesson_screen(self, instance):
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'lessons'


class PyLearnApp(App):
    def build(self):
        lessons = [
            {
                'title': 'Introduction to Programming and Logic Design',
                'content': 'Lesson content for Basic of Python Programming',
                'topics': [
                    {'title': 'Computational Thinking', 'content': """Computational Thinking
        - Computational Thinking is the thought processes involved in understanding a problem and expressing its solution in 
        a way that a computer can effectively carry out.

         Conceptualizing, not programming. Fundamental, not rote skill.
         A way that humans, not computers, think.
         Complements and combines mathematical and engineering thinking.
         Ideas, not artifacts. For everyone, everywhere.
        """},
                    {'title': 'Algorithms', 'content': """An algorithm specifies a series of steps that perform a particular computation or task

Properties of an algorithm *
1.	An algorithm is an unambiguous description that makes clear what has to be implemented in order to solve the problem.
2.	An algorithm expects a defined set of inputs.
3.	An algorithm produces a defined set of outputs.
4.	An algorithm is guaranteed to terminate and produce a result, always stopping after a finite time.
5.	Must be general for any input it is given.
6.	It is at the right level of detail.

Verifying Your Algorithm *
How do we know if an algorithm is unambiguous, correct, comes to an end, in general, and is at the right level of detail? We must test the algorithm. 
Testing means verifying that the algorithm does what we expect it to do. 
A test case is a set of inputs, conditions, and expected results developed for a particular computational problem to be solved.

Good (Effective) Test Cases: *
•	are easy to understand and execute 
•	are created with the user in mind (what input mistakes will be made? what are the preconditions?) 
•	make no assumptions (you already know what it is supposed to do) 
•	consider the boundaries for a specified range of values.

Process of Computational Problem Solving *
	Analyze the Problem
•	clearly understand the computational problem
•	what is the output? what is the input?
•	can we break the problem into parts?

	Design the solution
•	determine the connections between the input and the output
•	design the algorithm
	Implement the Solution
•	implement the algorithm in a programming language

	Test
•	determine test cases
•	thoroughly test the program
•	correct errors
"""},
                    {'title': 'Values and Variables', 'content': """-	A value is one of the basic things computer programs work with, like a password or a number of errors.
-	Variables are exactly what the name implies – their value can vary, i.e., you can store anything using a variable.
"""},
                    {'title': 'What is a Program?', 'content': """--	A program is a sequence of instructions that specifies how to perform a computation
Basic Elements of Programming Constructs
•	input 
•	output 
•	Sequential execution 
•	conditional execution 
•	repeated execution 
•	Reuse

"""},
                    {'title': 'Computational Problem Design Using Basic Programming', 'content': """	The key to better algorithm design and thus to programming lies in limiting the control structure to only three constructs
The Basic Programming Constructs
1.	The Sequence structure (sequential execution) 
2.	The Decision, Selection, or Control structure (conditional execution) 
3.	Repetition or Iteration Structure (repeated execution)


        """},

                ]
            },
            {
                'title': 'Basic of Python Programming',
                'content': 'Lesson content for Basic of Python Programming',
                'topics': [
                    {'title': 'Data Types and Variables', 'content': """Data Types and Variables in Python
	Data Types
-	Data Type is nothing but a categorization of data of different types. A data type defines set of values along with 
operations that can be performed on those values.

	Variables
-	Variables are used to store data in our programs. We also use variables to access data as well as manipulate data.
 A variable is called so because it’s value can be changed.

Creating Variables *
To create a variable in Python we use the assignment statement which has the following format.
variable_name = expression

Variable Names *
We have the following rules in Python to create a valid variable name:
1.	Only letters ( a-z, A-Z ), underscore ( _ ), and numbers ( 0-9 ) are allowed to create variable names, nothing else. 
2.	Variable names must begin with an underscore ( _ ) or a letter. You can’t use reserved keywords to create variable names. 
3.	A variable name can be of any length.

Python Keywords
Python Keywords are words that denote something specific in a Python language. That’s why we’re not allowed to use them 
as variable names. 

Here is the list of Python keywords:
    False	   await	    else	     import	        pass
    None	   break	    except	     in	            raise
    True	   class	    finally	     is	            return
    and	       continue	    for	         lambda	        try
    as	       def	        from	     nonlocal	    while
    assert	   del	        global	     not	        with
    async	   elif	        if	         or	            yield

Comments *
Comments are used to add notes to a program. In a large program, comments may describe the purpose of the program and how it works.
Named Constants
Constants are variables whose values do not change during the lifetime of the program.
Getting Input
•	The basic structure is: variable name = input(message to user) 
•	The input function is a simple way for your program to get information from people using your program. Here is an example: 
•	name = input('Enter your name: ') print('Hello, ' , name)

Printing *
Here is a simple example: print('Hi there') The print function requires parenthesis around its arguments. In the program above, its only argument is the string 'Hi there'. Anything inside quotes will (with a few exceptions) be printed exactly as it appears. In the following, the first statement will output 3+4, while the second will output 7. 
print('3+4') 
print(3+4)

Printing (Optional Arguments)
There are two optional arguments to the print function.
sep Python will insert a space between each of the arguments of the print function. There is an optional argument called 
sep, short for separator, that you can use to change that space to something else. For example, using sep=':' 
would separate the arguments by a colon and sep='##' would separate the arguments by two pound signs
One particularly useful possibility is to have nothing inside the quotes, as in sep=''. This says to put no separation 
between the arguments. 

Here is an example where sep is useful for getting the output to look nice:

print ('The value of 3+4 is', 3+4, '.')
print ('The value of 3+4 is ', 3+4, '.', sep='') 
Output:
The value of 3+4 is 7 .
The value of 3+4 is 7. 

end - The print function will automatically advance to the next line. For instance, the following will print on two lines:

print('On the first line')
print('On the second line')
On the first line
On the second line 

There is an optional argument called end that you can use to keep the print function from advancing to the next line. Here is an example:

print('On the first line', end='')
print('On the second line')
Output:
On the first lineOn the second line 

"""},
                    {'title': 'Numbers in Python', 'content': """In Python, numbers are of 4 types:
1.	Integer. 
2.	Floating Point or Real Numbers. 
3.	Complex Numbers. 
4.	Boolean.

Common Mathematical Functions
Python provides following builtin function to help you accomplish common programming tasks:

* abs(number) - Returns the absolute value of the number. In other words, 
              the abs() function just returns the number without any sign.
Example:
abs(-12) is 12
abs(112.21) is 112.21

* pow(a, b) - Returns a^b.
Example:
pow(2, 3) is 8
pow(10, 3) is 1000

* round (number) - Rounds the number to the nearest integer.
Example:
round (17.3) is 17
Output: round (8.6) is 9

* round (number, ndigits) - Rounds the number to ndigits after decimal point
Example:
(3.14159, 2) is 3.14
 round (2.71828, 2) is 2.72

* min(arg1, arg2, argN)- Returns the smallest item among arg1, arg2, ... argN
Example:
min(12, 2, 44,199) is 2
Output: min(4, -21, -99) is -99

*max(arg1, arg2, argN) - Returns the largest item among arg1, arg2, ... argN
Example:
max(991, 22, 19) is 991 
Output: max(- 2, -1, -5) is -1

Math Module
Python’s math module also provides some standard mathematical functions and constants. Recall that, to use the math 
module we first need to import it using import statement as follows:

* math.pi - Returns the value of pi.
Example:
math.pi is 3.141592653589793

* math.e - Returns the value of e
Example:
math.e is 2.718281828459045

* math.ceil(n) - Returns smallest integer greater than or equal to n
Example:
math.ceil(3.621) is 4

* math.floor(n) - Returns largest integer smaller than or equal to n
Example:
math.floor(3.621) is 3

* math.fabs(n) - Returns absolute value of x as float
Example:
math.fabs(5) is 5.0

* math.sqrt(n) - Returns the square root of x as float
Example:
math.sqrt(225) is 15.0

* math.log(n) - Returns the natural log of n to the base e
Example:
math.log(2) is 0.6931

* math.log(n, base) - Returns the natural log of n to the given base
Example:0
math.log(2, 2) is 1.0

* math.sin(n) - Returns the sine of n radians
Example:
math.sin(math.pi/2) is 1.0

Formatting Numbers
	format() Function
Sometimes it is desirable to print the number in a particular format. The syntax of the format() function is as follows:
                             format(value, format-specifier)

	Formatting Floating Point Numbers
To format floating point numbers we use the following format specifier. 
width.precisionf 
Example: 
print(format(34.712, "9.2f")) Output: 34.71

	Formatting Numbers in Scientific Notation
To format a number in Scientific Notation just replace type code from f to e or E.
print(format(5482.52291, "10.2E")) 
Output: 5.48E+03

	Formatting Number as Percentages
We can use % type code to format a number as a percentage. When % is used in the format specifier, it multiplies the
 number by 100 and outputs the result as a float followed by a % sign. We can also specify width and precision as usual.
print(format(95, ".2%")) 
Output: 9500.00%

	Formatting Number System
We can also use format() function to format integers. Type codes d, b, o, x can be used to format in decimal, binary,
 octal and hexadecimal respectively. Remember that while formatting integers only width is allowed not precision.

print(format(95, "5d")) 
Output: 95 

print(format(4, "b")) # prints the binary equivalent of decimal 
Output: 100 

print(format(255, "x")) # prints the hexadecimal equivalent of decimal 255 
Output: ff 

print(format(9, "o")) # prints the octal equivalent of decimal 9
Output: 11
"""},
                    {'title': 'Operators in Python', 'content': """Operator: An operator is a symbol which specifies a 
                    specific action. Operand: An operand is a data item on which operator acts.

Arithmetic Operators
Arithmetic operators are commonly used to perform numeric calculations. Python has following arithmetic operators.

* (+) - Addition Operator
Example: 100 + 45 = 145

* (-) -Subtraction Operator
Example: 500 - 65 = 435

* (*) - Multiplication Operator
Example: 25 * 4 = 100

* (/)- Float Division Operator
Example: 10 / 2 = 5.0

* (//) - Integer Division Operator
Example: 10 // 2 = 5

* (**) - Exponentiation Operator
Example: 5 ** 3 = 125

* (%) - Remainder Operator
Example: 10 % 3 = 1

Type Conversion
When it comes to performing a calculation involving data of different types Python has the following rules:
1.	When both operands involved in an expression are int, then the result will be an int. 
2.	When both operands are involved in an expression float, then the result will be a float. 
3.	When one operand is of float type and the other is of type int then the result will always be a float value. In such 
cases, the Python interpreter automatically converts the int value to float temporarily, then performs the calculation. 
This process is known as Type Conversion.

int() - It accepts a string or number and returns a value of type int.
Example:
int(2.7) returns 2, int(“30”) returns 30

float() - It accepts a string or number and returns a value of type float.
Example:
float(42) returns 42.0, float (“3.4”) returns 3.4

str() - It accepts any value and returns a value type str.
Example:
str(12) returns “12”, str(3.4) returns “3.4”

Relational Operators
To compare the values we use relational operators. An expression containing relational operators is known as a 
relational expression. If the expression is true then a bool value True is returned and if the expression is false a 
bool value False is returned. Relational operators are binary operators. The following table lists relational operators 
available in Python:

* (<) - Smaller than
Example:
3 < 4
Output: True

* (>) - Greater than
90 > 450
Output: False

* (<=) - Smaller than or equal to
10 <= 11
Output: True

* (>=) - Greater than or equal to
Example:
31 >= 40
Output: False

(!=) - Not equal to
Example:
100 != 101
Output: True

(==) - Equal to
Example:
50 == 50
Output: True

Logical Operators
Logical operators are used to combining two or more boolean expressions and test whether they are true or false. 
Expressions containing logical operators are known as Logical expressions. The following table lists logical operators 
available in Python.  The and and or are binary operators, while not is unary.

AND Operator
The and-operator returns a bool value True if both operands are true. Otherwise, it returns False. 
Syntax: operand_1 and operand_2 
The truth table for and operator is as follows:

operand_1  ------ operand_2  --------- Result
False              False               False
False              True                False
True               False               False
True               True                True

Here are some examples:
Example ------------Intermediate Expression ----------- Result
(10>3) and (15>6)         True and True                  True
(1>5) and (43==6)        False and False                False
(1==1) and (2!=2)         True and False                False

OR Operator
The or operator returns False when both operands are False. Otherwise, it returns True. 
Its syntax is: Syntax: operand_1 or operand_2 
The truth table for or operator is as follows:

operand_1  ------ operand_2  --------- Result
False              False               False
False              True                True
True               False               True
True               True                True


Here are some examples:
Example ------------Intermediate Expression ----------- Result
(11>55) and (6==6)         False or True                  True
(1>12) and (2==3)         False or  False                False
(10<22) and (20<3)         True or True                  False

NOT Operator
The not operator negates the value of the expression. In other words, if the expression is True, then the not operator
returns False and if it is False, it returns True. Unlike the other two logical operators, the not operator is unary. 
The precedence of the not operator is higher than that of and and or operator. Its syntax is:
Syntax: not operand

The truth table for not operator is as follows:
operand ----------- Result
True                False
False               True

"""}

                ]
            },
            {
                'title': 'Flowchart',
                'content': 'Lesson content for Flowchart',
                'topics': [
                    {'title': 'What is Flowchart?', 'content': """What is a Flowchart?
-	Flowchart is a graphical representation of an algorithm. Programmers often use 
it as a program-planning tool to solve a problem. It makes use of symbols which are connected among them to indicate 
the flow of information and processing.
"""""},

                    {'title': 'Types of Flowcharts', 'content': """Types of Flowcharts

	Program Flowcharts
-	These are used by programmers. 
-	It is graphical description of sequence of logical operations performed by the computer in a computer program. PFC are drawn by use of specific symbols. 
-	A program flowchart shows the program structure, logic flow and operations performed. 
-	The emphasis in a program flowchart is on the logic.

	System Flowcharts
-	System flowcharts are used by system analyst to show various processes, sub systems, outputs and operations on data
    in a system. 
-	It is graphical description of relationships among the inputs, outputs and processes in an IS (modeling systems in 
    physical terms). SFC are drawn by use of specific symbols.

	DFD (Data Flow Diagrams)
-	It shows how the data moves within a system. DFD are also drawn by some specific symbols.
"""},

                    {'title': 'Purpose of Program Flowchart', 'content': """
                    An aid in developing the logic of a program. 

-	Verification that all possible conditions have been considered in a program. 
-	Provides means of communication with others about the program. 
-	A guide in coding the program. 
-	Documentation for the program
"""},

                    {'title': 'Desk Checking', 'content': """•	The process of testing the flowchart with different data 
                    as input, and checking the output. 
•	The test data should include nonstandard data as well as typical data.
"""},

                    {'title': 'General Rules in Flowcharting', 'content': """1.	All boxes of the flowchart are connected with Arrows. (Not lines)
2.	Flowchart symbols have an entry point on the top of the symbol with no other entry points. The exit point for all flowchart symbols is on the bottom except for the Decision symbol. 
3.	The Decision symbol has two exit points; these can be on the sides or the bottom and one side. 
4.	Generally a flowchart will flow from top to bottom. However, an upward flow can be shown as long as it does not exceed 3 symbols. 
5.	Connectors are used to connect breaks in the flowchart. 
Examples are: 
•	From one page to another page. 
•	From the bottom of the page to the top of the same page. 
•	An upward flow of more then 3 symbols. 
6.	Subroutines and Interrupt programs have their own and independent flowcharts. 
7.	All flow charts start with a Terminal or Predefined Process (for interrupt programs or subroutines) symbol. 
8.	All flowcharts end with a terminal or a contentious loop. 

"""},
                    {'title': 'Advantages in Flowchart', 'content': """
1.	Communication
2.	Effective Analysis
3.	Documentation of Program/System
4.	Coding of the Program
"""},
                    {'title': 'Flowcharts for Decision Making', 'content': """
•	Computers are used extensively for performing various types of analysis. The decision symbol is used in 
    flowcharts to indicate it. 
•	The general format of steps for flowcharting is as follows: 
-	Perform the test of the condition. 
-	If condition evaluates true branch to Yes steps. 
-	If condition evaluates false branch to No steps.
"""},
                    {'title': 'Flowchart for Loops', 'content': """•	Looping refers to the repeated use of one or more steps. i.e. the statement or block of statements within the loop are executed repeatedly. 
•	There are two types of loops. One is known as the fixed loop where the operations are repeated a fixed number of times. In this case, the values of the variables within the loop have no effect on the number of times the loop is to be executed.
•	In the other type which is known as the variable loop, the operations are repeated until a specific condition is met. Here, the number of times the loop is repeated can vary.
•	The loop process in general includes : 
-	Setting and initializing a counter 
-	execution of operations 
-	testing the completion of operations 
-	incrementing the counter 
•	The test could either be to determine whether the loop has executed the specified number of times, or whether a specified condition has been met.
"""}
                ]
            },
            {
                'title': 'Strings in Python',
                'content': 'Lesson content for Control Statements',
                'topics': [
                    {'title': 'Strings in Python', 'content': """Strings in Python
-	A string is a sequence of characters enclosed in single ('') or double quotation ("") marks.
-	In programming, the choice between using single quotes (''), double quotes ("") or triple quotes (\""") for defining a string depends on the specific requirements and conventions of the programming language you are using. Here are some general guidelines:

-   Single quotes (\'') : Single quotes are commonly used to define a string literal in many programming languages. For example: 'Hello World'. However, some languages treat single quotes as a character literal, so using them for strings may not be valid syntax in those cases.
-	Double quotes (\""): Double quotes are widely used to define a string literal in most programming languages. For example: "Hello World". Using double quotes is often the default choice.
-	Triple quotes (\"""): Triple quotes are typically used in programming languages to define multi-line strings or strings that span across multiple lines. It allows you to include line breaks and preserve the formatting within the string. Not all programming languages support triple quotes, so it's important to check the documentation or language specifications for the specific language you are using.
 """},
                    {'title': 'Counting Number of Characters Using len() Function', 'content': """The len() built-in function counts the number of characters in the string.

For example:
text = "Hello, World!"
count = len(text)
print("The number of characters in the text is:", count)
 """},
                    {'title': 'Creating Empty Strings', 'content': """Creating an empty string refers to initializing a variable that can hold a string value, but initially does not contain any characters. 

Example: 
                empty_string = \""

In this example, an empty string is created by assigning double quotation marks with no characters inside to the variable empty_string.
"""},
                    {'title': 'Escape Sequences', 'content': """Escape Sequences are set of special characters used to print characters that can't be typed directly using the keyboard. Each Escape Sequence starts with a backslash ( \ ) character.
Escape Sequence	Meaning
\n	        Newline - Prints a newline character
\t	        Tab - Prints a tab character
\\	        Backslash - Prints a backslash (\) character
\’	        Single quote - Prints a single quote
\”	        Double quote - Prints a double quote
"""},
                    {'title': 'String Repetition Operator (*)', 'content': """Just as with numbers, we can also use the * operator with strings. When used with strings * operator repeats the string n number of times. It's general format is:
	String * n 

For example:
                text = "Hello!"
                repeated_text = text * 3
                print(repeated_text)

Expected Output: Hello!Hello!Hello!
"""},
                    {'title': 'Membership Operators - in and not in', 'content': """The in or not in operators are used to check the existence of a string inside another string.
Example of in: 

        fruits = ['apple', 'banana', 'orange']
        print('apple' in fruits)  # True
        print('grape' in fruits)  # False

Example of Not in:

        fruits = ['apple', 'banana', 'orange']
        print('grape' not in fruits)  # True
        print('apple' not in fruits)  # False


"""},
                    {'title': 'Accessing Individual Characters in a String', 'content': """In Python, characters in a string are stored in a sequence. We can access individual characters inside a string by using an index. An index refers to the position of a character inside a string. In Python, strings are 0 indexed, which means that the first character is at the index 0, the second character is at index 1, and so on. The index position of the last character is one less than the length of the string

To access individual characters inside a string we type the name of the 
variable, followed by the index number of the character inside the 
square brackets [].

Example 1:
            text = "Hello, World!"
            print(text[0])    # Accessing the first character
            print(text[7])    # Accessing the eighth character
            print(text[-1])   # Accessing the last character

Expected Output : 
H
W
!

Example 2:
            text = "Hello, World!"
            print(text[0:5])    # Accessing characters from index 0 to 4

Expected Output:
Hello
"""},
                    {'title': 'Slicing Strings', 'content': """String slicing allows us to get a slice of characters from the string. We use the slicing operator ( [start_index:end_index] ) to get a slice of string. Its syntax is: 
str_name[start_index:end_index] returns a slice of string starting from index start_index to the end_index. The character at the end_index will not be included in the slice.

Example of slicing:
                    text = "Hello, World!"

                    # Slicing to extract a substring
                    substring = text[7:12]
                    print(substring)  # Output: World

                    # Slicing with step value
                    every_other = text[::2]
                    print(every_other)  # Output: Hlo ol!"""},

                    {'title': 'Strings Methods in Python', 'content': """Strings Methods in Python
String class i.e. str provides many useful methods to manipulate string. Specifically, we will discuss methods that do the following.
1.	Search for a substring inside a string. 
2.	Test strings. 
3.	Format strings. 
4.	Convert strings.



"""},

                ]
            },
            {
                'title': 'Lists in Python',
                'content': 'Lesson content for Control Statements',
                'topics': [
                    {'title': 'List Definition', 'content': """What is a List?
            A list is a sequence of multiple items separated by a comma and enclosed inside square brackets i.e. []. The syntax for creating a list is as follows:

            variable = [item1, item2, item3, …, itemN]

            list1 = list()	# an empty list
            list2 = list([3.2, 4, 0.12])		    # again elements in a list can be of different types
            list3 = list([“@@”, “###”, “>>>”])		# you can use symbols too
            list4 = list(“1234”)	                # creating list from string


            The elements of a list can be a list too

            1	>>>
            2	>>> list5 = [
            3	. . .	[33, 55, 77],	# first element
            4	. . .	[99, 31, 64]	# second element
            5	. . .   ]
            6	>>>
            7	>>>
            8	>>> list5
            9	[[33, 55, 77], [99, 31, 64]] 

            """},
                    {'title': 'Creating a Lists using Range() Function', 'content': """The range() function can also be used to create long lists.

            1	>>>
            2	>>> list1 = list(range(5))
            3	>>> list1
            4	[0, 1, 2, 3, 4]
            5	>>>
            6	>>>

            """},
                    {'title': 'List Functions', 'content': """The following table lists some functions, we commonly use while working with lists.

            len() - returns the number of elements in the sequence

                    Example of using len():
                            text = "Hello, World!"

                            length = len(text)
                            print(length)

                    Output: 13


            sum() - returns the sum of elements in the sequence

                    Example of using sum():
                            numbers = [1, 2, 3, 4, 5]

                            total = sum(numbers)
                            print(total)

                    Output: 15


            max() - returns the element with greatest value in the sequence

                    Example of using max():
                            numbers = [5, 9, 2, 7, 3]

                            maximum = max(numbers)
                            print(maximum)

                    Output: 9


            min() - returns the element with smallest value in the sequence

                    Example of using min():
                            numbers = [5, 9, 2, 7, 3]

                            minimum = min(numbers)
                            print(minimum)

                    Output: 2

            """},
                    {'title': 'Index Operator', 'content': """ the index operator, represented by square brackets [], is used to access individual elements or characters within a sequence-like object such as a string, list, or tuple. 

                    Example:
                            -index = -6   -5   -4   -3   -2   -1
                            list1 = [ 88, 99, 4.12, 199, 993, 9999 ]
                            index =   0    1    2    3    4    5

                    Example:

                            fruits = ["apple", "banana", "cherry"]

                            print(fruits[0])  # Accesses the first element: "apple"
                            print(fruits[1])  # Accesses the second element: "banana"
                            print(fruits[2])  # Accesses the third element: "cherry"

                    Output: 
                            apple
                            banana
                            cherry
                    """},
                    {'title': 'Iterating Through Elements in a List', 'content': """ To iterate though a list we can use for loop as follows:

                    fruits = ["apple", "banana", "cherry"]

                    for fruit in fruits:
                        print(fruit)

                    Output: 
                            apple
                            banana
                            cherry


            we can use a for loop in conjunction with the range() function, as follows:

                    for i in range(5):
                        print(i)

                    Output: 
                            0
                            1
                            2
                            3
                            4

            Although, the for loop is a preferred way to iterate over list, if we want, we can use while loop too. For example:

                    fruits = ["apple", "banana", "cherry"]
                    index = 0

                    while index < len(fruits):
                        print(fruits[index])
                        index += 1

                    Output: 
                            apple
                            banana
                            cherry

            """},

                    {'title': 'List Slicing', 'content': """The slicing operator we discussed in the lesson Strings in Python is also available in the list. The only difference is that instead of returning a slice of string, here it returns a slice of list. It's syntax is:

            list[start:end]

            >>> list1 = [11, 33, 55, 22, 44, 89] 
            >>> list1[0:4] 
            >>> list1[1:5] 
            >>> list1[4:5]
            >>> list1[:2]   # same as list1[0:2] 
            >>> list1[2:]   # same as list1[2:len(list1)] 
            >>> list1[:]    # same as list1[0:len(list1)]

            """},
                    {'title': 'List Concatenation', 'content': """The list can be joined too using the + operator. When operands on both sides are lists + operator creates a new list by combing elements from both lists. 

                    For example:
                                list1 = [1,2,3] # create list1 
                                list2 = [11,22,33] # create list2 
                                list3 = list1 + list2 # concatenate list1 and list2 and create list3 
                                print(list3) 

                                output: [1, 2, 3, 11, 22, 33] 

            Another way to concatenate list is use += operator. The += operator modifies the list instead of creating a new list. 

                    Here is an example: 
                                list1 = [1,2,3] # create list1 
                                list2 = [11,22,33] # create list2 
                                list1 += list2 # append list2 to list1 
                                print(list1) 

                                output: [1, 2, 3, 11, 22, 33]

            """},
                    {'title': 'Repetition Operator', 'content': """List comprehension is a concise and powerful way to create new lists in Python. It provides a compact syntax for generating lists based on existing iterables, such as lists, strings, or ranges, with optional filtering and transformation of elements.

            The basic structure of a list comprehension consists of square brackets [ ] containing an expression followed by a for clause. Here's a general syntax:

                    new_list = [expression for item in iterable]

                    (1) example:
                            numbers = [1, 2, 3, 4, 5]
                            squares = [num ** 2 for num in numbers]
                            print(squares)

                    Output: [1, 4, 9, 16, 25]

                    (2) example:
                            numbers = [1, 2, 3, 4, 5]
                            even_numbers = [num for num in numbers if num % 2 == 0]
                            print(even_numbers)

                    Output: [2, 4]

                    (3) example:
                            text = "Hello, World!"
                            uppercase_chars = [char.upper() for char in text if char.isalpha()]
                            print(uppercase_chars)

                    Output: ['H', 'E', 'L', 'L', 'O', 'W', 'O', 'R', 'L', 'D']


            """},
                    {'title': 'List Methods', 'content': """The list class has many built-in methods which allow us to add an element, remove an element, update an element, and much more. The following table lists some common methods provided by the list class to manipulate lists.

            append(item) - adds an item to the end of the list

                    Example of using append(item):

                            fruits = ["apple", "banana", "cherry"]
                            fruits.append("orange")
                            print(fruits)

                    Output: ["apple", "banana", "cherry", "orange"]


            insert(index, item) - inserts an item at the specified index. If index specified is greater than the last valid index, item is added to the end of the list.

                    Example of using insert(index, item):

                            fruits = ["apple", "banana", "cherry"]
                            fruits.insert(1, "orange")
                            print(fruits)

                    Output: ["apple", "orange", "banana", "cherry"]


            index(item) - returns the index of the first occurrence of specified item. If the specified item doesn’t exists in the list, an exception is raised.

                    Example of using index(item):
                            fruits = ["apple", "banana", "cherry"]
                            index = fruits.index("banana")
                            print(index)

                    Output: 1


            remove(item) - removes the first occurence of specified item. If the specified item doesn’t exists in the list, an exception is raised.

                    Example of using remove(item) :

                            fruits = ["apple", "banana", "cherry"]
                            fruits.remove("banana")
                            print(fruits)

                    Output: ["apple", "cherry"]


            count(item) - returns the number of times an item appears in the list.

                    Example of using count(item):

                            fruits = ["apple", "banana", "cherry", "banana", "banana"]
                            count = fruits.count("banana")
                            print(count)

                    Output: 3


            clear() - removes all the element from the list.

                    Example of using clear():

                            fruits = ["apple", "banana", "cherry"]
                            fruits.clear()
                            print(fruits)

                    Output: []


            sort() - sorts the list in ascending order.

                    Example of using sort():
                            numbers = [5, 2, 8, 1, 9, 3]
                            numbers.sort()
                            print(numbers)

                    Output: [1, 2, 3, 5, 8, 9]


            reverse() - reverse the order of elements in the list.

                    Example of using reverse():

                            numbers = [5, 2, 8, 1, 9, 3]
                            numbers.reverse()
                            print(numbers)

                    Output: [3, 9, 1, 8, 2, 5]


            extend(sequence) - appends the elements of the sequence to the end of the list.

                    Example of using extend(sequence):

                            fruits = ["apple", "banana", "cherry"]
                            more_fruits = ["orange", "grape"]
                            fruits.extend(more_fruits)
                            print(fruits)

                    Output: ["apple", "banana", "cherry", "orange", "grape"]


            pop([index]) - removes the element at the specified index and returns that element. If index is not specified, it removes and returns last element from the list. When index is not valid, an exception is raised.

                    Example of using pop([index]):
                            fruits = ["apple", "banana", "cherry"]
                            removed_fruit = fruits.pop(1)
                            print(removed_fruit)
                            print(fruits)

                    Output: 
                            banana
                            ["apple", "cherry"]

            """}
                ]
            },
            {
                'title': 'Dictionary in Python',
                'content': 'Lesson content for Control Statements',
                'topics': [
                    {'title': 'Dictionary Introduction', 'content': """Dictionary is another built-in data type which allows us to store a collection of key-value pairs. Each element in a dictionary has two parts: a key and a value.

            Think of Dictionary like a list, unlike a list, however, elements stored in the dictionary are stored in no order and we use a key to access a specific value. Most of the time key is a string, but it can be any immutable type such as int, float, tuple, string etc. Each key maps to a value, so we can't have duplicate keys. Dictionaries are mutable objects which means we can add, remove, or update the elements after it is created.

            """},
                    {'title': 'Creating Dictionary', 'content': """ We can create a dictionary using the following syntax:

            variable_name = { 'key1' : 'value1',
                              'key2' : 'value2', 
                              'key3' : 'value3',
                              ... 'keyN' : 'valueN' 
                            }

                Example of Dictionary:
                        phonebook = {
                                    "John": 1234567890,
                                    "Alice": 9876543210,
                                    "Bob": 5555555555
                                    }

            Note that the order in which the elements are displayed in the console is not the same order in which they are created. This shows that the elements in the dictionary are stored in no order.

            To create an empty dictionary do this:
                empty_dict = {}

                            """},
                    {'title': 'Accessing Value From a Dictionary', 'content': """As already discussed, the order of elements in a dictionary may vary. Consequently, we can't use element's index position to access the value. Instead, we use a key. To access the value from the dictionary we use the following syntax:

            To access the value associated with a specific key in a dictionary, you can use square brackets [] or the get() method.
                Here is an example of using square brackets []:

                    # Creating a dictionary
                    student = {"name": "John Doe", "age": 20, "grade": "A"}

                    # Accessing values using square brackets
                    print(student["name"])  # Output: John Doe
                    print(student["age"])   # Output: 20
                    print(student["grade"]) # Output: A

                Here is an example of using get():    
                    # Creating a dictionary
                    student = {"name": "John Doe", "age": 20, "grade": "A"}

                    # Accessing values using the get() method
                    print(student.get("name"))  # Output: John Doe
                    print(student.get("age"))   # Output: 20
                    print(student.get("grade")) # Output: A

            NOTE: If the key exists in the dictionary, using either approach will return the associated value. 

            However, there is a difference when the key does not exist:
                --  When using square brackets, if the key is not found, it will raise a KeyError exception.

                        Example:
                                student = {"name": "John Doe", "age": 20, "grade": "A"}
                                print(student["address"])  # Raises KeyError: 'address'

                --  When using the get() method, if the key is not found, it will return None by default, or you can specify a default value to be returned instead.

                        Example: 
                                student = {"name": "John Doe", "age": 20, "grade": "A"}
                                print(student.get("address"))           # Output: None
                                print(student.get("address", "N/A"))    # Output: N/A

            """},
                    {'title': 'Adding and Modifying Values', 'content': """We can add a new element to a dictionary using the following syntax:

            dict_name[key] = value

                    For example:
                        # Creating a dictionary
                        student = {"name": "John Doe", "age": 20}

                        # Adding a new key-value pair
                        student["grade"] = "A"
                        print(student)  

                    Output: {"name": "John Doe", "age": 20, "grade": "A"}


            if key already exists in the dictionary, then its value is updated.
                    For example:
                        # Creating a dictionary
                        student = {"name": "John Doe", "age": 20, "grade": "A"}

                        # Modifying an existing value
                        student["age"] = 21
                        print(student) 

                    Output: {"name": "John Doe", "age": 21, "grade": "A"}

            """},
                    {'title': 'Deleting Elements', 'content': """To delete an element from a dictionary, we use the del statement. The syntax of 
            the del statement is as follows:

            del dict_name[key]

                    For example:
                        # Creating a dictionary
                        student = {"name": "John Doe", "age": 20, "grade": "A"}

                        # Deleting a specific key-value pair
                        del student["age"]
                        print(student)  

                    Output: {"name": "John Doe", "grade": "A"}

            NOTE: If the key doesn't exist in the dictionary, KeyError exception is raised.   

            """},
                    {'title': 'Getting Length of Dictionary using len()', 'content': """We can use the built-in len() function to count the number of elements in a dictionary. 

                The syntax of the del statement is as follows:

                    my_dict = {'key1': 'value1', 'key2': 'value2', 'key3': 'value3'}

                    # Counting the number of key-value pairs (entries) in the dictionary
                    num_elements = len(my_dict)
                    print(num_elements)  # Output: 3

                    # Counting the number of keys in the dictionary
                    num_keys = len(my_dict.keys())
                    print(num_keys)  # Output: 3

                    # Counting the number of values in the dictionary
                    num_values = len(my_dict.values())
                    print(num_values)  # Output: 3
            """},
                    {'title': 'Iterating through Elements Using for Loop', 'content': """We can use for loop to iterate through all the keys in the dictionary as follows:

                my_dict = {'key1': 'value1', 'key2': 'value2', 'key3': 'value3'}

                # Iterating over the keys in the dictionary
                for key in my_dict:
                    print(key)

                # Output:
                # key1
                # key2
                # key3

            If you need to access both the keys and their corresponding values, you can use the .items() method to iterate over key-value pairs. 

                Here's an example:
                    my_dict = {'key1': 'value1', 'key2': 'value2', 'key3': 'value3'}

                    # Iterating over key-value pairs in the dictionary
                    for key, value in my_dict.items():
                        print(key, value)

                    # Output:
                    # key1 value1
                    # key2 value2
                    # key3 value3

            """},
                    {'title': 'Membership Operators with Dictionary', 'content': """The in and not in operators can be used to test the existence of a key inside a dictionary. 

            Here is an example:
                my_dict = {'key1': 'value1', 'key2': 'value2', 'key3': 'value3'}

                # Check if a key is present in the dictionary
                if 'key1' in my_dict:
                    print("Key 'key1' is present")

                # Check if a key is not present in the dictionary
                if 'key4' not in my_dict:
                    print("Key 'key4' is not present")

                # Output:
                # Key 'key1' is present
                # Key 'key4' is not present
            """},
                    {'title': 'Comparison Operators with Dictionary', 'content': """We can use == and != operators to test whether two dictionaries contains same elements or not.

                    For example:
                        dict1 = {'key1': 'value1', 'key2': 'value2'}
                        dict2 = {'key1': 'value1', 'key2': 'value2'}
                        dict3 = {'key1': 'value1', 'key2': 'value3'}

                        # Comparing dict1 and dict2 for equality
                        if dict1 == dict2:
                            print("dict1 and dict2 are equal")

                        # Comparing dict1 and dict3 for inequality
                        if dict1 != dict3:
                            print("dict1 and dict3 are not equal")

                        # Output:
                        # dict1 and dict2 are equal
                        # dict1 and dict3 are not equal


                """},
                    {'title': 'Dictionary Methods', 'content': """The lists are some common methods we can call on a dictionary object.

            keys() - Returns a sequence containing only the keys from the dictionary.

                    Example of using keys():

                                colors = {
                                "red": "#FF0000",
                                "green": "#00FF00",
                                "blue": "#0000FF"
                             }

                            # Retrieving a view object containing the keys
                            key_view = colors.keys()

                            # Printing the keys using a loop
                            for key in key_view:
                                print(key)

                    Output:
                            red
                            green
                            blue


            values() - Returns a sequence containing only the values from the dictionary.

                    Example of using values():

                            scores = {
                                "math": 95,
                                "science": 87,
                                "history": 92
                            }

                            # Retrieving a view object containing the values
                            value_view = scores.values()

                            # Printing the values using a loop
                            for value in value_view:
                                print(value)

                    Output:
                            95
                            87
                            92


            items() - Returns a sequence of tuples, where each tuple contains a key and value of an element.

                    Example of using items():

                            fruits = {
                                "apple": "red",
                                "banana": "yellow",
                                "grape": "purple"
                            }

                            # Retrieving a view object containing the key-value pairs
                            item_view = fruits.items()

                            # Printing the key-value pairs using a loop
                            for key, value in item_view:
                                print(key, "->", value)

                    Output:
                            apple -> red
                            banana -> yellow
                            grape -> purple


            get(key, [default]) - Returns the value associated with the key. If the key is not found, it returns None. We can also provide an optional default value as the second argument in which case if the key is not found, default value will be returned instead of None.

                    Example of using get(key,[default]):

                            fruits = {"apple": "red", "banana": "yellow", "grape": "purple"}

                            # Retrieving the value for a specific key using get()
                            fruit_color = fruits.get("banana")

                            # Printing the value
                            print(fruit_color)  

                    Output: Yellow


            pop(key) - Returns the value associated with the key then removes the specified key and its corresponding value from the dictionary. If key doesn’t exist, KeyError exception is raised.

                    Example of using pop(key):

                            contacts = {
                                "USA": "Washington D.C.",
                                "France": "Paris",
                                "India": "New Delhi",
                                "Japan": "Tokyo"
                            }

                            # Removing a key-value pair using pop()
                            capital = countries.pop("India")

                            # Printing the removed value
                            print(capital)  # Output: New Delhi

                            # Printing the updated dictionary
                            print(countries)

                    Output: {'USA': 'Washington D.C.', 'France': 'Paris', 'Japan': 'Tokyo'}


            popitem() - Removes and return a random element from the dictionary as a tuple.

                    Example of using popitem():

                            fruits = {"apple": "red", "banana": "yellow", "grape": "purple"}

                            # Removing and returning an arbitrary key-value pair using popitem()
                            removed_item = fruits.popitem()

                            # Printing the removed key-value pair
                            print(removed_item)  # Output: ('grape', 'purple')

                            # Printing the updated dictionary
                            print(fruits)  


                    Output: {'apple': 'red', 'banana': 'yellow'}


            copy() - Creates a new copy of the dictionary.

                    Example of using copy():

                            student_scores = {"Alice": 85, "Bob": 92, "Charlie": 78, "David": 90}

                            # Creating a copy of the dictionary using copy()
                            scores_copy = student_scores.copy()

                            # Modifying the copied dictionary
                            scores_copy["Charlie"] = 82

                            # Printing both dictionaries
                            print(student_scores)  
                            print(scores_copy) 

                    Output: 
                            {"Alice": 85, "Bob": 92, "Charlie": 78, "David": 90}
                            {"Alice": 85, "Bob": 92, "Charlie": 82, "David": 90}

            clear() - Removes all the elements from the dictionary.

                    Example of using clear():

                        fruits = {"apple": "red", "banana": "yellow", "grape": "purple"}

                        # Clearing the dictionary using clear()
                        fruits.clear()

                        # Printing the cleared dictionary
                        print(fruits)  

                    Output: {}

            """}
                ]
            }
        ]

        sm = ScreenManager()
        sm.add_widget(MainScreen(lessons=lessons, name='main'))
        sm.add_widget(LessonScreen(name='lessons'))
        sm.add_widget(TopicScreen(name='topics'))

        return sm


if __name__ == '__main__':
    PyLearnApp().run()
