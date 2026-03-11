import json
from datetime import datetime, timedelta
from telegram import Update,KeyboardButton,ReplyKeyboardMarkup,InlineKeyboardButton,InlineKeyboardMarkup,ReplyKeyboardRemove
from telegram.ext import Application,CommandHandler,MessageHandler,ContextTypes,filters,InlineQueryHandler

TOKEN="YOUR_TOKEN_HERE"
app=Application.builder().token(TOKEN).build()

admin_commands=[[KeyboardButton("1-رؤية الرسائل التي لم ترد عليها والرد عليها.")],[KeyboardButton("2-رؤية الاعضاء الذين تم حظرهم والغاء حظر المستخدمين المحظورين.")],[KeyboardButton("3-حظر مستخدم")],[KeyboardButton("4-اذاعة رسالة.")],[KeyboardButton("5-رؤية الاعضاء في هذا البوت.")]]
admin_commands_exepting=["1-رؤية الرسائل التي لم ترد عليها والرد عليها.","2-رؤية الاعضاء الذين تم حظرهم والغاء حظر المستخدمين المحظورين.","3-حظر مستخدم","4-اذاعة رسالة.","5-رؤية الاعضاء في هذا البوت."]
admin_commands_final=ReplyKeyboardMarkup(admin_commands,resize_keyboard=True,one_time_keyboard=True)
def read_data_base():
    with open(r"your_json_file", "r", encoding="utf-8") as f:
        return json.load(f)
def name_num_of_users():
    data_file=read_data_base()
    users_list=[]
    for id in data_file["members"]:
        user_id=data_file["members"][id]["user_id"]
        users_list.append(user_id)

    return [len(users_list),users_list]

def find_messages ():
    file_data=read_data_base()
    for id in  file_data ["members"]:
        x=0
        for message in file_data ["members"][id]["his_message"]:
            if not file_data["members"][id]["his_message"][x]["is_admin_answered"]:
                return [file_data["members"][id]["his_message"][x]["message_text"],id,x]
            x+=1
    return None





def show_banned_users ():
    file_data=read_data_base()
    banned_users_list=[]
    for id in  file_data ["members"]:
        if file_data ["members"][id]["is_banned"]:
            user_user_name= file_data ["members"][id]["user_id"]
            banned_users_list.append(user_user_name)

    banned_users_num=len(banned_users_list)
    return [banned_users_num,banned_users_list]

def show_users_data ():
    file_data = read_data_base()
    users_list = []
    users_list.append(file_data["members"])
    return ((((str(users_list).replace(",","\n")).replace("[","")).replace("]","")).replace("}","")).replace("{","\n")

def save_data_base(data_file):
    with open(r"your_json_file", "w", encoding="utf-8") as f:
        json.dump(data_file,f,indent=4,ensure_ascii=False)

def date ():
    return str(datetime.now())

def is_admen (user_id):
    file_data=read_data_base()
    if user_id in file_data["admin_id"]:
        return  True
    else:
        return False


async def start (update:Update,context:ContextTypes.DEFAULT_TYPE):
    data_file=read_data_base()

    user_id = str(update.effective_user.id)
    user_full_name = update.message.from_user.full_name
    user_user_name=update.effective_user.username
    user_device_languages=update.effective_user.language_code
    user_is_subscribed=bool(update.effective_user.is_premium)


    if is_admen(user_id):
        await update.message.reply_text("كيف حالك سيدي , ما الذي تأمر به اليوم؟\n لعرض قائمه اوامرك اضغط على /commands.")
    else:
        if user_id in data_file["members"]:
            await update.message.reply_text(f"مرحبا بك مره اخرى {user_full_name} اضغط على /send. لارسال رساله الى مالك البوت")
            data_file["members"][user_id]["name"] = user_full_name
            data_file["members"][user_id]["user_name"] = user_user_name
            data_file["members"][user_id]["device_languages"] = user_device_languages
            data_file["members"][user_id]["premium_status_on_last_registration"] = user_is_subscribed
            data_file["members"][user_id]["last_join"] = date()

            save_data_base(data_file)

        else:
            await update.message.reply_text(f""" مرحبا  {user_full_name} لم اسمع باسمك قط 
            لابد انك مستخدم جديد يجب ان اعرف عن نفسي انا بوت للتواصل مع المطور للتواصل مع صاحب هذا البوت اضغط على /send.  """)

            data_file["members"][user_id]={"name":user_full_name,
                                           "user_name":user_user_name,
                                           "user_id":user_id,
                                           "join_date":date(),
                                           "is_banned":False,
                                           "warning_count":0,
                                           "device_languages":user_device_languages,
                                           "premium_status_on_last_registration":user_is_subscribed,
                                           "last_join":date(),
                                           "his_message":[]}
            save_data_base(data_file)

