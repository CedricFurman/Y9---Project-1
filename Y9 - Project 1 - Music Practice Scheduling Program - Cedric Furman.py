
# December, 2020 - January, 2021
# Cedric Furman
# Upper Canada College Y9
# This is my program for criterion C ii, it's meant to aid into music practice
# The program is divided into three sections that may be told apart in the GUI: Section 1 - the practice schedule, section 2 - the practice report, and section 3 - the stopwatch

'''
Section 1, the practice schedule contains the starting point of the program, which is why it's located on the top left
Section 2, the practice report contains a report of all practice and achievements, its located on the bottom left
Section 3, the stopwatch is a bit more distanced from the rest of the program, on the right. This is because other parts of the program passively change according to it, the achievements report and practice report
'''

############################### Imports and Setup ###############################

#
# IMPORTANT: In order to run this program you must have the Matplotlib module installed, this can be done by entering "pip3 install matplotlib" in a terminal 
#

import Tkinter as tk 

import time as tm # Used in the practice schedule, practice report, and stopwatch

import random # Used to decide between equivalent situations

import math # Used in the practice schedule

from matplotlib import pyplot as plt # Used in the generation of graphs
plt.rcParams["toolbar"] = "None" # Disables the toolbar that comes with matplotlib graphs - refrence: https://www.xspdf.com/resolution/51676734.html#:~:text=Matplotlib%20figure%20hide%20toolbar,in%20graphs%20plotted%20by%20matplotlib.

root = tk.Tk() # This is the main window where the GUI will be located

root.title("Music Practice Scheduler") 

root.resizable(False, False) # Disables the window from resizing in the x and y axes, this is used because "sticky" does not work with "tk.place"

root.geometry("1000x470") # This is the same ratio as my design from criterion B iii

################################ Helper Functions ###############################

# This is a helper function that takes a string and splits it into two different list. This is used significantly in practice scheduling
def splitIntoLists(string, splitItem, list1, list2):

	# The string is split into two items based on the split item the user inputted, the two items are temporarly stored in a single list
	temporaryList = string.split(splitItem)

	# The first new item is added to list one and the second new item is added to list 2
	list1.append(temporaryList[0])
	list2.append(temporaryList[1])

# This function takes two lists and creates a new list that contains ranges between each of the corresponding items in the two lists
def rangesFromLists(list1, list2):

 	incriment = 0 # This incriment is used to correspond items between the two lists that will form a range between each other

	newList = [] # This is the new list that will store the new ranges

	# In all the cases where the function is used both lists passed as parameters have the same length, meaning that for each in list 1 is the correct for loop for both
	for item in list1:

		# A range is created from the two lists by taking the an index value of the incriment varible from the first list as beginning, and an index value of the incriment varible from the second list as the end. The new range is added to the new list
		newList.append(range(list1[incriment], (list2[incriment] + 1)))

		incriment += 1 # The incriment is increased to create another range from the lists using the next index

	return newList

# This function takes a list, and for each value in that list, it converts it into 24-hour time, which is easier to use for calculations
def alterEachInList(list1):
	
	# Each item in the list is altered
	for item in list1:
		
		# The variable "newItem" stores the altered 24-hour time version of the current item in the list
		newItem = convert24HourTime(item)

		# The current item in the list is reassigned as the new altered 24-hour time version of itself
		item = newItem

	return list1

# This function takes a string time and converts it into 24-hour time
def convert24HourTime(time):

	# If the time is pm, it is chagned accordingly
	if "pm" in str(time):

		# The time has its charecters removed, and is stroed in the "newTime" variable
		newTime = str(time).replace("pm", "")

		# The new time is added to 12 before being returned, because a time in pm plus 12 is its 24-hour time equivalent, like 5pm and 17
		newTime = int(newTime) + 12

		return newTime

	# If the time is am, it's changed differently
	else:

		# The new time is the am time without its charecters, because am time is already in the 24-hour time format
		newTime = str(time).replace("am", "")
		newTime = int(newTime)

		return newTime


# Converts an imputted time into string 12-hour time
def convert12HourTime(time):

	# If the 24-hour time is greater than 12, it becomes pm time
	if time > 12:

		# The time is subtracted by 12 because that produces the pm time equivalent to a 24-hour time, like 14 and 2pm
		time = time - 12

		# The time is converted to a string and pm is added to the end
		time = str(int(time)) + " pm"

	else:

		# If the time is 12 or less, then it's only converted to a string and has am added, because it's already 12-hour time 
		time = str(int(time)) + " am"

	return time

