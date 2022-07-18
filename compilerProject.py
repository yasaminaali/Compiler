import numpy as np
import pandas as pd
import re


f = open("decaf_input3.decaf", "r")
x = f.read()


Keywords = []
Operators = []
Decimals = []
Symbols = []
Identifiers = []


List_Keywords = ['def', 'if', 'else', 'while', 'return', 'break', 'continue', 'int', 'bool', 'void', 'true', 'false', 'for', 'callout', 'class', 'interface', 'extands', 'implements', 'new', 'this', 'string', 'float', 'double', 'null']
List_Symbols = ['(', '{', '[', ']', '}', ')', ',', ';', '=', '+', '-', '*', '/', '%', '<', '>', '<=', '>=', '==', '!=', '&&', '||', '!']
List_Decimals = []
List_String = []
List_Hex = []
List_Id = []

print('x', x)


def remove_Spaces(x):

    y = []
    for line in x:
        if (line.strip() != ''):
            y.append(line.strip())

    return y


def remove_Comments(x):

    Multi_Comments_Removed = re.sub("/\*[^*]*\*+(?:[^/*][^*]*\*+)*/", "", x)
    Single_Comments_Removed = re.sub("//.*", "", Multi_Comments_Removed)
    Comments_removed = Single_Comments_Removed


    return Comments_removed



Comments_removed = remove_Comments(x)
z = Comments_removed.split('\n')
z_ = remove_Spaces(z)

print('z', z)
print('z_', z_)


a = '\n'.join([str(elem) for elem in z_])
scanned_Program_lines = a.split('\n')


C = []
for line in scanned_Program_lines:
    C.append(line)

za = []
for x in C:
    za.append(x.split())

print('za', za)

# Decimal
for q in za:
    for i in q:
        if i.isdecimal():
            List_Decimals.append(i)
print('List_Decimals', List_Decimals)

# String
for q in za:
    for i in q:
        if(i.startswith('"')):
            List_String.append(i)

print(List_String)

# Identifiers
for q in za:
    for i in q:
        if(i.isidentifier()):
            List_Id.append(i)
print('List_Id', List_Id)

# Jadvale Namad

name = List_Id + List_Keywords
nemune = list(set(name))
print('nemune', nemune)

Nemune = pd.DataFrame(nemune)
print(Nemune)



# Donbale Tokens

tokens = []

for u in za:
    for i in u:
        for l in List_Keywords:
            if(i == l):
                index = nemune.index(i)
                token = ['KEY', index]
                tokens.append(token)

        for o in List_Id:
            if(i == o):
                index = nemune.index(i)
                token = ('ID', index)
                tokens.append(token)

        for m in List_Symbols:
            if(i == m):
                token = ('SYM', i)
                tokens.append(token)


        for n in List_String:
            if(i == n):
                token = ('STR', i)
                tokens.append(token)

        for p in List_Decimals:
            if(i == p):
                token = ('DEC', i)
                tokens.append(token)

        """for q in List_Hex:
            if(i == q):
                token = ('HEX', i)
                tokens.append(token)"""

print("-------------------------------------------------------")
print(tokens)

Tokens = pd.DataFrame(tokens)
print(Tokens)