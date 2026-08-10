
import json
import telegram



def load_data():
    try:
        with open ('youtube.txt', 'r')as file:
          return json.load(file)
    except FileNotFoundError:
        return []
    
def save_data_helper(videos):
    with open ('youtube.txt', 'w')as file:
        json.dump(videos, file)

def list_all_videos(videos):
    print("\n")
    print("*" * 70)
    for index, video in enumerate(videos, start=1):
        print(f"{index}. {video['name']}, {video['time']}")
    print("\n")
    print("*" * 70)

def add_videos(videos):
    name=input("enter video name:")
    time=input("enter video time:")
    videos.append({'name':name, 'time':time})
    save_data_helper(videos)

def update_videos(videos):
    list_all_videos(videos)
    index = int (input("Enter the video number to update"))
    if 1<=index<=len(videos):
        name=input("enter new video name")
        time=input("its time:")
        videos[index-1]={'name':name, 'time':time}
        save_data_helper(videos)
    else:
        print("invalid")

def delet_videos(videos):
    list_all_videos(videos)
    index= int(input("enter value u have to delete"))
    if 1<=index<=len(videos):
        del videos[index-1]
        save_data_helper(videos)
    else:
        print("invalid selection")

def main():
    videos=load_data()
    while True:
        print("\n Youtube Manager | Please select an option: ")
        print("1. List all youtube videos ")
        print("2. Add a youtube video ")
        print("3. Update a youtube video details ")
        print("4. Delete a youtube video ")
        print("5. exit the app ")

        choice=input("enter your choice 1-5:  ")

        match choice:
            case'1':
                list_all_videos(videos)

            case'2':
                add_videos(videos)
            
            case'3':
                update_videos(videos)

            case'4':
                delet_videos(videos)

            case'5':
                break
            case _ :
                print(" invalid input ")

if __name__ == "__main__":
    main()