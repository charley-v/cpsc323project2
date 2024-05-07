grammar = [
    ('E', ['E', '+', 'T']),
    ('E', ['T']),
    ('T', ['T', '*', 'F']),
    ('T', ['F']),
    ('F', ['(', 'E', ')']),
    ('F', ['id'])
]

parsing_table = {
    (0, 'id'): 's5',
    (0, '('): 's4',
    (0, 'E'): '1',
    (0, 'T'): '2',
    (0, 'F'): '3',


    (1, '+'): 's6',
    (1, '$'): 'acc',

    (2, '+'): 'r2',
    (2, '*'): 's7',
    (2, ')'): 'r2',
    (2, '$'): 'r2',

    #State 3
    (3, '+'): 'r4',
    (3, '*'): 'r4',
    (3, ')'): 'r4',
    (3, '$'): 'r4',


    #State 4
    (4, 'id'): 's5',
    (4, '('): 's4',
    (4, 'E'): '8',
    (4, 'T'): '2',
    (4, 'F'): '3',

    #State 5
    (5, '+'): 'r6',
    (5, '*'): 's7',
    (5, '$'): 'r3',
    (5, ')'): 'r3',

    #State 6
    (6, 'id'): 's5',
    (6, '('): 's4',
    (6, 'T'): '9',
    (6, 'F'): '3',

    #State 7
    (7, 'id'): 's5',
    (7, '('): 's4',
    (7, 'F'):  '10',

    #State 8 
    (8, '+'): 's6',
    (8, ')'): 's11',

    #State 9
    (9, '+'): 'r1',
    (9, '*'): 's7',
    (9, ')'): 'r1',
    (9, '$'): 'r1',

    #State 10
    (10, '+'): 'r3',
    (10, '*'): 'r3',
    (10, ')'): 'r3',
    (10, '$'): 'r3',

    #State 11
    (11, '+'): 'r5',
    (11, '*'): 'r5',
    (11, ')'): 'r5',
    (11, '$'): 'r5'
}


class trace_string:
    def __init__(self, parsing_table, grammar):
        self.parsing_table = parsing_table
        self.grammar = grammar

    def tracer(self, input_string):
        stack = [0] #initial state
        input_string += '$' 
        pointer = 0
        step = 0 

        print("{:<6} {:<15} {:<15} {:<15}".format("Step", "Stack", "Input", "Action"))
        print("-" * 60)
        print("{:<6} {:<15} {:<15} {:<15}".format(step, ''.join(map(str, stack)), input_string[pointer:], ""))
        step+=1
        while True:
            state = stack[-1]
            symbol = input_string[pointer]

            if pointer < len(input_string) - 1:
                next_symbol = input_string[pointer + 1]
                combined_symbol = symbol + next_symbol
                if (state, combined_symbol) in self.parsing_table:
                    symbol = combined_symbol
                    pointer += 1

            action = self.parsing_table.get((state, symbol))

            if action is None:
                print("Error: No action for state {} and symbol {}".format(state, symbol))
                print("-" * 15 + "INPUT NOT ACCEPTED!" + "-" * 15 )
                return False

            if action == 'acc':
                print("{:<6} {:<15} {:<15} {:<15}".format("Accept", ''.join(map(str, stack)), input_string[pointer:], ""))
                print("-" * 15 + "INPUT ACCEPTED!" + "-" * 15 )
                return True
            elif action.startswith('s'):
                stack.append(symbol)
                stack.append(int(action[1:]))
                pointer += 1
                print("{:<6} {:<15} {:<15} {:<15}".format(step, ''.join(map(str, stack)), input_string[pointer:], "Shift (to state {})".format(action[1:])))
                step += 1
            elif action.startswith('r'):
                production_index = int(action[1:])
                production = self.grammar[production_index - 1]
                for _ in range(len(production[1])):
                    stack.pop()
                    stack.pop()  # Remove corresponding states
                state = stack[-1]  # Get the current state after popping
                non_terminal = production[0]
                new_state = self.parsing_table.get((state, non_terminal))  # Get the new state
                if new_state is None:
                    print("Error: No action for state {} and symbol {}".format(state, non_terminal))
                    print("-" * 15 + "INPUT NOT ACCEPTED!" + "-" * 15 )
                    return False
                stack.append(non_terminal)
                stack.append(int(new_state))
                print("{:<6} {:<15} {:<15} {:<15}".format(step, ''.join(map(str, stack)), input_string[pointer:], "Reduce (by {})".format(production[0])))
                step += 1
            else:
                print("Invalid action: {}".format(action))
                return False


print("Valid entries: ['id', '+', '*', ')', '(']")
input_string = input("Enter a string: ")
lr_parser = trace_string(parsing_table, grammar)
lr_parser.tracer(input_string)
