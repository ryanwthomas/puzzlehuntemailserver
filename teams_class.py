import re
import deformatter
import basic_send

# FUNCTIONS:
# isTeam(str) -> bool
# getFormatted(str) -> str
# addTeam(str) -> bool

class Teams:
    teamnames = {}

    def __init__(self, filename):
        #self.teamnames = {}
        self.filename = filename
        tempfile = open(filename, 'r')
        f = tempfile.readlines()
        tempfile.close()

        line_no = 1
        for line in f:
            temp = re.search( '([A-Z0-9]+):(.*)$', line, re.IGNORECASE)

            if temp:
                self.teamnames[ temp.group(1) ] = temp.group(2).strip()
            else:
                print( "team_class.py\tError on savefiles/teams.txt line "+str(line_no)+"\n"+line)
            line_no += 1

    def isTeam(self, input):
        df = deformatter.df_string(input)
        return df in self.teamnames

    def getFormatted(self, input, isSafe=True):
        if self.isTeam(input):
            df = deformatter.df_string(input)
            formatted = self.teamnames[df]
            normal = re.search('^[A-Z0-9\\\/\.\^\$\*\+\?\[\]\(\)\|'\
            ',<>{}!@#%&_=`~ :;"]+$', formatted, re.IGNORECASE)

            # if the formatted team name is normal, or you don't about safety, then return formatted teamname
            if normal or not isSafe:
                return formatted
            else:
                return input
        else:
            return input

    def addTeam(self, input):
        # is team already listed?
        df = deformatter.df_string(input)
        if (not self.isTeam(input)) and len(df) > 0:
            # add to team hash
            self.teamnames[df] = input

            # add on to team textfile
            tempfile = open(self.filename, "a+")
            tempfile.write("%s:%s\r\n" % (df, input))
            tempfile.close()

            return True
        else:
            return False

# t = Teams('savefiles/teams.txt')
# print(t.teamnames)

# input_team = input('give team name 1:\t')
# print( t.isTeam( input_team ) )
# if t.isTeam( input_team ):
#     print( t.getFormatted(input_team) )
# else:
#     t.addTeam( input_team )
#
# print(t.teamnames)
# print()
# input_team = input('give team name 2:\t')
# print( t.isTeam( input_team ) )
# if t.isTeam( input_team ):
#     print( t.getFormatted(input_team) )
# else:
#     t.addTeam( input_team )
#
# print(t.teamnames)
#
# t = Teams('savefiles/teams.txt')
# print(t.teamnames)
