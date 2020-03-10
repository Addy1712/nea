import tkinter
import datetime
import mysql.connector
from statistics import mode

def executequery(query,data,W): #procedure that creates a connection to the database and queries the data
    databaseconnection = mysql.connector.connect(user='PythonAPI', password='Password2',
                              host='213.171.200.102',
                              database='1407SQN')
    cursor = databaseconnection.cursor()
    cursor.execute(query,data)
    if W:
        cursor.close()
        databaseconnection.commit()
        databaseconnection.close()
        return cursor
    else:
        result = cursor.fetchall()
        cursor.close()
        databaseconnection.close()
        return result
        
    
def usercheck(username, password): #checks the database for the entered username and password
    users = executequery("SELECT * FROM Users ",None,False)
    userstate = False
    for user in users:
        if username == user[1]:
            if password == user[2]:
              userstate = True
    return userstate

def getinfo(username): #gets the users essential info for the program
    users = executequery("SELECT * FROM Users",None,False)
    userstate = False
    for user in users:
        if username == user[1]:
            truename = user[3]
            permissions = user[4]
            UserID=user[0]
    return permissions,truename,UserID

def Log(usernameentered,passwordentered): #used to check if the users info is correct and if not create error message
        userstate = usercheck(usernameentered,passwordentered)
        if userstate == True:
            root.destroy()
            permissions,truename,UserID =getinfo(usernameentered)
            Menu(permissions,truename,UserID)
        else:
            msg=tkinter.Tk()
            login_failure=tkinter.Message(msg, text ="password or username incorrect")
            login_failure.pack()
            close = tkinter.Button(msg,text="OK",command=lambda:msg.destroy())
            close.pack()
            msg.mainloop()

def Login(): #creates the login page
        global root
        root = tkinter.Tk()
        root.configure(background ='light blue')
        root.title("Login")
        root.geometry("450x200")
        title = tkinter.Label(root, text="Welcome to the login page for the 1407 squadron event planner").pack()
        username_label = tkinter.Label(root, text="Username:").pack(side=tkinter.LEFT)
        
        password_entry = tkinter.Entry(root,show="*")
        password_entry.pack(side=tkinter.RIGHT)
        password_label = tkinter.Label(root,text="Password:").pack(side=tkinter.RIGHT)
        
        username_entry = tkinter.Entry(root)
        username_entry.pack(side=tkinter.LEFT)
        
        login = tkinter.Button(root,text="Login",fg="red",command=lambda:Log(username_entry.get(),password_entry.get()))
        login.pack(side=tkinter.BOTTOM)
        root.mainloop()
        
def Events(permissions,name,UserID): #creates event page and displayes query results
        events = tkinter.Tk()
        events.configure(background ='light blue')
        events.title('Events')
        events.geometry("1080x700")
        title_text = str("Welcome to events " + name)
        title = tkinter.Label(events,text=(title_text)).pack(side=tkinter.TOP)
        result = executequery("SELECT * FROM Event",None,False)
        i=0
        eventid = []
        eventdates = []
        eventdatee = []
        eventname = []
        eventinfo = []
        bidsdueby = []
        eventtext = []
        event = []
        apply = []
        for eventR in result:
                eventid.append(eventR[0])
                eventname.append(eventR[1])
                eventdates.append(eventR[2].strftime("%d-%b-%Y"))
                eventdatee.append(eventR[3].strftime("%d-%b-%Y"))
                bidsdueby.append(eventR[4].strftime("%d-%b-%Y"))
                eventinfo.append(eventR[5])
                i+=1
        for i in range(0,i):
                eventtext.append("Event: "+ eventname[i]+" | Starts: "+eventdates[i]+" | ends: " +eventdatee[i]+" | Bids due by : "+bidsdueby[i]+" | extra info: " +eventinfo[i])
                event.append(tkinter.Label (events, text=eventtext[i]).pack())
                apply.append(tkinter.Button(events,text=(eventname[i]),command=lambda i=i:Apply_to_event(eventid[i],permissions,name,UserID)))
                apply[i].pack()
        back = tkinter.Button(events,text="Back to Menu",command=lambda:[events.destroy(),Menu(permissions,name,UserID)])
        back.pack(side = tkinter.BOTTOM)
        if permissions == 1:
                newevent = tkinter.Button(events,text="Add Event",command=lambda:[events.destroy(),New_event_form(name,permissions,UserID)])
                newevent.pack(side = tkinter.BOTTOM)
                managebids = tkinter.Button(events,text="Manage bids",command=lambda:[events.destroy(),Manage_Bids(name,permissions,UserID)])
                managebids.pack(side=tkinter.BOTTOM)
        bids = executequery("SELECT EventID FROM Bids",None,False)
        mostbid = executequery('SELECT Event.EventName FROM Event,Bids WHERE Event.EventID=Bids.BidID AND Bids.BidID ='+str(mode(bids[0])),None,False)
        mostbidtext=('most bidded for event is '+ mostbid[0][0])
        MostBidL = tkinter.Label(events,text=mostbidtext).pack(side = tkinter.RIGHT)
        