def convert(allSeconds): # Takes in an amount of seconds, then the function converts the total seconds into hours, minutes, and seconds, this is stored as a string and returned

	hours = int(allSeconds // 3600) # The amount of hours is calculated by integer dividing the total seconds by 3600 (60^2)

	totalMinutes = allSeconds // 60 # The total amount of minutes is calculated by integer dividing the total seconds by 60

	minutes = int(totalMinutes - hours * 60) # The amount of minutes to be displayed (under 60) is calculated by subtracting the amount of hours times 60, this is because the minutes have to reset everytime an hour passes

	seconds = int(round(allSeconds - totalMinutes * 60)) # The amount of seconds to be displayed is calculated using the same method as the amount of minutes to be displayed

	# The hours, minutes, and seconds are concatenated as the convertedTime variable, meaning the elapsed time is displayed in a user-friendly way, with the amount of hours, minutes, and seconds each distinguished

	# The conditional statements are used in order to give each present value of time a suffix, h for hours, m for minutes, and s for seconds, creating a format like, 5h 3m 43s. The conditional statements also make it so that only present time values are displayed, so something like, 0h 0m 34s, does not happen

	if hours >= 1 and minutes >= 1 and seconds >= 1:
		convertedTime = str(hours) + "h " + str(minutes) + "m " + str(seconds) + "s " 

	elif hours >= 1 and minutes >= 1 and seconds < 1:
		convertedTime = str(hours) + "h " + str(minutes) + "m "

	elif hours >= 1 and minutes < 1 and seconds < 1:
		convertedTime = str(hours) + "h "

	elif minutes >= 1 and seconds >= 1:
		convertedTime = str(minutes) + "m " + str(seconds) + "s "

	elif minutes >= 1 and seconds < 1:
		convertedTime = str(minutes) + "m "

	else:
		convertedTime = str(seconds) + "s "

	return convertedTime

# This helper function changes a scale between two options 
def changeScale(scale, scaleDispalyString, scaleDisaplyWidget, scaleDispalyStringOption1, scaleDispalyStringOption2):

	# If the scale is true, it is switched and becomes false
	if scale == True:

		scale = False

		# The possible scale option that is displayed is switched to the first option
		scaleDispalyString = scaleDispalyStringOption1
		scaleDisaplyWidget.config(text=scaleDispalyString)

		# The scale is returned so its new value can be accesed 
		return scale

		pass # The function is ended so the newly altered scale does not apply to the statement below

	# If the scale is false, then it becomes true
	elif scale == False:

		scale = True

		# The displayed possible scale option is switched again, now to the second option
		scaleDispalyString = scaleDispalyStringOption2
		scaleDisaplyWidget.config(text=scaleDispalyString)

		return scale

################################### Functions ###################################

# Section 1 (practice schedule) functions:

scheduledPractice = False # A boolean that stores if the user has scheduled their practice, it's used when checking for achievements 

minutesScale = False # This boolean stores whether or not the user's practice schedule will be displayed in minutes or hours 

dailyPracticeAmount = 0 # Stores the amount of daily practice, which is determined through practice sheduling function

practiceTarget = 1 # Stores the user's practice target in hours

practiceDays = 1 # Stores the number of days the user plans to practice for

schedule = '' # A string that stores the schedule that will be displayed to the user

# This is one of the main parts of the program, the practice scheduling algorithm 

# It takes in user input, alters that input into the correct format using several helper functions, then uses the altered input to generate a schedule

def schedulePractice():
	
	# The "scheduledPractice" boolean is set to true so the user can earn the achievement for scheduling practice
	global scheduledPractice
	scheduledPractice = True

	global schedule 

	global practiceTarget
	global practiceDays

	# If the user has their schedule displayed in the weekly scale instead of the daily scale, it has to be completely different 
	global weeklyScale
	if weeklyScale == True:

		# The number of practice weeks as a decimal is the practice days divided by 7
		practiceWeeksDecimal = practiceDays / float(7)

		# The number of practice weeks as an integer is the practice days integer divided by 7
		practiceWeeksWhole = practiceDays // 7

		# The the remainder week (a decimal to represent what portion of a week the remaining days are) is calculated by finding the positive difference between the decimal and integer practice weeks
		remainderWeek = float(abs(practiceWeeksWhole - practiceWeeksDecimal))

		# A practice multiplier is multiplied by the practice target to find the practice time of the time span that the multiplier represents

		# The reaminder week practice multiplier is found by dividing the remainder week by the total weeks

		remainderWeekPracticeMultiplier = float(remainderWeek / practiceWeeksDecimal)

		# If the practice week number is at least 1 then the practice weeks may be divided without an error
		try:

			# The regular week practice multiplier is the number of weeks divided by the decimal number of weeks, then divided for each full week
			regularWeekPracticeMultiplier = float(practiceWeeksWhole / practiceWeeksDecimal / practiceWeeksWhole)

		# If the practice week number is zero then there is only one week and the regular week practice multiplier is 1
		except ZeroDivisionError:

			regularWeekPracticeMultiplier = 1

		# The remainder week amount of practice is the practice target times the remainder week practice multiplier, that gives the remainder week practice amount in hours, but that times 3600 is the time in seconds, and those seconds are passed into the convert function to output the reaminder week practice amount in a clear format
		remainderWeekPractice = convert(int(round((remainderWeekPracticeMultiplier * practiceTarget) * 3600)))

		# The regular week practie amount is calculated using the same method as the remainder week practice, except the regular practice week multiplier is used instead of the remainder week practice multiplier
		regularWeekPractice = convert(int(round((regularWeekPracticeMultiplier * practiceTarget) * 3600)))

		weekNumber = 1 # An incriment that will be concatenated to display each week's number in the schedule, week 1, week 2...

		# The schedule is reset before it's altered to make sure that previous schedule will not still be present
		schedule = ''

		# For each full practice week, that practice week gets a description in the schedule
		for week in range(practiceWeeksWhole):

			# The description of a full practice week is the week number and the regular practice week time
			schedule = schedule + "Week " + str(weekNumber) + ": " + regularWeekPractice + "\n"

			weekNumber += 1 # The next week is one week later

		# If there is a remainder week, it also receives a description in the schedule
		if remainderWeekPractice > 0:

			# The description of a remainder week is the week number and the remainder week practice, the exact format as regular weeks, but the practice amount is different
			schedule = schedule + "Week " + str(weekNumber) + ": " + remainderWeekPractice + "\n"

		# The schedule display is updated to display the schedule in its new weekly form
		displayPracticeSchedule.config(text=schedule)

	# Below is the daily scale practice schedule generation:

	# The daily practice amount is always the same, unlike the weekly practice amounts, because there are no remainder days

	# The daily practice amount is the practice target divided by the days of practice
	global dailyPracticeAmount
	dailyPracticeAmount = float(practiceTarget) / float(practiceDays)

	# If daily practice amount is less than 1 hour, the minute scale is being used, which requires the hourly practice amount to be multiplied by 60 so it's in minutes
	global minutesScale
	if dailyPracticeAmount < 1:

		dailyPracticeAmount = dailyPracticeAmount * 60
		minutesScale = True

	global whenCanPracticeList
	global whenCantPracticeList

	# The following lists are in two sets, the first of each set contains the starts of the intervals they apply to (when can practice or when can't practice intervals), and the second of each set contains the end of those intervals

	# When can practice intervals:
	whenCanPracticeIntervalsBeginningsList = [] # Beginnings
	whenCanPracticeIntervalsEndingsList = [] # Endings

	# When can't practice intervals:
	whenCantPracticeIntervalsBeginningsList = [] # Beginnings
	whenCantPracticeIntervalsEndingsList = [] # Endings

	# The when can practice list stores user inputs on when they can practice in string intervals
	for interval in whenCanPracticeList:

		# The beginning of each string interval goes to the when can practice intervals beginnings and the endings go to the when can practice intervals endings, explained above

		# The string intervals of the list are split using the helper function "splitIntoLists", which is defined near the top of the program
		splitIntoLists(interval, "-", whenCanPracticeIntervalsBeginningsList, whenCanPracticeIntervalsEndingsList)

	# The when can't practice intervals list undergoes the same transition as the when can practice intervals list
	for interval in whenCantPracticeList:

		splitIntoLists(interval, "-", whenCantPracticeIntervalsBeginningsList, whenCantPracticeIntervalsEndingsList)

	# For each of the new lists that store beginnings or endings of sets of intervals, each of their items are converted to integer 24-hour time through the "alterEachInList" helper function, also defined near the top of the program

	whenCanPracticeIntervalsBeginningsList = alterEachInList(whenCanPracticeIntervalsBeginningsList)

	whenCanPracticeIntervalsEndingsList = alterEachInList(whenCanPracticeIntervalsEndingsList)

	whenCantPracticeIntervalsBeginningsList = alterEachInList(whenCantPracticeIntervalsBeginningsList)

	whenCantPracticeIntervalsEndingsList = alterEachInList(whenCantPracticeIntervalsEndingsList)

	# Now that the beginnings and endings of the when can and can't practice intervals are integers, they can be made into proper intervals, by being turned into ranges

	# New lists are used to store ranges created using using an item from the beginnings list as the beginning, and a corresponding item from the endings list as an ending. This is done with the "rangesFromLists" helper function, yet again defined near the beginning of the program

	whenCanPracticeIntervals = rangesFromLists(whenCanPracticeIntervalsBeginningsList, whenCanPracticeIntervalsEndingsList)
	whenCantPracticeIntervals = rangesFromLists(whenCantPracticeIntervalsBeginningsList, whenCantPracticeIntervalsEndingsList)

	possiblePracticeStartTimes = [] # Stores possible start times that the daily practice might begin at

	# Each hour that the user can practice on is checked and stored temporarly in the "currentHour" variable 
	for interval in whenCanPracticeIntervals:

		for hour in interval:

			currentHour = hour 

			# The current hour varible is now checked for each of the new when can't practice intervals
			for interval in whenCantPracticeIntervals:

				# If the hour is not in any when can't practice intervals, it's added to the possible start times list
				if currentHour not in interval:	

					possiblePracticeStartTimes.append(currentHour)

	# Stores start times that are final canidates for the beginning of daily practice
	startTimes = []

	# If the minutes scale is true, then the practice schedule is generated in a specific way
	if minutesScale == True:

		# The index is a random number in the list of possible practice start times
		index = random.randrange(len(possiblePracticeStartTimes))

		# The start hour in the recently randomized index of the possble practice start times

		# The possible practiec start times are good enough in the minutes scale because the practice will begin and end in the same hour, meaning that the possible start times don't need to be checked for what their end times would be

		startHour = convert12HourTime(possiblePracticeStartTimes[index])

		# The minutes varible is the daily practice amount rounded and in string format
		minutes = str(int(round(dailyPracticeAmount)))

		# The index variable is not an incriment to iterate through each practice day that has to be described iin the schedule
		index = 1

		# For each day in the practice schedule, that day receives a description
		for day in range(practiceDays):

			# The description for a day of practice in the minutes scale is, the day number and the minutes of practice
			schedule = schedule + "Day " + str(index) + ": At " + startHour + ", for " + minutes + " minutes\n"

			index += 1

	# If the regular hourly scale is being used to display the schedule, then things have to be done differently
	else:
		
		# Because the practice will span over an hour, there now has to be an end time too, and that end time also can not be in the when can't practice intervals
		for time in possiblePracticeStartTimes:

			currentStartTime = time

			# For each hour in the range between the start time and end time ("int(round(dailyPracticeAmount) + 1") of daily practice, that hour has to be checked if it's in any of the when can't practice intervals
			for hour in range(currentStartTime + (int(round(dailyPracticeAmount) + 1))):

				# The current hour that's being checked is stored in the "currentHour" variable so it may be accessed in other for loops
				hour = currentHour 

				# The current hour is checked for each interval, and if it's not a part of it, the possible practice start time it corresponds to becomes a final canidate for the daily practice start time
				for interval in whenCantPracticeIntervals:

					if currentHour not in interval:

						startTimes.append(currentStartTime)

		# Just as in the minute scale schedule, the start time is chosen from the options randomly, again as an index of the list that stores the canidates
		index = random.randrange(len(startTimes))

		# The chosen start time is the random index value of the start times list, converted into string 12-hour time
		startTime = convert12HourTime(startTimes[index])

		# The end time is the start time plus the practice amound rounded up, because the times in the schedule are done by the hour
		endTime = convert12HourTime(startTimes[index] + (math.ceil(dailyPracticeAmount)))

		# The daily practice span stores the start to the end of practice as a string
		dailyPracticeSpan = startTime + " to " + endTime

		# The hours of practice is turned into a string by passing the daily practice amound as seconds into the convert function
		hours = convert(dailyPracticeAmount * 3600)

		iterable = 1 # Iterates through each day of practice 

		# Each day of practice gets a description in the schedule
		for day in range(practiceDays):

			# The hourly scale daily description contains the day number, the daily practice span, and the daily practice amount
			schedule = schedule + "Day " + str(iterable) + ": " + dailyPracticeSpan + ", " + hours + "\n"
			iterable += 1  

	# If the weekly scale were true, then the schedule would already have been displayed, and displaying it again would display the daily scale version
	if weeklyScale == False:

		# The practice schedule is displayed for the user to see it
		displayPracticeSchedule.config(text=schedule)

	# The schedule is reset so there will nothing will be left over if practice is scheduled again
	schedule = ''

	# The boolean that tells if the user has inputted a practice target and time is set to false so they may do so again and generate a new schedule
	global inputtedPracticeTargetAndPracticeTime
	inputtedPracticeTargetAndPracticeTime = False

# Section 2 (practice report) functions:

# The functions below are apart of the first part of the second section, the playing report:

# A practice session class that makes reporting the different times the user has practiced simpler
# Refrence: https://www.w3schools.com/python/python_classes.asp
class PracticeSession:

	# An instance of the practice session class requires a start time
	def __init__(self, startTime):
		self.startTime = startTime

	# This class function generates a string practice session description, that is eventually displayed on the screen
	def spanPracticeHourly(self):

		# If the practice session was one hour, it will be displayed with "at hour" and then the practice time
		if self.startTime == self.endTime:
			self.practiceSpan = str("At " + self.startTime + ", you practiced\nfor: " + self.practiceTime + "\n")

		# If the practice session took multiple hours, the only differrence is that the description will begin with "from hour to hour"
		elif self.startTime != self.endTime:
			self.practiceSpan = str("From " + self.startTime + "to " + self.endTime + ", you\npracticed for: " + self.practiceTime + "\n")

	# If the daily practice report scale is being used, then the practice session will have to be described in a daily fashion
	def spanPracticeDaily(self):

		# A daily practice session description will always begin with "on day" and continue with the practice time, which remains the same
		self.practiceSpan = str("On " + tm.strftime("%A") +", you practiced\nfor: " + self.practiceTime + "\n")

	endTime = '' # Stores the time a practice session ended

	practiceSpan = '' # Stores the description of a practice session

	practiceTime = '' # Stores the amount of practice in a practice session

	practiceTimeMinutes = '' # Stores the amount of practice in a session in minutes, used for the practice report graph

resetTimes = 0 # Stores the number of times the stopwatch has been reset

practiceSessionTimes = [] # Stores the different times practice sessions occured, used as the x-axis in the practice report graph

practiceSessionLengths = [] # Stores the different minute spans of practice sessions, used as the y-axis in the practice report graph

# This function is ran before reporting practice, which requires specific conditions
def checkReportPractice():

	# The display is updated at the beginning to display the most recent practice sesssion that may have been cut off because of the report practice session ending
	global report
	displayPracticeReport.config(text=report)

	# "currentPracticeSession" is an instance of the practice session class that begins at the current time and will be used to display the current practice session
	currentPracticeSession = PracticeSession(tm.strftime("%I %p"))

	# This nested function does the actual work in reporting practice, but is called upon the correct conditions only
	def reportPractice():

		# The display is configured at the beginning so if something strange happens in the calculation, the function will end and it will not be displayed 
		global report
		displayPracticeReport.config(text=report)

		currentPracticeSession.endTime = currentPracticeSession.startTime

		# If the hourly scale is being used, the current practice session will be described hourly
		global dailyScale
		if dailyScale == False:
			currentPracticeSession.spanPracticeHourly()

		# If the practice session is false, it will be described in the daily format
		elif dailyScale == True:
			currentPracticeSession.endTime = tm.strftime("%A")
			currentPracticeSession.spanPracticeDaily()

		# The report, which is the string that displays the practice report to the user, becomes the description of the current practice session
		report = ''
		report = currentPracticeSession.practiceSpan

		# If the stopwatch is not paused, or reset (at 0 seconds), then the practice time of the current practice report is determined
		global totalSeconds
		global paused
		if totalSeconds != 0 and paused == False:

			# The regular practice time of the session is in hours, minutes, and seconds, and is calculated through the convert function
			currentPracticeSession.practiceTime = convert(totalSeconds)

			# The hourly practice time (used for the graph), is only in minutes, and is found by integer dividing the total seconds by 60, to find the number of minutes
			currentPracticeSession.practiceTimeMinutes = totalSeconds//60

		# If the practice count and reset times are the same, the timer has not been reset, thus the current practice session will continue to be updated, that means the report practice function will be called again
		global practiceCount
		global resetTimes
		if resetTimes == practiceCount:
			displayPracticeReport.after(1000, reportPractice)

		# If the timer has been reset, a new current practice session will be used, meaning the function will be exited, and the cycle restarted
		else:

			# Because the current practice session is now over, its end time is the current time
			currentPracticeSession.endTime = tm.strftime("%I %p")

			# The practice session's end time is stored in the practice sessions times list to be used in the practice report graph
			global practiceSessionTimes
			practiceSessionTimes.append(tm.strftime("%a, %I %p"))

			# The length of the practice session is stored in a list to be used in the practice report graph
			global practiceSessionLengths
			practiceSessionLengths.append(int(currentPracticeSession.practiceTimeMinutes))

			# The reset times are now equal to the practice count becuase the most recent practice session has been processed, now the function is exited, and the cycle restarted at beginnning of the check practice function
			resetTimes = practiceCount
			displayPracticeReport.after(1000, checkReportPractice)

	global practiceCount
	global resetTimes

	resetTimes = practiceCount

	# If the stopwatch is running and not restarted, then the current practice session may be displayed
	if practiceCount == resetTimes and running == True:
		reportPractice()

	# After each second the check practice report function will be ran again, until the correct conditions for the report practice function are satisfied
	displayPracticeReport.after(1000, checkReportPractice)

# The following functions and class are in the second part of the practice report section, achievements:

allAchievements = [] # Stores all achievements that may be earned

achievementsList = [] # stores all earned achievements 

# An achievement class, to make creating and handling achievements easier
class Achievement: 

	# An achievment will have one attribute passed in when it is declared, its name
	def __init__(self, name):
		self.name = name

	# The earn method is used to add an acheivement to the list of earned achievemtns, where it will be turned into a string and displayed to the user
	def earn(self): 

		global achievementsList	
		achievementsList.append(str(self.name) + ",\n" + str(self.timeEarned) + "\n")

	# An achievement will also have another three attributes that can be declared later through an instance, if its criteria has been met, whether it has been earned, and the time it was earned
	criteriaMet = False
	earned = False
	timeEarned = ''

# Declaration of all achievement class instances:

SchedulePracticeAchievement = Achievement("Scheduled music practice") # An achievement earned after scheduling music practice with the program

viewGraphAchievement = Achievement("Viewed a graph") # An achievement earned after viewing one of the program's graphs

practiceOnceAchievement = Achievement("Practiced once") # An achievement that is earned when the user practices once using the program

practiceTenTimesAchievement = Achievement("Practiced ten times") # An achievement that the user may earn by practicing ten times with the program

practiceForFiveMinutesAchievement = Achievement("Practiced for five minutes") # This achievement is earned when the user has practiced for five minutes

practiceForOneHourAchievement = Achievement("Practiced for one hour") # An achievement earned after practicing for one hour

# All achievements are added to the list of earnable achievements 
allAchievements.append(SchedulePracticeAchievement)
allAchievements.append(viewGraphAchievement)
allAchievements.append(practiceOnceAchievement)
allAchievements.append(practiceTenTimesAchievement)
allAchievements.append(practiceForFiveMinutesAchievement)
allAchievements.append(practiceForOneHourAchievement)

# Runs continuously to check if any achievements have been earned, earned achievements are exported to a list, from which they are displayed
# Refrence: https://docs.python.org/3/library/time.html 
def checkAchievements():

	# Each achievment is obtained through the global statement, along with it's completion boolean

	# If an achievemnt's completion boolean is true, the criteria of that achievement is met 

	global SchedulePracticeAchievement
	global scheduledPractice
	if scheduledPractice == True:
		SchedulePracticeAchievement.criteriaMet = True

	global viewGraphAchievement
	global graphed
	if graphed == True:
		viewGraphAchievement.criteriaMet = True

	global practiceOnceAchievement
	global practiceCount
	if practiceCount >= 1:
		practiceOnceAchievement.criteriaMet = True

	global practiceTenTimesAchievement
	if practiceCount >= 10:
		practiceTenTimesAchievement.criteriaMet = True

	global practiceForFiveMinutesAchievement
	global totalSeconds
	if totalSeconds // 60 == 5:
		practiceForFiveMinutesAchievement.criteriaMet = True

	global practiceForOneHourAchievement
	if scheduledPractice // 3600 == 1:
		practiceForOneHourAchievement.criteriaMet = True


	global allAchievements
	for achievement in allAchievements:

		# Each achievemtn is checked to see if it's criteria has been met, but also if it has already been earned, if it has, it will not be displayed a second time
		if achievement.criteriaMet == True and achievement.earned == False:

			achievement.earned = True # If the achievement was not already earned, it now is

			# The time the achievement was earned is stored using the current string time
			achievement.timeEarned = tm.strftime("%A, at %I:%M %p")

			# The hour the achievment was earned is also stored in a seperate list
			global achievementsHoursEarned
			achievementsHoursEarned.append(int(tm.strftime("%H")))

			# Becuase an achievement has been earned, it must now be displayed, which is done by adding it to the list of earned achievemnts in a strig format, through achievement.earn(), and then displaying those earned achievements through displayAchievements() 
			achievement.earn()
			displayAchievements()

	# After each second, achievements are checked for again
	displayAchievementsReport.after(1000, checkAchievements)

achievementsHoursEarned = [] # Stores the hours that achievments were earned on

# This function displays earned achievements 
def displayAchievements():

	incriment = 0 # An incriment to iterate through earned achievments

	global achievementsHoursEarned
	global achievementsList 
	global achievements
	achievements = '' # Clears the variable, so there are no duplicate achievements

	# If there are achievements, then while the incriment is less than the number of achievements, for each achievement, an if statement will run to decide if it will be shown
	if len(achievementsList) >= 1 and len(achievementsHoursEarned) >= 1:

		while incriment < len(achievementsList) and incriment < len(achievementsHoursEarned):

			global allAchievementsScale 

			# If the achievement has been earned in the past hour (recent achievement scale), or, if the all achievement scale is true, then the achievement will be displayed

			if achievementsHoursEarned[incriment] >= (int(tm.strftime("%I")) - 1) or allAchievementsScale == True:

				# If the current achievement in the cycle has satisfied the if statement, it is added to the string that is displayed as the achievements report
				achievements = achievements + "\n" + achievementsList[incriment]

				# The achievements report widget is reconfigured to display the latest achievements
				displayAchievementsReport.config(text=str(achievements))

			incriment += 1 # Has to be increased to continue the cycle											

# Section 3 (stopwatch) functions:

# Tells the current time
def tellTime(): 

	# The current time is updated and stored as a string in the format: Abreviated day of the week, abreviated month, day of the month, hour, minute, and am or pm
	# Refrence: https://docs.python.org/3/library/time.html 
	currentTime = tm.strftime("%a, %b %d, %I:%M %p") 

	# The current time is diaplayed on the current time label
	currentTimeDisplay.config(text="Current time: " + str(currentTime))

	# After each second, the function is ran again to check if the time has changed
	currentTimeDisplay.after(1000, tellTime)

################################ Button Commands ################################

# Section 1 (practice schedule) commands:

whenCanPracticeList = [] # A list used to store times the user can practice, which are retrieved by the following command

def getWhenCanPractice(): # Used to take store user input on when they can practice 

	global whenCanPracticeList

	# The input is obtained from a string variable, and is then stored in the list as a string to be used later
	whenCanPracticeList.append(str(whenCanPractice.get())) 

# Same process as the above function

whenCantPracticeList = []

def getWhenCantPractice(): 

	global whenCantPracticeList
	whenCantPracticeList.append(str(whenCantPractice.get()))

# Similar process as the above functions, except the string varible that is being stored contains two values that need to be stored seperately

inputtedPracticeTargetAndPracticeTime = False # Stores whether the command has been already called

# The user's practice target and practice time are retrieved by this function

def getPracticeTargetAndPracticeTime():

	global inputtedPracticeTargetAndPracticeTime # Uses the global variable, and does not use a non-existant regional variable

	# The command is only meant to be used once because there is only one practice target and practice time, so only when the inputtedPracticeTargetAndPracticeTime boolean is false, the command is ran
	if inputtedPracticeTargetAndPracticeTime == False:

		# The string variable is split along a comma, turning it into two items that are placed in a list
		practiceTargetAndPracticeTimeList = str(practiceTargetAndPracticeTime.get()).split(",")

		global practiceTarget
		global practiceDays

		# The two items from the list are stored into different variables
		practiceTarget = float(practiceTargetAndPracticeTimeList[0]) # Stores the practice target in hours
		practiceDays = int(practiceTargetAndPracticeTimeList[1]) # Stores the practice time in full days

		# inputtedPracticeTargetAndPracticeTime is set to true, so the command may not be ran again
		inputtedPracticeTargetAndPracticeTime = True
		return inputtedPracticeTargetAndPracticeTime

	schedulePractice() # Function used to generate the user's practice schedule, defined earlier

graphed = False # A boolean that stores whether the user has graphed data in the program, it's relevant when awarding achievements

# The funtion below grpahs the user's practice schedule

# Refrences: https://www.geeksforgeeks.org/how-to-embed-matplotlib-charts-in-tkinter-gui/ and https://matplotlib.org/Matplotlib.pdf

def graphSchedule():

	# The graphed boolean is set to true, so an achievement will be earned
	global graphed
	graphed = True

	# The daily practice amount is displayed on the y-axis, and the practice days are stored on the x-axis
	global dailyPracticeAmount
	global practiceDays

	practiceDaysList = [] # stores the practice days in the format, day 1, day 2, day 3... This is because the practice days are an integer and have to be iterated through and stored in a list to be graphed
	incriment = 1 # Used for the iteration of practice days

	for day in range(practiceDays):

		# Each practice day is stored in the list using by adding the current incriment value
		practiceDaysList.append(incriment)
		incriment += 1

	dailyPracticeAmountList = [] # Again, an integer value for the dialy practice amount will not suffice, it will have to be a list 

	# Each day has an amount of practice to correspond to it, so the daily practice amount is added to the list a number of times equal to amount of pracitce days
	for day in practiceDaysList:

		dailyPracticeAmountList.append(dailyPracticeAmount)
	
	# If the daily practice amount is in minutes, the graph will have to adjust
	global minutesScale
	if minutesScale == True:

		# The graph is created with the pracice days as the x-axis, and the daily practice amount (the same value displayed for each practice day) is the y-axis 
		plt.bar(practiceDaysList, dailyPracticeAmountList, bottom=0, align="center")

		# The y-axis label specifies that the daily practice time is in minutes 
		plt.ylabel("Time (Minutes)")

	# If the daily pracice time is in hours, the graph will still have to change
	else:

		plt.bar(practiceDaysList, dailyPracticeAmountList, bottom=0, align="center")

		# The y-axis title now displays that the daily practice time is in hours
		plt.ylabel("Time (Hours)")

	plt.title("Scheduled Days of Practice and Daily Practice Load") 

	plt.xlabel("Day Number") 

	# The graph is displayed in its own window
	plt.show(block=False) # "block=False" allows the graph to be shown without freezing the Tkinter window

weeklyScale = False #

# This command only really calls on the helper function "changeScale" (defined at the beginning of the program) to change the scale of the schedule
def changeScheduleScale():
	
	global weeklyScale
	global scheduleScale

	# Determines and displays whether or not the weekly scale is being used
	weeklyScale = changeScale(weeklyScale, scheduleScale, practiceScheduleScale, "Weekly scale", "Daily scale")

	# The schdule practice function is called to display the schedule with the new scale 
	schedulePractice()

# Section 2 (practice report) commands:

# This function graphs the user's practice report, it uses a very similar method to the "graphSchedule" command, the second function above
def graphReport():

	global graphed
	graphed = True

	global practiceSessionTimes
	global practiceSessionLengths

	# The main differnce between the practice report graph and the pracitce schedule graph, is that the pracitce report graph contains string values in the axes

	# the "xAxisPositions" list stores the position that the string values of the x-axis will be assigned to

	# Because each practice session has a practice time, iterating through the practice session length list, and adding the current incriment value to the "xAxisPositions" list creates a set of values that can take the place of the string values of the x-axis until they are assinged to their positions

	incriment = 1 
	xAxisPositions = [] 

	for session in practiceSessionLengths:
		xAxisPositions.append(incriment)
		incriment += 1
	
	# The graph is plotted, with the xAxisPositions as the x-axis, holding the positions for the pracitce session times, and the practice session lengths as the y-axis
	plt.bar(xAxisPositions, practiceSessionLengths, align="center")

	# Assigns the string practice session times to their x-axis positions
	plt.xticks(xAxisPositions, practiceSessionTimes)

	plt.title("The Times and Lengths of Your Previous Practice Sessions")

	plt.xlabel("Time")

	plt.ylabel("Length (Minutes)")
	
	plt.show(block=False) # Again "block=False" is used to prevent the Tkinter window from freezing
		
dailyScale = False

# Changes the current practice report scale being used
def changeReportScale():
	
	global dailyScale
	global reportScale

	# Through the change scale function, the report scale is changed, and the other scale option that is displayed is changed as well
	dailyScale = changeScale(dailyScale, reportScale, practiceReportScale, "Daily view", "Hourly view")

allAchievementsScale = False # A boolean that tells whether or not the user has the "view all avhievements" scale activated

# This function changes the achivement scale being used, also means reconfiguring the achivement display to show achievements in a different scale   
def changeAchievementsScale():

	global allAchievementsScale
	global achievementsScale

	# Again through the change scale function is used to change a scale, this time the achievements report scale, the other achievements scale option is also changed and displayed
	allAchievementsScale = changeScale(allAchievementsScale, achievementsScale, achievementsReportScale, "All achievements", "Recent achievements")

# Section 3 (stopwatch) commands:

# Refrence: https://docs.python.org/3/library/time.html 

paused = False # A boolean used to tell if the program is paused or not

running = False # A boolean to indicate whether the stopwatch is running

totalSeconds = 0 # Stores the total elapsed time in seconds

# Starts the stopwatch, which the user may use to time their practice

def startCheck(): # Before the nested start function that starts the stopwatch may run, the function must be checked
	
	# Before the stopwatch begins, it must be checked whether it's the first time it's being ran, because running the stopwatch multiple times at once would alter the program
	global running
	if running == True:
		return

	def start(): # This nested function calls itself continuosly in a loop, in order to count time 

		global paused	
		global running

		if paused == True: # If the stopwatch is paused, the function is stopped

			paused = False # the paused boolean is set to false again, so the next time the start button is pressed, the stopwatch will go on
			running = False # The stopwatch is no longer running
			return

		running = True # The stopwatch is now running

		global totalSeconds
		global timeElapsed
		timeElapsed = convert(totalSeconds) # Calls the convert function, located right above this function, the current total second count is passed in, outputting the timeElapsed variable with the current amount of hours, minutes, and seconds

		stopwatch.config(text="Time elapsed: " + timeElapsed) # Refreshes the stopwatch label to display the current timeElapsed variable

		# One second is added to the total second count, because the function is 1 second long, and repeats to count another second
		totalSeconds += 1

		# The function is repeated after 1000 milliseconds (one second), this means the total second count will go up by 1, changing the time elapsed, and reconfiguring the stopwatch with the new timeElapsed variable, so the new current time spent practicing will be displayed 
		stopwatch.after(1000, start)

	start() # Start function is ran, and the stopwatch begins

def pause(): # Pauses the stopwatch, so the user can take a break from practicing 
	
	global paused
	paused = True

practiceCount = 0 # Stores the amount of times the user has practiced

def reset(): # Resets the stopwatch, so the user may end their practice

	# The practice count is increased by one, this is because the user has finished practicing by resetting the stopwatch, the practice count is used later when checking for achievements
	global practiceCount
	practiceCount += 1
	
	global totalSeconds
	totalSeconds = 0 # The total second count is reset as zero

	# The reset total second count is passed into the convert function, which resets the time elapsed variable to 0 seconds, next, the reset time elapsed variable is displayed
	global timeElapsed
	timeElapsed = convert(totalSeconds)
	stopwatch.config(text="Time elapsed: " + timeElapsed)
	
	global paused
	global running

	# If the stopwatch is currently running, it is paused so it doesn't continue counting after being reset
	if running == True:
		running = False
		paused = True 
		pass

	# If the stopwatch is already paused, it is set to false, not so that it continues counting right away, but so that it will continue to count when the start button is pressed 
	elif paused == True:
		paused = False

############################## Buttons and Widgets ##############################

logo = tk.Frame(root, # A frame to display the logo of the program
	width=150,
	height=75,
	bg="light grey")

# logoImage = Image.open("imageName.jpeg") - source: https://github.com/ajugoon/y9-sample-code/blob/master/tkinter/tk-ex5.py TO BE DELETED

title = tk.Label(root, # Title of the program
	bg="light blue",
	font="Calibri 50", # Calibri is the font to be used throughout the program, the same as in my design from criterion B iii
	text="Music Practice Scheduler",
	padx=160, # Makes the label span its designated area
	pady=5)

section1Label = tk.Label(root, # For the scheduling section of the program
	font="Calibri 36",
	text="Schedule\nPractice")

section2Label = tk.Label(root, # For the practice report section 
	fg="black",
	font="Calibri 36",
	text="Practice\nReport",
	padx=10) # Aligns the label with the first section's label, directly above

section3Label = tk.Label(root, # For the practice report section 
	font="Calibri 36",
	text="Practice Now",
	padx=32) # Centers the label in its designated region

divider1 = tk.Frame(root, # Seperates sections 1 and 2 horizontally
	width=600,
	height=5,
	bg="black")

divider2 = tk.Frame(root, # Seperates section 3 from the other sections vertically
	width=5,
	height=340,
	bg="black")

# The following widgets are in section 1 of the program, practice scheduling:

# The following sting variables store the input from the entry widgets below
whenCanPractice = tk.StringVar()

whenCantPractice = tk.StringVar() 

practiceTargetAndPracticeTime = tk.StringVar() 

whenCanPracticeEntry = tk.Entry(root, # An entry widget that takes in when the user can practice, which is to be used when creating a schedule
	width=12,
	bg="blue",
	bd=0,
	font="Calibri 12",
	highlightcolor="light blue",
	textvariable=whenCanPractice)

whenCantPracticeEntry = tk.Entry(root, # An entry widget that stores when the user can't practice, which will also be used for scheduling
	width=12,
	bg="blue",
	bd=0,
	font="Calibri 12",
	highlightcolor="light blue",
	textvariable=whenCantPractice)

practiceTargetEntry = tk.Entry(root, # An entry widget that collects the user's target practice amount and days to practice, this will also be used when scheduling
	width=12,
	bg="blue",
	bd=0,
	font="Calibri 12",
	highlightcolor="light blue",
	textvariable=practiceTargetAndPracticeTime)

whenCanPracticeExplaination = tk.Label(root, # A label to go above its correspoding entry widget in order to explain its use
	font="Calibri 9",
	text="Input when you can practice\nex: 10am-11am",
	padx=12)

whenCantPracticeExplaination = tk.Label(root, # A label to go above its correspoding entry widget in order to explain its use
	font="Calibri 9",
	text="Input when you can't practice\nex: 11am-12pm",
	padx=8)
	
practiceTargetExplaination = tk.Label(root, # A label to go above its correspoding entry widget in order to explain its use
	font="Calibri 9",
	text="Input your practice goal (hours) and the\ntime for practice (days), ex: 12, 14")

whenCanPracticeConfirmation = tk.Button(root, # A button the user presses to submit the information they entered
	font="Calibri 12",
	text="Submit",
	command=getWhenCanPractice) # Stores submitted information in a list

whenCantPracticeConfirmation = tk.Button(root, 
	font="Calibri 12",
	text="Submit",
	command=getWhenCantPractice)

practiceTargetConfirmation = tk.Button(root, 
	font="Calibri 12",
	text="Submit",
	command=getPracticeTargetAndPracticeTime)

practiceSchedule = tk.Frame(root, # This is where the user's practice schedule will be
	width=230,
	height=130) 

schedule = "This is where your practice\nschedule will appear" # Stores the user's practice schedule

displayPracticeSchedule = tk.Label(practiceSchedule, # The label that will display the outputed practice schedule
	height=6,
	bg="light grey", # Colour to be used for all output displays, just like in my design from criterion B iii
	font="Calibri 14",
	text=schedule)

graphPracticeSchedule = tk.Button(practiceSchedule, # The user can use this button to view a graph of their practice schedule
	font="Calibri 12",
	text="Graph schedule",
	command=graphSchedule)

scheduleScale = "Weekly scale" # Displays the different scale option that may be used (daily or weekl

practiceScheduleScale = tk.Button(practiceSchedule, # The user may use this button to change the scale their practice shcedule is seen in (daily or weekly)
	font="Calibri 12",
	text=scheduleScale,
	command=changeScheduleScale) 

# The following widgets are in section 2 of the program, the practice report:

practiceReport = tk.Frame(root, # This is where the user's practice report will be 
	width=230, 
	height=130)

report = "This is where your practice\nreport will appear" # Stores the user's practice report

displayPracticeReport = tk.Label(practiceReport, # This is the label where the user's practice report is displayed
	height=6,
	bg="light grey",
	font="Calibri 14",
	text=report) 

graphPracticeReport = tk.Button(practiceReport, # This button graphs the user's practice report
	font="Calibri 12",
	text="Graph report",
	command=graphReport)

reportScale = "Daily view" # Indicates the other scale that may be used (daily or weekly)

practiceReportScale = tk.Button(practiceReport, # This button changes the scale the practice report uses (daily or weekly)
	font="Calibri 12",
	text=reportScale,
	command=changeReportScale)

achievementsReport = tk.Frame(root, # This is where the user's earned achievements will be
	width=175,
	height=130,
	bg="light grey")

achievements = "This is where your\nachievements will appear" # Displays achievements earned by the user

displayAchievementsReport = tk.Label(achievementsReport, # This is where achievements the user has earned are displayed
	height=6,
	bg="light grey",
	font="Calibri 12",
	text=achievements,
	padx=13,
	pady=7)

achievementsScale = "View all achievements" # This variable indicates the scale that is not being used (recent or all time)

achievementsReportScale = tk.Button(achievementsReport, # This button changes the scale the user's achievemetns are shown in (recent or all time)
	font="Calibri 12",
	text=achievementsScale,
	command=changeAchievementsScale) 

# The following widgets are in section 3 of the program, the stopwatch:

currentTimeDisplay = tk.Label(root, # This label displays the current time
	width=30,
	bg="light blue",
	font="Calibri 14",)

timeElapsed = "0s" # This stores the time the stopwatch has been running for

stopwatch = tk.Label(root, # This is a stopwatch to be used for timing music practice
	width=18,
	font="Calibri 24",
	text="Time elapsed: " + timeElapsed)

stopwatchOptions = tk.Frame(root, # This is a frame where the stopwatch buttons will be placed
	width=100,
	height=50)

startStopwatch = tk.Button(stopwatchOptions, # The user may use this button to begin the stopwatch and start practicing
	font="Calibri 12",
	text="Start",
	command=startCheck)

pauseStopwatch = tk.Button(stopwatchOptions, # This button will pause the stopwatch
	font="Calibri 12",
	text="Pause",
	command=pause)

resetStopwatch = tk.Button(stopwatchOptions, # This button will be used to reset the stopwatch and finish practicing
	font="Calibri 12",
	text="Reset",
	command=reset)

##################### Assigning Button and Widget Positions #####################

# With help from a diagram: https://docs.google.com/drawings/d/11-gD1XjtcAV7nWwi3eWiYTPewOtwT_V6VRKURssmj74/edit?usp=sharing

# I used the place() layout manager because it provides more control over where the widgtets may go without, meaning no worrying over blank space

# I chose the correct cordinates of each widget through calculations with other pre-existing widgets 

logo.place(x=0, y=0)

title.place(x=150, y=0)

section1Label.place(x=30, y=125)

section2Label.place(x=30, y=325)

section3Label.place(x=695, y=105)

divider1.place(x=30, y=270) 

divider2.place(x=660, y=105)

# Section 1:

whenCanPracticeEntry.place(x=210, y=105)

whenCantPracticeEntry.place(x=210, y=160)

practiceTargetEntry.place(x=210, y=215)

whenCanPracticeExplaination.place(x=210, y=77)

whenCantPracticeExplaination.place(x=210, y=132)

practiceTargetExplaination.place(x=195, y=187)

whenCanPracticeConfirmation.place(x=310, y=102)

whenCantPracticeConfirmation.place(x=310, y=157)

practiceTargetConfirmation.place(x=310, y=212)

practiceSchedule.place(x=400, y=105)

displayPracticeSchedule.pack(side=tk.TOP, fill=tk.X) # Uses pack because it's inside a frame

graphPracticeSchedule.pack(side=tk.LEFT)

practiceScheduleScale.pack(side=tk.RIGHT)

# Section 2:

practiceReport.place(x=210, y=310)

displayPracticeReport.pack(side=tk.TOP, fill=tk.X) # fill is used to make the label the same length as the frame

graphPracticeReport.pack(side=tk.LEFT)

practiceReportScale.pack(side=tk.RIGHT)

achievementsReport.place(x=440, y=310)

displayAchievementsReport.pack(side=tk.TOP, fill=tk.X)

achievementsReportScale.pack(side=tk.BOTTOM, fill=tk.X) 

# section 3:

currentTimeDisplay.place(x=695, y=175)

stopwatch.place(x=695, y=270)

stopwatchOptions.place(x=740, y=417)

startStopwatch.pack(side=tk.LEFT)

pauseStopwatch.pack(side=tk.LEFT)

resetStopwatch.pack(side=tk.RIGHT)

############################# Running The Program ###############################

tellTime()
checkAchievements()
checkReportPractice()
root.mainloop()

