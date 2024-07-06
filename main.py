import threading
import time
from tkinter import *
from tkinter.ttk import Progressbar
import speedtest


def animate_speed(speed_value, progress_bar, scaling_factor):
    def animate():
        max_value = speed_value * scaling_factor
        increment = max_value / 100
        for i in range(int(max_value) + 1):
            progress_bar['value'] = i
            progress_bar.update()
            time.sleep(0.02)

    threading.Thread(target=animate).start()


def check_speed():
    try:
        download_label.config(text="Testing Download Speed...")
        upload_label.config(text="Testing Upload Speed...")
        ping_label.config(text="Testing Ping...")

        st = speedtest.Speedtest()

        download_speed = st.download() / 1000000
        download_label.config(text=f"Download Speed: {download_speed:.2f} Mbps")
        animate_speed(download_speed, download_progress, 5)

        upload_speed = st.upload() / 1000000
        upload_label.config(text=f"Upload Speed: {upload_speed:.2f} Mbps")
        animate_speed(upload_speed, upload_progress, 3)

        ping = st.results.ping
        ping_label.config(text=f"Ping: {ping:.2f} ms")
        animate_speed(ping, ping_progress, 2)

    except Exception as e:
        download_label.config(text="Error: Unable to fetch speeds")
        upload_label.config(text="")
        ping_label.config(text="")
        print(f"Error: {e}")


def threaded_check_speed():
    threading.Thread(target=check_speed).start()


root = Tk()
root.title("Internet Speed Checker")
root.config(bg="#212121")
root.geometry("500x400")
root.resizable(False, False)

label1 = Label(root, text="Internet Speed Checker", font=(
    "Helvetica", 30, "bold"), bg="#212121", fg="#ffffff")
label1.pack()

download_label = Label(root, font=("Helvetica", 16),
                       bg="#212121", fg="#ffffff")
download_label.pack(pady=10)

download_progress = Progressbar(
    root, orient=HORIZONTAL, length=300, mode='determinate')
download_progress.pack(pady=10)

upload_label = Label(root, font=("Helvetica", 16), bg="#212121", fg="#ffffff")
upload_label.pack(pady=10)

upload_progress = Progressbar(
    root, orient=HORIZONTAL, length=300, mode='determinate')
upload_progress.pack(pady=10)

ping_label = Label(root, font=("Helvetica", 16), bg="#212121", fg="#ffffff")
ping_label.pack(pady=10)

ping_progress = Progressbar(root, orient=HORIZONTAL,
                            length=300, mode='determinate')
ping_progress.pack(pady=10)

button_refresh = Button(root, text="Refresh", font=(
    "Helvetica", 14, "bold"), bg="#03a9f4", fg="#ffffff", command=threaded_check_speed)
button_refresh.pack(pady=20)

threaded_check_speed()

root.mainloop()
