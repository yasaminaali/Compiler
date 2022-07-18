import pandas as pd


grammar = open("C:\My Files\Programming\compilerPhase2Final\grammar.txt", "r")
x = grammar.read()
g = x.split('\n')



nonTerminalList = []
rhs = []

tempList = []

for line in g:
	tempList.append(line.split(" "))



for t in tempList:
	for i in t:
		if( i == '->'):
			c = t.index(i)
			nonTerminalList.append(t[c-1])

for t in tempList:
	for i in t:
		if( i == '->'):
			c = t.index(i)
			rhs.append(t[c+1:])

print("non: \n", nonTerminalList)
print("rhs: \n", rhs)



productions = dict()

print("test", len(nonTerminalList))

counter = 0
for t in tempList:
	for i in t:
		if(i == nonTerminalList[counter]):
			productions[nonTerminalList[counter]] = rhs[counter]
			counter = counter + 1
			print(counter, 'time coorect')
			if(counter == len(nonTerminalList) - 1):
				break
	if(counter == len(nonTerminalList) - 1):
		break


first_dict = dict()
follow_dict = dict()

print("productions: \n", productions)

#---first---

def first(nonTerminalList, productions):
	c = nonTerminalList[0]
	print("c",c)
	ans = set()
	if c.isupper():
		c = nonTerminalList
		print("c2", c)
		for st in productions[c]:
			print("st", st)
			if st == '#' :				
				if len(nonTerminalList)!=1 :
					ans = ans.union( first(nonTerminalList[1:], productions) )
				else :
					ans = ans.union('@')
			else :	
				f = first(st, productions)
				ans = ans.union(x for x in f)
				print("if else", ans)
	else:
		ans = ans.union(c)
		print("else", ans)
	return ans


print ('\nFirst\n')


for nonTerminalList in productions:
	first_dict[nonTerminalList] = first(nonTerminalList, productions)


print("done")

for f in first_dict:
	print(str(f) + " : " + str(first_dict[f]))

#---follow---

def follow(s, productions, ans):
	if len(s) != 1 :
		return {}

	for key in productions:
		for value in productions[key]:
			f = value.find(s)
			if f != -1:
				if f == (len(value)-1):
					if key != s:
						if key in ans:
							temp = ans[key]
						else:
							ans = follow(key, productions, ans)
							temp = ans[key]
						ans[s] = ans[s].union(temp)
				else:
					first_of_next = first(value[f+1:], productions)
					ans[s] = ans[s].union(first_of_next)
	return ans


print ('\nFollow\n')

start = nonTerminalList[0]

for nonTerminalList in productions:
	follow_dict[nonTerminalList] = set()
	start = nonTerminalList

follow_dict[start] = follow_dict[start].union('$')

for nonTerminalList in productions:
	follow_dict = follow(nonTerminalList, productions, follow_dict)

for f in follow_dict:
	print(str(f) + " : " + str(follow_dict[f]))


#---parsingTable----

def Table(follow, productions):
	
	print ("\nParsing Table\n")

	table = {}
	for key in productions:
		for value in productions[key]:
			if value != '#':
				for element in first(value, productions):
					table[key, element] = value
			else:
				for element in follow[key]:
					table[key, element] = value

	for key,val in table.items():
		print( key, "=>", val)

	new_table = {}
	for pair in table:
		new_table[pair[1]] = {}

	for pair in table:
		new_table[pair[1]][pair[0]] = table[pair]


	print ("\n")
	print ("\nParsing Table in matrix form\n")
	print (pd.DataFrame(new_table).fillna('-'))
	print ("\n")

	return table


#---parser----

def parse(tokens, start_symbol, parsingTable):

	flag = 0

	#appending dollar to end of input
	tokens = tokens + "$"

	stack = []
	
	stack.append("$")
	stack.append(start_symbol)

	input_len = len(tokens)
	index = 0

	
	while len(stack) > 0:

		#element at top of stack
		top = stack[len(stack)-1]

		print ("Top =>",top)

		#current input
		current_input = tokens[index]

		print ("Current_Input => ",current_input)

		if top == current_input:
			stack.pop()
			index = index + 1	
		else:	

			#finding value for key in table
			key = top , current_input
			print (key)

			#top of stack terminal => not accepted
			if key not in parsingTable:
				flag = 1		
				break

			value = parsingTable[key]
			if value != '#':
				value = value[::-1]
				value = list(value)
				
				#poping top of stack
				stack.pop()

				#push value chars to stack
				for element in value:
					stack.append(element)
			else:
				stack.pop()		

	if flag == 0:
		print ("String accepted!")
	else:
		print ("String not accepted!")	


tokensFile = open("C:\My Files\Programming\compilerPhase2Final\tokens.txt", "r")
t = tokensFile.read()
tokens = t.split('\n')

parsingTable = Table(follow_dict, productions)

parse(tokens, start, parsingTable)

