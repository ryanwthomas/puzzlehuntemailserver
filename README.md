# Spring 2019 UMD Puzzlehunt Email Server

THIS DOCUMENT IS WIP

Goal:
Puzzle solving teams should be able to send a email and be award points for correct answers. In addition, all email inputs should have appropriate responses. The program should run with little to no human oversight.
Note: Reading through the code may spoil some puzzles of the Spring 2019 Puzzlehunt. The puzzles and their solutions are located here: go.umd.edu/goosechasepuzzles

I've never written in Python before and never write a program to deal with emails before, so this was entirely experiment, but I think it was pretty successful.

General Design:
The program stores data in textfiles and imports them when executed and writes to them when data is receieved. The emails_class.py, teams_class.py, puzzles_class.py, and solves_class.py handle all file IO.


<strong>deformatter.py<\strong>
Description: Many strings need to be compared using only the letters and numbers, ignoring case. Strings are considered "deformatted" if they only contain upper-case letters and numbers. 

Implementation:
deformatter.df_string(input): sets all letters to uppercase and removes any non-alphanumeric characters.


emails_class.py
Description: Tracks a list of emails to use when messaging all hunt participants. Uses a blacklist to not block certain emails from being added to the list, namely the email used by the server, as this would cause an infinite loop of emails.

Implementaion:
savefiles_emails.txt: every line contains a different email address
emails_class.Emails(savefilename): inputs data from the savefile
Emails.addEmail(new_email): adds email if it's new and not on the blacklist.


teams_class.py
Description: Tracks a list of registered teams; returns information about teams.
Teams are tracked only by their deformatted names, e.g. "Super Solvers" is considered the same ".....supers^o%l^v#e@rs!!!!" because they both deformat to "SUPERSOLVERS". Team uniqueness is determined by the deformating strings, but each team also has a formated name.
About Emoji: A quirk of the program is that emoji can't be read from nor included in emails (as this the text settings), but emoji can be included in a textfile, read into a string, and outputted to a textfile. (WRITE THIS LATER)

Implementation:
savefile_teams.txt: every line contains a given team's deformatted name followed by a colon followed by their deformatted name, e.g. "SUPERSOLVERS:Super Solvers!".
teams_class.Teams(savefilename): inputs data from the savefile; any malformed line prints an error message and are ignored
Teams.isTeam(teamname): returns whether the team is registered
Teams.getFormatted(teamname): returns team's formatted name; if team isn't registered or team's name isn't safe to include in emails, returns input
Teams.getFormatted(teamname, saftey): returns team's formatted name even if it isn't safe to include in emails; if team isn't registered, returns input
Teams.addTeam(teamname): if team name is unregistered and contains at least 1 alphanumeric character, the team name is registered and returns true; else, do nothing and return false


puzzles_class.py
Description: Reads and stores information about puzzles.
Each puzzles has several data:
- a primary title, and 0 or more other titles
- the number of points earned when the puzzle is solved
- a primary solution, and 0 or more other acceptable solutions
- 0 or more non-final solutions

Implementation:
savefile_puzzles.txt: every line contains data about a given puzzle. Pieces of data are put inside square brackets, with the type of data written in all caps and colon and then the data. For lists of strings, the list is put inside parathesis with vertical bars seperating the strings. An example line might be "\[NAME:(Star Connections|E)]\[POINTS:20]\[SOLVE:(XXX)]\[PARTIAL:(XXX)]", where the actual solution and partial solution have been replaced with Xs. Puzzles without partial answers shouldn't include a bracket for partial. Note: the order of NAME-POINTS-SOLVE-(PARTIAL) is mandatory.
puzzles_class.Puzzles(savefilename): inputs data from the savefile; any malformed line prints an error message and are ignored.
Puzzles.isPuzzle(title): returns whether input is the title of a puzzle
Puzzles.getPoints(title): returns point value of puzzle; throws error if title doesn't belong to any puzzle
Puzzles.getProperTitle(title): returns primary, formatted value of puzzle; throws error if title doesn't belong to any puzzle
Puzzles.getProperDeformatted(title): returns primary, deformatted value of puzzle; throws error if title doesn't belong to any puzzle
Puzzles.getProperAnswer(title): returns primary solution to puzzle; throws error if title doesn't belong to any puzzle
Puzzles.answerResponse(title, answer): returns a postive number if answer is correct; returns 0 if answer is partially correct; returns a negative number if answer is incorrect; throws error if title doesn't belong to any puzzle


solves_class.py
Description: Tracks which teams and have solved which puzzles and the ranking of teams. When a team solves a puzzle (for the first time) they are awarded points. Teams are ranked by greatest number of points gained in the shortest amount of time. It publishes the scoreboard (which contains team names and their point total ranked from first to last place) and the distribution of puzzle solves (which contains the puzzle title and the number of solves it has) into textfiles.

Implementation:
savefile_solves.txt: every line contains a deformatted team name, a colon, a deformatted puzzle title, then a 9-tuple of ints representing the time a puzzle was solved. E.g. "SUPERSOLVERS:STARCONNECTIONS(2019, 10, 6, 13, 11, 24, 0, 1, -1)".
solves_class.Solves(savefilename, puzzles): Stores puzzles (a puzzles_class.Puzzles object); inputs data from the savefile; any malformed line prints an error message and are ignored. Teams written in the savefile are assumed to be registered. Throws error if puzzle in savefile doesn't exist in Puzzles object.
Solves.isSolved(team, title): returns whether team has solved puzzle with given title; throws error if title doesn't belong to any puzzle
Solves.addSolves(team, title, time): If team and puzzle exist and team hasn't already solved puzzle, records solve and awards team their points, adds to savefile, and return true; else do nothing and return false; throws error if title doesn't belong to any puzzle
Solves.addSolves(team, title, time, writing): If writing is False, doesn't add to savefile (used in constructor)
Solves.getScores(team): returns score of team; returns 0 if team is unregistered
Solves.updateScoreboard(team): (used internally) updates team's position on scoreboard, does not publish
Solves.getScoreboard(teams): generates scoreboard with unsafe foramtted team names from teams
Solves.writeScoreboard(teams): publishes scoreboard and puzzle breakdown
Solves.solvesPerPuzzle(): generates the number of solves per puzzle

Driver (TO BE WRITTEN)

