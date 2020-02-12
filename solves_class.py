import re
import deformatter, puzzles_class, teams_class
import calendar
import functools
import itertools

# FUNCTIONS:
# isSolved(str, str) -> bool
# addSolve(str, str) -> bool
# getScore(str) -> int
# getScoreboard(str) -> str

class Solves:

    scoreboard_textfile = "exports/scoreboard.txt"
    puzzle_breakdown_textfile = "exports/puzzle_breakdown.txt"

    # timer = 0
    # input team name (str), get puzzles solved (str list)
    solves_by_team = {}
    # input team name (str), get the most recent solvetime (int)
    solvetime_by_team = {}
    # input team name (str), get the team's score (int)
    score_by_team = {}
    # input team name (str), get the number of solves (int)
    solves_by_puzzle = {}
    filename = ""

    scoreboard = []

    def __init__(self, filename, puzzles):
        self.puzzles = puzzles
        self.filename = filename

        for p in puzzles.proper_title_by_puzzle:
            p = puzzles.proper_title_by_puzzle[p]
            p = deformatter.df_string(p)
            self.solves_by_puzzle[p] = 0

        # print( self.solves_by_puzzle )

        tempfile = open(filename, 'r')
        f = tempfile.readlines()
        tempfile.close()

        line_no = 1
        puzzle_id = 1

        for line in f:
            # print(line, end = '')
            temp = re.search( '([A-Z0-9]+):'\
            '([A-Z0-9]+)'\
            '\((-?[0-9]+(, -?[0-9]+){8})\)', line, re.IGNORECASE)

            if temp:
                # any acceptable titles should point to the same number ID
                # we will trust any teamname that exist in the savefile
                teamname = temp.group(1)
                puzzle = temp.group(2)
                time = temp.group(3).split(', ')

                time = tuple(map(int, time))

                self.solvetime_by_team[teamname] = time

                result = self.addSolve( teamname, puzzle, time, False )
            else:
                print( "solves_class.property\tError on savefiles/puzzles.txt line "+str(line_no))
            # print('')
            line_no += 1

    def isSolved(self, teamname, puzzle):
        teamname = deformatter.df_string( teamname )
        puzzle = self.puzzles.getProperDeformatted( puzzle )

        return (teamname in self.solves_by_team) \
        and (puzzle in self.solves_by_team[teamname])

    def addSolve(self, teamname, puzzle, time, write_to_file = True):
        teamname = deformatter.df_string( teamname )
        puzzle = self.puzzles.getProperDeformatted(puzzle)

        # if not previously solved
        if not self.isSolved(teamname, puzzle) and self.puzzles.isPuzzle(puzzle):
            # if team is not on the board
            if (teamname not in self.solves_by_team):
                self.solves_by_team[teamname] = []
                self.solvetime_by_team[teamname] = tuple((0,0,0,0,0,0,0,0,0))
                self.score_by_team[teamname] = 0

            # print( ">>>"+teamname+"<<<" )
            self.solves_by_team[teamname].append(puzzle)

            # print( time )
            # print (time.__class__.__name__)
            # print( self.solvetime_by_team[teamname] )

            if time > self.solvetime_by_team[teamname]:
                self.solvetime_by_team[teamname] = time

            self.score_by_team[teamname] += self.puzzles.getPoints(puzzle)
            self.solves_by_puzzle[puzzle] += 1

            # print( "}"+teamname+"{" )
            self.updateScoreboard(teamname)

            # add on to team textfile
            if write_to_file:
                tempfile = open(self.filename, "a+")
                tempfile.write("\r\n%s:%s%s" % (teamname, puzzle, str(time)))
                tempfile.close()

            # update timer
            # self.timer = max(self.timer, time+1)
            return True
        return False

    # def addSolveNoTime(self, teamname, puzzle):
    #     temp = self.timer
    #     return self.addSolve(teamname, puzzle, temp)

    def getScore(self, teamname):
        teamname = deformatter.df_string(teamname)
        if teamname in self.solves_by_team:
            score = 0
            # set funciton removes duplicates, though I think duplicate will never get added
            for puzzle in set(self.solves_by_team[teamname]):
                score += self.puzzles.getPoints(puzzle)
            return score
        else:
            return 0

    def updateScoreboard(self, team):
        team = deformatter.df_string(team)
        # if team is in scoreboard, then delete team from scoreboard
        if( team in [x[2] for x in self.scoreboard] ):
            self.scoreboard =  [x for x in self.scoreboard if team not in x ]

        # find first team with
        solvetime = self.solvetime_by_team[ team ]
        score = self.score_by_team[ team ]

        index = 0
        ## THIS IS WHERE I STOPPED WORKING
        ## GETTING A LIST INDEX OUT OF RANGE ERROR
        while index < len(self.scoreboard) and (\
        self.scoreboard[index][0] > score or \
        (self.scoreboard[index][0] == score and \
        self.scoreboard[index][1] < solvetime)):
            index += 1

        self.scoreboard.insert(index, (score, solvetime, team))

    # getScoreboard(str) -> str
    def getScoreboard(self, teams):
        temp_display = [teams.getFormatted(x[2], False)+"\t"+str(x[0]) for x in self.scoreboard]

        temp_display = functools.reduce((lambda x, y: x+"\n"+y), temp_display, "" )

        return temp_display

    def writeScoreboard(self, teams):
        lines = self.getScoreboard(teams)

        tempfile = open(self.scoreboard_textfile, "w+")

        # write to scoreboard
        for f in lines:
            tempfile.write("%s" % (f))
        tempfile.close()

        # write f
        tempfile2 = open(self.puzzle_breakdown_textfile, "w+")

        for key in self.solves_by_puzzle:
            if key != "INTRODUCTION":
                tempfile2.write("%s\t%s\r\n" % (self.puzzles.getProperTitle(key), self.solves_by_puzzle[key]))

        tempfile2.close()

        # # add all teams into list
        # for team in self.solves_by_team:
        #     list.append(team)
        #
        # # selection sort by time
        # temp_list = list
        # list = []
        # while temp_list:
        #     index = 0
        #
        #     # find earliest solvetime
        #     for x in range(1, len(temp_list)-1):
        #         if( self.solvetime_by_team[ temp_list[index] ] > \
        #         self.solvetime_by_team[ temp_list[x] ] ):
        #             index = x
        #
        #     # add indexth ele to temp_list then remove it from list
        #     list.append( temp_list[index] )
        #     del temp_list[index]
        #
        # # insertion sort by score
        # temp_list = list
        # list = []
        #
        # while temp_list:
        #     index = 0
        #
        #     # find earliest solvetime
        #     for x in range(1, len(temp_list)):
        #         if( self.score_by_team[ temp_list[index] ] < \
        #         self.score_by_team[ temp_list[x] ] ):
        #             index = x
        #
        #     # add indexth ele to temp_list then remove it from list
        #     list.append( temp_list[index] )
        #     del temp_list[index]
        #
        # toReturn = ""
        # for team in list:
        #     toReturn += '%s\t%d\r\n' % (teams.getFormatted(team, False),self.score_by_team[team])
        #
        # return toReturn

    # getScoreboard(str) -> str
    def solvesPerPuzzle(self):
        toReturn = ""
        for p in self.solves_by_puzzle:
            toReturn += '%s\t%d\r\n'% (self.puzzles.getProper(p), self.solves_by_puzzle[p])

        return toReturn

