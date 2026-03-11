EN
# 🤖 Telegram Admin Master

### Overview
**Telegram Admin Master** is a comprehensive, open-source management solution designed to streamline the administration of Telegram communities. Built with the `python-telegram-bot` framework, this bot acts as a centralized command center for administrators, enabling efficient user management, automated moderation, and direct communication channels.

### 🌟 Key Features
* **Intelligent Spam Protection**: The bot monitors message frequency; users who send messages too rapidly receive warnings and face automated bans after a configurable threshold.
* **Direct Support Ticketing**: Admins can receive private messages from users and reply to them directly within the bot interface.
* **Broadcast Engine**: Reach your entire community instantly with broadcast messages, featuring robust error handling to skip users who have blocked the bot.
* **Persistent JSON Storage**: All user data, chat history, and ban statuses are stored in a local `data.json` database, ensuring data integrity across bot restarts.
* **Admin Control Panel**: A fully interactive interface powered by reply keyboards, making management tasks as simple as clicking a button.

### 🚀 Deployment Guide
1.  **Repository Setup**: Clone this repository to your local machine: `git clone <your-repo-url>`.
2.  **Environment Preparation**: Ensure Python 3.x is installed, then install the required library: `pip install python-telegram-bot`.
3.  **Configuration**: Open `hmm.py` and replace `YOUR_TOKEN_HERE` with your unique bot token obtained from @BotFather. Additionally, verify the file path to `data.json` inside the `read_data_base` and `save_data_base` functions.
4.  **Launch**: Run the bot using the command: `python hmm.py`.

### 📝 Developer's Note
I am truly excited to share this project with the developer community! As a developer, I am continuously refining my skills and codebase. This project represents a milestone in my learning journey. If you happen to encounter any bugs, logical issues, or typos, please accept my sincerest apologies. I warmly welcome any feedback or "Pull Requests" that could help improve this tool. Thank you for choosing my project to power your community!



AR
# 🤖 Telegram Admin Master

### نظرة عامة
**Telegram Admin Master** هو أداة إدارة شاملة ومفتوحة المصدر، صُممت خصيصاً لمساعدة مديري مجموعات وقنوات تيليجرام على تنظيم مجتمعاتهم بفعالية. يعتمد البوت على مكتبة `python-telegram-bot` ليكون بمثابة مركز تحكم متكامل، يتيح لك إدارة الأعضاء، الرد على الاستفسارات، وتطبيق سياسات الحظر تلقائياً.

### 🌟 الميزات الأساسية
* **نظام حماية ذكي من الإزعاج (Spam):** يراقب البوت سرعة إرسال الرسائل، ويقوم بإعطاء تحذيرات للمستخدمين الذين يرسلون رسائل متكررة في وقت قصير، ويحظرهم تلقائياً عند تجاوز الحد المسموح.
* **نظام تذاكر الدعم الفني:** يمكن للأعضاء مراسلة الإدارة عبر البوت، ويمكن للمدير الرد على هذه الرسائل مباشرة من داخل واجهة البوت.
* **محرك البث (Broadcast):** يتيح لك إرسال رسائل إعلانية لجميع الأعضاء بضغطة زر، مع نظام معالجة أخطاء ذكي يتجاهل المستخدمين الذين قاموا بحظر البوت.
* **قاعدة بيانات مستقرة (JSON):** يتم حفظ كافة بيانات المستخدمين، تاريخ المحادثات، وحالات الحظر في ملف `data.json` محلي، مما يضمن عدم ضياع البيانات عند إعادة تشغيل البوت.
* **لوحة تحكم إدارية:** واجهة تفاعلية سهلة الاستخدام تعتمد على أزرار التحكم (Reply Keyboards) لتنفيذ المهام الإدارية بسرعة.

### 🚀 خطوات التشغيل
1.  **نسخ المشروع:** قم بتحميل نسخة من المستودع على جهازك: `git clone <your-repo-url>`.
2.  **تجهيز البيئة:** تأكد من تثبيت Python 3.x، ثم قم بتثبيت المكتبة اللازمة: `pip install python-telegram-bot`.
3.  **إعدادات البوت:** افتح ملف `hmm.py` واستبدل `YOUR_TOKEN_HERE` بـ "توكن" البوت الخاص بك من @BotFather. تأكد أيضاً من تعديل مسار ملف `data.json` في دالتي `read_data_base` و `save_data_base`.
4.  **التشغيل:** قم بتشغيل البوت بالأمر: `python hmm.py`.

### 📝 رسالة من المطور
أنا سعيد جداً باهتمامكم باستخدام مشروعي! بصفتي مطوراً، لا أزال في رحلة تعلم مستمرة، وهذا المشروع يمثل خطوة هامة في مسيرتي البرمجية. إذا واجهتكم أي أخطاء برمجية أو إملائية، أرجو أن تتقبلوا اعتذاري الصادق. ملاحظاتكم واقتراحاتكم لتطوير الكود تعني لي الكثير وتساعدني على النمو. أتمنى أن يكون هذا البوت إضافة مميزة لإدارة مجتمعاتكم!