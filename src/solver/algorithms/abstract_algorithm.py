from abc import ABC, abstractmethod
from typing import List,Union,Deque, Dict
from src.solver.utils import assemble_parsed_content,assemble_one_equation,get_variable_string,get_terminal_string

from src.solver.DataTypes import Assignment, Term, Terminal, Variable, Equation


class AbstractAlgorithm(ABC):
    def __init__(self, terminals: List[Terminal], variables: List[Variable], equation_list:List[Equation]):
        self.terminals = terminals
        self.variables = variables
        self.equation_list=equation_list


    @abstractmethod
    def run(self):
        pass

    def visualize(self,file_path:str):
        pass

    def pretty_print_current_equation(self, left_terms: Union[List[Term], Deque[Term]],
                                      right_terms: Union[List[Term], Deque[Term]],mute=True):

        string_equation = assemble_one_equation(left_terms, right_terms,Assignment())
        string_terminals = get_terminal_string(self.terminals)
        string_variables = get_variable_string(self.variables)
        # print("string_terminals:",string_terminals)
        #print("string_variables:", string_variables)
        if mute==False:
            print("string_equation:", string_equation)
            print("-" * 10)
        return string_equation, string_terminals, string_variables

    def check_equation(self, left_terms: List[Term], right_terms: List[Term],
                       assignment: Assignment = Assignment()) -> bool:
        left_side = self.extract_values_from_terms(left_terms, assignment)
        right_side = self.extract_values_from_terms(right_terms, assignment)

        # todo: this need to be improved
        left_str = "".join(left_side).replace("<EMPTY>", "")
        right_str = "".join(right_side).replace("<EMPTY>", "")
        if left_str == right_str:
            return True
        else:
            return False

    def extract_values_from_terms(self, term_list, assignments):
        value_list = []
        for t in term_list:
            if type(t.value) == Variable:
                terminal_list = assignments.get_assignment(t.value)
                for tt in terminal_list:
                    value_list.append(tt.value)
            else:  # type(t.value) == Terminal
                value_list.append(t.value.value)
        return value_list

