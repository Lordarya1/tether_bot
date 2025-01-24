# import yt_dlp
# import requests
# import random
# import tkinter as tk
# from tkinter import filedialog, messagebox, ttk
# import threading

# # متغیر برای ذخیره پروکسی
# proxy_list = []

# # تابع برای دریافت پروکسی‌ها
# def fetch_proxies():
#     global proxy_list
#     try:
#         response = requests.get("https://www.proxy-list.download/api/v1/get?type=http")  # دریافت لیست پروکسی
#         if response.status_code == 200:
#             proxy_list = response.text.splitlines()
#             print(f"{len(proxy_list)} پروکسی دریافت شد.")
#         else:
#             messagebox.showerror("خطا", "خطا در دریافت پروکسی‌ها!")
#     except Exception as e:
#         print(f"خطا در دریافت پروکسی‌ها: {e}")
#         proxy_list = []

# # تابع برای بررسی اعتبار پروکسی
# def validate_proxy(proxy):
#     try:
#         response = requests.get("http://www.google.com", proxies={"http": proxy, "https": proxy}, timeout=5)
#         return response.status_code == 200
#     except:
#         return False

# # تابع دانلود ویدیو
# def download_video():
#     try:
#         url = url_input.get().strip()
#         folder = folder_path.get().strip()

#         if not url:
#             messagebox.showerror("خطا", "لطفاً لینک ویدیو را وارد کنید!")
#             return
#         if not folder:
#             messagebox.showerror("خطا", "لطفاً مسیر ذخیره‌سازی را انتخاب کنید!")
#             return

#         if not proxy_list:
#             fetch_proxies()  # دریافت پروکسی‌ها اگر لیست خالی است

#         # بررسی و انتخاب پروکسی معتبر
#         valid_proxies = [proxy for proxy in proxy_list if validate_proxy(f"http://{proxy}")]
#         if not valid_proxies:
#             messagebox.showerror("خطا", "هیچ پروکسی معتبر یافت نشد!")
#             return
#         proxy = random.choice(valid_proxies)
#         proxies = f"http://{proxy}"
#         print(f"استفاده از پروکسی: {proxies}")

#         # تنظیمات yt-dlp
#         def progress_hook(d):
#             if d['status'] == 'downloading':
#                 downloaded = d.get('downloaded_bytes', 0)
#                 total = d.get('total_bytes', 1)
#                 percent = int(downloaded / total * 100)
#                 progress_var.set(percent)

#         ydl_opts = {
#             'outtmpl': f'{folder}/%(title)s.%(ext)s',
#             'format': 'bestvideo+bestaudio/best',
#             'proxy': proxies,  # تنظیم پروکسی
#             'progress_hooks': [progress_hook],
#         }

#         # دانلود ویدیو
#         with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#             ydl.download([url])

#         messagebox.showinfo("دانلود موفق", "ویدیو با موفقیت دانلود شد!")
#     except Exception as e:
#         messagebox.showerror("خطا", f"مشکلی پیش آمده است:\n{str(e)}")
#         print(f"خطا: {e}")
#     finally:
#         progress_var.set(0)  # ریست کردن نوار پیشرفت

# # اجرای دانلود در رشته جداگانه
# def download_video_thread():
#     thread = threading.Thread(target=download_video, daemon=True)
#     thread.start()

# # تابع فعال‌سازی منوی کلیک راست (کپی، پیست و کات)
# def make_entry_context_menu(entry):
#     def copy():
#         entry.event_generate("<<Copy>>")
#     def paste():
#         entry.event_generate("<<Paste>>")
#     def cut():
#         entry.event_generate("<<Cut>>")

#     menu = tk.Menu(app, tearoff=0)
#     menu.add_command(label="کپی", command=copy)
#     menu.add_command(label="پیست", command=paste)
#     menu.add_command(label="کات", command=cut)

#     def show_context_menu(event):
#         menu.post(event.x_root, event.y_root)

#     entry.bind("<Button-3>", show_context_menu)  # فعال‌سازی منوی کلیک راست
#     entry.bind("<Control-c>", lambda e: copy())  # فعال‌سازی Ctrl+C
#     entry.bind("<Control-v>", lambda e: paste())  # فعال‌سازی Ctrl+V
#     entry.bind("<Control-x>", lambda e: cut())  # فعال‌سازی Ctrl+X

# # تنظیم رابط گرافیکی
# app = tk.Tk()
# app.title("youtube downloader")
# app.geometry("500x450")
# app.resizable(False, False)

# # متغیرها برای ورودی‌ها
# url_input = tk.StringVar()
# folder_path = tk.StringVar()
# progress_var = tk.IntVar()

# # رابط گرافیکی
# tk.Label(app, text="لینک ویدیو یوتیوب:", font=("Arial", 12, "bold")).pack(pady=10)
# url_entry = tk.Entry(app, textvariable=url_input, width=50, font=("Arial", 10))
# url_entry.pack(pady=5)
# make_entry_context_menu(url_entry)  # اضافه کردن کلیک راست به ورودی لینک

# tk.Label(app, text="مسیر ذخیره‌سازی:", font=("Arial", 12, "bold")).pack(pady=10)
# folder_entry = tk.Entry(app, textvariable=folder_path, width=50, font=("Arial", 10))
# folder_entry.pack(pady=5)
# make_entry_context_menu(folder_entry)  # اضافه کردن کلیک راست به ورودی مسیر ذخیره‌سازی

