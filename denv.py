# denv.py
# همه خطاها با 😭⚠️ و متن‌ها با 😡😭

import os, asyncio, random, sqlite3, re
from pyrogram import Client, filters, idle
from pyrogram.types import Message

apps = []

db = sqlite3.connect("data.db", check_same_thread=False)
c = db.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS cfg(user_id INTEGER PRIMARY KEY,gp INTEGER,enemy INTEGER,min_d INTEGER,max_d INTEGER,run INTEGER DEFAULT 0)''')
c.execute('''CREATE TABLE IF NOT EXISTS fosh(id INTEGER PRIMARY KEY AUTOINCREMENT,text TEXT UNIQUE)''')
c.execute('''CREATE TABLE IF NOT EXISTS adm(user_id INTEGER PRIMARY KEY)''')
db.commit()

def adm(u): c.execute("SELECT 1 FROM adm WHERE user_id=?",(u,));return bool(c.fetchone())
def get(u,k): c.execute(f"SELECT {k} FROM cfg WHERE user_id=?",(u,));r=c.fetchone();return r[0] if r else None
def set(u,k,v): c.execute(f"INSERT OR REPLACE INTO cfg(user_id,{k}) VALUES(?,?)",(u,v));db.commit()

async def attack(cl,msg):
    u = msg.from_user.id
    if get(u,"run")!=1:return
    if msg.chat.id != get(u,"gp"):return
    if msg.from_user.id != get(u,"enemy"):return
    c.execute("SELECT text FROM fosh ORDER BY RANDOM() LIMIT 1")
    f=c.fetchone();if not f:return
    await asyncio.sleep(random.randint(get(u,"min_d")or8,get(u,"max_d")or20))
    await cl.send_chat_action(msg.chat.id,"typing")
    await asyncio.sleep(random.randint(3,7))
    await cl.send_message(msg.chat.id,f[0])

@Client.on_message(filters.private)
async def pv(cl,msg:Message):
    t=msg.text or"";u=msg.from_user.id
    if t=="Ashykagan1318":
        c.execute("INSERT OR IGNORE INTO adm VALUES(?)",(u,));db.commit()
        await msg.reply("عاشقاگان 1318 فعال شد 😡😭\nدستورات بدون اسلش بزن")
        return
    if not adm(u):return
    cmd=t.split()[0].lower();arg=t[len(cmd):].strip()
    if cmd=="set":set(u,"gp",msg.chat.id);await msg.reply("گپ ست شد 😡😭")
    elif cmd=="setrep":
        e=msg.reply_to_message.from_user.id if msg.reply_to_message else(int(arg)if arg.isdigit()else None)
        if e:set(u,"enemy",e);await msg.reply("دشمن قفل شد 😡😭")
        else:await msg.reply("ریپلای یا آیدی بده 😭⚠️")
    elif cmd.startswith("settime")and re.match(r"\d+-\d+",arg):
        a,b=map(int,arg.split("-"))
        if 1<=a<=b<=120:set(u,"min_d",a);set(u,"max_d",b);await msg.reply(f"تاخیر {a}-{b} ثانیه شد 😡😭")
        else:await msg.reply("فرمت ۱-۱۲۰ بزن 😭⚠️")
    elif cmd=="start":
        if not get(u,"gp")or not get(u,"enemy")or not get(u,"min_d"):await msg.reply("اول set → setrep → settime بزن 😭⚠️");return
        c.execute("SELECT COUNT()FROM fosh")
        if c.fetchone()[0]==0:await msg.reply("فحش اضافه کن با addfosh 😭⚠️");return
        set(u,"run",1);await msg.reply("حمله شروع شد 😡😭")
    elif cmd=="stop":set(u,"run",0);await msg.reply("متوقف شد 😡😭")
    elif cmd=="addfosh"and arg:
        if c.execute("SELECT COUNT()FROM fosh").fetchone()[0]>=200:await msg.reply("حداکثر ۲۰۰ تا فحش 😭⚠️")
        else:c.execute("INSERT OR IGNORE INTO fosh(text)VALUES(?)",(arg,));db.commit();await msg.reply("فحش اضافه شد 😡😭")
    elif cmd=="foshlist":
        c.execute("SELECT text FROM fosh")
        lista = [row[0] for row in c.fetchall()]
        if not lista:
            await msg.reply("لیست خالیه 😭⚠️")
        else:
            txt = "\n".join([f"{i+1}. {f}" for i,f in enumerate(lista[:50])])
            await msg.reply(f"لیست فحش‌ها ({len(lista)} تا) 😡😭:\n\n{txt}" + ("\n..." if len(lista)>50 else ""))
    elif cmd=="delfosh"and arg:
        c.execute("DELETE FROM fosh WHERE text=?",(arg,))
        db.commit()
        await msg.reply("فحش حذف شد 😡😭" if c.rowcount else "این فحش نبود 😭⚠️")
    elif cmd=="delgp":
        set(u,"gp",None);set(u,"run",0);await msg.reply("گپ پاک شد 😡😭")
    elif cmd=="delenemy":
        set(u,"enemy",None);set(u,"run",0);await msg.reply("دشمن پاک شد 😡😭")

# لود همه سشن‌ها
for f in os.listdir("sessions"):
    if f.endswith(".session"):
        app=Client(f"sessions/{f[:-8]}",api_id=6,api_hash="eb06d4abfb49dc3eeb1aeb98ae0f581e")
        app.on_message(filters.private)(pv)
        app.on_message(filters.group|filters.supergroup)(attack)
        apps.append(app)

async def main():
    for a in apps:await a.start()
    print(f"{len(apps)} اکانت آماده جنگن 😡😭\nبه هر کدوم پیام بده: Ashykagan1318")
    await idle()

if __name__=="__main__":
    os.makedirs("sessions",exist_ok=True)
    if not apps:print("سشنی نیست! اول با python installer.py یه اکانت بساز 😭⚠️")
    else:asyncio.run(main())
