from datetime import datetime,date
import sys
import MySQLdb
import calendar

# InputDay = calander.weekday(YYYYMMDD) outputs day in number 0-6 with 0 as monday
# if SearchedDay > InputDay:

conn=MySQLdb.connect(host="localhost", user="root", passwd="MIYE",db="miye_hotel_sys")

##Check user and assign admin number
userCheck=True
while userCheck:
    
    userCheck=input(" Please enter your name with a . between first and last ")

    if userCheck=="Jack.Torrance":
        user="Jack.Torrance"
        admin="1"
        userCheck = None
    elif userCheck=="Wendy.Torrance":
        user="Wendy.Torrance"
        admin="2"
        userCheck = None
    elif userCheck=="Danny.Torrance":
        user="Danny.Torrance"
        admin="3"
        userCheck = None
    elif userCheck=="Dick.Hallorann":
        user="Dick.Hallorann"
        admin="4"
        userCheck = None
    elif userCheck=="Delbert.Grady":
        user="Delbert.Grady"
        admin="5"
        userCheck = None
    elif userCheck=="y.y":
        user="y.y"
        admin="6"
        userCheck = None
        
##Main Menu
ans=True
while ans:
    print("""
    1. Reserve Room
    2. Cancel Reservation
    3. Reserve Service
    4. Cancel Service
    5. Exit
    """)
    ans=input("What would you like to do? ")

##Get Check in and out dates
    if ans=="1":

      resCheckInDate=input("What day will you be checking in? MM-DD-YY " )

      formatter_string="%m-%d-%y"
      datetimeIN_object = datetime.strptime(resCheckInDate, formatter_string)
      dateIN_object = datetimeIN_object.date()

      print(dateIN_object)
      print("The day of the week is " + calander.weekday(dateIN_object))
      
      resCheckOutDate=input("What day will you be checking out? MM-DD-YY ")

      datetimeOUT_object = datetime.strptime(resCheckOutDate, formatter_string)
      dateOUT_object = datetimeIN_object.date()
      
##      print(dateOUT_object)

## Find the number of vacancies for each type of room
      single_vac = 0
      double_vac = 0
      quadruple_vac = 0

      try:
           cursor1=conn.cursor()
           cursor1.execute ("""
           SELECT RoomID, RoomType FROM t_room
           WHERE NOT EXISTS (SELECT RoomID FROM t_roomguest
           WHERE t_room.RoomID=t_roomguest.RoomID
           AND(t_roomguest.CheckIn < %s AND t_roomguest.CheckOut > %s));
           """, (datetimeOUT_object, datetimeIN_object ))

           while(1):
               row=cursor1.fetchone()
               if row==None:
                   break
 ##              print("%s" %(row[0]))
               if row[1] == "single":
                   single_vac = single_vac + 1
               elif row[1] == "double":
                   double_vac = double_vac + 1
               elif row[1] == "quadruple":
                   quadruple_vac = quadruple_vac + 1




      except MySQLdb.Error:
           print ("Error connecting to MySQL")
           sys.exit(1)
      cursor1.close()

      print(single_vac, " Single Rooms Available")
      print(double_vac, " Double Rooms Available")
      print(quadruple_vac, "  Quadruple Rooms Available")

##Select room type and quantity, along with payment information
      while(1):
          print("""
          Please select a room type code to reserve
          1. Single Room
          2. Double Room
          4. Quadruple Room
          0. Main Menu
          
          """)
          roomCap=int(input())
##          print ("roomCap ", roomCap)
          if roomCap==0:
              break
          else:
              roomCount=int(input("How many would you like to reserve? "))
              roomCost=float(input("What was charged per room? "))
              count1 = 0
              stop1 = 1

##Get room numbers that are available for the selected room type              
              while(1):
                  if stop1 == 0:
                      break
                  else:
                      try:
                           cursor2=conn.cursor()
                           cursor2.execute ("""
                           SELECT RoomID FROM t_room
                           WHERE t_room.MaxGuestAllowed = %s
                           AND NOT EXISTS (SELECT RoomID FROM t_roomguest
                           WHERE t_room.RoomID=t_roomguest.RoomID
                           AND(t_roomguest.CheckIn < %s AND t_roomguest.CheckOut > %s));
                           """, (roomCap, datetimeOUT_object, datetimeIN_object ))


                           while(1):
                               row=cursor2.fetchone()
                               if row==None:
                                   break                                    
                               elif count1 >= roomCount:
                                   stop1 = 0
                                   break
                           
                               else:
##Insert reservation into t_roomguest for the selected number of rooms                                   
                                   try:
                                        cursor3=conn.cursor()
                                        cursor3.execute ("""
                                        INSERT INTO t_roomguest (RoomID, CheckIn, CheckOut, RoomInvoice, AdminID)
                                        VALUES (%s, %s, %s, %s, %s);
                                        """, (row[0], datetimeIN_object, datetimeOUT_object, roomCost, admin))
                                        conn.commit()
##                                        print ("One row inserted")
                                   except MySQLdb.Error:
                                        print ("Error connecting to MySQL")
                                        sys.exit(1)
                                   cursor3.close()
                                   
                                   print("Room number ", "%s" %(row[0]), " reserved from ", resCheckInDate, " to ", resCheckOutDate)   
                                   count1 = count1 + 1
                                   
                      except MySQLdb.Error:
                           print ("Error connecting to MySQL")
                           sys.exit(1)
                      cursor2.close()



    elif ans=="2":
        
      roomNum=int(input("What is the room number? "))
      resCheckInDate=input("What is the check in date? MM-DD-YY " )
      formatter_string="%m-%d-%y"
      datetimeIN_object = datetime.strptime(resCheckInDate, formatter_string)
      dateIN_object = datetimeIN_object.date()
      print(dateIN_object)
      cursor=conn.cursor()
      cursor.execute ("SELECT RoomID FROM t_roomguest WHERE RoomID = %s AND CheckIn = %s", (roomNum, dateIN_object))
      row=cursor.fetchone()
      if row==None:
           print ("No reservation found with that information")

      else:
           cursor.execute ("DELETE FROM t_roomguest WHERE RoomID = %s AND CheckIn = %s", (roomNum, dateIN_object))
           print ("Reservation deleted")
      cursor.close()
      conn.commit()

    elif ans=="3":
      print("\n What type of service would you like to reserve?")

    elif ans=="4":
      print("\n What is the reservation number?")

    elif ans=="5":
      print("\n Goodbye")
      conn.close()
      ans = None
    else:
       print("\n Not valid choice try again")

       