def Manage_Bids(name,permissions,UserID):
    bids = tkinter.Tk()
    bids.configure(background ='light blue')
    bids.title('Events')
    bids.geometry("1080x700")
    title_text = str("Welcome to events " + name)
    result = executequery("SELECT Bids.*,Users.TrueName,Event.EventName,Event.StartDate FROM Bids,Users,Event WHERE Bids.UserID=Users.UserID AND Bids.EventID=Event.EventID ORDER BY Selected ASC",None,False)
    BidID =[]
    i=0
    DateFrom =[]
    EName =[]
    CName =[]
    Statelist =[]
    bidtext=[]
    for Bid in result:
                BidID.append(Bid[0])
                DateFrom.append(Bid[6].strftime("%d-%b-%Y"))
                State= Bid[3]
                EName.append(Bid[5])
                CName.append(Bid[4])
                if State == 1:
                    Statelist.append("Approved")
                else:
                    Statelist.append("Unapproved")
                bidtext.append("Bid: "+str(BidID[i])+" | From: " +DateFrom[i]+" | Event: " +EName[i]+" | Cadet: "+ CName[i]+ " | Approved: "+Statelist[i])
                bid = tkinter.Label (bids, text=bidtext[i]).pack()
                if Statelist[i] == "Unapproved":
                    approve = tkinter.Button(bids,text='Approve', command = lambda i=i:[ApproveBid(BidID[i],permissions,name,UserID),bids.destroy()])
                    approve.pack()
                i+=1
    backtomenu=tkinter.Button(bids,text='Back to Events',command=lambda:[bids.destroy(),Events(permissions,name,UserID)])
    backtomenu.pack(side = tkinter.BOTTOM)

def ApproveBid(BidID,permissions,name,UserID):
    executequery("UPDATE Bids SET Selected =1 WHERE BidID ="+str(BidID),None,True)
    Manage_Bids(name,permissions,UserID)
                
def Absences(permissions,name,UserID): # creates absence page and displayes query results
        absences = tkinter.Tk()
        absences.title('Absences')
        absences.configure(background ='light blue')
        absences.geometry("1080x700")
        title_text = str("Welcome to absences " + name)
        title = tkinter.Label(absences,text=(title_text)).pack(side=tkinter.TOP)
        ID = str(UserID)
        result = executequery("SELECT * FROM Absences WHERE UserID ="+ID,None,False)
        for CurrentAbsence in result:
                AbsenceName = CurrentAbsence[0]
                DateFrom = CurrentAbsence[2].strftime("%d-%b-%Y")
                DateTo = CurrentAbsence[3].strftime("%d-%b-%Y")
                Reason = CurrentAbsence[4]
                State = CurrentAbsence[5]
                if State == 1:
                    State = "Approved"
                else:
                    State = "unapproved"
                absencetext = "absence: From: " +DateFrom+" | Until: " +DateTo+" | Reason: "+ Reason+ " | Approved: "+State
                absence = tkinter.Label (absences, text=absencetext).pack()
        if permissions == 1:
                review = tkinter.Button(absences, text='review absences', command=lambda:[absences.destroy(),Reviewabsences(permissions,name,UserID)])
                review.pack()
        NewAbsence = tkinter.Button(absences,text='New Absence',command=lambda:[absences.destroy(),NewAbsenceForm(permissions,name,UserID)])
        NewAbsence.pack()
        backtomenu=tkinter.Button(absences,text='Back to Menu',command=lambda:[absences.destroy(),Menu(permissions,name,UserID)])
        backtomenu.pack(side = tkinter.BOTTOM)

