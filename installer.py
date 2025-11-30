from pyrogram import Client
import os, asyncio

async def main():
    phone = input("شماره رو با + بزن (مثل +989123456789): ")
    app = Client(f"sessions/{phone}", api_id=6, api_hash="eb06d4abfb49dc3eeb1aeb98ae0f581e", phone_number=phone)
    await app.connect()
    code = await app.send_code(phone)
    code_in = input("کد تأیید رو بزن (حتی انگلیسی): ")
    w2n = {"zero":"0","one":"1","two":"2","three":"3","four":"4","five":"5","six":"6","seven":"7","eight":"8","nine":"9"}
    num = "".join(w2n.get(i,i) for i in code_in.lower().split() if i.isdigit() or i in w2n)
    try:
        await app.sign_in(phone, code.phone_code_hash, num)
    except:
        pw = input("رمز دو مرحله‌ای (اگه نداری انتر بزن): ")
        await app.check_password(pw)
    print("نصب شد! حالا denv.py رو اجرا کن 😡😭")
    await app.stop()

if not os.path.exists("sessions"): os.makedirs("sessions")
asyncio.run(main())
