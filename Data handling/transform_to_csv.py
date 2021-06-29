destination_file = open("dialogue_docpat.csv", "w")

# Adding the column headers of the csv file
destination_file.write("S.no,conv_id,speaker,turn_num,utterance_id,utterance")
destination_file.write("\n")

# Declare all the required variable
sno = 0
conv_id = 0
turn_num = 0
utterance = []
check_id = "id="
next_line = "\n"
check_doc = "Doctor:"
check_pat = "Patient:"

no_of_dialogues = 0

no_of_utterances = 0
max_utterances = 0
min_utterances = 10000
avg_utterances = float(0)
count = 0

no_of_tokens = 0
max_tokens = 0
min_tokens = 10000
avg_tokens = float(0)

with open("Dialogue.txt", "rt") as origin_file:
    for line in origin_file.readlines():

        # Checking if the line starts with id
        if line.find(check_id) != -1:
            conv_id += 1
            no_of_dialogues += 1
            turn_num = 1

            # count cannot of 0 as in a dialogue there are at least 2 utterances
            if count != 0:
                max_utterances = max(max_utterances, count)
                min_utterances = min(min_utterances, count)
                count = 0
            pass

        # Checking if the line starts with new line ('\n')
        elif line == next_line:
            pass

        else:
            # Storing the string containing line as a list
            utterance = line.split()
            '''print(conv_id, utterance)
            print(line)'''
            # If the first element of the string is Patient:
            if utterance[0] == check_pat:
                sno += 1
                no_of_utterances += 1
                count += 1
                utterance.pop(0)

                # Calculating the no of token in doctor utterances as well calculating the min and the max tokens
                no_of_tokens += len(utterance)
                min_tokens = min(len(utterance), min_tokens)
                max_tokens = max(len(utterance), max_tokens)

                utterance_string = " ".join(utterance)
                utterance_string = '"' + utterance_string + '"'
                destination_file.write(
                    str(sno) + ',' + str(conv_id) + ', Patient ,' + str(turn_num) + ',' + str(conv_id) + '_' + str(
                        count) + ',' + utterance_string)
                destination_file.write("\n")


            # If the first element of the string is Doctor:
            else:
                sno += 1
                no_of_utterances += 1
                count += 1

                utterance.pop(0)

                # Calculating the no of token in doctor utterances as well calculating the min and the max tokens
                no_of_tokens += len(utterance)
                min_tokens = min(len(utterance), min_tokens)
                max_tokens = max(len(utterance), max_tokens)

                utterance_string = " ".join(utterance)
                utterance_string = '"' + utterance_string + '"'
                destination_file.write(
                    str(sno) + ',' + str(conv_id) + ', Doctor ,' + str(turn_num) + ',' + str(conv_id) + '_' + str(
                        count) + ',' + utterance_string)
                destination_file.write("\n")
                turn_num += 1


# Calculating the average utterances and tokens
avg_utterances = float(no_of_utterances / no_of_dialogues)
avg_tokens = float(no_of_tokens / no_of_utterances)

destination_file.write(',' + 'Number of dialogues: ' + str(no_of_dialogues))
destination_file.write('\n')
destination_file.write(',' + 'Number of utterance: ' + str(no_of_utterances))
destination_file.write('\n')
destination_file.write(',' + 'Number of tokens: ' + str(no_of_tokens))
destination_file.write('\n')

destination_file.write(',' + 'Average number of utterances in an dialogue: ' + str(round(avg_utterances, 2)))
destination_file.write('\n')
destination_file.write(',' + 'Max number of utterances in an dialogue: ' + str(max_utterances))
destination_file.write('\n')
destination_file.write(',' + 'Min number of utterances in an dialogue: ' + str(min_utterances))
destination_file.write('\n')

destination_file.write(',' + 'Average number of tokens in an utterance: ' + str(round(avg_tokens, 2)))
destination_file.write('\n')
destination_file.write(',' + 'Max number of tokens in an utterance: ' + str(max_tokens))
destination_file.write('\n')
destination_file.write(',' + 'Min number of tokens in an utterance: ' + str(min_tokens))
destination_file.write('\n')

origin_file.close()
destination_file.close()