async def send (update:Update,context:ContextTypes.DEFAULT_TYPE):
    setup=context.user_data.get("setup")

    msg_id = find_messages()
    text=update.message.text
    data_file=read_data_base()
    user_id = str(update.effective_user.id)
    user_full_name = update.message.from_user.full_name
    user_user_name = update.effective_user.username
    user_device_languages = update.effective_user.language_code
    user_is_subscribed = bool(update.effective_user.is_premium)
    if setup == "waiting_answer" and is_admen(user_id):
        target_id = context.user_data.get("reply_to_id")
        num_of_message=context.user_data.get("num_of_message")
        message_text=context.user_data.get("message_text")
        is_enter= False
        data_file["members"][target_id]["his_message"][num_of_message]["is_admin_answered"]=True

        try:
            await context.bot.send_message(chat_id=target_id,
            text=f"مرحبا {data_file['members'][target_id]['name']}هذا هو رد المطور عليك:\n{text}")
            save_data_base(data_file)
            await update.message.reply_text("تم ارسال الرسالة بنجاح")
            the_msg=list(data_file["members"][target_id]["his_message"][num_of_message].values())[0]

            data_file["admin_answers"].append({
                "from_user": data_file["members"][target_id]["name"],
                "user_msg": message_text,
                "admin_reply": text,
                "date": date()
            })
            save_data_base(data_file)
            is_enter=True
        except Exception as e:
            if is_enter==False:
                await update.message.reply_text("لا ادري ماذا اقول لك يا سيدي ,لكن هذا المستخدم  حظرني لا يمكنني ارسال رساله له .")
                data_file["members"][target_id]["his_message"][num_of_message]["is_admin_answered"]=True
                save_data_base(data_file)


                print(e)
            
        context.user_data.clear()
        return
    if setup=="waiting_id" and is_admen(user_id)  :
        id=update.message.text
        try:
            is_available=data_file["members"][id]
            is_banned_var=data_file["members"][id]["is_banned"]
            is_available=True

        except:
            await update.message.reply_text("اعتذر سيدي, هذا عنوان الي دي هذا غير متوفر.")
            return

        if is_banned_var and is_available:
            data_file["members"][id]["is_banned"] = False
            save_data_base(data_file)
            await update.message.reply_text("تم تنفيذ الامر بنجاح سيدي.")
        else:
            await update.message.reply_text("سيدي هذا الاي دي غير محظور بالفعل") 
        return
    if setup=="waiting_id_to_block" and is_admen(user_id)  :
        id=update.message.text
        try:
            is_available=data_file["members"][id]
            is_banned_var=data_file["members"][id]["is_banned"]
            is_available=True

        except:
            await update.message.reply_text("اعتذر سيدي, هذا عنوان الي دي هذا غير متوفر.")
            return

        if not is_banned_var and is_available:
            data_file["members"][id]["is_banned"] = True
            save_data_base(data_file)
            await update.message.reply_text("تم تنفيذ الامر بنجاح سيدي.")
        else:
            await update.message.reply_text("سيدي هذا الاي دي محظور بالفعل") 
        return
    if setup == "waiting_message_to_send":
        message = update.message.text
        num=0
        for id in data_file ["members"]:
            try:
                await context.bot.send_message(chat_id=id,text=f"اذاعه الادمن : \n {message}")
            except:
                num+=1
        data_file ["admin_broadcasts"].append(message)
        await update.message.reply_text(f"تم ارسال الرسالة الي كل المستخدمين سيدي عدا ({str(num)})مستخدم/مستخدمين بسبب خطا.")
        return

    try:
        time_difference =datetime.strptime(date(), "%Y-%m-%d %H:%M:%S.%f") - datetime.strptime(data_file["members"][user_id]["his_message"][-1]["message_time"],"%Y-%m-%d %H:%M:%S.%f")
        if time_difference < timedelta(seconds=10):
            data_file["members"][user_id]["warning_count"]+=1
            save_data_base(data_file)
            await update.message.reply_text(f"⚠️ لا يمكنك إرسال رسالتين في أقل من 10 ثوانٍ! \n لقد تم اعطائك تحذير, مجموع تحذيراتك هو ({data_file['members'][user_id]['warning_count']})")

            if  data_file["members"][user_id]["warning_count"]>= 3:
                data_file["members"][user_id]["is_banned"]= True
                await update.message.reply_text(" تم حظرك بسبب ارسال رسائل كثيره بوقت قصير ولعدة مرات ")
                save_data_base(data_file)
            return

    except:
        pass
    if setup== "waiting_id_to_get_info" and is_admen(user_id) :

        try:  
            await update.message.reply_text(((((str(data_file["members"][text]).replace(",","\n")).replace("[","")).replace("]","")).replace("}","")).replace("{","\n"))
            return
        except:
            await update.message.reply_text("عذرا سيدي لكن المستخدم غير موجود.")
            return
    if not is_admen(user_id) and data_file["members"][user_id]["is_banned"] :
        await update.message.reply_text("عذرا , لقد تم حظرك سابقا ")
        return

    if text=="/send" and user_id in data_file["members"]:
        await update.message.reply_text("ما هي الرسالة التي تريد ارسالها؟\nالرجاء عدم ارسال رسالتين كل عشر ثواني.")
        context.user_data["setup"]="waiting_text"
        return

    elif setup=="waiting_text" :
        if update.message.text:
            new_message={"text":update.message.text,"type":"text"}
        elif update.message.photo:
            new_message={"photo_id":str(update.message.photo[-1].file_id),"caption":update.message.caption,"type":"photo"}
        elif update.message.voice:
            new_message={"voice_id":str(update.message.voice.file_id),"type":"voice"}
        elif update.message.sticker:
            new_message={"sticker_id":str(update.message.sticker.file_id),"type":"sticker"}
        elif update.message.video:
            new_message={"video_id":str(update.message.video.file_id),"caption":update.message.caption,"type":"video"}
        else:
            await update.message.reply_text("البوت لا يستقبل هذا النوع من الملفات.\n اضغط /send لاعاده المحاولة.")
            data_file["members"][user_id]["name"] = user_full_name
            data_file["members"][user_id]["user_name"] = user_user_name
            data_file["members"][user_id]["device_languages"] = user_device_languages
            data_file["members"][user_id]["premium_status_on_last_registration"] = user_is_subscribed
            data_file["members"][user_id]["last_join"] = date()
            save_data_base(data_file)
            return

        data_file["members"][user_id]["name"]=user_full_name
        data_file["members"][user_id]["user_name"]=user_user_name
        data_file["members"][user_id]["device_languages"]=user_device_languages
        data_file["members"][user_id]["premium_status_on_last_registration"]=user_is_subscribed
        data_file["members"][user_id]["last_join"]=date()
        data_file["members"][user_id]["his_message"].append({"message_text":new_message,
                                                             "message_time":date(),
                                                             "is_admin_answered":False})
        save_data_base(data_file)
        await context.bot.send_message(chat_id=data_file["admin_id"][0],text="سيدي , لقد وصلتك رسالة")
        await update.message.reply_text("تم ارسال الرسالة شكرا على مراسلتنا.")

        context.user_data.clear()
    else:
        await update.message.reply_text("الرجاء الضغط على /start.")