# p = puzzles_class.Puzzles('savefiles/puzzles.txt')
# s = Solves( 'savefiles/solves.txt', p )
# print()
# print( s.solves_by_team )
# print()
# print( s.solvetime_by_team )
# print()
#
# t = teams_class.Teams('savefiles/teams.txt')
#
# print( s.getScoreboard(t) )
# # s.addSolve("PuzzlesRFun", "Code of Arms", (2019, 10, 4, 22, 22, 0, 0, 0, 0))
# # s.addSolve("PuzzlesRFun", "Star Connections", (2019, 10, 4, 22, 22, 0, 0, 0, 0))
# # s.addSolve("PuzzlesRFun", "Code of Arm", (2019, 10, 4, 22, 22, 0, 0, 0, 0))
# # s.addSolve("I Love Danny", "Wig Flew", (2019, 10, 5, 1, 15, 0, 0, 0, 0))
# # s.addSolve("I Love Danny", "Everything has changed", (2019, 10, 5, 1, 17, 0, 0, 0, 0))
# # s.addSolve("I Love Danny", "Meta", (2019, 10, 5, 1, 17, 0, 0, 0, 0))
# # s.addSolve("My Coolteamname", "Smokey Signs", (2019, 10, 5, 2, 0, 0, 0, 0, 0))
#
# print()
# print( s.solvetime_by_team )
# print()
# print( s.getScoreboard(t) )


# for team in s.solves_by_team:
#     score = s.getScore(team)
#     print('%s\t%d' % (team, score))
#
# t = teams_class.Teams('savefiles/teams.txt')
# print( t.teamnames )
# print()
# print( '>%s< ' % s.getScoreboard(t) )
#
# tempfile = open('exports/scoreboard.txt', "w+")
# tempfile.write(s.getScoreboard(t))
# tempfile.close()
#
# print()
# print( '>%s< ' % s.solvesPerPuzzle() )
# tempfile = open('exports/solvesperpuzzle.txt', "w+")
# tempfile.write(s.solvesPerPuzzle())
# tempfile.close()
