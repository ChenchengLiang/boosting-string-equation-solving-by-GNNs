import random
import string
import os

def main():
    track_1_mixed_folder = "/home/cheli243/Desktop/CodeToGit/string-equation-solver/boosting-string-equation-solving-by-GNNs/Woorpje_benchmarks/01_track_generated/mixed"
    start_idx = 501
    end_idx = 1000
    save_equations(start_idx, end_idx, track_1_mixed_folder, generate_one_track_1_unsat)

    # track_2_folder = "/home/cheli243/Desktop/CodeToGit/string-equation-solver/boosting-string-equation-solving-by-GNNs/Woorpje_benchmarks/02_track_generated"
    # generate_track_2(folder=track_2_folder)



def generate_one_track_2(num_variables=1):


    # Generate variable and terminal sets
    variables = [string.ascii_uppercase[i] for i in range(num_variables)]
    terminals = ["a", "b"]

    # Create a equation with the partten "X_{n}aX_{n}bX_{n-1}bX_{n-2}\cdots bX_{1} = aX_{n}X_{n-1}X_{n-1}bX_{n-2}X_{n-2}b \cdots b X_{1}X_{1}baa"
    left_terms = []
    right_terms = []
    for i,v in enumerate(variables):
        if i==0:
            left_terms.extend([v,"a",v])
            right_terms.extend(["a",v])
        else:
            left_terms.extend(["b",v])
            right_terms.extend([v,v,"b"])
    right_terms.extend(["a", "a"])
    equation_left = "".join(left_terms)
    equation_right = "".join(right_terms)


    # Format the result
    result = f"Variables {{{''.join(variables)}}}\n"
    result += f"Terminals {{{''.join(terminals)}}}\n"
    result += f"Equation: {equation_left} = {equation_right}\n"
    result += "SatGlucose(100)"

    return result

def generate_track_2(num_variables=15,folder=""):
    if not os.path.exists(folder):
        os.makedirs(folder)

    for i in range(1, num_variables+1):
        equation = generate_one_track_2(i)
        filename = os.path.join(folder, f"g_02_track_{i}.eq")
        with open(filename, 'w') as file:
            file.write(equation)



def save_equations(start_index, end_index, folder, equation_generator):
    if not os.path.exists(folder):
        os.makedirs(folder)
    for i in range(start_index, end_index + 1):  # +1 because range is exclusive at the end
        equation = equation_generator()
        filename = os.path.join(folder, f"g_01_track_{i}.eq")
        with open(filename, 'w') as file:
            file.write(equation)


def generate_equation(max_variables=15, max_terminals=10, max_length=300, unsat=False):
    # Choose a number of variables and terminals
    num_variables = random.randint(1, max_variables)
    num_terminals = random.randint(1, max_terminals)

    # Generate variable and terminal sets
    variables = [string.ascii_uppercase[i] for i in range(num_variables)]
    terminals = random.sample(string.ascii_lowercase, num_terminals)

    # Create a random string of the terminals
    random_string = ''.join(random.choice(terminals) for _ in range(max_length))

    # Create a dictionary to store variable replacement values
    var_replacements = {}

    # Replace parts of the string with variables randomly
    for var in variables:
        start_index = random.randint(0, max_length - 1)
        end_index = random.randint(start_index, max_length)
        substring = random_string[start_index:end_index]

        # Replace and store the replacement value
        random_string = random_string.replace(substring, var, 1)
        var_replacements[var] = substring

    # Create the equation string
    equation_left = random_string
    equation_right = equation_left
    for var, value in var_replacements.items():
        equation_right = equation_right.replace(var, value, 1)

    if unsat:
        # Make a single modification to the right side to make the equation UNSAT
        random_index = random.randint(0, len(equation_right) - 1)
        random_character = random.choice(terminals)
        equation_right = equation_right[:random_index] + random_character + equation_right[random_index+1:]


    # Format the result
    result = f"Variables {{{''.join(variables)}}}\n"
    result += f"Terminals {{{''.join(terminals)}}}\n"
    result += f"Equation: {equation_left} = {equation_right}\n"
    result += "SatGlucose(100)"

    return result

def generate_one_track_1():
    return generate_equation(unsat=False)

def generate_one_track_1_unsat():
    return generate_equation(unsat=True)




if __name__ == '__main__':
    main()