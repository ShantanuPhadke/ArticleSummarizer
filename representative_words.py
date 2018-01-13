import sys, re, random

# (1) Produce the appropriate dictionary of words to counts from the inputted 
# reference text file
def process_input(filename):
	word_counts = {}
	joined_words = {} # Dictionary in form (Key = <Individual Word #1>, Value = <Joined Word>)
					  #					   (Key = <Individual Word #2>, Value = <Joined Word>)
	counts_to_words = {} # Dictionary in the form (Key = <Count Associated with Current Word>, Value = <Words with that count>)
	counts = [] # List of counts we will sort and then use to keep track of both the highest and lowest valid frequencies

	file = open(filename, 'r')
	#current_line = re.sub(r'[^a-zA-Z0-9\s]', '', file.readline()).split()

	for current_line in file.readlines():
		current_line = re.sub(r'[^a-zA-Z0-9\s]', ' ', current_line).split()
		#print(current_line)
		index = 0
		while index < len(current_line):
			two_worded_term = False
			if current_line[index].isalpha():
				word = current_line[index].lower()
				if current_line[index][0] >= 'A' and current_line[index][0] <= 'Z':
					if index < len(current_line)-1:
						if current_line[index+1][0] >= 'A' and current_line[index+1][0] <= 'Z':
							if (word in joined_words) == (current_line[index+1].lower() in joined_words):
								word = word + " " + current_line[index+1].lower()
								two_worded_term = True
								if current_line[index].lower() not in joined_words:
									joined_words[current_line[index].lower()] = word
								if current_line[index+1].lower() not in joined_words:
									joined_words[current_line[index+1].lower()] = word
								index+=1
				if word not in word_counts:
					if word in joined_words:
						two_word_term = joined_words[word]
						word_counts[two_word_term] = word_counts[two_word_term]+1
					else:
						word_counts[word] = 1
				else:
					word_counts[word] = word_counts[word] + 1
			index+=1

		#current_line = re.sub(r'[^a-zA-Z0-9\s]', '', file.readline()).split()

	for word in word_counts:
		if word_counts[word] not in counts_to_words:
			counts_to_words[word_counts[word]] = [word]
		else:
			counts_to_words[word_counts[word]].append(word)
		counts.append(word_counts[word])

	for count in counts_to_words:
		if type(counts_to_words[count]) is list:
			counts_to_words[count].sort(key=len, reverse=False)

	counts.sort()

	return (word_counts, counts_to_words, joined_words, counts)

# (2) Repeatedly remove items from the map constructed in (1) until it has in between 3 and 7 elements remaining
def perform_term_extraction(word_tuple, num_high_cycles, num_low_cycles):
	(word_counts, counts_to_words, joined_words, counts) = word_tuple

	while len(counts) > 7:
		for i in range(num_high_cycles):
			if len(counts) > 3:
				highest_frequency = counts.pop(len(counts)-1)
				(word_counts, counts_to_words) = remove_word_with_count(word_counts, counts_to_words, highest_frequency)

		for i in range(num_low_cycles):
			if len(counts) > 3:
				lowest_frequency = counts.pop(0)
				(word_counts, counts_to_words) = remove_word_with_count(word_counts, counts_to_words, lowest_frequency)

	return word_counts


# Helper function for deleting one of the words with the given count 
def remove_word_with_count(word_counts, counts_to_words, current_count):
	possible_removals = counts_to_words[current_count]
	word_removed = None
	if type(possible_removals) is list:
		word_removed = possible_removals.pop(0)
		if len(possible_removals) == 0:
			counts_to_words.pop(current_count, None)
	else:
		word_removed = possible_removals

	word_counts.pop(word_removed)

	return (word_counts, counts_to_words)

# (3) Prints the two components that are needed to be returned from 
def print_map_and_extracted_terms(filename):
	map_scores = {}
	word_tuple = process_input(filename)
	original_word_tuple = process_input(filename)
	print("Constructed Map: " + str(word_tuple[0]))
	print

	for low_cycles in range(1, 10):
		for high_cycles in range(1, low_cycles):
			#word_tuple = process_input(filename)
			word_count_map = perform_term_extraction(process_input(filename), high_cycles, low_cycles)
			#print(str(low_cycles) + ", " + str(high_cycles) + ", " + str(word_count_map))
			current_map_score = sum([(word_count_map[s] + len(s)) * len(s.split()) * 1.0 if len(s) > 5 or len(s.split()) > 1 else (word_count_map[s] * len(s)) * (-1.0/len(s.split())) for s in word_count_map.keys()])
			#current_map_score/=(len(word_count_map)*1.0)
			#current_map_score+=(len(word_count_map)*1.25)
			#print("Current Score Being Processed: " + str(current_map_score))
			#print
			map_scores[current_map_score] = (word_count_map, low_cycles, high_cycles)

	max_score = max(map_scores.keys())

	print("Best Set of Extracted Words: " + str([key for key in map_scores[max_score][0].keys()]))
	print
	print("Best Set of Combinations for High/Low Eliminations: # High Element Eliminations = " + str(map_scores[max_score][2]) + ", # Low Element Eliminations = " + str(map_scores[max_score][1]))
	print
	print

print_map_and_extracted_terms("tax_bill.txt")
print_map_and_extracted_terms("Moodys_India.txt")
print_map_and_extracted_terms("keystone_pipeline.txt")
print_map_and_extracted_terms("lonzo_ball.txt")
print_map_and_extracted_terms("there_will_be_blood.txt")
print_map_and_extracted_terms("ugba105_self_reflection.txt")