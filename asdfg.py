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
