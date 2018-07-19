#!/usr/bin/env python3
import praw
import re

#TODO: SEARCH FOR TODOs when testing and editing

#Converts numeric words zero through ninety-nine to their associated float value
def numWords(num):
    ones = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven',
    'eight', 'nine']

    tens = ['ten', 'eleven', 'twelve', 'thirteen', 'fourteen'
    'fifteen', 'sixteen', 'seventeen', 'eighteen', 'nineteen']

    tens2 = ['twenty', 'thirty', 'fourty', 'fifty', 'sixty', 'seventy', 'eighty',
    'ninety']

    numSplit = re.split(r' |-', num.lower())
    result = 0

    isNum = 0

    if (num.isdecimal() or num.isdigit()):
        return float(num)

    for word in numSplit:
        if (word in tens2):
            isNum = 1
            result += (tens2.index(word) + 2) * 10
        elif (word in tens):
            isNum = 1
            result += tens.index(word) + 10
        elif (word in ones):
            isNum = 1
            result += ones.index(word)
        else:
            continue
    if isNum:
        return result
    else:
        return -1

#The meat of the bot! Gets the average rating if a user comments the call string '!AverageRating'
def AverageRating():

    #The call string
    callStr = r'!averagerating'

    #Regular expression for normal ratings (i.e. 3/10, six out of ten, 5 outta 5, etc.)
    rateRE = r'([a-zA-Z]+[\- ]?[a-zA-Z]*|\d*.?\d+)\s?/\s?([a-zA-Z]+[\- ]?[a-zA-Z]*|\d*.?\d+)|([a-zA-Z]+[\- ]?[a-zA-Z]*|\d*.?\d+) out of ([a-zA-Z]+[\- ]?[a-zA-Z]*|\d*.?\d+)|([a-zA-Z]+[\- ]?[a-zA-Z]*|\d*.?\d+) outta ([a-zA-Z]+[\- ]?[a-zA-Z]*|\d*.?\d+)'
    #Regular expression for the comments that have a range for ratings (i.e. 5 - 6/10, seven out of ten to eight out of ten, etc.)
    rangeRE = r'((\d*.?\d+)\s?/\s?(\d*.?\d+)|(\d*.?\d+) out of (\d*.?\d+)|(\d*.?\d+) outta (\d*.?\d+)|(\d*.?\d+))\s?-\s?((\d*.?\d+)\s?/\s?(\d*.?\d+)|(\d*.?\d+) out of (\d*.?\d+)|(\d*.?\d+) outta (\d*.?\d+))|(([a-zA-Z]+[\- ]?[a-zA-Z]*)\s?/\s?([a-zA-Z]+[\- ]?[a-zA-Z]*)|([a-zA-Z]+[\- ]?[a-zA-Z]*) out of ([a-zA-Z]+[\- ]?[a-zA-Z]*)|([a-zA-Z]+[\- ]?[a-zA-Z]*) outta ([a-zA-Z]+[\- ]?[a-zA-Z]*)|([a-zA-Z]+[\- ]?[a-zA-Z]*))\s+-\s+(([a-zA-Z]+[\- ]?[a-zA-Z]*)\s?/\s?([a-zA-Z]+[\- ]?[a-zA-Z]*)|([a-zA-Z]+[\- ]?[a-zA-Z]*) out of ([a-zA-Z]+[\- ]?[a-zA-Z]*)|([a-zA-Z]+[\- ]?[a-zA-Z]*) outta ([a-zA-Z]+[\- ]?[a-zA-Z]*))|(([a-zA-Z]+[\- ]?[a-zA-Z]*|\d*.?\d+)\s?/\s?([a-zA-Z]+[\- ]?[a-zA-Z]*|\d*.?\d+)|([a-zA-Z]+[\- ]?[a-zA-Z]*|\d*.?\d+) out of ([a-zA-Z]+[\- ]?[a-zA-Z]*|\d*.?\d+)|([a-zA-Z]+[\- ]?[a-zA-Z]*|\d*.?\d+) outta ([a-zA-Z]+[\- ]?[a-zA-Z]*|\d*.?\d+)|([a-zA-Z]+[\- ]?[a-zA-Z]*|\d*.?\d+)) to (([a-zA-Z]+[\- ]?[a-zA-Z]*|\d*.?\d+)\s?/\s?([a-zA-Z]+[\- ]?[a-zA-Z]*|\d*.?\d+)|([a-zA-Z]+[\- ]?[a-zA-Z]*|\d*.?\d+) out of ([a-zA-Z]+[\- ]?[a-zA-Z]*|\d*.?\d+)|([a-zA-Z]+[\- ]?[a-zA-Z]*|\d*.?\d+) outta ([a-zA-Z]+[\- ]?[a-zA-Z]*|\d*.?\d+))'
    #Compile each expression into a pattern
    ratePattern = re.compile(rateRE)
    rangePattern = re.compile(rangeRE)

    #Call Pattern
    callPattern = re.compile(callStr)

    #Get the bot user account and reddit api
    reddit = praw.Reddit('AverageRatingBot')

    #Subreddits that this bots operates on
    subreddits = reddit.multireddit("Average_Rating_Bot", "ratingsubs")

    #Number of comments that are ratings
    count = 0
    #Sum of the ratings
    sum = 0.0

    #Fetch the latest comments for parsing
    for comment in subreddits.stream.comments():
        callMatch = callPattern.search(comment.body.lower())
        if callMatch:
            #Check if the comment has been replied to. If not, record and reply
            inFile = 0
            with open('replied.txt', 'a+') as f:
                if f.tell() != 0:
                    f.seek(0)
                for line in f:
                    if line == comment.id + '\n':
                        inFile = 1
                        #print("Call comment in file.")
                        break
                if inFile:
                    continue
                else:
                    #print("Call comment added.")
                    #TODO: Comment out when testing
                    f.write(comment.id + '\n')

            #Grab the thread that the call comment is in for parsing
            submission = comment.submission
            for top_level_comment in submission.comments:
                rngMatch = rangePattern.search(top_level_comment.body)
                rtMatch = ratePattern.search(top_level_comment.body)
                #Check if the top lvl comment has a range of ratings
                if rngMatch:
                    #print("Range Comment: " + top_level_comment.body)
                    #First numerator
                    n1 = -1
                    #Second numerator
                    n2 = -1
                    #Common denominator
                    d = -1
                    for i in range(1, 45):
                        if i in [2, 4, 6, 8, 17, 19, 21, 23, 32, 34, 36, 38]:
                            #Get first numerator
                            n1 = numWords(str(rngMatch.group(i)))
                            if n1 > -1:
                                break
                    for i in range (10, 45):
                        if i in [10, 12, 14, 25, 27, 29, 40, 42, 44]:
                            #Get second numerator and denominator
                            n2 = numWords(str(rngMatch.group(i)))
                            d = numWords(str(rngMatch.group(i + 1)))
                            if n2 > -1 and d > -1:
                                break
                    #If a valid range rating is found, add to the average
                    if n1 > -1 and n2 > -1 and d > -1:
                        count += 1
                        #print("Count: " + str(count))
                        sum += ((n1 + n2)/2) * (10.0 / d)
                        #print("Sum: " + str(sum))

                #Check if the top lvl comment has a normal rating
                elif rtMatch:
                    #print("Normal Comment: " + top_level_comment.body)
                    for i in range(1, 6, 2):
                        rtg1 = numWords(str(rtMatch.group(i)))
                        rtg2 = numWords(str(rtMatch.group(i + 1)))
                        if (rtg1 > -1 and rtg2 > -1):
                            count += 1
                            #print("Count: " + str(count))
                            if rtg1 > rtg2:
                                sum += rtg2
                            else:
                                sum += rtg1 * (10.0 / rtg2)
                            #print("Sum: " + str(sum))
                            break

            #Reply to the call comment with the thread average rating!
            if count == 0:
                #print("No valid ratings available for average.")
                #TODO: Comment out when testing
                comment.reply('There are no ratings I can read yet. Try again later with a reply to this comment!')
            else:
                #print("Sum = %.2f" % sum)
                #print("Count = " + str(count))
                #print("Average = %.2f" % (sum/count))
                #TODO: Comment out when testing
                comment.reply('The average rating is %.2f' % (sum / count) + '/10!\n\nGo to my profile for help and more information!')

AverageRating()
