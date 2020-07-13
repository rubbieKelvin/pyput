# PyPut: `a better version of python's native input function`

> no dependencies :)

## importing the pyput module


```python
import pyput
from pyput.validators import * # validators

# imports below are not required
from pprint import PrettyPrinter # for pretty printing

printer = PrettyPrinter()
pprint = printer.pprint
```

## Usage:

##### collect `string` from user


```python
name = pyput.CliInput("enter your name: ").result(str)
print(name, "is of type", type(name))
```

    enter your name: rubbie kelvin
    rubbie kelvin is of type <class 'str'>


##### collect an `integer` from user



```python
age = pyput.CliInput("enter your age: ").result(int)
print(age, "is of type", type(age))
```

    enter your age: 18
    18 is of type <class 'int'>


##### collect a `boolean` from user


```python
is_active_on_media = pyput.CliInput("are you active on media? ").result(bool)
print(is_active_on_media, "is of type", type(age))
```

    are you active on media? 
    False is of type <class 'int'>


##### collect a `list` from user


```python
friends = pyput.CliInput("enter your friends name").result(str, str, str)  # collects 3 strings and returns list
print(friends, "is of type", type(friends))
```

    enter your friends name[0]rezzy
    enter your friends name[1]brumeh
    enter your friends name[2]middo
    ['rezzy', 'brumeh', 'middo'] is of type <class 'list'>



```python
# in the above example, the length of the list is determined by the types passed into pyput.CliInput.result
# somthing like this could help :)

n = pyput.CliInput("how many friends do you have? ").result(int)
friends = pyput.CliInput("enter thier names").result([str]*n)
print(friends)
```

    how many friends do you have? 3
    enter thier names[0]brumeh
    enter thier names[1]kandy
    enter thier names[2]jerome
    ['brumeh', 'kandy', 'jerome']


##### working with a `dictionary`


```python
name_dict = pyput.CliInput("what's your name? ").result(firstname=str, lastname=str)
print(name_dict)
```

    what's your name? [firstname]rubbie
    what's your name? [lastname]kelvin
    {'firstname': 'rubbie', 'lastname': 'kelvin'}



```python
# working with large dictionaries
# lets say we have a default data template for a user
userdata = {
    "name": {"first":"Anonymous", "last":""},
    "gender":"male",
    "email":"no email",
    "numbers":[0, 0]
}

# we wouldnt need to start specifying types
# there's an inbuilt function to deal with that for us; puput.typed
userdata = pyput.CliInput("enter you details:").result(pyput.typed(userdata))
pprint(userdata)
```

    enter you details:[name][first]rubbie
    enter you details:[name][last]kelvin
    enter you details:[gender]male
    enter you details:[email]rubbiekelvinvoltsman@gmail.com
    enter you details:[numbers][0]2348141342356
    enter you details:[numbers][1]0
    {'email': 'rubbiekelvinvoltsman@gmail.com',
     'gender': 'male',
     'name': {'first': 'rubbie', 'last': 'kelvin'},
     'numbers': [2348141342356, 0]}


### What does `typed()` do?

<span style="color: orange;">typed()</span> takes in a container, either a dictionary or a list, then iterates through it to change integers, strings, and booleans to thier respective datatypes


```python
# look at this:
typed_example = pyput.typed([1, 2, dict(name="rubbie", age=18, ismale=True)])
pprint(typed_example)
```

    [<class 'int'>,
     <class 'int'>,
     {'age': <class 'int'>, 'ismale': <class 'bool'>, 'name': <class 'str'>}]


### collecting 2D List


```python
matrix = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0]
]

matrix = pyput.CliInput("enter matrix number").result(pyput.typed(matrix))
pprint(matrix)
```

    enter matrix number[0][0]1
    enter matrix number[0][1]2
    enter matrix number[0][2]3
    enter matrix number[1][0]4
    enter matrix number[1][1]5
    enter matrix number[1][2]6
    enter matrix number[2][0]7
    enter matrix number[2][1]8
    enter matrix number[2][2]9
    [[1, 2, 3], [4, 5, 6], [7, 8, 9]]


## Validating input


```python
# lets make sure the user enters a string with greater than 8 characters
def validator(value):
    return len(value) > 8

data = pyput.CliInput("enter a string: ", validator=validator).result(str)
```

    enter a string: this is valid



```python
# using lambdas
data = pyput.CliInput("enter a string: ", validator=lambda x:len(x)>8).result(str)
```

    enter a string: this is valid


### Validator Classes
#### Inbuilt Validator classes

* StringSizeValidator
* EmailValidator
* PasswordValidator
* RangeValidator

#### Simple password validator


```python
password = pyput.CliInput("enter your password: ", validator=PasswordValidator()).result(str)
```

    enter your password: qwertyA2!


#### Creating validator classes
all validator classes should have a `validate` method that takes in a string argument that returns a bool value :). you might also want to inherit the `pyput.validators.Validator` class (may not be neccessary).


```python
class SquareIntValidator(Validator):
    """this class validates if a number is a perfect square
    """
    def validate(self, value):
        root = value**0.5
        return value == root*root
    
perfect_square = pyput.CliInput("enter a perfect square: ", validator=SquareIntValidator()).result(int)
```

    enter a perfect square: 9



```python

```
