import teams_class, puzzles_class, solves_class, emails_class
import basic_send, deformatter
import email, email.utils
import imaplib
import re
import os
import locale
import time
import itertools

# email types subject lines
team_registration = "Puzzlehunt Team Registration"
answer_submission = "Puzzlehunt Answer Submission"
ask_for_help = "Ask For Help"
admin_command = "Admin Command"

# enforce deformatting
team_registration = deformatter.df_string(team_registration)
answer_submission = deformatter.df_string(answer_submission)
ask_for_help = deformatter.df_string(ask_for_help)
admin_command = deformatter.df_string(admin_command)

admin_emails = ["ryan.w.thomas@live.com", "ryanwhthomas@gmail.com","umdpuzzle@gmail.com","umdpuzzlehunt@gmail.com"]

# load save files
teams = teams_class.Teams('savefile_teams.txt')
puzzles = puzzles_class.Puzzles('savefile_puzzles.txt')
solves = solves_class.Solves('savefile_solves.txt', puzzles)
emails = emails_class.Emails('savefile_emails.txt')

debug = True
send_emails = True
delete_emails = True

if debug:
    print(teams.teamnames)
    print()
    print(puzzles.puzzle_id_hash)
    print(puzzles.proper_title_by_puzzle)
    print(puzzles.points_per_puzzle)
    print(puzzles.solutions_per_puzzle)
    print(puzzles.partials_per_puzzle)
    print()
    print(solves.solves_by_team)
    print(solves.solvetime_by_team)
    print(solves.score_by_team)
    print(solves.solves_by_puzzle)
    print()

# one time
username = 'umdpuzzlehunt@gmail.com'
password = input("Enter password: ")

# instaniate basic sender object
email_sender = basic_send.EmailSender(username, password, send_emails)

# log into email
mail = imaplib.IMAP4_SSL("imap.gmail.com")
mail.login(username, password)

# the number of times to check the email before stopping
# used to make sure the program doesn't accidentally run forever
loops = 100

# this was a the stop time for the Fall 2019 Puzzlehunt
# stop_time = (2019, 10, 6, 17, 30, 0, 0, 0, 0)
# place holder stop time
stop_time = (2038, 1, 19, 3, 14, 7, 0, 0, 0)

# does the scoreboard need to be redrawn?
rewrite_scoreboard = True

empty_inbox_wait = 20

