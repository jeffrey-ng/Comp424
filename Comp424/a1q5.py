import random
import string
import sys



#========= START PROVIDED CODE =========

def parse_input_file(f_name):
	#Taken from demo
    """Read and parse the 'problem definition' file with name 'f_name'."""
    f_lines = [[w.strip() for w in l.split(' ')] for l in open(f_name).readlines()]
    word_list = []
    i = 0
    while (f_lines[i][0] != 'STATE'):
        word_list.append(f_lines[i][0])
        i = i + 1
    i = i + 1
    start_state = {}
    while (f_lines[i][0] != 'STATE'):
        start_state[f_lines[i][0]] = f_lines[i][1]
        i = i + 1
    return [word_list, start_state]

def parse_state_file(f_name):
    """Parse the given file into a list of state dicts."""
    try:
        f_lines = [l.strip() for l in open(f_name).readlines()]
    except:
        print "Could not open file: {0}.".format(str(f_name))
        sys.exit(0)
    state_dicts = []
    new_state = 0
    i = 0
    while (i < len(f_lines)):
        state_lines = []
        # Set aside the lines in the file describing the current state
        if (f_lines[i] == 'STATE START'):
            i = i + 1
            while (f_lines[i] != 'STATE END'):
                state_lines.append(f_lines[i])
                i = i + 1
        else:
            i = i + 1
        # Parse the description of the current state into a dict
        s_dict = {}
        for s_line in state_lines:
            position, word = s_line.split(' ')
            s_dict[position] = word
        state_dicts.append(s_dict)
        i = i + 1
    return state_dicts

def count_conflicts(state_dict):
    """Count the number of across/down word conflicts in the given state."""
    indices = set()
    across_words = {}
    down_words = {}
    for (key, val) in state_dict.items():
        idx = int(key[1:]) - 1
        indices.add(idx)
        if (key[0] == 'A'):
            across_words[idx] = val
        elif (key[0] == 'D'):
            down_words[idx] = val
        else:
            print "Bad state: {0}".format(str(state_dict))
            sys.exit(0)
    indices = list(indices)
    indices.sort()
    # Infer "board size" from the key/value pairs in the state dict.
    max_idx = max(indices)
    # Get lists of across and down words, sorted by position.
    across_sorted = [across_words[i] for i in range(max_idx+1)]
    down_sorted = [down_words[i] for i in range(max_idx+1)]
    # Check for conflicts between across/down words
    conflicts = 0
    for i in range(len(across_sorted)):
        a_word = across_sorted[i]
        for j in range(len(a_word)):
            d_word = down_sorted[j]
            if (a_word[j] != d_word[i]):
                conflicts = conflicts + 1
    return conflicts

def print_state(state_dict, out_file=' '):
    """Output the given state (an assignment of words to positions)."""
    if (out_file == ' '):
        out_file = sys.stdout
    print >>out_file, "STATE START"
    for (key, val) in state_dict.items():
        print >>out_file, "{0} {1}".format(key, val)
    print >>out_file, "STATE END"
    return

def is_full_state(state_dict, word_list):
    """Check if all across/down positions in this state are associated with
    some word from word_list."""
    word_set = set(word_list)
    full_state = 1
    for (key, value) in state_dict.items():
        if not (value in word_set):
            full_state = 0
    return full_state

def score_state(state_dict, word_list):
    """Check the number of across/down word conflicts are present in the state
    encoded by state_dict. Scoring is only performed for "full states", i.e.
    those in which all across/down positions are mapped to words in word_list.
    """
    if is_full_state(state_dict, word_list):
        return count_conflicts(state_dict)
    else:
        print "{0:s} is not a full state.".format(str(state_dict))
        return -1

# ========= END PROVIDED CODE =========

def 


def random_string():
	size = 3
	chars = string.ascii_lowercase
	return ''.join(random.choice(chars) for x in range(size))

def hill_climbing(A):
	best_val = sys.sizemax
	best_sol = None


	return hill_climbing(best_sol)





def heuristic(conf):
	#The heuristic for this problem is the number of conflicts 



def main():

	copies = 10

	for i in range(copies):
		conf = 

	in_file = sys.argv[1]
	[word_list, start_state] = parse_input_file(in_file)
	print random_string()

if __name__ == "__main__":
	main()


	# A1[1] = D1[1]
	# A1[2] = D2[1]
	# A1[3] = D3[1]
	# A2[1] = D1[2]
	# A2[2] = D2[2]
	# A2[3] = D3[2]
	# A3[1] = D1[3]
	# A3[2] = D2[3]
	# A3[3] = D3[3]