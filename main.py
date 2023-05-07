# ------------------------------ REQUIRED MODULES ------------------------------#

from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json
import hashlib
import cv2 as cv
import datetime
import os
from cryptography.fernet import Fernet
import requests


sha256=hashlib.sha256()
# ---------------------------- PASSWORD GENERATOR ------------------------------- #

def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)

    password = "".join(password_list)

    #password_entry.delete(password_entry.index(END)-1,0)
    password_entry.insert(0,password)
    pyperclip.copy(password)
    return password
# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():

    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "email": email,
            "password": password,
        }
    }

    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo(title="Oops", message="Please make sure you haven't left any fields empty.")
    else:
        password_encrypt=encryption(new_data[website]['password'])
        print(type(password_encrypt))
        new_data[website]['password']=password_encrypt.decode()
        try:
            with open("files/data.json", "r") as data_file:
                #Reading old data
                data = json.load(data_file)
        except FileNotFoundError:
            with open("files/data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            #Updating old data with new data
            data.update(new_data)

            with open("files/data.json", "w") as data_file:
                #Saving updated data
                json.dump(data, data_file, indent=4)
        finally:
                website_entry.delete(0, END)
                password_entry.delete(0, END)


# ---------------------------- FIND PASSWORD ------------------------------- #
def find_password():
    website = website_entry.get()
    strkey=master_key.get()
    key=master_key.get().encode()
    sha256.update(key)
    key=sha256.hexdigest()
    if len(strkey)==0:
        messagebox.showinfo(title='error', message='You left the master key field empty.')
    else:
        with open('files/masterkeyfile.txt','r') as confirmData:
            dataKey=confirmData.read()
            if key==dataKey:
                try:
                    with open("files/data.json") as data_file:
                        data = json.load(data_file)
                except FileNotFoundError:
                    messagebox.showinfo(title="Error", message="No Data File Found.")
                else:
                    if website in data:
                        email = data[website]["email"]
                        password = data[website]["password"]
                        password=decryption(password)
                        messagebox.showinfo(title=website, message=f"Email: {email}\nPassword: {password}")
                        pyperclip.copy(password)

                    else:
                        messagebox.showinfo(title="Error", message=f"No details for {website} exists.")
            else:
                try:
                    with open('files/data.json','r') as data_file:
                        data=json.load(data_file)
                except FileNotFoundError:
                    messagebox.showinfo(title="Error", message="No Data File Found.")
                else:
                    intruder_image()
                    salt_list=['a','b','c','d','e','f','g','h','i','j','k','l','m','!','@','#','$','*']
                    password=''
                    if website in data:
                        email=data[website]['email']
                        password=generate_password()
                        # password=data[website]['password']
                    #     salt=[choice(salt_list) for _ in range(randint(0, 5))]
                    #
                    #     salt_str=''.join(salt)
                    #     password=password+salt_str
                    #     password=decryption(password)
                        messagebox.showinfo(title=website, message=f"Email: {email}\nPassword: {password}")
                        pyperclip.copy(password)

# ------------------------------ INTRUDER IMAGE CAPTURING --------------------------#
def intruder_image():
    filename='image.jpg'
    directory=r'C:\Users\ASUS\PycharmProjects\password_manager_and_security\intruder_phtots'
    camera = cv.VideoCapture(0)
    res, image = camera.read()
    camera.release()
    if res:
        picture_path = "image.jpg"
        os.chdir(directory)
        curr_datetime = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')
        splitted_path = os.path.splitext(picture_path)

        modified_picture_path = splitted_path[0] +curr_datetime + splitted_path[1]
        cv.imwrite(modified_picture_path, image)

#----------------------------Encryption--------------------------------#


def encryption(new_data):
    with open('files/filekey.key','r') as file_key:
        key=file_key.read()

    fernet=Fernet(key)
    password=fernet.encrypt(new_data.encode())
    print(password)
    return password

#---------------------------- Decryption ------------------------------ #


def decryption(data):
    with open('files/filekey.key','r') as file_key:
        key=file_key.read()
    fernet=Fernet(key)
    decrypt_password=fernet.decrypt(data)
    return decrypt_password.decode()
# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.config(height=515,width=815)
bg_img = PhotoImage(file="images/bg_dark.png")
logo_img=PhotoImage(file='images/new_logo4.png')
window.title("Full Pledge Password Manager")
#window.config(height=505,width=805)


#Labels
label=Label(image=bg_img,highlightthickness=5,highlightbackground='black')
label.place(x=0,y=0)
logo_label=Label(image=logo_img,highlightthickness=5,highlightbackground='black')
logo_label.place(x=0,y=0)
masterKey_label = Label(text="Master Key:",font=("Aerial",13),background="#19A7CE")
masterKey_label.place(x=175,y=150)
website_label = Label(text="Website:",font=("Aerial",13),background="#19A7CE")
website_label.place(x=175,y=200)
email_label = Label(text="Email:",font=("Aerial",13),background="#19A7CE")
email_label.place(x=175, y=250)
password_label = Label(text="Password:",font=("Aerial",13,),background="#19A7CE")
password_label.place(x=175, y=300)

#Entries
master_key= Entry(width=40,background='white')
master_key.place(x=290,y=150)
website_entry = Entry(width=40,background='white')
website_entry.place(x=290,y=200)
website_entry.focus()
email_entry = Entry(width=40,background='white')
email_entry.place(x=290,y=250)
email_entry.insert(0, "testclient@gmail.com")
password_entry = Entry(width=40,background='white')
password_entry.place(x=290,y=300)

# Buttons
search_button = Button(text="Search", width=15,command=find_password,background="#EA5455" )
search_button.place(x=600,y=175)
generate_password_button = Button(text="Generate Password",width=15,background="#EA5455",command=generate_password)
generate_password_button.place(x=600,y=225)
add_button = Button(text="Add", width=15,background='#EA5455',highlightcolor='black',command=save)
add_button.place(x=600,y=275)

window.mainloop()



