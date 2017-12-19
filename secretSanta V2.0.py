##-------------------------IMPORTS----------------------------------------------

#smtplib is for interfacing with smtp which allows the program to send e-mails
import smtplib
#tkinter is the GUI and all graphical elements
from tkinter import *
#randint is able to generate a random integer between two values
from random import randint
#-------------------------------------------------------------------------------


#-------------------------METHODS-----------------------------------------------

#A funtion to send an e-mail to the relevant person letting them know who their secret santa is
def sendEmail(address, secretSantaName, gmailUser, gmailPassword):
    #Defining the message that is going to be sent
    message=("Your secret santa is " + secretSantaName)
    #Setting up the mail server
    mailServer = smtplib.SMTP('smtp.gmail.com', 587)
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.ehlo()
    #Logging into the mail server
    mailServer.login(gmailUser, gmailPassword)
    #Sending the e-mail from the user to the participant with the message
    mailServer.sendmail(gmailUser, address, message)
    #Closing the connection to the mail server
    mailServer.close()

#A function to create labels from a given list
def createLabels(window, labelNames, incriment, startingRow, **options):
    #Setting i to the starting row
    i=startingRow
    #Sets the starting column
    column=0
    #Sets the starting padding
    padx=0
    #Creating a for loop to create to labels from the given list
    for name in labelNames:
        #If the list exceeds the window size it moves to the next column
        if i>11:
            #Increases the value for column by 2
            column = column+2
            #Resets i to the starting row
            i=startingRow
            #Sets the padding on the left to 20
            padx = (20,0)
        #Creating the label and the locaiton of the label
        lbl = Label(window, text=name)
        lbl.grid(row=i, sticky=W, column=column, padx=padx, **options)
        i=i+incriment

#A function to create fields from a given list in a grid layout in given incriments of rows and then add them to a set which is returned
def createEntries(window, entryNames, incriment, startingRow, **options):
    #Creating a blank set in which to store the created entries
    entries={}
    #Setting i to the starting row
    i=startingRow
    #Setting the starting column to 1
    column=1
    #Creating a for loop to create the entries from a given list
    for name in entryNames:
        #If the list exceeds the window size it moves to the next column
        if i>11:
            #Increases the value for column by 2
            column = column+2
            #Resets i to the starting row
            i=startingRow

        #Creating the entry
        e = Entry(window)
        #Assigning the location of the entry
        e.grid(row=i, column=column, **options)
        #Adding the entry to the set
        entries[name] = e
        i=i+incriment
    #Returning the set of entries that were created
    return entries

#A function to assign the varibles from the setup window to global variables so that they can be used within the rest of the class
def setupComplete():
    global userEmailAddress
    userEmailAddress=setupEntries["userEmail"].get()
    global userEmailPassword
    userEmailPassword=setupEntries["userPassword"].get()
    global numberOfParticipants
    numberOfParticipants=int(setupEntries["numberOfParticipants"].get())
    global nameLabels
    nameLabels=createPersonArray(numberOfParticipants, " name:")
    global emailLabels
    emailLabels=createPersonArray(numberOfParticipants," E-mail address:")
    global nameEntryFields
    nameEntryFields=createArray(numberOfParticipants)
    global emailEntryFields
    emailEntryFields=nameEntryFields
    setup.destroy()

#A function to create an array to set up the root window
def createPersonArray(number, message):
    #Creating a blank array to store the labels
    array=[]
    #Creating a for loop to fill the array
    for i in range(number):
        #Turning i+1 into a string
        a=str(i+1)
        #Adding the generated label to the array
        array.append("Person " + a + message)
    #Returning the generated array
    return array

#A function to create an array of consecutive numbers as strings
def createArray(number):
    #Creating a blank array in order to store the generated array
    array=[]
    #Creating a for loop in order to generate the array
    for i in range(number):
        #Adding the generated string to the array
        array.append(str(i))
    return array

def rootSubmit():
    global details
    details=[]
    for name in rootNameEntries:
        details.append(rootNameEntries[name].get())
        details.append(rootEmailEntries[name].get())
    root.destroy()

#-------------------------------------------------------------------------------


#-------------------------------MAIN METHOD-------------------------------------

#-------------------------------SETUP WINDOW------------------------------------

numberOfParticipants=0

#Creating a setup window
setup = Tk()
#Titling the setup window
setup.title("Setup")

#Setting the icon to a picture of santa
setup.iconbitmap("santa.ico")

