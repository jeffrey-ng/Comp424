import sys
import random
import time

def parse_input_file(f_name):
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

def random_state(state_dict, word_list):
    """Generate a random mapping of across/down positions to the words in
    word_list, given the board structure implied by state_dict."""
    max_idx = len(word_list) - 1
    for key in state_dict.keys():
        state_dict[key] = word_list[random.randint(0,max_idx)]
    return state_dict

def print_state(state_dict, out_file=' '):
    """Output the given state (an assignment of words to positions)."""
    if (out_file == ' '):
        out_file = sys.stdout
    print >>out_file, "STATE START"
    for (key, val) in state_dict.items():
        print >>out_file, "{0} {1}".format(key, val)
    print >>out_file, "STATE END"
    return

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
                # print a_word + ' + ' + d_word

    return conflicts

def is_full_state(state_dict, word_list):
    """Check if all across/down positions in this state are associated with
    some word from word_list."""
    word_set = set(word_list)
    full_state = 1
    for (key, value) in state_dict.items():
        if not (value in word_set):
            full_state = 0
    return full_state

def is_valid_state(start_state, proposed_state):
    """Check that the set of across/down locations described by start_state are
    all present in proposed_state."""
    valid_state = 1
    for key in start_state.keys():
        if not proposed_state.has_key(key):
            print "key: {0:s} is missing from dict {1:s}".format(str(key),str(proposed_state))
            valid_state = 0
    return valid_state

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

def check_solution(input_file, output_file):
    """This is function will be used in grading your submitted code. If you
    pass the names of the input file used to define a problem instance and the
    name of the output file produced by your code as arguments to this, the
    returned result and displayed output will let you know if your program
    produced an acceptable output from the given input. Note that the first
    state recorded in output_file should be equivalent to the initial state
    encoded in input_file. If this condition does not hold, you will receive
    no credit."""
    [word_list, start_state] = parse_input_file(input_file)
    output_states = parse_state_file(output_file)
    # First, check for equivalence of start_state and first output state.
    for (key, value) in start_state.items():
        if not output_states[0].has_key(key):
            print "Mismatched start state in {0} and first state in {1}.".format(input_file, output_file)
        else:
            if not (output_states[0][key] == value):
                print "Mismatched start state in {0} and first state in {1}.".format(input_file, output_file)
    # Check values of all valid states in output_file
    out_state_vals = [score_state(s, word_list) for s in output_states]
    out_state_vals = [val for val in out_state_vals if (val >= 0)]
    min_val = min(out_state_vals)
    start_val = score_state(start_state, word_list)
    print "Found {0:d} conflicts in start state from {1:s}.".format(start_val, input_file)
    print "Found {0:d} conflicts in best state from {1:s}.".format(min_val, output_file)
    return {'start_val': start_val, 'min_val': min_val}

################
# Instructions #
#--------------#################################################################
# This file can be run from the command line in either of two modes.           #
#                                                                              #
# To run a simple demo, which reads from "input_file" and writes a set of      #
# states (in the format which the grading script can understand) to            #
# "output_file", type: "python this_file 1 input_file output_file".            #
#                                                                              #
# To run a demo of the grading process, which also serves to verify that the   #
# output of your code will be parseable by the grading script, given the       #
# file input_file which was input to your code and the file output_file which  #
# was output by your code, type: "python this_file 2 input_file output_file".  #
#                                                                              #
# Note: Basically, you want the "score" associated your input/output file pair #
#       to be as _large_ as possible, corresponding to a greater reduction in  #
#       conflicts from the start state in input_file to the least conflicted   #
#       state described in output_file.                                        #
#                                                                              #
# Note: For students coding in java, your code should be executable as         #
#       follows: "java csp_solver.java input_file output_file", where          #
#       input_file will be in the same format as the example input that was    #
#       disseminated alongside this file, and output_file is such that running #
#       the current file in "grading" mode (i.e. mode 2) gives a reasonable    #
#       result. If your executable java file is not named csp_solver.java,     #
#       you will receive no credit.                                            #
################################################################################

def hill_climbing(start_state, word_list, out_file):
    #Save best hill climbing
    #Run until current best and next are same = local maximum.
    #Output the maximum since hill climbing doesn't know if local maximum or global.

    best_val = sys.maxsize
    
    best_state = start_state.copy()
    current_state = start_state.copy()
    current_val = sys.maxsize
    next_state = None

    # iterations = 0
    while True:
        # iterations = iterations + 1
        next_state = next_solution(current_state.copy(), word_list)
        #print 'Iteration: ' + repr(iterations)
        # print_state(current_state, out_file)
        next_val = score_state(next_state, word_list)
        # print repr(next_val)
        if current_state == next_state:
            #Local maximum
            # print current_state
            # print next_state
            best_state = current_state
            best_val = current_val
            # return [best_state, best_val]
            return best_state

        if current_val >= next_val:
            current_val =  next_val
            current_state = next_state.copy()

    


def next_solution(state_dict, word_list):
    #Parse through Each of variables (a1,a2...) 
    #compare each one with one of the 40 words given. 
    #save best one locally
    #Do this for each of the 6 variables and return the state.
    for key in state_dict.keys():
        best_word = state_dict[key]
        current_score = score_state(state_dict, word_list)

        current_state = state_dict.copy()
        random.shuffle((word_list))
        for current_word in word_list:
            current_state[key] = current_word
            if is_full_state(current_state, word_list):
                new_score = score_state(current_state, word_list)

                if new_score <= current_score:
                    # print 'new best word' + best_word
                    current_score = new_score
                    best_word = current_word

        state_dict[key] = best_word
        # print best_word

    return state_dict


if __name__=="__main__":
    if (len(sys.argv) != 3):
        print "usage: python {0} input_file output_file".format(sys.argv[0])
        sys.exit(0)
    else:
        in_file = sys.argv[1]
        out_file_name = sys.argv[2]
        print "Parsing input file: {0}".format(in_file)
        [word_list, start_state] = parse_input_file(in_file)
        out_file = open(out_file_name, 'w')

        #You can change this value.
        copies = 100
        # print "Printing {0} copies of start state to {1}.".format(copies, str(out_file))
        print_state(start_state, out_file)
        # for i in range(copies):
        #     print_state(random_state(start_state,word_list), out_file)

        # Load bar stuff
        bar_length = 20
        for i in xrange(0, copies):

            print_state(hill_climbing(start_state,word_list,out_file), out_file)
            
            percent = float(i) / copies
            hashes = '#' * int(round(percent * bar_length))
            spaces = ' ' * (bar_length - len(hashes))
            sys.stdout.write("\rPercent: [{0}] {1}%".format(hashes + spaces, int(round(percent * 100))))
            sys.stdout.flush()


        out_file.close()
        print "\nParsing states described by {0}.".format(out_file_name)
        state_dicts = parse_state_file(out_file_name)
        print "{0:s} described {1:d} states.".format(out_file_name, len(state_dicts))


