import os
import xml.etree.ElementTree as ET
import tkinter as tk
from tkinter import messagebox

def modify_game_files():
    # قائمة بالمسارات الشائعة المحتملة لملف الحفظ
    possible_paths = [
        "/storage/emulated/0/Android/data/com.playrix.township/files/default.xml",
        "/sdcard/Android/data/com.playrix.township/files/default.xml",
        "/data/data/com.playrix.township/files/default.xml",
    ]
    
    target_file = None
    for path in possible_paths:
        if os.path.exists(path):
            target_file = path
            break
            
    if not target_file:
        # إذا لم يتم العثور عليه تلقائياً، يمكن وضعه يدوياً أو إظهار رسالة
        target_file = entry_path.get().strip().strip('"').strip("'")
        
    if not target_file or not os.path.exists(target_file):
        messagebox.showerror("خطأ", "لم يتم العثور على ملف الحفظ أو المسار غير صحيح!")
        return

    try:
        tree = ET.parse(target_file)
        root = tree.getroot()
        
        new_coins = entry_coins.get().strip()
        new_cash = entry_cash.get().strip()
        
        if not new_coins or not new_cash:
            messagebox.showwarning("تنبيه", "الرجاء إدخال القيم المطلوبة للعملات والكاش!")
            return

        updated = False
        for elem in root.iter():
            if elem.tag == 'coins' or elem.tag == 'Money':
                elem.text = new_coins
                updated = True
            elif elem.tag == 'cash' or elem.tag == 'Banknotes':
                elem.text = new_cash
                updated = True

        tree.write(target_file, encoding='utf-8', xml_declaration=True)
        messagebox.SUCCESS("نجاح", "تم تعديل وحفظ القيم في اللعبة بنجاح تام!")
        
    except Exception as e:
        messagebox.showerror("خطأ", f"حدث خطأ أثناء تعديل الملف: {e}")

# بناء الواجهة الرسومية (GUI)
root = tk.Tk()
root.title("أداة تعديل Township")
root.geometry("350x400")
root.config(bg="#f0f0f0")

title_label = tk.Label(root, text="أداة تعديل Township", font=("Arial", 16, "bold"), bg="#f0f0f0", fg="#333")
title_label.pack(pady=15)

# حقل العملات
tk.Label(root, text="عدد العملات (Coins):", font=("Arial", 12), bg="#f0f0f0").pack(anchor="w", padx=30)
entry_coins = tk.Entry(root, font=("Arial", 12), width=25)
entry_coins.pack(pady=5)

# حقل الكاش
tk.Label(root, text="عدد الكاش (Cash):", font=("Arial", 12), bg="#f0f0f0").pack(anchor="w", padx=30)
entry_cash = tk.Entry(root, font=("Arial", 12), width=25)
entry_cash.pack(pady=5)

# حقل المسار اليدوي (احتياطي)
tk.Label(root, text="مسار الملف (اختياري لو لم يُوجد تلقائياً):", font=("Arial", 10), bg="#f0f0f0").pack(anchor="w", padx=30, pady=(10,0))
entry_path = tk.Entry(root, font=("Arial", 10), width=30)
entry_path.pack(pady=5)

# زر التعديل الرئيسي (يشبه أزرار التطبيقات الجاهزة)
btn_modify = tk.Button(root, text="تعديل وحفظ القيم", font=("Arial", 14, "bold"), bg="#4CAF50", fg="white", width=20, command=modify_game_files)
btn_modify.pack(pady=20)

root.mainloop()