# tk.Button(app, text="انتخاب مسیر", command=lambda: folder_path.set(filedialog.askdirectory()), font=("Arial", 10), bg="#007BFF", fg="white").pack(pady=5)

# progress_bar = ttk.Progressbar(app, orient="horizontal", length=400, mode="determinate", variable=progress_var)
# progress_bar.pack(pady=15)

# tk.Button(app, text="⬇️ دانلود ویدیو ⬇️", command=download_video_thread, font=("Arial", 14, "bold"), bg="#28A745", fg="white", width=20, height=2).pack(pady=20)

# # اجرای برنامه
# app.mainloop()


import tkinter as tk
from tkinter import ttk
import requests
import threading
import time
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import rcParams
from matplotlib import font_manager

# تنظیم فونت فارسی در Matplotlib
iran_sans_font_path = "Vazir-Bold.ttf"  # مسیر فایل فونت ایران‌سانس
iran_sans_font = font_manager.FontProperties(fname=iran_sans_font_path)
rcParams["font.family"] = iran_sans_font.get_name()

# تابع برای دریافت قیمت لحظه‌ای تتر از نوبیتکس
def fetch_tether_price():
    try:
        url = "https://api.nobitex.ir/v2/orderbook/USDTIRT"
        response = requests.get(url, timeout=10)
        data = response.json()
        if data.get("status") == "ok" and "asks" in data:
            # گرفتن اولین قیمت فروش (ask)
            return float(data["asks"][0][0])
        else:
            print("ساختار API تغییر کرده است.")
            return None
    except requests.exceptions.RequestException as e:
        print(f"خطا در اتصال به API: {e}")
        return None

# فرمت قیمت با کاما و اضافه کردن "تومان"
def format_price(price):
    return f"{price:,.0f} ریال"

# به‌روزرسانی قیمت در رابط گرافیکی
def update_price():
    global previous_price  # قیمت قبلی را به‌عنوان متغیر جهانی تعریف می‌کنیم
    while True:
        price = fetch_tether_price()
        if price:
            # محاسبه تغییر قیمت
            if previous_price is not None:
                change = price - previous_price
                if change > 0:
                    change_label.config(text=f"▲ {format_price(change)}", fg="green")
                elif change < 0:
                    change_label.config(text=f"▼ {format_price(abs(change))}", fg="red")
                else:
                    change_label.config(text="بدون تغییر", fg="gray")
            else:
                change_label.config(text="بدون تغییر", fg="gray")

            # به‌روزرسانی قیمت فعلی
            previous_price = price
            price_label.config(text=format_price(price))

            # ذخیره قیمت برای رسم نمودار
            prices.append(price)
            if len(prices) > 50:  # نگه‌داشتن آخرین 50 قیمت
                prices.pop(0)
            update_chart()  # به‌روزرسانی نمودار
        else:
            price_label.config(text="خطا در دریافت قیمت")
        time.sleep(5)  # هر 5 ثانیه قیمت را به‌روزرسانی کن

# رسم نمودار قیمت
def update_chart():
    fig.clear()
    ax = fig.add_subplot(111)
    ax.plot(prices, marker="o", linestyle="-", color="cyan", label="قیمت تتر")
    ax.set_facecolor("#2b2b2b")
    ax.set_title("نمودار قیمت لحظه‌ای تتر", fontproperties=iran_sans_font, color="white")
    ax.set_ylabel("قیمت (تومان)", fontproperties=iran_sans_font, color="white")
    ax.set_xlabel("زمان", fontproperties=iran_sans_font, color="white")
    ax.tick_params(colors="white")
    ax.legend(prop=iran_sans_font, facecolor="#3c3c3c", edgecolor="white")
    canvas.draw()

# رابط گرافیکی
root = tk.Tk()
root.title("نمایش لحظه‌ای قیمت تتر")
root.geometry("600x600")
root.configure(bg="#1e1e1e")

# تنظیم فونت ایران‌سانس برای Tkinter
iran_sans_tk = (iran_sans_font.get_name(), 20)

# عنوان اصلی
title_label = tk.Label(root, text="قیمت لحظه‌ای تتر", font=iran_sans_tk, bg="#1e1e1e", fg="white")
title_label.pack(pady=20)

# نمایش قیمت
price_label = tk.Label(root, text="در حال دریافت قیمت...", font=(iran_sans_font.get_name(), 35, "bold"), bg="#1e1e1e", fg="cyan")
price_label.pack(pady=10)

# نمایش تغییر قیمت
change_label = tk.Label(root, text="بدون تغییر", font=iran_sans_tk, bg="#1e1e1e", fg="gray")
change_label.pack(pady=10)

# نمودار قیمت
fig = Figure(figsize=(5, 3), dpi=100)
fig.patch.set_facecolor("#1e1e1e")
prices = []  # لیست ذخیره قیمت‌ها
previous_price = None  # قیمت قبلی
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(pady=20)

# شروع به‌روزرسانی قیمت در یک رشته (Thread)
thread = threading.Thread(target=update_price, daemon=True)
thread.start()

# اجرای برنامه
root.mainloop()