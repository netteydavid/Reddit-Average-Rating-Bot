README

About the bot:
	
	This bot responds to "!AverageRating" with the average of ratings in the top level comments of the thread. 
	
How it works:

	If a user wants the average rating in a certain thread, they must comment "!AverageRating". The bot will reply to the comment with the average. The average will always be to two decimal places and out of ten.
	
	In order for a rating to be included it must conform to the following criteria:
	
		- The ratings must use numbers, either spelled out or using digits.
		
			Examples: 4/10, six/ten, five out of ten, 9 out of 10, etc.
			
		- The bot will take the first rating in the comment. So make sure the final rating is listed first!
		
		- The ratings must be in one of the following forms: #/#, # out of #, # outta #
		
			Examples: 3/10, six out of ten, 9 outta 10, etc.
			
		- Ratings must have a denominator of 99 or less.
		
			Good Examples: 9/10, six out of twelve, 8/9, 22/99, four outta fifty
			
			Bad Examples: 10 out of 100, 300/1000
		
		- Ratings can have a numerator that is greater than the denominator, but the bot treats it as a perfect score.
		
			Example: 11/10 will be counted as 10/10
			
		- Ranges of ratings can be used. This bot will take the midpoint of the range into account for the average.
		
			Example: 5 - 6/10 will be counted as 5.5/10
			
		- Ranges must be of the following forms: rating - rating, rating to rating, # - rating, # to rating
		
			Examples: 3/10 - 4/10, 5 - 7/10, six out of ten to seven out of ten, 8 to 9/10, etc.
			
		- Ranges using a hyphens must either have numerators and denominators that are all words or all digits
		
			Good Examples: eight - nine out of ten, 2 - 3/5, 9 - 10 out of 10, etc.
			
			Bad Examples: 6 - seven out of 10, two - 3/10, four - 5 outta ten, etc.

Subreddits:

	Subreddits for this but can be found on the averageratingbotsubs multireddit.

	/r/pythonforengineers
	/r/Rateme
	
		