def NewAbsenceForm(permissions,name,UserID): # creates a new absence for for the user to complete
        new_absence_form = tkinter.Tk()
        new_absence_form.configure(background ='light blue')
        new_absence_form.geometry("1080x700")
        new_absence_form.title("New absence Form")
        Help = tkinter.Label(new_absence_form, text='Date Format: YYYY-MM-DD').pack()
        date_from = tkinter.Label(new_absence_form,text="Start date of absence:").pack()
        date_from_entry = tkinter.Entry(new_absence_form)
        date_from_entry.pack()
        end_date = tkinter.Label(new_absence_form,text="End date of absence:").pack()
        end_date_entry = tkinter.Entry(new_absence_form)
        end_date_entry.pack()
        reason = tkinter.Label(new_absence_form,text="Extra information for the absence:").pack()
        reason_entry = tkinter.Entry(new_absence_form)
        reason_entry.pack()
        create_absence = tkinter.Button(new_absence_form,text="Submit absence", command = lambda:[AddAbsence(date_from_entry.get(),end_date_entry.get(),reason_entry.get(),permissions,name,UserID),new_absence_form.destroy()])
        create_absence.pack()
        cancel_absence = tkinter.Button(new_absence_form,text="Cancel", command = lambda:[new_absence_form.destroy(),Absences(permissions,name,UserID)])
        cancel_absence.pack()
        new_absence_form.mainloop()

def AddAbsence(date_from,end_date,reason,permissions,name,UserID): # updates database with the new absence
        absence = executequery('SELECT AbsenceID FROM Absences ORDER BY EventID DESC',None,False)
        absenceid = absence[0][0] + 1
        executequery('INSERT INTO Absences (AbsenceID, UserID, DateFrom, DateTo, Reason, Approved) VALUES(%s, %s, %s, %s, %s, %s)',(absenceid,UserID,date_from,end_date,reason,'0'),True) 
        Absences(permissions,name,UserID)    