#Setting the height and width of the setup window
width, height = setup.winfo_screenwidth(), setup.winfo_screenheight()
#Setting the height and width to a fourth of the screen size
setup.geometry('%dx%d+0+0' % (width/5,height/10))
#Ensuring the setup window is ontop of the root window
setup.attributes("-topmost", True)

#List of all the label texts
setupLabelNames=["What is your e-mail?", "What is your password?", "How many participants?"]
#list of all the names of the entries for the setup window
setupEntryNames=["userEmail", "userPassword", "numberOfParticipants"]
#Creating a blank set to store the entries in so that you can refer back to them later
setupEntries={}

#Calling the createFields function to create the fields for the setup window
createLabels(setup, setupLabelNames, 1, 0)
#Calling the setupEntries function to create the entries for the setup window. The function then returns a set containing all the entries so that they can be referred to
setupEntries = createEntries(setup, setupEntryNames, 1, 0, padx=10)

#Setting the password entry field to display * instead of normal characters
setupEntries["userPassword"].config(show="*")

#Creating the submit button
setupSubmit = Button(setup, text="Submit", command=setupComplete).grid(row=4, column=1, pady=15)

#Running a loop of the setup window
setup.mainloop()
#-------------------------------------------------------------------------------


#--------------------------------ROOT WINDOW------------------------------------

#Creating a root window for the GUI
root = Tk()
#Titling the root window
root.title("Secret Santa")
#Setting the icon to a picture of santa
root.iconbitmap("santa.ico")
#Setting the height and width of the root window
width, height = root.winfo_screenwidth(), root.winfo_screenheight()
#Setting the height and width to a third of the screen size
root.geometry('%dx%d+0+0' % (width/3,height/3))

#Creating all the labels and entries in the root window
createLabels(root, nameLabels, 2, 0, pady=(10,0))
rootNameEntries = createEntries(root, nameEntryFields, 2, 0, pady=(10,0))
createLabels(root, emailLabels, 2, 1)
rootEmailEntries = createEntries(root, emailEntryFields, 2, 1)

#Creating a submit button on the root window
rootSubmitButton = Button(root, text="Submit", command=rootSubmit).grid(column=2, pady=20, sticky=S)

#Creating a loop for the root window to run in
root.mainloop()
#-------------------------------------------------------------------------------


#----------------------COMPLETE WINDOW------------------------------------------

#Creating a new window which will show up when the program has sent all the e-mails
complete = Tk()
#Setting the icon to a picture of santa
complete.iconbitmap("santa.ico")
#Ensuring the window appears ontop of all other windows
complete.attributes("-topmost", True)
#Setting the title of the window to complete
complete.title("Complete")
#Creating a label to say Done!
completeLabel = Label(complete, text="Done!")
#Packing the label in the complete window
completeLabel.pack()

#--------------------------LOGIC------------------------------------------------

#Creating a counter
counter = 1
#Setting the selectedPersonID to the first person
selectedPersonID = 0
#Creating a blank array to keep track of who has already been chosen
chosen =[]

#Creating a while loop to cycle through all the participants
while counter<=numberOfParticipants:
    #Creating a boolean to check when someone ellegible has been chosen
    done = False
    #Creating a while loop to pick an ellegible participant
    while done == False:
        #Generates a random number between 0 and one less than the number of participants as the array starts from 0
        randNumber = randint(0,numberOfParticipants-1)
        #Gets the name of the person chosen
        selectedPerson = details[selectedPersonID]
        #If the person selected is the same person chosen then reject the choice
        if selectedPerson == details[randNumber*2]:
            pass
        #If the chosen person has already been chosen then reject the choice
        elif (randNumber*2) in chosen:
            pass
        #If the chosen person passes the previous two conditions then they are ellegible
        else:
            #Add the chosen person to the chosen array
            chosen.append(randNumber*2)
            #Set done to true to break the loop
            done = True

    #Gets the address of the selected person
    address = details[(selectedPersonID+1)]
    #Gets the name of the chosen person
    secretName = details[randNumber*2]
    #Calling the sendEmail function to sent the selected person the chosen person's name
    sendEmail(address, secretName, userEmailAddress, userEmailPassword)
    #Increases the counter by 1
    counter = counter+1
    #Increases the selected personID by two to select the next person
    selectedPersonID = selectedPersonID+2

#Creating a main loop to run the complete window in
complete.mainloop()
#-------------------------------------------------------------------------------
