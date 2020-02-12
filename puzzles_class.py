import re
import deformatter

# FUNCTIONS:
# isPuzzle(str) -> bool
# getPoints(str) -> int
# getProper(str) -> str
# getProperDeformatted(str) -> str
# isSolution(str) -> bool
# isPartial(str) -> bool

class Puzzles:

    # input title of puzzle (str), get puzzle id (int)
    puzzle_id_hash = {}
    # input puzzle id (str), get properly formatted puzzle title (int)
    proper_title_by_puzzle = {}
    # input puzzle id (str), get properly formatted puzzle title (int)
    proper_answer_by_puzzle = {}
    # input puzzle id (int), get points assigned to puzzle (int)
    points_per_puzzle = {}
    # input puzzle id (int), get list of acceptable solutions (str list)
    solutions_per_puzzle = {}
    # input puzzle id (int), get list of partial solutions (str list)
    partials_per_puzzle = {}

    def __init__(self, filename):
        tempfile = open(filename, 'r')
        f = tempfile.readlines()
        tempfile.close()

        line_no = 1
        puzzle_id = 1

        for line in f:
            # perhaps remove this conditional in the final version?
            if not (re.search('^\#', line)):
                # print(line, end = '')
                temp = re.search( '\[NAME:\(([^\]]*)\)\]'\
                '\[POINTS:([0-9]*)\]'\
                '\[SOLVE:\(([^\]]*)\)\]'\
                '(\[PARTIAL:\(([^\]]*)\)\])?', line, re.IGNORECASE)

                if temp:
                    # any acceptable titles should point to the same number ID
                    list_of_titles = temp.group(1).split('|')
                    self.proper_title_by_puzzle[puzzle_id] = list_of_titles[0]

                    for title in list(map(deformatter.df_string, list_of_titles)):
                        self.puzzle_id_hash[title] = puzzle_id

                    # assign points to puzzle
                    self.points_per_puzzle[puzzle_id] = int( temp.group(2) )

                    list_of_answers = temp.group(3).split('|')
                    # assign list solutions to puzzle
                    self.proper_answer_by_puzzle[puzzle_id] = list_of_answers[0]

                    self.solutions_per_puzzle[puzzle_id] = \
                        list(map(deformatter.df_string, list_of_answers))

                    # assign partial solutions to puzzle
                    if temp.group(4) is not None:
                        # print(str(puzzle_id), end = '')
                        # print(' has partial')
                        self.partials_per_puzzle[puzzle_id] = \
                            list(map(deformatter.df_string, temp.group(5).split('|')))
                    # if no partial solutions, then add empty list
                    # DOUBLE CHECK IF THIS IS RIGHT
                    else:
                        self.partials_per_puzzle[puzzle_id] = []
                    puzzle_id += 1
                else:
                    print( "puzzles_class.py\tError on savefiles/puzzles.txt line "+str(line_no))
                # print('')
                line_no += 1

    def isPuzzle(self, title):
        dfed = deformatter.df_string(title)
        return dfed in self.puzzle_id_hash

    def getPoints(self, title):
        id = self.puzzle_id_hash[deformatter.df_string(title)]
        return self.points_per_puzzle[id]

    def getProperTitle(self, title):
        id = self.puzzle_id_hash[deformatter.df_string(title)]
        return self.proper_title_by_puzzle[id]

    def getProperAnswer(self, title):
        id = self.puzzle_id_hash[deformatter.df_string(title)]

        return self.proper_answer_by_puzzle[id]

    def getProperDeformatted(self, title):
        temp = self.getProperTitle(title)
        return deformatter.df_string(temp)

    def answerResponse(self, title, answer):
        id = self.puzzle_id_hash[deformatter.df_string(title)]
        dfed_answer = deformatter.df_string(answer)

        if (dfed_answer in self.solutions_per_puzzle[id]):
            return 1
        elif (dfed_answer in self.partials_per_puzzle[id]):
            return 0
        else:
            return -1

    # def isSolution(self, title, answer):
    #     id = self.puzzle_id_hash[deformatter.df_string(title)]
    #     dfed_answer = deformatter.df_string(answer)
    #
    #     return (dfed_answer in self.solutions_per_puzzle[id])
    #
    # def isPartial(self, title, answer):
    #     id = self.puzzle_id_hash[deformatter.df_string(title)]
    #     dfed_answer = deformatter.df_string(answer)
    #
    #     return (dfed_answer in self.partials_per_puzzle[id])

# p = Puzzles('savefiles/puzzles.txt')
# print('Properly Titled Puzzle:\t',end ='')
# print(p.proper_title_by_puzzle)
# print()
# print('Titles:\t',end ='')
# print(p.puzzle_id_hash)
# print()
# print('Points:\t',end ='')
# print(p.points_per_puzzle)
# print()
# print('Solutions:\t',end ='')
# print(p.solutions_per_puzzle)
# print()
# print('Partials:\t',end ='')
# print(p.partials_per_puzzle)
# print()
#
# # for k in p.puzzle_id_hash.keys():
# #     print(k)
# #     print( p.getProperTitle(k) )
#
#
#
# # num = int(input('how many inputs?'))
# num = 1
#
# for x in range(0, num):
#     # puzzle = input('name of puzzle:\t')
#     # answer = input('answer:\t')
#     puzzle = "poetic pathway"
#     answer = "nevermore"
#     if p.isPuzzle(puzzle):
#         print( p.getProperTitle(puzzle) )
#         print( 'worth %d points' % p.getPoints(puzzle))\
#
#         print("puzzle name:\t"+puzzle)
#         print("answer:\t"+answer)
#
#         puzzle = deformatter.df_string(puzzle)
#         answer = deformatter.df_string(answer)
#
#         print( p.puzzle_id_hash[ puzzle ] )
#         print( p.solutions_per_puzzle[p.puzzle_id_hash[ puzzle ] ] )
#         print( answer in p.solutions_per_puzzle[p.puzzle_id_hash[ puzzle ] ] )
#
#
#         response = p.answerResponse( puzzle, answer )
#         if response > 0:
#             print("Correct!")
#         elif response == 0:
#             print("Keep going.")
#         else:
#             print("Incorrect.")
#     else:
#         print("no such puzzle")
#     print()
