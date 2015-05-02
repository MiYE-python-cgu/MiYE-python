from datetime import datetime, date, timedelta
import sys
import MySQLdb
import calendar

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
           WHERE t_admin.UserName = '%s' AND AdminType = 'manager';
           """ % userName)

           while(1):
               row=cursor0.fetchone()
               if row==None:
                   break

               admin= row[0]

               if admin >= 0:
                   userCheck = None

               else:
                   print("Only Managers may use this application")
                   userCheck = True

    except MySQLdb.Error:
           print ("Error connecting to MySQL")
           sys.exit(1)
    cursor0.close()
    conn.commit()

    ##Main Menu
ans=True
while ans:
    print("""
     1. View Rooms
     2. Change Room Capacity
     3. Add Room
     4. Delete Room
     5. Manage Room Prices
     6. View Spa Services
     7. Edit Spa Service
     8. Add Spa Service
     9. Delete Spa Service
    10. Display Users
    11. Add User
    12. Delete User
    13. Exit
    """)
    ans=input("What would you like to do? ")

    ##Print all rooms
    if ans=="1":

              try:
                  cursor1=conn.cursor()
                  print ("RoomID\t\tRoomType\t\tMaxGuestAllowed\t\tWkDayOffPrice\t\tWkEndOffPrice\t\tWkDayOnPrice\t\tWkEndOnPrice")
                  cursor1.execute ("SELECT * FROM t_room;")

                  while(1):

                      row=cursor1.fetchone()
                      if row==None:
                          break

                      else:
                          print(row[0], '\t\t', row[1], '\t\t\t', row[2], '\t\t\t\t\t', row[3], '\t\t\t\t', row[4],'\t\t\t\t', row[5], '\t\t\t\t', row[6])

              except MySQLdb.Error:
                    print ("Error connecting to MySQL")
                    sys.exit(1)
              cursor1.close()
              conn.commit()

    elif ans=="2":

              try:
                  roomNum = int(input("What room number would you like to alter the capacity? "))
                  cursor1=conn.cursor()
                  print ("RoomID\t\tRoomType\t\tMaxGuestAllowed\t\tWkDayOffPrice\t\tWkEndOffPrice\t\tWkDayOnPrice\t\tWkEndOnPrice")
                  cursor1.execute ("SELECT * FROM t_room WHERE RoomID = %s;", (roomNum,))

                  row=cursor1.fetchone()
                  if row==None:
                      print("That room number does dot exist. You can add it using Add Rooms")
                      break

                  else:
                      print(row[0], '\t\t', row[1], '\t\t\t', row[2], '\t\t\t\t\t', row[3], '\t\t\t\t', row[4],'\t\t\t\t', row[5], '\t\t\t\t', row[6])
                      cap = int(input("What will the new room capacity be?\nNote: If the capacity does not already exist in another room\nyou will need to set the price and type using Manage Rooms after you change the capacity " ))

                      try:

                          cursor2=conn.cursor()
                          cursor2.execute ("SELECT RoomType, WkDayOffPrice,  WkEndOffPrice,  WkDayOnPrice,  WkEndOnPrice FROM t_room WHERE MaxGuestAllowed = %s;", (cap,))
                          row2=cursor2.fetchone()

                          if row2==None:
                              cursor1.execute ("""
                              UPDATE t_room SET MaxGuestAllowed = %s, RoomType = 'NONE', WkDayOffPrice = 0, WkEndOffPrice = 0, WkDayOnPrice = 0, WkEndOnPrice = 0
                              WHERE RoomID = %s""", (cap, roomNum))
                              print("Room capacity updated. WARNING: The price and type will be empty until added using Manage Rooms")

                          else:
                              cursor1.execute ("""
                              UPDATE t_room SET MaxGuestAllowed = %s, RoomType = %s, WkDayOffPrice = %s, WkEndOffPrice = %s, WkDayOnPrice = %s, WkEndOnPrice = %s
                              WHERE RoomID = %s""", (cap, row2[0], row2[1], row2[2], row2[3], row2[4], roomNum))
                              print("Room capacity, type and price updated.")

                      except MySQLdb.Error:
                          print ("Error connecting to MySQL cursor2")
                          sys.exit(1)
                      cursor2.close()
                      conn.commit()

              except MySQLdb.Error:
                    print ("Error connecting to MySQL")
                    sys.exit(1)
              cursor1.close()
              conn.commit()

    elif ans=="3":

              try:
                  roomNum = int(input("What is the new room number? "))
                  cursor1=conn.cursor()
                  cursor1.execute ("SELECT * FROM t_room WHERE RoomID = %s;", (roomNum,))
                  row=cursor1.fetchone()
                  if row==None:
                      roomCap = int(input("What is the capacity of the new room? "))

                      try:
                          cursor3=conn.cursor()
                          cursor3.execute ("SELECT RoomType, WkDayOffPrice, WkEndOffPrice, WkDayOnPrice, WkEndOnPrice FROM t_room WHERE MaxGuestAllowed = %s;", (roomCap,))
                          row3=cursor3.fetchone()

                          if row3==None:

                              roomType=input("What is the new room type? ")
                              WkDayOffPrice = float(input("What is the weekday off-season price? "))
                              WkEndOffPrice = float(input("What is the weekend off-season price? "))
                              WkDayOnPrice = float(input("What is the weekday on-season price? "))
                              WkEndOnPrice = float(input("What is the weekday on-season price? "))
                              cursor1.execute ("""
                              INSERT INTO t_room (RoomID, RoomType, MaxGuestAllowed, WkDayOffPrice, WkEndOffPrice, WkDayOnPrice, WkEndOnPrice) VALUES (%s, %s, %s, %s, %s, %s, %s);
                              """, (roomNum, roomType, roomCap, WkDayOffPrice, WkEndOffPrice, WkDayOnPrice, WkEndOnPrice))
                              print("The new room and type have been added")

                          else:
                              cursor1.execute ("""
                              INSERT INTO t_room (RoomID, RoomType, MaxGuestAllowed, WkDayOffPrice, WkEndOffPrice, WkDayOnPrice, WkEndOnPrice) VALUES (%s, %s, %s, %s, %s, %s, %s);
                              """, (roomNum, row3[0], roomCap, row3[1], row3[2], row3[3], row3[4]))
                              print("The new room has been added")

                      except MySQLdb.Error:
                          print ("Error connecting to MySQL cursor2")
                          sys.exit(1)
                      cursor3.close()
                      conn.commit()

                  else:
                      print("That room number already exists")

              except MySQLdb.Error:
                    print ("Error connecting to MySQL")
                    sys.exit(1)
              cursor1.close()
              conn.commit()

    elif ans=="4":

        try:
            roomNum = int(input("What is the room number to delete? "))
            cursor1=conn.cursor()
            cursor1.execute ("DELETE FROM t_room WHERE RoomID = %s;", (roomNum,))
            print("Room # ", roomNum, " has been deleted")

        except MySQLdb.Error:
            print ("Error connecting to MySQL")
            sys.exit(1)
        cursor1.close()
        conn.commit()

    elif ans=="5":

        try:
            roomCap = int(input("For which room capacity would you like to edit the prices? "))
            cursor1=conn.cursor()
            cursor1.execute ("SELECT RoomID FROM t_room WHERE MaxGuestAllowed = %s;", (roomCap,))
            row=cursor1.fetchone()
            if row==None:
                print("That room capacity does not exist")

            else:
                WkDayOffPrice = float(input("What is the new weekday off-season price? "))
                WkEndOffPrice = float(input("What is the new weekend off-season price? "))
                WkDayOnPrice = float(input("What is the new weekday on-season price? "))
                WkEndOnPrice = float(input("What is the new weekday on-season price? "))
                cursor2=conn.cursor()
                cursor2.execute ("""
                UPDATE t_room SET WkDayOffPrice = %s, WkEndOffPrice = %s, WkDayOnPrice = %s, WkEndOnPrice = %s
                WHERE MaxGuestAllowed = %s;""", (WkDayOffPrice, WkEndOffPrice, WkDayOnPrice, WkEndOnPrice, roomCap))
                print("All room with capacity = ", roomCap, " have been updated")


        except MySQLdb.Error:
            print ("Error connecting to MySQL")
            sys.exit(1)
        cursor1.close()
        conn.commit()


    elif ans=="6":

              try:
                  cursor1=conn.cursor()
                  print ("SpaID\tSpaType\t\tSpaService\t\tCapacity\t\tPricePerMinute\t\tAvailable30\t\tAvailable60\t\tAvailable90")
                  cursor1.execute ("SELECT * FROM t_spaservice;")

                  while(1):

                      row=cursor1.fetchone()
                      if row==None:
                          break

                      else:
                          print ('{:<8} {:<10} {:<20} {:<14}  {:<16}  {:<14}  {:<14}  {:<10} '.format(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]))

              except MySQLdb.Error:
                    print ("Error connecting to MySQL")
                    sys.exit(1)
              cursor1.close()
              conn.commit()

    elif ans=="7":

              try:
                  spaID = int(input("What SpaID would you like to edit? "))
                  print ("SpaID\tSpaType\t\tSpaService\t\tCapacity\t\tPricePerMinute\t\tAvailable30\t\tAvailable60\t\tAvailable90")
                  cursor1=conn.cursor()
                  cursor1.execute ("SELECT * FROM t_spaservice WHERE SpaID = %s;", (spaID,))

                  row=cursor1.fetchone()
                  if row==None:
                      print("That SpaID does dot exist. You can add it using Add Spa Service")
                      break

                  else:
                      print ('{:<8} {:<10} {:<20} {:<14}  {:<16}  {:<14}  {:<14}  {:<10} '.format(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]))
                      spaType = input("What will the new SpaType be for the service " )
                      spaService = input("What is the new name of the service " )
                      spaCap = int(input("What will be new capacity be for the service? "))
                      spaPrice = float(input("What will the new price per minute be for the service? "))
                      spa30 = int(input("Will this service be available at 30 minute intervals? 1 for Yes and 0 for No "))
                      spa60 = int(input("Will this service be available at 30 minute intervals? 1 for Yes and 0 for No "))
                      spa90 = int(input("Will this service be available at 30 minute intervals? 1 for Yes and 0 for No "))

                      cursor1.execute ("""
                      UPDATE t_spaservice SET SpaType = %s, SpaService = %s, Capacity = %s, PricePerMinute = %s, Available30 = %s, Available60 = %s, Available90 = %s
                      WHERE SpaID = %s;""", (spaType, spaService, spaCap, spaPrice, spa30, spa60, spa90, spaID))
                      print("SpaID = ", spaID, " has been updated")

              except MySQLdb.Error:
                    print ("Error connecting to MySQL")
                    sys.exit(1)
              cursor1.close()
              conn.commit()

    elif ans=="8":

              try:
                  spaID = int(input("What is the new SpaID? "))
                  cursor1=conn.cursor()
                  cursor1.execute ("SELECT * FROM t_spaservice WHERE SpaID = %s;", (spaID,))
                  row=cursor1.fetchone()
                  if row==None:
                      spaType = input("What will the new SpaType be for the service " )
                      spaService = input("What is the new name of the service " )
                      spaCap = int(input("What will be new capacity be for the service? "))
                      spaPrice = float(input("What will the new price per minute be for the service? "))
                      spa30 = int(input("Will this service be available at 30 minute intervals? 1 for Yes and 0 for No "))
                      spa60 = int(input("Will this service be available at 30 minute intervals? 1 for Yes and 0 for No "))
                      spa90 = int(input("Will this service be available at 30 minute intervals? 1 for Yes and 0 for No "))

                      cursor1.execute ("""
                      INSERT INTO t_spaservice (SpaID, SpaType, SpaService, Capacity, PricePerMinute, Available30, Available60, Available90)
                      VALUES(%s, %s, %s, %s, %s, %s, %s, %s);""", (spaID, spaType, spaService, spaCap, spaPrice, spa30, spa60, spa90))
                      print("SpaID = ", spaID, " has been added")

                  else:
                      print("That SpaID already exists")

              except MySQLdb.Error:
                    print ("Error connecting to MySQL")
                    sys.exit(1)
              cursor1.close()
              conn.commit()

    elif ans=="9":

        try:
            spaID = int(input("What is the SpaID to delete? "))
            cursor1=conn.cursor()
            cursor1.execute ("DELETE FROM t_spaservice WHERE SpaID = %s;", (spaID,))
            print("SpaID # ", spaID, " has been deleted")

        except MySQLdb.Error:
            print ("Error connecting to MySQL")
            sys.exit(1)
        cursor1.close()
        conn.commit()

    elif ans=="10":

              try:
                  cursor1=conn.cursor()
                  print ("AdminID\t\tUserName\t\t\t\tAdminType")
                  cursor1.execute ("SELECT * FROM t_admin;")

                  while(1):

                      row=cursor1.fetchone()
                      if row==None:
                          break

                      else:
                          print('{:<10} {:<20} {:^20} '.format(row[0], row[1], row[2]))

              except MySQLdb.Error:
                    print ("Error connecting to MySQL")
                    sys.exit(1)
              cursor1.close()
              conn.commit()

    elif ans=="11":

              try:
                  adminID = int(input("What is the new AdminID? "))
                  cursor1=conn.cursor()
                  cursor1.execute ("SELECT * FROM t_admin WHERE AdminID = %s;", (adminID,))
                  row=cursor1.fetchone()
                  if row==None:
                      userName = input("What will the new UserName be for the new user (first.last) " )
                      adminType = input("What is the users AdminType? Only manager can use this application " )
                      cursor1.execute ("""
                      INSERT INTO t_admin (AdminID, UserName, AdminType)
                      VALUES(%s, %s, %s);""", (adminID, userName, adminType))
                      print("AdminID = ", adminID, " has been added")

                  else:
                      print("That AdminID already exists")

              except MySQLdb.Error:
                    print ("Error connecting to MySQL")
                    sys.exit(1)
              cursor1.close()
              conn.commit()

    elif ans=="12":

        try:
            adminID = int(input("What is the adminID to delete? "))
            cursor1=conn.cursor()
            cursor1.execute ("DELETE FROM t_admin WHERE AdminID = %s;", (adminID,))
            print("AdminID # ", adminID, " has been deleted")

        except MySQLdb.Error:
            print ("Error connecting to MySQL")
            sys.exit(1)
        cursor1.close()
        conn.commit()

    elif ans=="13":
      print("\n Goodbye")
      conn.close()
      break

    else:
        print("Invalid choice please try again")
