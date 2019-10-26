# Spring 2019 UMD Puzzlehunt Email Server

Goal:
Create an email server to replace the manual email processing of the previous 2 years' puzzlehunts. Puzzle solving teams should be able to send in emails and be award points for correct answers. In addition, all email inputs should have appropriate responses. The program should run with little to no human oversight.
Note: Reading through the code may spoil some puzzles of the Spring 2019 Puzzlehunt. The puzzles and their solutions are located here: go.umd.edu/goosechasepuzzles

I've never written in Python before and never write a program to deal with emails before, so this was entirely experiment, but I think it was pretty successful.

General Design:
The program stores data in textfiles and imports them when executed and writes to them when data is receieved. The emails_class, teams_class, puzzles_class, and solves_class handle all file IO.

emails_class
Description: Tracks a list of emails to use when messaging all hunt participants. Uses a blacklist to not block certain emails from being added to the list, namely the email used by the server, as this would cause an infinite loop of emails.

Implementaion:
savefiles_emails.txt: every line contains a different email address
emails_class.Emails(savefilename): reads from the savefile
Emails.addEmail(new_email): adds email if it's new and not on the blacklist.

teams_class
Description: Tracks a list of registered teams; returns information about teams.
Teams have 2 "names", so to speak. They have deformatted names (more on that later) and formatted names. The deformatted name is used to as the key to find the formatted name. This is done to accommodate teamnames which have special formatting, namely emoji. A quirk of the program is that emoji can't be read from nor included in emails (as this the text settings), but emoji can be included in a textfile, read into a string, and outputted to a textfile. Teams with emoji in their names, i.e. formatted names, also have a non-emoji name which functions as their deformatted.

Implementation:
savefile_teams.txt: every line contains a given team's deformatted name followed by a colon followed by their deformatted name, e.g. "HEARTEYES:😍".
teams_class.Teams(savefilename):
Creates object Teams which upon instantiation inputs list of teams from savefile. Each team has a defortmatted name (more on that later) and a formatted name.


