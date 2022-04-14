from email import message
from textwrap import indent
from tkinter import *
from os import system
from tkinter import messagebox
import random
from matplotlib.pyplot import fill
import pyperclip
import json

system("cls")


#GENERATE PASSWORDS

letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 
           'u', 'v', 'w','x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
            'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

#COLORS
GREEN ="#16697A"
YELLOW = "#EAEA7F"
FONT = ("courier",16,"bold")
FONT_B = ("courier",11,"bold")
FONT_E = ("courier",12,"normal")

root = Tk()
root.title("Save Logins Information")
root.minsize(width=400,height=200)

root.resizable(False,False)

#FRAMES
content = Frame(root,bg=GREEN)
footer = Frame(root,bg="red")

root.columnconfigure(0,weight=1) #100%
content.config(padx=60,pady=80, bg=GREEN)

root.rowconfigure(0,weight=9) #90%
root.rowconfigure(1,weight=1) #10%

content.grid(row=0,sticky="news")
footer.grid(row=1,sticky="news")

#FUNCTIONS

#Generate automatic password
def pass_generate():
    
    rand_letter = random.sample(letters,6)
    rand_num = random.sample(numbers,2)
    rand_syb = random.sample(symbols,2)
    pass_list = rand_letter + rand_num + rand_syb
    if len(pas_entry.get()) == 0:
        combine = "".join(random.sample(pass_list,10))
        pyperclip.copy(combine)
        pas_entry.insert(0,combine)

#Reset Entry
def delete_entry():
    web_entry.delete(0,END)
    email_entry.delete(0,END)
    pas_entry.delete(0,END)


def save_files():
    wed_data = web_entry.get()
    email_data = email_entry.get()
    pass_data = pas_entry.get()
    

    
    if wed_data == "" or email_data == "" or pass_data == "":
        messagebox.showwarning(title="Warning",message="No field should be blank.\n Check each empty box")
        if wed_data == "":
            web_entry.focus()
        elif email_data == "":
            email_entry.focus()
        else:
            pas_entry.focus()

    else:
        json_data = {
        wed_data.title():{"email":email_data,
                  "password":pass_data}
        }
        yes_ok = messagebox.askyesno(title="Confirm",message=f'''You entered these information;\n\n{wed_data}\n{email_data}\n{pass_data} \n\n Are they correct?''')
        if yes_ok:
            try:
                with open("./my_info.txt","r") as pass_file:
                    read_data = json.loads(pass_file.read())   #raed json data
                    
            except ValueError:
                with open("./my_info.txt","w") as pass_file:
                    json.dump(json_data,pass_file,indent=4)
            
            else:
                read_data.update(json_data)    #Update new data


                with open("./my_info.txt", "w") as pass_file:
                    json.dump(read_data,pass_file,indent=4) #write to the file
                    
                    messagebox.showinfo("Submitted","Information Saved!!")
    
        delete_entry()
    

#READ TEXT FILES

def read_files():
    with open("./my_info.txt","r") as all_data:
        try:
            data_r = json.load(all_data)
        except ValueError:
            messagebox.showwarning(title="Empty", message="No login infomation saved.")
        else:
            user = web_entry.get().title() 
            user2 = web_entry.get()
            all_keys = [each_key for each_key in data_r]
        
            if user in all_keys and web_entry.get() != "":
                messagebox.showinfo(title=user,message=f"Email/Username:  {data_r [user]['email']}\nPassword:  {data_r[user]['password']}")
                
            
            elif web_entry.get() == "":
                messagebox.showwarning("Empty",message="Website entry can't be blank")
            
            else:
                messagebox.showerror(title="No Data",message=f"\'{user2}\' does not exist, try a different name.")

            
#DELETE A LOGIN INFO
def delete_data():
    with open("./my_info.txt", "r") as del_data:
        try:
            data = json.load(del_data)
        except ValueError:
            messagebox.showwarning(title="Empty", message="No login information saved.")
        else:
            data_keys = [each_key for each_key in data]
            user_del = web_entry.get().title()
            user2_del = web_entry.get()
            if user_del in data_keys and web_entry.get() != "":
                del_yes= messagebox.askyesno(title="Delete", message=f"Are you sure, you want to delete \'{user2_del}\' information?")
                if del_yes:
                    data.pop(user_del)
                    with open("./my_info.txt","w") as del_dat:
                        json.dump(data,del_dat,indent=4)
                        messagebox.showinfo(title=f"{user_del}",message=f"{user_del} has been deleted.")
                        delete_entry()

            elif web_entry.get() == "":
                messagebox.showwarning(title="Nothing to delete",message="Website entry is blank, cannot delete blank entry.")
            else:
                messagebox.showerror(title="No Data",message=f"\'{user2_del}\' does not exist, nothing to delete.")

                
                

                


#Import images to tkinter
tk_image = PhotoImage(file="./pas1.png")

#Create canvas Widget to hold image

canvas = Canvas(content,height=200, width=200, bg=GREEN,highlightthickness=0)
canvas.create_image(100,100,image=tk_image)
canvas.grid(column=1,row=0)

#Create LABELS
website = Label(content,text="Website:", bg=GREEN,fg="white",font=FONT)
email = Label(content,text="Email/Username:",bg=GREEN,fg="white",font=FONT)
password = Label(content,text="Password:",bg=GREEN,fg="white",font=FONT)

#BUTTON
button = Button(content,text="Generate Password",width=17, command=pass_generate,font=FONT_B,padx=12,pady=5,bg=YELLOW)
button.grid(column=2,row=3,sticky="E")

button_add = Button(content,text="Add",width=40,command=save_files,font=FONT_B, padx=5,pady=4,bg=YELLOW)
button_add.grid(column=1,row=4,columnspan=2,sticky="WE")

button_search = Button(content,text="Search", width=17,font=FONT_B,padx=2,pady=2,command=read_files,bg=YELLOW)
button_search.grid(column=2,row=1,sticky="E")

button_search = Button(content,text="Delete", width=17,font=FONT_B,padx=2,pady=2,bg=YELLOW,command=delete_data)
button_search.grid(column=2,row=2,sticky="E")


#CREATE ENTRY
web_entry = Entry(content,width=30, font=FONT_E)
web_entry.focus()
email_entry = Entry(content,width=30,font=FONT_E)
pas_entry = Entry(content,width=45)

#SHOW WIDGETS USING GRID METHOD
website.grid(column=0,row=1,sticky="W")
email.grid(column=0,row=2,sticky="W")
password.grid(column=0,row=3,sticky="W")

#SHOW ENTRY WIDGETS
web_entry.grid(column=1,row=1,sticky="W")
email_entry.grid(column=1,row=2,sticky="W")
pas_entry.grid(column=1,row=3,sticky="W")


#STATUS BAR
status = Label(footer, text="© 2022 EDBAAH",bd=1,relief=SUNKEN, anchor=S, font=("Arial",9,"bold","italic"))
status.pack(side=BOTTOM,fill="both")


root.mainloop()