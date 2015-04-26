from datetime import datetime, date, timedelta
import sys
import MySQLdb
import calendar

# InputDay = calander.weekday(YYYYMMDD) outputs day in number 0-6 with 0 as monday
# if SearchedDay > InputDay:

conn=MySQLdb.connect(host="localhost", user="root", passwd="MIYE",db="miye_hotel_sys")

##Check user and assign admin number
userCheck=True
while userCheck:
    
    userName=input(" Please enter your name with a . between first and last ")
    admin = -1

    try:
           cursor0=conn.cursor()
           cursor0.execute ("""
           SELECT AdminID FROM t_admin
           WHERE t_admin.UserName = '%s';
           """ % userName)

           while(1):
               row=cursor0.fetchone()
               if row==None:
                   break

               admin= row[0]

               if admin >= 0:
                   userCheck = None

               else:
                   userCheck = True

    except MySQLdb.Error:
           print ("Error connecting to MySQL")
           sys.exit(1)
    cursor0.close()

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
      print("The day of the week is " + str(calendar.weekday(dateIN_object.year, dateIN_object.month, dateIN_object.day)))

      resCheckOutDate=input("What day will you be checking out? MM-DD-YY ")

      datetimeOUT_object = datetime.strptime(resCheckOutDate, formatter_string)
      dateOUT_object = datetimeOUT_object.date()
      
##      print(dateOUT_object)
      day_count = (datetimeOUT_object - datetimeIN_object).days + 1
      for single_date in (datetimeIN_object + timedelta(n) for n in range(day_count)):
        print(single_date.strftime("%Y-%m-%d"))

#      d = dateIN_object.
#      delta = datetime.
#      while d <= dateOUT_object:
#          print (d.strftime("%Y-%m-%d"))
#          d += 1

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
           AND t_roomguest.Canceled = 0
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
##            roomCost=float(input("What was charged per room? "))
##              if roomCap == 1 AND calendar.weekday(dateIN_object.year, dateIN_object.month, dateIN_object.day) >= 6 AND  dateIN_object.month, dateIN_object.day
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
                           SELECT RoomID, WkDayOffPrice, WkEndOffPrice, WkDayOnPrice, WkEndOnPrice FROM t_room
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
##Determine total price for rooms
                                   roomCost=float = 0
                                   day_count = (datetimeOUT_object - datetimeIN_object).days
                                   for single_date in (datetimeIN_object + timedelta(n) for (n) in range(day_count)):

                                       if (calendar.weekday(single_date.year, single_date.month, single_date.day)) <= 4:

                                           if ((int(single_date.strftime("%m")) > 1) & (int(single_date.strftime("%m")) < 5)):
                                               print('Off Season Weekday')
                                               roomCost += row[1]

                                           elif ((int(single_date.strftime("%m")) > 8) & (int(single_date.strftime("%m")) < 12)):
                                               print('Off Season Weekday')
                                               roomCost += row[1]

                                           elif ((int(single_date.strftime("%m")) == 1) & (int(single_date.strftime("%d")) > 15)):
                                               print('Off Season Weekday')
                                               roomCost += row[1]

                                           elif ((int(single_date.strftime("%m")) == 12) & (int(single_date.strftime("%d")) < 15)):
                                               print('Off Season Weekday')
                                               roomCost += row[1]

                                           elif ((int(single_date.strftime("%m")) == 5) & (int(single_date.strftime("%d")) < 15)):
                                               print('Off Season Weekday')
                                               roomCost += row[1]

                                           elif ((int(single_date.strftime("%m")) == 8) & (int(single_date.strftime("%d")) > 15)):
                                               print('Off Season Weekday')
                                               roomCost += row[1]

                                           else:
                                               print('In Season Weekday')
                                               roomCost += row[3]

                                       else:

                                           if ((int(single_date.strftime("%m")) > 1) & (int(single_date.strftime("%m")) < 5)):
                                               print('Off Season Weekend')
                                               roomCost += row[2]

                                           elif ((int(single_date.strftime("%m")) > 8) & (int(single_date.strftime("%m")) < 12)):
                                               print('Off Season Weekend')
                                               roomCost += row[2]

                                           elif ((int(single_date.strftime("%m")) == 1) & (int(single_date.strftime("%d")) > 15)):
                                               print('Off Season Weekend')
                                               roomCost += row[2]

                                           elif ((int(single_date.strftime("%m")) == 12) & (int(single_date.strftime("%d")) < 15)):
                                               print('Off Season Weekend')
                                               roomCost += row[2]

                                           elif ((int(single_date.strftime("%m")) == 5) & (int(single_date.strftime("%d")) < 15)):
                                               print('Off Season Weekend')
                                               roomCost += row[2]

                                           elif ((int(single_date.strftime("%m")) == 8) & (int(single_date.strftime("%d")) > 15)):
                                               print('Off Season Weekend')
                                               roomCost += row[2]

                                           else:
                                               print('In Season Weekend')
                                               roomCost += row[4]

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
      cursor.execute ("SELECT RoomID, RoomInvoice FROM t_roomguest WHERE Canceled = 0 AND RoomID = %s AND CheckIn = %s", (roomNum, dateIN_object))
      row=cursor.fetchone()
      if row==None:
           print ("No reservation found with that information")

      else:
           today = datetime.today()
           refundMult = float = 0
           if (datetimeIN_object - today).days > 21:
               refundMult = 1
           elif (datetimeIN_object - today).days > 3:
               refundMult = .75
           else:
               refundMult = 0

           refund = row[1] * refundMult
           cursor.execute ("UPDATE t_roomguest SET RoomRefund = %s, Canceled = 1 WHERE Canceled = 0 AND RoomID = %s AND CheckIn = %s", (refund, roomNum, dateIN_object))
           print ("Reservation canceled. Refund is ", refund)

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

       
    