while loops > 0:
    loops = loops-1

    mail.select("inbox")

    # get data about emails
    result, data = mail.uid('search', None, "ALL")

    # get list of email IDs
    inbox_item_list = data[0].split()

    if debug:
        print(inbox_item_list)

    # if no emails received, wait
    if( len(inbox_item_list) <= 0 ):
        if debug:
            print("Sleeping")
        time.sleep(empty_inbox_wait)
    else:
        if debug:
            print("Received %d new emails." % len(inbox_item_list))

    # iterate over all emails
    for index in range(0,len(inbox_item_list)):
        # get indexth email
        item = inbox_item_list[index]

        if debug:
            print(item)

        # get email's data
        result2, email_data = mail.uid('fetch', item, '(RFC822)')
        raw_email = email_data[0][1].decode("utf-8")
        email_message = email.message_from_string(raw_email)
        dir(email_message)

        recipient = email_message['To']
        sender = email_message['From']
        subject = email_message['Subject']
        date = email_message['date']

        # get email address from string <John Doe john.doe@gmail.com>
        temp = re.search( \
        "([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", \
        sender, re.IGNORECASE)
        if debug:
            print(sender)

        sender = temp.group(1)

        # add email to email list
        emails.addEmail( sender )

        time_tuple = email.utils.parsedate( date )

        payload = ""

        subject = deformatter.df_string(subject)

        if debug:
            print( sender )
            print( subject )

        # print( "Email Time %s" % str(time_tuple) )
        # print( "Stop Time %s" % str(stop_time) )

        if( time_tuple > stop_time ):
            if debug:
                print("Email past stop time")
            email_sender.send_email_ff('puzzlehuntover.txt', sender,())
        # if an email that requries the payload to be accessed
        elif (subject == team_registration or\
            subject == answer_submission or\
            subject == ask_for_help):
            # iterate over parts of email, eg if there's attachments
            for part in email_message.walk():
                if part.get_content_maintype() == "multipart":
                    continue

                content_type = part.get_content_type()
                if debug:
                    print(content_type )

                # if the content is text, add it to payload
                if "plain" in content_type:
                    payload += part.get_payload()
                elif debug:
                    print("not plain text")

            if debug:
                print("sujbect:\t%s" % subject)
                print('>%s<' % payload)

            if subject == team_registration:
                ### TEAM REGISTRATION  ###
                regex = 'Team\s*:\s*(\S[^\n]*\S)'

                temp = re.search( regex, payload, re.IGNORECASE)

                # matches format and valid team name (has at least 2 letters and/or numbers)
                if temp and len(deformatter.df_string( temp.group(1) ))>=2:
                    team = temp.group(1)
                    if teams.isTeam(team):
                        team = teams.getFormatted(team)
                        email_sender.send_email_ff('registration_error_preexisting.txt', sender,(team))
                    else:
                        teams.addTeam(team)
                        email_sender.send_email_ff('registration_success.txt', sender,(team))

                # matches format, invalid team name
                elif re.search( 'Team\s*:', payload, re.IGNORECASE):
                    email_sender.send_email_ff('registration_error_invalidteamname.txt', sender,())
                # invalid format
                else:
                    email_sender.send_email_ff('registration_error_malformation.txt', sender,())

            ### ANSWER SUBMISSION ###
            elif subject == answer_submission:
                regex = 'Team\s*:\s*(\S[^\n]*\S)\s*Puzzle\s*:\s*(\S([^\n]*\S)?)\s*Answer\s*:\s*(\S[^\n]*\S)'
                temp = re.search( regex, payload, re.IGNORECASE)

                # matches
                if temp:
                    team = temp.group(1)
                    puzzle = temp.group(2)
                    answer = temp.group(4)

                    if not teams.isTeam( team ):
                        email_sender.send_email_ff('submission_error_unregistered.txt', sender,(team))
                    elif not puzzles.isPuzzle( puzzle ):
                        email_sender.send_email_ff('submission_error_puzzledne.txt', sender,())
                    else: # is team and is puzzle
                        puzzle = deformatter.df_string( puzzle )

                        # special case hardcoded in: feeder puzzles that share a title but are awarded seperate points
                        # if answer is correct for a feeder puzzle, change title to specific feeder puzzle title
                        if puzzle == "A" or puzzle == "EVERYTHINGHASCHANGED":
                            if puzzles.answerResponse("WIGFLEW", answer) >= 0:
                                puzzle = "WIGFLEW"
                            elif puzzles.answerResponse("OPERATIONEDUCATION", answer) >= 0:
                                puzzle = "OPERATIONEDUCATION"

                        team = teams.getFormatted(team)
                        puzzle = puzzles.getProperTitle(puzzle)

                        # correct
                        if puzzles.answerResponse(puzzle, answer) > 0:
                            answer = puzzles.getProperAnswer(puzzle)
                            if solves.isSolved(team, puzzle):
                                email_sender.send_email_ff('submission_correct_presolved.txt', sender,(puzzle, puzzle, answer, team))
                            else:
                                rewrite_scoreboard = True
                                solves.addSolve(team, puzzle, time_tuple)
                                email_sender.send_email_ff('submission_correct.txt', sender,\
                                (puzzle, puzzle, answer, team, puzzles.getPoints(puzzle), solves.getScore(team)))
                        # partial
                        elif puzzles.answerResponse(puzzle, answer) == 0:
                            answer = deformatter.df_string(answer)
                            if solves.isSolved(team, puzzle):
                                email_sender.send_email_ff('submission_partial_presolved.txt', sender,(puzzle, answer, puzzle))
                            else:
                                email_sender.send_email_ff('submission_partial.txt', sender,(puzzle, answer, puzzle))
                        # incorrect
                        else:
                            if solves.isSolved(team, puzzle):
                                email_sender.send_email_ff('submission_incorrect_presolved.txt', sender,(puzzle, puzzle))
                            else:
                                email_sender.send_email_ff('submission_incorrect.txt', sender,(puzzle, puzzle))
                # does not match format
                else:
                    email_sender.send_email_ff('submission_error_malformation.txt', sender,())

            ### ASK FOR HELP ###
            else:
                # forward email to umdpuzzle
                email_sender.send_basic_email("New Ask For Help Request\r\n"+payload+"\nFrom "+sender, 'umdpuzzle@gmail.com')
                # # send "askforhelp_success" email
                # email_sender.send_email_ff('askforhelp_success.txt', sender,())
        # if admin command and from admin email, halts program
        elif subject == admin_command and sender in admin_emails:
            loops = 0
            print("Admin command received. Halting Program")
        # if the email has an unexpected header
        else:
            # send "how to send emails" email
            email_sender.send_email_ff('subject_dne.txt', sender,())

        # desti_folder_name = "Processed"
        # src_folder_name = 'ALL'
        #
        # typ, data = mail.uid('STORE', inbox_item_list[index], '+X-GM-LABELS', desti_folder_name )
        # typ, data = mail.uid('STORE', inbox_item_list[index], '-X-GM-LABELS', src_folder_name )

        # deleting emails and closing connection
        # # if this is commented out, the email won't be deleted
        # If you are looping more than once, you MUST delete emails, otherwise many emails will be sent for each email received
        if delete_emails or loops > 0:
            mail.uid('STORE', inbox_item_list[index], '+FLAGS', "\\Deleted")

    mail.expunge()

    if( rewrite_scoreboard ):
        rewrite_scoreboard = False
        solves.writeScoreboard(teams)
    time.sleep(1)

mail.close()
mail.logout()

print("Program ended")
