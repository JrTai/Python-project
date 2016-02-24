"""
Planner for Yahtzee
Simplifications:  only allow discard and roll, only score against upper level
"""

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

def gen_all_sequences(outcomes, length):
    """
    Iterative function that enumerates the set of all sequences of
    outcomes of given length.
    """
    
    answer_set = set([()])
    for dummy_idx in range(length):
        temp_set = set()
        for partial_sequence in answer_set:
            for item in outcomes:
                new_sequence = list(partial_sequence)
                new_sequence.append(item)
                temp_set.add(tuple(new_sequence))
        answer_set = temp_set
    return answer_set

def score(hand):
    """
    Compute the maximal score for a Yahtzee hand according to the
    upper section of the Yahtzee score card.

    hand: full yahtzee hand

    Returns an integer score 
    """
    
    # NOTE: This code only work with sorted hand value
    score_ls = []
    temp = list(hand)
    score_ls.append(temp[0])
    temp.pop(0)
    count = 0
    for value in temp:
        if score_ls[-1] == value:
            count += 1
            score_ls.insert(0, value)
            score_ls[0] += value * count
        else:
            score_ls.append(value)
            count = 0        
    return max(score_ls)


def expected_value(held_dice, num_die_sides, num_free_dice):
    """
    Compute the expected value based on held_dice given that there
    are num_free_dice to be rolled, each with num_die_sides.

    held_dice: dice that you will hold
    num_die_sides: number of sides on each die
    num_free_dice: number of dice to be rolled

    Returns a floating point expected value
    """
    
    exp_value = 0.
    # produce outcomes for gen_all_sequences function
    out_comes = set([val + 1 for val in range(num_die_sides)])
    all_sequences = gen_all_sequences(out_comes, num_free_dice)
    for sequence in all_sequences:
        dice = list(held_dice + sequence)
        dice.sort()
        dice = tuple(dice)
        exp_value += float(score(dice)) / (len(all_sequences))
    return exp_value

def count_number_each(hand):
    """
    Caculate number of hand, ex (1, 1, 2, 2), return {1: 2, 2: 2}

    Returns a dict of counted hand
    """
    temp_count = {}
    for val in hand:
        if val in temp_count:
            temp_count[val] += 1
        else:
            temp_count[val] = 1
    return temp_count

def gen_all_holds(hand):
    """
    Generate all possible choices of dice from hand to hold.

    hand: full yahtzee hand

    Returns a set of tuples, where each tuple is dice to hold
    """
    # count each number appear how many times
    hand_count = count_number_each(hand)
    difference = len(hand) - len(hand_count.keys())
    if difference != 0:
        bin_num = 2 ** (len(hand)) - 2 ** difference
    else:
        bin_num = 2 ** (len(hand))
    #print hand_count, bin_num, len(hand), len(hand_count.keys()), difference
    
    binary_counts =[bin(x)[2:].rjust(len(hand),'0') for x in range(bin_num)]
    #print binary_counts,
    #print list(hand)
    all_set = set([()])
    for count in binary_counts:
        all_set.add(tuple([list(hand)[dummy_i] for dummy_i in range(len(count))
                           if count[dummy_i] == '1']))
    all_set.add(hand)
    for dummy_num in range(len(hand)):
        hand = list(hand)
        hand.pop(-1)
        #print hand
        all_set.add(tuple(hand))
    
    return all_set

def strategy(hand, num_die_sides):
    """
    Compute the hold that maximizes the expected value when the
    discarded dice are rolled.

    hand: full yahtzee hand
    num_die_sides: number of sides on each die

    Returns a tuple where the first element is the expected score and
    the second element is a tuple of the dice to hold
    """
    hand_subset = gen_all_holds(hand)
    exp_value = 0.
    for subset in hand_subset:
        if expected_value(subset, num_die_sides, len(hand) - len(subset)) > exp_value:
            best_hand = subset
            exp_value = expected_value(subset, num_die_sides, len(hand) - len(subset))
            
    return (exp_value, best_hand)


def run_example():
    """
    Compute the dice to hold and expected score for an example hand
    """
    num_die_sides = 6
    hand = (1, 1, 1, 5, 6)
    hand_score, hold = strategy(hand, num_die_sides)
    print "Best strategy for hand", hand, "is to hold", hold, "with expected score", hand_score
    
    
run_example()
# My Test
#print score((2, 2, 2, 4, 4))
#outcomes = set([value + 1 for value in range(8)])
#print outcomes
#print gen_all_holds((1, 1, 2, 2))


#import poc_holds_testsuite
#poc_holds_testsuite.run_suite(gen_all_holds)
                                       
    
    
    



