#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json
from pathlib import Path
import sqlite3
import csv
import re
import webbrowser
from datetime import datetime
import random

class LeadDB:
    def __init__(self):
        self.conn = sqlite3.connect("yeldiz_leads.db", check_same_thread=False)
        self.conn.execute('''CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY, date TEXT, name TEXT, mobile TEXT UNIQUE,
            reg_no TEXT, car_model TEXT, variant TEXT, year TEXT, km TEXT,
            address TEXT, follow_up TEXT, source TEXT, context TEXT, license TEXT,
            remark TEXT, platform TEXT, city TEXT, is_owner INTEGER, msg_sent INTEGER,
            whatsapp_sent INTEGER, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
        self.conn.commit()
    
    def add_lead(self, lead):
        m = lead.get("mobile", "").strip()
        if not m: return False, "No mobile"
        try:
            self.conn.execute('''INSERT INTO leads VALUES (NULL,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,CURRENT_TIMESTAMP)''', (
                lead.get("date", datetime.now().strftime("%Y-%m-%d")), lead.get("name", "N/A"), m,
                lead.get("reg_no", "N/A"), lead.get("car_model", "N/A"), lead.get("variant", "N/A"),
                lead.get("year", "N/A"), lead.get("km", "N/A"), lead.get("address", "N/A"),
                "Pending", "Unknown", "", "Verified", "", lead.get("platform", "Unknown"),
                lead.get("city", "Unknown"), 1, 0, 0
            ))
            self.conn.commit()
            return True, m
        except:
            return False, "Duplicate"
    
    def get_stats(self):
        today = datetime.now().strftime("%Y-%m-%d")
        total = self.conn.execute("SELECT COUNT(*) FROM leads").fetchone()[0] or 0
        today_c = self.conn.execute("SELECT COUNT(*) FROM leads WHERE date=?", (today,)).fetchone()[0] or 0
        owners = self.conn.execute("SELECT COUNT(*) FROM leads WHERE is_owner=1 AND date=?", (today,)).fetchone()[0] or 0
        return {"total": total, "today": today_c, "owners": owners}
    
    def export(self):
        fn = f"YELDIZ_LEADS_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        rows = self.conn.execute("SELECT date,name,mobile,reg_no,car_model,variant,year,km,address,follow_up,source,context,license,remark FROM leads ORDER BY created_at DESC").fetchall()
        with open(fn, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["DATE","NAME","MOBILE","REG_NO","CAR_MODEL","VARIANT","YEAR","KM","ADDRESS","FOLLOW_UP","SOURCE","CONTEXT","LICENSE","REMARK"])
            w.writerows(rows)
        return fn

if __name__ == "__main__":
    print("[✓] YELDIZ AI v2.0 Ready!")
    print("[✓] GitHub Repository: https://github.com/umairraza9464-spec/yeldiz-ai")
