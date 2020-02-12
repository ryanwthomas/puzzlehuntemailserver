# Fall 2019 UMD Puzzlehunt Email Server

THIS DOCUMENT IS WIP

Goal:
Puzzlehunt: teams send in answer submissions. If the answer is correct, and the puzzle hasn't already solved the puzzle, the team is awarded points. If the answer is incorrect or the email is malformed, no points are awarded. All incoming emails should be responded with an appropriate email.
Puzzle solving teams should be able to send a email and be award points for correct answers. In addition, all email inputs should have appropriate responses. The program should run with little to no human oversight.
Note: Reading through the code may spoil some puzzles of the Fall 2019 Puzzlehunt. The puzzles and their solutions are located here: go.umd.edu/goosechasepuzzles

I've never written in Python before and never write a program to deal with emails before, so this was entirely experiment, but I think it was pretty successful.

General Design:
The program stores data in textfiles and imports them when executed and writes to them when data is receieved. The emails_class.py, teams_class.py, puzzles_class.py, and solves_class.py handle all file IO.


<strong>deformatter.py</strong><br>
Description: Strings are considered "deformatted" if they only contain upper-case letters and numbers. 

Implementation:
deformatter.df_string(input): sets all letters to uppercase and removes any non-alphanumeric characters.

<strong>emails_class.py</strong><br>
Description: Tracks a list of emails to use when messaging all hunt participants. Uses a blacklist to not block certain emails from being added to the list, namely the email used by the server, as this would cause an infinite loop of emails.

Implementaion:
savefiles/emails.txt: every line contains a different email address
emails_class.Emails(savefilename): inputs data from the savefile
Emails.addEmail(new_email): adds email if it's new and not on the blacklist.


<strong>teams_class.py</strong><br>
Description: Tracks a list of registered teams; returns information about teams.
Teams are tracked only by their deformatted names, e.g. "Super Solvers" is considered the same ".....sUpErS^o%L^v#E@rs!!!!" because they both deformat to "SUPERSOLVERS". Team uniqueness is determined by the deformating strings, but each team also has a formated name.
About Emoji: A quirk of the program is that emoji can't be read from nor included in emails (as this the text settings), but emoji can be included in a textfile, read into a string, and outputted to a textfile. Therefore, teamnames which contain emoji must be manually written into the savefile with a non-emoji name to serve as the deformatted name, i.e. the name that will be used in emails. 

Implementation:
savefile_teams.txt: every line contains a given team's deformatted name followed by a colon followed by their deformatted name, e.g. "SUPERSOLVERS:Super Solvers!".
teams_class.Teams(savefilename): inputs data from the savefile; any malformed lines encountered print an error message and are ignored
Teams.isTeam(teamname): returns whether the team is registered
Teams.getFormatted(teamname): returns team's formatted name; if team isn't registered or team's name isn't safe to include in emails, returns input
Teams.getFormatted(teamname, saftey): returns team's formatted name even if it isn't safe to include in emails; if team isn't registered, returns input
Teams.addTeam(teamname): if team name is unregistered and contains at least 1 alphanumeric character, the team name is registered and returns true; else, do nothing and return false


<strong>puzzles_class.py</strong><br>
Description: Reads and stores information about puzzles.
Each puzzles has several data:
- a primary title, and 0 or more other acceptable titles
- the number of points earned when the puzzle is solved
- a primary solution, and 0 or more other acceptable solutions
- 0 or more non-final solutions

Implementation:
<ul>
<li>savefile_puzzles.txt: every line contains data about a given puzzle. Pieces of data are put inside square brackets, with the type of data written in all caps and colon and then the data. For lists of strings, the list is put inside parathesis with vertical bars seperating the strings. An example line might be "\[NAME:(Cold, Hard Cash|F)]\[POINTS:20]\[SOLVE:(SIDEKICK)]\[PARTIAL:(QUICKBROWN|THEQUICKBROWNFOXJUMPSOVERTHELAZYDOG)]". Puzzles without partial answers shouldn't include a bracket for partial. Note: the order of NAME-POINTS-SOLVE-(PARTIAL) is mandatory.</li>
<li>puzzles_class.Puzzles(savefilename): inputs data from the savefile; any malformed lines encountered print an error message and are ignored.</li>
<li>Puzzles.isPuzzle(title): returns whether input is the title of a puzzle</li>
<li>Puzzles.getPoints(title): returns point value of puzzle; throws error if title doesn't belong to any puzzle</li>
<li>Puzzles.getProperTitle(title): returns primary, formatted value of puzzle; throws error if title doesn't belong to any puzzle</li>
<li>Puzzles.getProperDeformatted(title): returns primary, deformatted value of puzzle; throws error if title doesn't belong to any puzzle</li>
<li>Puzzles.getProperAnswer(title): returns primary solution to puzzle; throws error if title doesn't belong to any puzzle</li>
<li>Puzzles.answerResponse(title, answer): returns a postive number if answer is correct; returns 0 if answer is partially correct; returns a negative number if answer is incorrect; throws error if title doesn't belong to any puzzle</li>
</ul><br><br>