def Reviewabsences(permissions,name,UserID):         #shows staff all absences  
        absences2 = tkinter.Tk()
        absences2.configure(background ='light blue')
        absences2.title('Absences review')
        absences2.geometry("1080x700")
        title_text = str("Welcome to absences review " + name)
        i=0
        AbsenceID=[]
        AbsenceName=[]
        DateFrom=[]
        DateTo=[]
        Reason=[]
        Statelist=[]
        absencetext=[]
        AName=[]
        datearray=[]
        result = executequery("SELECT Absences.*,Users.TrueName FROM Absences,Users WHERE (Absences.UserID=Users.UserID)",None,False)
        for CurrentAbsence in result:
                AbsenceID.append(CurrentAbsence[0])
                DateFrom.append(CurrentAbsence[2].strftime("%d-%b-%Y"))
                DateTo.append(CurrentAbsence[3].strftime("%d-%b-%Y"))
                Reason.append(CurrentAbsence[4])
                State= CurrentAbsence[5]
                AName.append(CurrentAbsence[6])
                if State == 1:
                    Statelist.append("Approved")
                else:
                    Statelist.append("Unapproved")
                absencetext.append("absence: "+AName[i]+" | From: " +DateFrom[i]+" | until: " +DateTo[i]+" | Reason: "+ Reason[i]+ " | Approved: "+Statelist[i])
                absence = tkinter.Label (absences2, text=absencetext[i]).pack()
                if Statelist[i] == "Unapproved":
                    approve = tkinter.Button(absences2,text='Approve', command = lambda i=i:[ApproveAbsence(AbsenceID[i],permissions,name,UserID),absences2.destroy()])
                    approve.pack()
                a = int(CurrentAbsence[2].strftime("%Y%m%d"))
                b = int(CurrentAbsence[3].strftime("%Y%m%d"))
                counter =0
                for date in range(a,b):
                    date = datetime.datetime.strptime(str(date),'%Y%m%d').weekday()
                    if date == 0 or date ==3:
                        counter +=1
                datearray.append([counter,AName[i]])
                i+=1
        mostabsence = max(datearray)
        mostabsencetext = str(mostabsence[1]) +" is the most planned absent with "+  str(mostabsence[0]) +" days"
        mostABcentlabel = tkinter.Label(absences2,text=mostabsencetext).pack(side=tkinter.LEFT)
        backtomenu=tkinter.Button(absences2,text='Back to Absences',command=lambda:[absences2.destroy(),Absences(permissions,name,UserID)])
        backtomenu.pack(side = tkinter.BOTTOM)

def ApproveAbsence(AbsenceID,permissions,name,UserID): #updates the absences to have an approved state
        executequery("UPDATE Absence SET State =%d   WHERE AbsenceID="+str(AbsenceID),(1),True)
        Reviewabsences(permissions,name,UserID)
        
def Users(permissions,name,UserID): #shows the user their current details
        users= tkinter.Tk()
        users.configure(background ='light blue')
        users.title('Users')
        users.geometry("1080x700")
        title_text = str("Welcome to Users " + name)
        title = tkinter.Label(users,text=(title_text)).pack(side=tkinter.TOP)
        result = executequery("SELECT * FROM Users",None,False)
        i=0
        for user in result:
            if user[0] == UserID:
                if permissions == 1:
                    access = 'Staff'
                else:
                    access = 'Cadet'
                info ='User ID: '+ user[1]+' | Username: '+user[2]+" | User's name: "+user[3]+' | Access level: '+access
                userinfo = tkinter.Label(users,text =info)
                userinfo.pack()
                useredit =tkinter.Button(users,text=('Change details?'),command = lambda:[users.destroy(),ChangeUserInfo(permissions,name,UserID)])
                useredit.pack()
        if permissions ==1:
            viewusers=tkinter.Button(users,text='view users',command=lambda:[users.destroy(),ViewUsers(permissions,name,UserID)])
            viewusers.pack(side = tkinter.BOTTOM)
        backtomenu=tkinter.Button(users,text='Back to Menu',command=lambda:[users.destroy(),Menu(permissions,name,UserID)])
        backtomenu.pack(side = tkinter.BOTTOM)

def ViewUsers(permissions,name,UserID): # shows staff all users details(not including passwords)
    users2 = tkinter.Tk()
    users2.configure(background ='light blue')
    users2.title('Users')
    users2.geometry("1080x700")
    title_text = str("Welcome to Users " + name)
    title = tkinter.Label(users2,text=(title_text)).pack(side=tkinter.TOP)
    users = executequery("SELECT * FROM Users",None,False)
    ID =[]
    Username =[]
    TrueName=[]
    staff =[]
    i=0
    usertext=[]
    for user in users:
        ID.append(user[0])
        Username.append(user[1])
        TrueName.append(user[3])
        staff.append(user[4])
        if staff[i] ==1:
            access = 'staff'
        else:
            access = 'cadet'
        usertext.append('User ID: '+str(ID[i])+' | Username: '+Username[i]+" | User's Name: "+TrueName[i]+' | Access level: '+access)
        userlabel = tkinter.Label(users2, text=usertext[i]).pack()
        edituser = tkinter.Button(users2,text="edit user", command = lambda i=i:[EditUser(ID[i],Username[i],TrueName[i],staff[i],permissions,name,UserID),users2.destroy()])
        edituser.pack()
        i+=1
    backtomenu=tkinter.Button(users2,text='Back to Menu',command=lambda:[users2.destroy(),Menu(permissions,name,UserID)])
    backtomenu.pack(side = tkinter.BOTTOM)

