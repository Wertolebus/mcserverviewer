import customtkinter as ctk
import requests
import os
from PIL import Image
from base64 import b64decode
import traceback


def getserverinfo(ip : str):
    return eval(requests.get("https://api.mcstatus.io/v2/status/java/" + ip).content.decode().replace('true', 'True').replace('false', 'False').replace('null', 'None'))

def getplayers(ip):
    players = f"Players {getserverinfo(ip)['players']['online']}/{getserverinfo(ip)['players']['max']}: \n\n"
    for i in getserverinfo(ip)['players']['list']:
        players += i['name_clean'] + "\n"
    
    return players

def getdescription(ip):
    return f" ".join(f'Description: {getserverinfo(ip)["motd"]["clean"]}'.split())

def getversion(ip):
    return "Version: " + getserverinfo(ip)['version']["name_clean"]
 
def getfavicon(ip:str):
    _ip = ip.replace(".", "_")
    temp = os.getenv('temp')
    with open(temp + "\\" + _ip+".png", "bw") as favicon:
        favicon.write(b64decode(getserverinfo(ip)['icon'].replace("data:image/png;base64,", "")))
        favicon.close()
    
    img = Image.open(temp + "\\" + _ip+".png")
    img = img.resize((512, 512), Image.NEAREST)
    img.save(temp + "\\" + _ip+".png")
    
    return Image.open(temp + "\\" + _ip+".png")
def GUI():
    app = ctk.CTk()
    app.geometry("600x600")
    app.resizable(False, False)
    app.title("MinecraftServerViewer 1.0")
    def onSearch():
        if ip_entry.get().strip() != "":
            ip = ip_entry.get().strip()
            try:
                players_label.configure(text=getplayers(ip))
                server_description.configure(text=getdescription(ip))
                server_version.configure(text=getversion(ip))
                favicon = ctk.CTkImage(getfavicon(ip), size=(256, 256))
                favicon_label.configure(image=favicon)
            except:
                pass
            
    scrbarfr = ctk.CTkScrollableFrame(app, height=580, width=250)
    ip_entry = ctk.CTkEntry(app, width=300, placeholder_text="Minecraft Server IP", justify='center')
    players_label = ctk.CTkLabel(scrbarfr, text="", justify='left')
    server_description = ctk.CTkLabel(app, text="", justify='left', wraplength=300)
    server_version = ctk.CTkLabel(app, text="", justify='left', wraplength=300)
    search_button = ctk.CTkButton(app, text="Search", command=onSearch)
    favicon_label = ctk.CTkLabel(app, text="")
    
    
    favicon_label.place(anchor='center', relx=0.272, rely=0.6)
    scrbarfr.place(relx = 0.995, rely=0.5, anchor='e')
    players_label.pack(side='left')
    server_description.place(relx=0.25, rely=0.2, anchor='center')
    server_version.place(relx=0.25, rely=0.3, anchor='center')
    search_button.place(relx = 0.135, rely=0.11, anchor='w')
    ip_entry.place(relx = 0.01, rely=0.05, anchor='w')

    
    app.mainloop()
    

GUI()