# Spring 2019 UMD Puzzlehunt Email Server

Goal:
Create an email server to replace the manual email processing of the previous 2 years' puzzlehunts. Puzzle solving teams should be able to send in emails and be award points for correct answers. In addition, all email inputs should have appropriate responses. The program should run with little to no human oversight.
Note: Reading through the code may spoil some puzzles of the Spring 2019 Puzzlehunt. The puzzles and their solutions are located here: go.umd.edu/goosechasepuzzles

I've never written in Python before and never write a program to deal with emails before, so this was entirely experiment, but I think it was pretty successful.

General Design:
The program stores data in textfiles and imports them when executed and writes to them when data is receieved. The emails_class.py, teams_class.py, puzzles_class.py, and solves_class.py handle all file IO.

deformatter.py
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

h2.Implementation:
savefile_teams.txt: every line contains a given team's deformatted name followed by a colon followed by their deformatted name, e.g. "SUPERSOLVERS:Super Solvers!".
teams_class.Teams(savefilename): inputs data from the savefile; any malformed line prints an error message and are ignored
Teams.isTeam(teamname): returns whether the 