def EditUser(ID,UserName,TrueName,staff,permissions,name,UserID):
    edituser= tkinter.Tk()
    edituser.title('Edit User Info')
    edituser.configure(background ='light blue')
    edituser.geometry("1080x700")
    title_text = str("Welcome to Edit User Info " + name)
    title = tkinter.Label(edituser,text=(title_text)).pack(side=tkinter.TOP)
    Username = tkinter.Label(edituser,text="Username:").pack()
    Username_entry = tkinter.Entry(edituser)
    Username_entry.insert(0,UserName)
    Username_entry.pack()
    Password = tkinter.Label(edituser,text="Password:").pack()
    Password_entry = tkinter.Entry(edituser)
    Password_entry.pack()
    Truename = tkinter.Label(edituser,text="TrueName:").pack()
    Truename_entry = tkinter.Entry(edituser)
    Truename_entry.pack()
    Truename_entry.insert(0,TrueName)
    permissionl = tkinter.Label(edituser,text='Permissions (staff/cadet):').pack()
    permissions_entry = tkinter.Entry(edituser)
    permissions_entry.pack()
    if staff == 1:
        staff = 'Staff'
    else:
        staff = 'Cadet'
    permissions_entry.insert(0,staff)
    update  = tkinter.Button(edituser,text = 'Change', command = lambda:[changeuser(ID,permissions_entry.get(),Username_entry.get(),Password_entry.get(),Truename_entry.get(),permissions,name,UserID), edituser.destroy()])
    update.pack()
    cancel = tkinter.Button(edituser,text='Cancel',command = lambda: [edituser.destroy(),ViewUsers(permissions,name,UserID)])
    cancel.pack(side = tkinter.BOTTOM)
                                           
def changeuser(ID, staff,Username,Password,TrueName,permissions,name,UserID): # updates the users account
    if staff.lower() == 'staff':
        staff = 1
    else:
        staff = 0
    executequery("UPDATE Users SET Username = %s, Password = %s, TrueName = %s Staff = %d WHERE UserID =%d",(Username,Password,TrueName,ID,staff),True)
    ViewUsers(permissions,name,UserID)

def ChangeUserInfo(permissions,name,UserID): #creates a form for changing details of a user account
    editinfo= tkinter.Tk()
    error = False
    editinfo.title('Edit User Info')
    editinfo.configure(background ='light blue')
    editinfo.geometry("1080x700")
    title_text = str("Welcome to Edit User Info " + name)
    title = tkinter.Label(editinfo,text=(title_text)).pack(side=tkinter.TOP)
    result = executequery("SELECT * FROM Users",None,False)
    userid = UserID
    Username = tkinter.Label(editinfo,text="Username:").pack()
    Username_entry = tkinter.Entry(editinfo)
    Username_entry.pack()
    Password = tkinter.Label(editinfo,text="Password:").pack()
    Password_entry = tkinter.Entry(editinfo)
    Password_entry.pack()
    TrueName = tkinter.Label(editinfo,text="TrueName:").pack()
    TrueName_entry = tkinter.Entry(editinfo)
    TrueName_entry.pack()
    update  = tkinter.Button(editinfo,text = 'Update', command = lambda:[updateuser(permissions,Username_entry.get(),Password_entry.get(),TrueName_entry.get(),userid), editinfo.destroy(),])
    update.pack()
    backtomenu=tkinter.Button(editinfo,text='Back to Menu',command=lambda:[editinfo.destroy(),Menu(permissions,name,UserID)])
    backtomenu.pack(side = tkinter.BOTTOM)