<strong>solves_class.py</strong><br>
Description: Tracks which teams and have solved which puzzles and the ranking of teams. When a team submits the correct answer for a puzzle (for the first time), they are awarded points. Teams are ranked by greatest number of points gained in the shortest amount of time. It publishes the scoreboard (which contains team names and their point total ranked from first to last place) and the distribution of puzzle solves (which contains the puzzle title and the number of solves it has) into textfiles in /exports.

Implementation:
<ul>
<li>savefile_solves.txt: every line contains a deformatted team name, a colon, a deformatted puzzle title, then a 9-tuple of ints representing the time a puzzle was solved. E.g. "SUPERSOLVERS:STARCONNECTIONS(2019, 10, 6, 13, 11, 24, 0, 1, -1)".</li>
<li>solves_class.Solves(savefilename, puzzles): Stores puzzles (a puzzles_class.Puzzles object); inputs data from the savefile; any malformed lines encountered print an error message and are ignored. Teams written in the savefile are assumed to be registered. Throws error if puzzle in savefile doesn't exist in Puzzles object.</li>
<li>Solves.isSolved(team, title): returns whether team has solved puzzle with given title; throws error if title doesn't belong to any puzzle</li>
<li>Solves.addSolves(team, title, time): If team and puzzle exist and team hasn't already solved puzzle, records solve and awards team their points, adds to savefile, and return true; else do nothing and return false; throws error if title doesn't belong to any puzzle</li>
<li>Solves.addSolves(team, title, time, writing): If writing is False, doesn't add to savefile (used in constructor)</li>
<li>Solves.getScores(team): returns score of team; returns 0 if team is unregistered</li>
<li>Solves.updateScoreboard(team): (used internally) updates team's position on scoreboard, does not publish</li>
<li>Solves.getScoreboard(teams): generates scoreboard with foramtted team names from teams</li>
<li>Solves.writeScoreboard(teams): publishes scoreboard and puzzle breakdown</li>
<li>Solves.solvesPerPuzzle(): generates the number of solves per puzzle</li>
</ul>
<br>

<strong>Driver (TO BE WRITTEN)</strong><br>
Description: Creates the IMAP connection to read emails. Contains the bulk of the input tree for how incoming emails are handled (in hindsight, this probably should've been split into a different class). Implements safeguards to ensure no infinite looping.

Implemenation:
<ul>
  <li>loops decreases every time inbox is checked</li>
  <li>Iterate over emails:
    <ul>
      <li>if the email's time signature* is past a predetermined time, response with /email_bases/puzzlehuntover.txt</li>
      <li>if email's payload needs to be accessed, iterate through parts of email; if the part is text, add to payload string </li>
      <li>if subject line is "Team Registration", respond with an email base from /email_bases/registration. Either "error_preexisting", "success", "invalidteamname", "error_malformation"</li>
      <li>if subject line is "Answer Submission", respond with an email base from /email_bases/submission. Either "correct(_presolved)", "incorrect(_presolved)", "partial(_presolved)", "error_(unregistered,puzzledne,malformation)". There is a hard coded portion of this code to handle a unique puzzle that was broken into parts but shared a title.</li>
      <li>if subject line is "Ask For Help", forward email's payload to a predetermined email </li>
      <li>if subject line is "Admin Command" and the sender is on the admin list, don't check the inbox anymore, but still finish processing current batch of emails</li>
      <li>else, no subject matches. respond with /email_bases/subject_dne.txt</li>
</ul>
      </li>
  <li>if its predetermined that emails will be deleted or if the program is going to check the inbox again, mark all processed emails as "deleted" and then expunge inbox</li>
  <li>rewrite the score baord a team has earned points</li>
</ul>


\* After the hunt, we noticed an anomally where we  recieved an email whose time signature was 2 hours before all emails read before and after it. I'm not sure what caused this, but the vunerability could allow teams to cheat by giving themselves quicker solve times. Thankfully, only one instance of this annomally occurred, and it didn't affect ranking.

\* the admin command is probably vunerable to actors who put their name as an admin email

Safety was, unfortunately, not a top priority for this program. Because it was quickly developed for a specific problem, only to be run on one device, and our audience are good actors, functionality and timeliness was put before safety.

Result: Overall, quite the success! Compared to our previous system where several people mannually read, scored, and responed to emails for the duration of the hunt, the program worked with ~5% less human work. Perhaps the biggest downside is that there is now an onus on users to learn how to match specific email formatting, whereas before any formatting was acceptable. Thankfully most users adapted quickly to the formatting, thought not all did.
For a majority of the hunt, no one had to monitor emails. A few times I was called to check on the program (once when the loops ended for the first time; once when someone was having trouble sending in emails). The biggest program came less than an hour before the hunted end when Google notified us that we'd reached the maximum numbers of emails that could be sent in one day. For the rest of the hunt, I read and responded to emails from a different account. Thankfully, I didn't need to score emails, as the program could still read and score emails fine. As a patch, I could've had emails send from a different account than the one I was reading from, but I didn't want to mess too much with code live, so I decided to go with the safer option of handling input manually.
I presumably should have used an XML or CSV file for storing data, but I knew I could get textfiles to work, even if it's a hassle to import and export them, and it's inefficient.

Thank you for reading!


