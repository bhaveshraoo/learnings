import sqlite3

conn=sqlite3.connect('youtube_video.db')

cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXIST videos()
               id INTEGER PRIMARY KEY,
               name TEXT NOT NULL,
               time TEXT NOT NULL
''')

def list_video():
    pass

def add_video():
    pass

def update_video():
    pass

def delet_video():
    pass

def main():
    while True:
        print("/n Youtube Manager app with DB")
        print("1. List all youtube videos ")
        print("2. Add a youtube video ")
        print("3. Update a youtube video details ")
        print("4. Delete a youtube video ")
        print("5. exit the app ")
        choice=input("enter your choice 1-5:  ")

        if choice=="1":
            list_video()
        
        elif choice=="2":
            name=input("enter vid name: ")
            time=input("enter vid time: ")
            add_video()

        elif choice=="3":
            video_id=input ("enter video id to update: ")  
            name=input("enter vid name: ")
            time=input("enter vid time: ")
            add_video()
            update_video(video_id, name, time)
    
if __name__ == "__main__":
    main()

