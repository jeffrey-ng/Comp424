import sys
import string

class Placement:
	first = 0
	second = 1
	third = 2

class Variable(object):
	def __init__(self, direction, place, list):
		self.direction = direction
		self.list = list
		self.place = place

	def set_constraints(self,variables):
		self.constraints = variables

def main():
	in_file = sys.argv[1]
	print "Parsing input file: {0}".format(in_file)
	word_list = parse_input_file(in_file)

	a1 = Variable('A', Placement.first, word_list[:])
	a2 = Variable('A', Placement.second, word_list[:])
	a3 = Variable('A', Placement.third, word_list[:])

	d1 = Variable('D', Placement.first, word_list[:])
	d2 = Variable('D', Placement.second, word_list[:])
	d3 = Variable('D', Placement.third, word_list[:])

	a1.set_constraints([d1,d2,d3])
	a2.set_constraints([d1,d2,d3])
	a3.set_constraints([d1,d2,d3])

	d1.set_constraints([a1,a2,a3])
	d2.set_constraints([a1,a2,a3])
	d3.set_constraints([a1,a2,a3])

	variables = [a1,a2,a3,d1,d2,d3]
	iterations = 0
	while True:
		removed = 0
		print '\n=== Iteration ' + repr(iterations) + ' ===\n'
		iterations = iterations + 1
		for d in variables:
			removed = removed + remove_words(d)
			print d.list
		if removed == 0:
			print 'interations done: ' + repr(iterations)
			break;


def parse_input_file(f_name):
    """Read and parse the 'problem definition' file with name 'f_name'."""
    f_lines = [[w.strip() for w in l.split(' ')] for l in open(f_name).readlines()]
    word_list = []
    i = 0
    while (f_lines[i][0] != 'STATE'):
        word_list.append(f_lines[i][0])
        i = i + 1
    i = i + 1
   
    return word_list


def remove_words(vari):
	word_list = vari.list
	copy = vari.list
	remove_words_list = []


	#First check if any other word contains the letter
	print 'Removing words for ' + vari.direction + repr(vari.place) + ' of size ' + repr(len(vari.list)) 


	for string in word_list:
		for x in range (0,3):
			c = vari.constraints[x]
			if not check_list(string[x],vari.place,c.list):
				if string not in remove_words_list:
						#print 'remove word: ' + outer_string
						remove_words_list.append(string)
				break

	for s in remove_words_list:
		word_list.remove(s)

	vari.list = word_list
	return len(remove_words_list)

def check_list(char, placement, word_list):
	for string in word_list:
		if string[placement] == char:
			return True
	else:
		return False

main()