async def commands (update:Update, context: ContextTypes.DEFAULT_TYPE):
    text=update.message.text
    setup=context.user_data.get("setup")
    file_data= read_data_base()
    user_id = str(update.effective_user.id)


    if is_admen(user_id):
        if text == "1-رؤية الرسائل التي لم ترد عليها والرد عليها.":
            msg_id = find_messages()
            if msg_id is not None :
                await context.bot.send_message(chat_id=file_data["admin_id"][0],
            text=(f"""تم تنفيذ أمرك سيدي.

الاسم: {file_data['members'][msg_id[1]]['name']}
اسم المستخدم: {file_data['members'][msg_id[1]]['user_name']}
رقم المستخدم: {file_data['members'][msg_id[1]]['user_id']}
"""
            ))

            
                context.user_data["setup"]="waiting_answer"
                if file_data["members"][msg_id[1]]["his_message"][msg_id[2]]["message_text"]["type"] == "text":
                    await update.message.reply_text(file_data["members"][msg_id[1]]["his_message"][msg_id[2]]["message_text"]["text"])
                    con="text"
                elif file_data["members"][msg_id[1]]["his_message"][msg_id[2]]["message_text"]["type"] == "photo":
                    await context.bot.send_photo(chat_id=user_id,photo=file_data["members"][msg_id[1]]["his_message"][msg_id[2]]["message_text"]["photo_id"],
                    caption=file_data["members"][msg_id[1]]["his_message"][msg_id[2]]["message_text"].get("caption","لا يوجد"))
                    con="photo_id"
                elif file_data["members"][msg_id[1]]["his_message"][msg_id[2]]["message_text"]["type"] == "voice":
                    await context.bot.send_voice(chat_id=user_id,voice=file_data["members"][msg_id[1]]["his_message"][msg_id[2]]["message_text"]["voice_id"])
                    con="voice_id"
                elif file_data["members"][msg_id[1]]["his_message"][msg_id[2]]["message_text"]["type"] == "sticker":
                    await context.bot.send_sticker(chat_id=user_id,sticker=file_data["members"][msg_id[1]]["his_message"][msg_id[2]]["message_text"]["sticker_id"])
                    con="sticker_id"
                elif file_data["members"][msg_id[1]]["his_message"][msg_id[2]]["message_text"]["type"] == "video":
                    await context.bot.send_video(chat_id=user_id,video=file_data["members"][msg_id[1]]["his_message"][msg_id[2]]["message_text"]["video_id"],
                    caption=file_data["members"][msg_id[1]]["his_message"][msg_id[2]]["message_text"].get("caption","لا يوجد"))
                    con="video_id"
                else:
                    await update.message.reply_text("حدث خطا!")
                
                context.user_data["reply_to_id"]=msg_id[1]
                context.user_data["num_of_message"]=msg_id[2]
                context.user_data["message_text"]=file_data["members"][msg_id[1]]["his_message"][msg_id[2]]["message_text"][con]

                file_data["members"][context.user_data.get("reply_to_id")]["his_message"][context.user_data.get("num_of_message")]["is_admin_answered"]=True
            else:
                await update.message.reply_text("انتهت الرسائل سيدي,هل لديك اوامر اخرى؟", reply_markup=admin_commands_final)

        elif text == "2-رؤية الاعضاء الذين تم حظرهم والغاء حظر المستخدمين المحظورين.":
            banned_users=[]
            show_banned_users_in=show_banned_users()
            await update.message.reply_text(f"عدد الاعضاء الذين تم تبنيدهم هو {show_banned_users_in[0]}")
            context.user_data["banned_users_num"]=show_banned_users_in[0]
            context.user_data["banned_users_name"]=show_banned_users_in[1:]
            banned_users_num = context.user_data.get("banned_users_num")
            banned_users_name=context.user_data.get("banned_users_name")
            if int(banned_users_num) >0 :
                for id_list in banned_users_name:
                    id=str(id_list[0])
                    banned_users.append("\nid:")
                    banned_users.append(id)
                    banned_users.append("\nname:")
                    banned_users.append(file_data["members"][id]["name"])
                    banned_users.append("\nuser name:")
                    banned_users.append(file_data["members"][id]["user_name"])
                banned_users="\n".join(map(str,banned_users))
                await update.message.reply_text(f"الاعضاء الذين تم تبديدهم هم:{banned_users}")
                await update.message.reply_text("اذا كنت تريد الغاء حظر مستخدم اكتب ايديه واذا لا اضغط على /commands")
                context.user_data["setup"]="waiting_id"
        
        elif text == "3-حظر مستخدم":
            await update.message.reply_text("تم استلام الامر سيدي , ما هو الايدي الذي تريد حظره؟")
            context.user_data["setup"]="waiting_id_to_block"
        
        elif text == "4-اذاعة رسالة.":
            await update.message.reply_text("تم استلام الامر سيدي , ما هي الرسالة التي تريد اذاعتها؟")
            context.user_data["setup"]="waiting_message_to_send"
        elif text == "5-رؤية الاعضاء في هذا البوت." :
            users_user_name= []
            for id in name_num_of_users()[1]:
                users_user_name.append(f"{file_data['members'][id]['user_name']}:😃     {str(id)}")
            await update.message.reply_text(((((str(users_user_name).replace(",","\n")).replace("[","")).replace("]",""))).replace("😃","\n"))
            await update.message.reply_text("هذه هي اسماء المستخدمين سيدي لكن ان اردت معلومات اكثر عن احدهم اكتب ايديه. ")
            context.user_data["setup"]="waiting_id_to_get_info"




        else:
            await update.message.reply_text("اهلا بك سيدي , ما هي اوامرك :", reply_markup=admin_commands_final)
        



    else:
        await update.message.reply_text("ليس من المفترض ان تكون هنا هذه الصلاحيات للادمن فقط \n اضغط على /start للبدا ")
        return


app.add_handler(CommandHandler("start",start))
app.add_handler(CommandHandler("send",send))
app.add_handler(CommandHandler("commands",commands))
app.add_handler(MessageHandler(filters.Text(admin_commands_exepting),commands))
app.add_handler(MessageHandler(filters.ALL&(~filters.COMMAND)&(~filters.Text(admin_commands_exepting)),send))
app.run_polling()


#have fun