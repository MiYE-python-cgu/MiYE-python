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
    3. Reserve Spa Service
    4. Cancel Spa Service
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

        print("What type of service would you like to reserve?")

        try:
            cursor4=conn.cursor()
            print ("The following services are available")
            print ("SpaID\t\tService\t\t\t\tPrice Per Minute")
            cursor4.execute ("SELECT SpaID, SpaService, PricePerMinute FROM t_spaservice;")

            while(1):

                row=cursor4.fetchone()
                if row==None:
                    break

                else:
                    print ('{:<10} {:<20} {:^30}'.format(row[0], row[1], row[2]))

            spaSelect=input("Select the SpaID you would like to reserve (select 0 to exit) ")
            if spaSelect == 0:
                break

            else:
                stop2 = 1

                while(1):

                    if stop2 == 0:
                      break

                    try:
                        cursor5=conn.cursor()
                        cursor5.execute ("""
                        SELECT Capacity, PricePerMinute, Available30, Available60, Available90 FROM t_spaservice
                        WHERE t_spaservice.SpaID=%s;
                        """, (spaSelect))

                        row=cursor5.fetchone()
                        if row==None:
                            print("There is no spa service matching that ID.")

                        else:

                            print("Please enter the duration or your spa service in minutes from the options below:")
                            if row[2] == 1:
                                print("30")
                            if row[3] == 1:
                                print("60")
                            if row[4] == 1:
                                print("90")

                            spaDuration= int(input())
                            spaCharge = float(spaDuration) * row[1]

                            if ((row[2] == 1) & (spaDuration == 30)) | ((row[3] == 1) & (spaDuration == 60)) | ((row[4] == 1) & (spaDuration == 90)):

                                spaInTime=input("What time and date would you like the spa service? HH:MM MM-DD-YY " )

                                formatter_string2="%I:%M %m-%d-%y"

                                spaTimeIN = datetime.strptime(spaInTime, formatter_string2)

                                spaTimeIN_object = datetime
                                spaTimeOUT_object = datetime

                                if spaTimeIN.hour < 8:
                                    spaTimeIN_object = spaTimeIN + timedelta(0,0,0,0,0,12,0)
                                    spaTimeOUT_object = spaTimeIN_object + timedelta(0,0,0,0,spaDuration,0,0)

                                else:
                                    spaTimeIN_object = spaTimeIN
                                    spaTimeOUT_object = spaTimeIN_object + timedelta(0,0,0,0,spaDuration,0,0)

                                print ('spaTimeIN_object =', spaTimeIN_object)
                                print ('spaTimeOUT_object =', spaTimeOUT_object)

                                guestName=input("What is the guests name? " )

                                roomNumCheck = input("What is the guest's room number? " )
                                roomNum2 = int(roomNumCheck)

                                spaDate = spaTimeIN_object.date()

                                reserveSpa = 1

                                try:
                                    cursor9=conn.cursor()

                                    cursor9.execute ("""
                                    SELECT RoomID FROM t_roomguest
                                    WHERE Canceled = 0 AND RoomID = %s
                                    AND ((CheckIn < %s AND CheckOut > %s)
                                    OR (CheckIn = %s) OR (CheckOut = %s));""", (roomNum2, spaDate, spaDate, spaDate, spaDate))

                                    #     ("""
                                    # SELECT RoomID FROM t_roomguest
                                    # WHERE t_roomguest.RoomID = %s;
                                    # """, (roomNum))

                                    #, spaDate, spaDate
                                    # AND t_roomguest.CheckIn =< %s AND t_roomguest.CheckOut >= %s;
                                    row4=cursor9.fetchone()
                                    print("room check")

                                    if row4==None:

                                        reserveSpa = 0
                                        stop2 = 0
                                        print("Only guests at the resort may schedule services")
                                        break

                                except MySQLdb.Error:
                                    print ("Error connecting to MySQL BUT WHY?")
                                    sys.exit(1)
                                cursor9.close()

                                try:
                                    cursor6=conn.cursor()
                                    cursor6.execute ("""
                                    SELECT SpaID, StartTime, EndTime, GuestName FROM t_spaguest
                                    WHERE t_spaguest.SpaID = %s AND t_spaguest.StartTime < %s AND t_spaguest.EndTime > %s;
                                    """, (spaSelect, spaTimeOUT_object, spaTimeIN_object))

                                    count2=0
                                    print('spa conflict check')
                                    while(1):
                                        row2=cursor6.fetchone()

                                        print("count2 = ", count2)

                                        if row2==None:
                                            break

                                        elif guestName == row2[3]:
                                            print("The guest has a conflicting spa reservation SpaID: ", row[0], "Start Time ", row[1], "End Time: ", row[2])
                                            reserveSpa = 0
                                            stop2 = 0

                                        elif count2 >= (row[0] - 1):
                                            print("That service has no reservations available at that time")
                                            reserveSpa = 0
                                            stop2 = 0

                                        else:
                                            count2 += 1


                                except MySQLdb.Error:
                                    print ("Error connecting to MySQL")
                                    sys.exit(1)
                                cursor6.close()

                                if spaSelect == '1':

                                    bathBuffIN = spaTimeIN_object + timedelta(0,0,0,0,1,-2,0)
                                    bathBuffOUT = spaTimeOUT_object + timedelta(0,0,0,0,-1,2,0)

                                    try:

                                        cursor7=conn.cursor()
                                        cursor7.execute ("""
                                        SELECT SpaID FROM t_spaguest
                                        WHERE t_spaguest.SpaID = 1 AND GuestName = %s AND t_spaguest.StartTime < %s AND t_spaguest.EndTime > %s;
                                        """, (guestName, bathBuffOUT, bathBuffIN))

                                        row3=cursor7.fetchone()
                                        print("bath check")

                                        if row3==None:

                                            break

                                        else:
                                            reserveSpa = 0
                                            stop2 = 0
                                            print("You cannot schedule mineral baths within two hours of one another")

                                    except MySQLdb.Error:
                                        print ("Error connecting to MySQL")
                                        sys.exit(1)
                                    cursor7.close()

                                if reserveSpa == 1:


                                    try:

                                        cursor8=conn.cursor()
                                        cursor8.execute ("""
                                        INSERT INTO t_spaguest (SpaID, StartTime, EndTime, SpaInvoice, AdminID, GuestName)
                                        VALUES (%s, %s, %s, %s, %s, %s);
                                        """, (spaSelect, spaTimeIN_object, spaTimeOUT_object, spaCharge, admin, guestName))
                                        conn.commit()
                                        print ("One row inserted")
                                        stop2 = 0

                                    except MySQLdb.Error:
                                        print ("Error connecting to MySQL")
                                        sys.exit(1)
                                    cursor8.close()


                            else:
                                print("Not a valid duration please try again")


                    except MySQLdb.Error:
                        print ("Error connecting to MySQL")
                        sys.exit(1)
                    cursor5.close()


        except MySQLdb.Error:
            print ("Error connecting to MySQL")
            sys.exit(1)
        cursor4.close()

    elif ans=="4":

        guestName=input("What is the guest's name? " )
        spaInTime=input("What is the time and date of the spa service reservation? HH:MM MM-DD-YY " )
        formatter_string2="%I:%M %m-%d-%y"
        spaTimeIN = datetime.strptime(spaInTime, formatter_string2)
        spaTimeIN_object = datetime

        if spaTimeIN.hour < 8:
            spaTimeIN_object = spaTimeIN + timedelta(0,0,0,0,0,12,0)

        else:
            spaTimeIN_object = spaTimeIN

        print(spaTimeIN_object)
        cursor=conn.cursor()
        cursor.execute ("SELECT GuestID, SpaInvoice, StartTime, ReservationTime FROM t_spaguest WHERE Canceled = 0 AND GuestName = %s AND StartTime = %s", (guestName, spaTimeIN_object))
        row=cursor.fetchone()

        if row==None:

            print ("No spa reservation found with that information")

        else:
            today = datetime.today()
            refund = 0

            if (today + timedelta(0,0,0,0,90,0,0)) < row[2]:
                refund = 1
            elif (row[3] + timedelta(0,0,0,0,10,0,0)) > today:
                refund = 1
            else:
                refund = 0

            spaRefund = row[1] * refund
            cursor.execute ("UPDATE t_spaguest SET SpaRefund = %s, Canceled = 1 WHERE Canceled = 0 AND GuestName = %s AND StartTime = %s", (spaRefund, guestName, spaTimeIN_object))
            print ("Spa Reservation canceled. Refund is ", spaRefund)

        cursor.close()
        conn.commit()

    elif ans=="5":
      print("\n Goodbye")
      break

       