def updateuser(permissions,Username,Password,TrueName,UserID): # updates the users account
    executequery("UPDATE Users SET Username = %s, Password = %s, TrueName = %s WHERE UserID =%d",(Username,Password,TrueName,UserID),True)
    Login()
            
def Menu(permissions,name,UserID): # creates main menu 
        menu=tkinter.Tk()
        menu.configure(background ='light blue')
        menu.title("Menu")
        menu.geometry("1080x700")
        title_text = str("Welcome to the main menu " + name)
        title = tkinter.Label(menu,text=(title_text)).pack(side=tkinter.TOP)
        event = tkinter.Button(menu,text="events",command=lambda:[menu.destroy(),Events(permissions,name,UserID)])
        event.pack()
        absence = tkinter.Button(menu,text="absence",command=lambda:[Absences(permissions,name,UserID),menu.destroy()])
        absence.pack()
        if permissions == 1:
                user = tkinter.Button(menu,text="users",command=lambda:[Users(permissions,name,UserID),menu.destroy()])
                user.pack()
        Logout = tkinter.Button(menu,text="logout",fg="red",command=lambda:[menu.destroy(),Login()])
        Logout.pack(side = tkinter.BOTTOM)
        menu.mainloop()
def Apply_to_event(eventid,permissions,name,UserId): # creates a bid record
    bids = executequery('SELECT BidID FROM Bids ORDER BY BidID DESC',None,False)
    eventid = bids[0][0] + 1
    executequery('INSERT INTO Bids (BidID, EventID, UserID, Selected) VALUES(%s, %s, %s, %s)',(eventid, eventid,UserId,'0'),True) 
    Events(permissions,name,UserID)
    
        
def New_event_form(name,permissions,UserID): #creates a form to create a new event
        new_event_form = tkinter.Tk()
        new_event_form.configure(background ='light blue')
        new_event_form.geometry("1080x700")
        new_event_form.title("New Event Form")
        Help = tkinter.Label(new_event_form, text='Date Format: YYYY-MM-DD').pack()
        date_from = tkinter.Label(new_event_form,text="Start date of event:").pack()
        date_from_entry = tkinter.Entry(new_event_form)
        date_from_entry.pack()
        end_date = tkinter.Label(new_event_form,text="End date of event:").pack()
        end_date_entry = tkinter.Entry(new_event_form)
        end_date_entry.pack()
        bid_date = tkinter.Label(new_event_form,text="bids are due by:").pack()
        bid_date_entry = tkinter.Entry(new_event_form)
        bid_date_entry.pack()
        name = tkinter.Label(new_event_form,text="Name of event:").pack()
        name_entry = tkinter.Entry(new_event_form)
        name_entry.pack()
        info = tkinter.Label(new_event_form,text="Extra information for the event:").pack()
        info_entry = tkinter.Entry(new_event_form)
        info_entry.pack()
        create_event = tkinter.Button(new_event_form,text="Create Event", command = lambda:[Add_event(date_from_entry.get(), end_date_entry.get(),bid_date_entry.get(),name_entry.get(),info_entry.get(),name,permissions,UserID),new_event_form.destroy()])
        create_event.pack()
        cancel_event = tkinter.Button(new_event_form,text="Cancel", command = lambda:[new_event_form.destroy(),Events(permissions,name,UserID)])
        cancel_event.pack()
        new_event_form.mainloop()

def Add_event(date_from,date_to,bid_date,name,info,username,permissions,UserID): #adds event to the database
        events = executequery('SELECT EventID FROM Event ORDER BY EventID DESC',None,False)
        eventid = events[0][0] + 1
        executequery('INSERT INTO Event (EventID, EventName, StartDate, EndDate, BidsDueBy, Description) VALUES(%s, %s, %s, %s, %s, %s)',(eventid, name, date_from, date_to, bid_date, info),True) 
        Events(permissions,username,UserID)
        
if __name__ == "__main__":
            Login()


