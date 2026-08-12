#!/usr/bin/env python3
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import minecraft_launcher_lib
import subprocess
import threading
from pathlib import Path

# Строгая черно-голубая палитра независимого софта
COLOR_BG = "#0f1015"        # Глубокий черный фон
COLOR_CARD = "#161720"      # Темно-серый контейнер карточек
COLOR_TEXT = "#ffffff"      # Чистый белый текст
COLOR_MUTED = "#525870"     # Приглушенный серый
COLOR_ACCENT = "#00a2ff"    # Яркий неоновый голубой (Arch)
COLOR_HOVER = "#33b5ff"     # Светло-голубой при наведении

minecraft_dir = str(Path.home() / ".arch_minecraft")
version = "1.20.1"

# Чистый и аккуратный список популярных серверов
SERVERS = [
    " Hypixel Network            [mc.hypixel.net]",
    " Mineplex                   [://mineplex.com]",
    " Wynncraft RPG              [://wynncraft.com]",
    " 2B2T Anarchy               [2b2t.org]",
    " CubeCraft Games            [play.cubecraft.net]",
    " HiveMC                     [://hivemc.com]"
]

def main():
    root = tk.Tk()
    root.title("Arch Launcher")
    root.geometry("720x420")
    root.configure(bg=COLOR_BG)
    root.resizable(False, False)

    # Кастомный заголовок окна в левом верхнем углу
    top_bar = tk.Frame(root, bg=COLOR_BG)
    top_bar.pack(anchor="w", padx=25, pady=(20, 10), fill=tk.X)
    
    title_label = tk.Label(top_bar, text="Arch Launcher", font=("Helvetica", 16, "bold"), bg=COLOR_BG, fg=COLOR_TEXT)
    title_label.pack(side=tk.LEFT)
    
    ver_label = tk.Label(top_bar, text=f"v0.3 (Core: {version})", font=("Helvetica", 9), bg=COLOR_BG, fg=COLOR_MUTED)
    ver_label.pack(side=tk.LEFT, padx=10, pady=5)

    # Настройка стандартных стилей элементов
    style = ttk.Style()
    style.theme_use('default')
    style.configure("TProgressbar", thickness=8, background=COLOR_ACCENT, troughcolor=COLOR_CARD)

    # Главный контейнер (разделен на Левую и Правую части)
    main_frame = tk.Frame(root, bg=COLOR_BG)
    main_frame.pack(padx=25, pady=5, fill=tk.BOTH, expand=True)

    # ================= ЛЕВАЯ ЧАСТЬ: СПИСОК СЕРВЕРОВ =================
    left_frame = tk.Frame(main_frame, bg=COLOR_CARD, bd=0, highlightbackground="#222430", highlightthickness=1)
    left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

    server_title = tk.Label(left_frame, text=" Доступные серверы для подключения:", font=("Helvetica", 10, "bold"), bg=COLOR_CARD, fg=COLOR_ACCENT, anchor="w")
    server_title.pack(fill=tk.X, pady=(15, 8), padx=15)

    server_list = tk.Listbox(
        left_frame, 
        bg=COLOR_BG, 
        fg=COLOR_TEXT, 
        bd=0, 
        highlightthickness=1, 
        highlightbackground="#222430",
        font=("Courier", 10),
        selectbackground=COLOR_ACCENT, 
        selectforeground=COLOR_BG, 
        activestyle="none"
    )
    for srv in SERVERS:
        server_list.insert(tk.END, srv)
    server_list.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))

    # ================= ПРАВАЯ ЧАСТЬ: УПРАВЛЕНИЕ И ВВОД =================
    right_frame = tk.Frame(main_frame, bg=COLOR_CARD, bd=0, highlightbackground="#222430", highlightthickness=1, width=280)
    right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(10, 0))
    right_frame.pack_propagate(False)

    label_user = tk.Label(right_frame, text="Идентификатор сессии", font=("Helvetica", 10, "bold"), bg=COLOR_CARD, fg=COLOR_TEXT)
    label_user.pack(pady=(35, 5))

    # Поле ввода ника
    entry_user = tk.Entry(right_frame, font=("Helvetica", 11), bg=COLOR_BG, fg=COLOR_TEXT, insertbackground=COLOR_TEXT, bd=0, highlightthickness=1, highlightbackground="#222430", highlightcolor=COLOR_ACCENT, justify="center")
    entry_user.insert(0, "David")
    entry_user.pack(pady=5, ipady=6, padx=30, fill=tk.X)

    status_label = tk.Label(right_frame, text="Проверка системного окружения...", font=("Helvetica", 9), bg=COLOR_CARD, fg=COLOR_MUTED, wraplength=240, justify="center")
    status_label.pack(pady=(20, 5))

    # Прогресс-бар скачивания
    progress = ttk.Progressbar(right_frame, style="TProgressbar", mode="indeterminate", maximum=100)
    progress.pack(fill=tk.X, padx=30, pady=5)

    # Кнопка ИГРАТЬ (изначально скрыта)
    btn_play = tk.Button(right_frame, text="ИГРАТЬ", font=("Helvetica", 11, "bold"), bg=COLOR_ACCENT, fg=COLOR_BG, activebackground=COLOR_HOVER, activeforeground=COLOR_BG, bd=0, cursor="hand2")

    # Функции для безопасного изменения текста статуса из фонового потока
    def set_status_safe(text, color=COLOR_MUTED):
        root.after(0, lambda: status_label.config(text=text, fg=color))

    def update_status_text(text):
        # Сама библиотека при скачивании будет присылать логи, мы их красиво укорачиваем
        clean_text = text.replace("Downloading", "Скачивание:").split("/")[-1]
        set_status_safe(clean_text)

    def launch_game():
        username = entry_user.get().strip()
        if not username:
            messagebox.showerror("Ошибка", "Введите ваш игровой ник!")
            return
        
        set_status_safe("Запуск ядра Java...", COLOR_ACCENT)
        btn_play.config(state=tk.DISABLED, text="ЗАПУСК...")
        
        def run():
            options = {"username": username, "uuid": "00000000-0000-0000-0000-000000000000", "token": "0"}
            cmd = minecraft_launcher_lib.command.get_minecraft_command(version, minecraft_dir, options)
            set_status_safe("Процесс передан системе.", COLOR_TEXT)
            root.after(0, lambda: btn_play.config(state=tk.NORMAL, text="ИГРАТЬ"))
            subprocess.call(cmd)
            
        threading.Thread(target=run, daemon=True).start()

    btn_play.config(command=launch_game)

    # Фоновый поток автоматической загрузки ассетов и библиотек при старте
    def download_assets():
        try:
            progress.start(15) 
            set_status_safe("Подключение к серверам Mojang...")
            
            # Навешиваем колбэк-мониторинг, чтобы видеть имена скачиваемых файлов прямо на экране
            callbacks = {"setStatus": update_status_text}
            minecraft_launcher_lib.install.install_minecraft_version(version, minecraft_dir, callback=callbacks)
            
            # Как только всё скачалось — останавливаем анимацию, прячем бар и выводим кнопку ИГРАТЬ
            root.after(0, progress.stop)
            root.after(0, progress.pack_forget) 
            
            set_status_safe("Синхронизация завершена. Клиент готов.", "#50fa7b")
            root.after(0, lambda: btn_play.pack(pady=(10, 20), ipady=10, padx=30, fill=tk.X))
            
            # Эффекты наведения на кнопку
            btn_play.bind("<Enter>", lambda e: btn_play.config(bg=COLOR_HOVER))
            btn_play.bind("<Leave>", lambda e: btn_play.config(bg=COLOR_ACCENT))
            
        except Exception as e:
            set_status_safe("Ошибка загрузки библиотек.", "#ff5555")
            root.after(0, progress.stop)

    threading.Thread(target=download_assets, daemon=True).start()

    root.mainloop()

if __name__ == "__main__":
    main()
