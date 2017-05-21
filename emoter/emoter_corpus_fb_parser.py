# -*- coding: utf-8 -*-
#!/usr/bin/env python

# Script wrapped around Emoter that parses Facebook messages (download the archive from Facebook) to make Emoter conversations based off of someone's
# Facebook messages.

# Must use fbchat-archive-parser from ownaginatious, here: https://github.com/ownaginatious/fbchat-archive-parser

# The Facebook messages archive must be parsed already and formatted into a CSV file with the columns ['thread'], ['sender'], ['date'], and ['message'].



import emote
import emoter
import os

import csv

import sqlite3
import sys

con = sqlite3.connect("msgs_db.db")
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS msgs (thread, sender, date, message);") # use your column names here

with open('msgs_csv.csv','rt', encoding = 'utf8', errors = 'ignore') as fin: # `with` statement available in 2.5+
    print("\n\tInitializing initial SQL db connection from file created with fbchart-archive-parser.")
    # csv.DictReader uses first line in file for column headings by default
    dr = csv.DictReader(fin) # comma is default delimiter
    to_db = [(i['thread'], i['sender'], i['date'], i['message']) for i in dr]

cur.executemany("INSERT INTO msgs (thread, sender, date, message) VALUES (?, ?, ?, ?);", to_db)
con.commit()
con.close()


def makeTuples():
    con = sqlite3.connect("new_msgs_db.db")
    cur = con.cursor()
    cur.execute("SELECT other, profile FROM msgs")
    f = open("final_msgs.txt","w")
    print("\n\tNow making final text file output of tuples.")
    for row in cur.execute("SELECT * FROM msgs"):
        try:
            f.write(str(row) + ",\n")
        except UnicodeDecodeError:
            continue
    con.close()



# Remove empty rows
def refineRows():
    con = sqlite3.connect("new_msgs_db.db")
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS msgs (other, profile);") # use your column names here
    with open('new_msgs_res.csv','rt', encoding = 'utf8', errors = 'ignore') as fin: # `with` statement available in 2.5+
        # csv.DictReader uses first line in file for column headings by default
        dr = csv.DictReader(fin) # comma is default delimiter
        for i in dr:
            try:
                to_db = [(i['other'], i['profile'])]
            except UnicodeDecodeError:
                continue
    print("\n\tFinished creating new CSV results.")
    cur.executemany("INSERT INTO msgs (other, profile) VALUES (?, ?);", to_db)
    con.commit()
    print("\n\tNow removing null / empty messages.")
    # cur.execute("DELETE FROM msgs WHERE other = ''")
    # cur.execute("DELETE FROM msgs WHERE profile = ''")
    cur.execute("DELETE FROM msgs WHERE other IS NULL")
    cur.execute("DELETE FROM msgs WHERE profile IS NULL")
    cur.execute("DELETE FROM msgs WHERE other=''")
    cur.execute("DELETE FROM msgs WHERE profile=''")
    con.commit()
    # print("\n\t", res)    
    con.close()
    makeTuples()


def writeToCSV(t1_msg, t2_msg):
    with open('new_msgs_res.csv', 'a', encoding = 'utf8', errors = 'ignore') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow([str(t1_msg), str(t2_msg)])  # requires a sequence [...]f


def checkRows():
    check_name = input("\n\tEnter the name of the Facebook profile you wish to make a text corpus from: \n\t")
    foundMatch = False
    msgToSenderFound = False
    con = sqlite3.connect("msgs_db.db")
    cur = con.cursor()
    # Prepares new csv file
    with open('new_msgs_res.csv', 'w', encoding = 'utf8', errors = 'ignore') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(["other", "profile"])  # requires a sequence [...]f
    for row in cur.execute("SELECT * FROM msgs"):
        name = row[1]
        if msgToSenderFound == False:
            if name != check_name:
                msgToSenderFound = True
                t1_name = str(row[1].strip())
                t1_msg = str(row[3].strip())
                t1_time = str(row[2].strip())
        else:
            if name != check_name:
                msgToSenderFound = False
                pass
            if name == check_name:
                t2_name = str(row[1].strip())
                t2_msg = str(row[3].strip())
                t2_time = str(row[2].strip())
                msgToSenderFound = False    
                writeToCSV(t1_msg, t2_msg)
    print("\n\tFinished parsing and exporting new CSV with sender messages.")
    refineRows()


checkRows()