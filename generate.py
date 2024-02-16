import sys

from crossword import *
from copy import deepcopy


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        #initially, contaisn all possible words
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    """def save(self, assignment, filename):
        
        #Save crossword assignment to an image file.
        
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)"""

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        #enforce unary constraints
        self.enforce_node_consistency()
        #enforce binary constraints
        self.ac3()
        #try to calculate solution
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        #iterate over variables of crossword
        
        """for var in self.domains:
            len_var = var.length

            for value in self.domains[var]:
                if len(value) != len_var:
                    self.domains[var].remove(value) """
        
        for variable in self.domains:
            len_var = variable.length
            to_remove = set()

            # Iterate through all values in the variable's domain
            for val in self.domains[variable]:
                # If value length does not match variable length, add to values to remove
                if len(val) != len_var:
                    to_remove.add(val)

            # Remove all invalide vals from variable domain
            self.domains[variable] = self.domains[variable] - to_remove

    def check_overlap(self, val_x, val_y,x , y):
        """
        Returns True if overlap is acr consistent, False otherwise
        """
        
        #case: there is no overlap at all
        if not self.crossword.overlaps[x, y]:
            return True
        #case: there is overlap
        else:
            #get index for x and y
            ix, iy  = self.crossword.overlaps[x, y]

            #check if is consistent (must be equal)
            if val_x[ix] == val_y[iy]:
                return True
            else:
                return False
    
    def revise(self, x, y)->bool:
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        revision = False
        remove_from_domain = set()

        for x_value in self.domains[x]:
            consistency = False
            for y_value in self.domains[y]:
                if x_value != y_value and self.check_overlap(x_value, y_value, x, y):
                    consistency = True
                    break

            if not consistency:
                remove_from_domain.add(x_value)
                revision = True

        self.domains[x] = self.domains[x] - remove_from_domain
        return revision

        """
        #status of revision variable
        revision = False

        #iterate over domains of x,y
        for x_value in self.domains[x]:
            for y_value in self.domains[y]:
                if not self.check_overlap(x_value,  y_value, x, y) or x_value == y_value:
                    #if it is inconsistent, a revision was mde
                    self.domains[x].remove(x_value)
                    revision = True

        return revision"""


    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        #build queue if none is passed to function
        if arcs == None:
            arcs = []
            for v1 in self.domains:
                for v2 in self.domains:
                    if v1 != v2:
                        arcs.append((v1, v2))

        # iterate until arc consistency ensured or not solution is pssible
        while arcs:
            #deque 1 arc
            variable_x, variable_y = arcs.pop()

            #case: revision on current arc (with variables x and y) return True
            if self.revise(variable_x, variable_y):
                #case: x´s domain is empty (no solution)
                if not self.domains[variable_x]:
                    return False
                #add back "innocent" arcs that might have been affected by revision
                for variable_w in self.crossword.neighbors(variable_x) - {variable_y}:
                    arcs.append((variable_w, variable_x)) 
        return True


    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        #if any variable is not part of the assingment, return false
        for variable in self.domains:
            if variable not in assignment:
                return False
        
        return True

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        #variable to store consistency status

        #list of already checked variables
        visited_variables = []

        #iterate over assingment
        for variable in assignment:
            var_value = assignment[variable]

            #check repeated variables
            if var_value in visited_variables:
                return False
            visited_variables.append(var_value)

            #check length
            if len(var_value) != variable.length:
                return False 
            
            #check neigjbors
            for neighbor in self.crossword.neighbors(variable):
                if neighbor in assignment:
                    #get value of neighbor
                    neighbor_val = assignment[neighbor]

                    #check constraints
                    if not self.check_overlap(var_value, neighbor_val, variable, neighbor):
                        return False
        #if no constraints violations found, return True 
        return True
        

    ############ IMPLEMENT FULLY ################
    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        
        #########CHANGE THIS ###############
        return [x for x in self.domains[var]]

    ############ IMPLEMENT FULLY ################
    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        
        #########CHANGE THIS ###############
        non_assigned = set(self.domains.keys()) - set(assignment.keys())
        return [var for var in non_assigned][0]

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """

        #check for goal state
        if self.assignment_complete(assignment):
            return assignment
        
        #select next variable to assing
        variable = self.select_unassigned_variable(assignment)
        
        #keep copy of domains pre assingmt in case backtracking is needed
        domain_pre_assingment =  deepcopy(self.domains)

        #iterave over variable domain 
        for value in self.order_domain_values(variable,assignment):
            #current value to test
            assignment[variable] = value

            #check consistency
            if self.consistent(assignment):
                #if is consistent, update domain of variable
                self.domains[variable] = {value}

                #remove values that are inconsistent from neighbors
                self.ac3([(neihgbor, variable) for neihgbor in self.crossword.neighbors(variable)])
                #recursive call to backtrack functin
                result = self.backtrack(assignment)

                #if assingment found, return it
                if result:
                    return result
                
            #if current tested assingment does not provide a solution, backtrack
            del assignment[variable]
            self.domains = domain_pre_assingment

        #if no solution found, reutrn None
        return None

def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
