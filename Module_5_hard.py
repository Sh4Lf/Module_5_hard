import hashlib


class User:
    def __init__(self, nickname, password, age):
        self.nickname = nickname
        self.password = hashlib.sha256(password.encode()).hexdigest()
        self.age = age
        self.adult_mode = False

    def toggle_adult_mode(self):
        self.adult_mode = not self.adult_mode


class Video:
    def __init__(self, title, description, adult_mode):
        self.title = title
        self.description = description
        self.adult_mode = adult_mode
        self.time_now = 0


class UrTube:
    def __init__(self):
        self.users = {}  # Хранит пользователей
        self.videos = []  # Хранит видео

    def register(self, nickname, password, age):
        if nickname in self.users:
            raise ValueError("Пользователь с таким ником уже существует.")
        self.users[nickname] = User(nickname, password, age)
        print(f"Пользователь {nickname} успешно зарегистрирован.")

    def log_out(self, nickname):
        if nickname not in self.users:
            raise ValueError("Пользователь не найден.")

        print(f"Пользователь {nickname} успешно вышел из системы.")

    def login(self, nickname, password):
        user = self.users.get(nickname)
        if not user:
            raise ValueError("Пользователь не найден.")
        if user.password != hashlib.sha256(password.encode()).hexdigest():
            raise ValueError("Неверный пароль.")

    def add_video(self, title, description, adult_mode):
        video = Video(title, description, adult_mode)
        self.videos.append(video)
        print(f"Видео {title} успешно добавлено.")

    def watch_video(self, nickname, title):
        user = self.users.get(nickname)
        if not user:
            raise ValueError("Пользователь не найден.")

        for video in self.videos:
            if video.title.lower() == title.lower():
                if video.adult_mode and not user.adult_mode and user.age < 18:
                    raise ValueError("Доступ запрещен: это видео предназначено для взрослых.")
                video.time_now += 1  # Увеличение времени просмотра
                return f"Вы смотрите видео: {video.title} - {video.description} на секунде {video.time_now}"

        raise ValueError("Видео не найдено.")

    def get_videos(self):
        return [
            (video.title, video.description)
            for video in self.videos
            if not video.adult_mode or (video.adult_mode and any(user.adult_mode for user in self.users.values()))
        ]


# Пример использования
if __name__ == "__main__":
    urtube = UrTube()

    v1 = Video("Котики", "Весёлые моменты с котиками", False)

    # Добавление видео
    urtube.add_video('Котики', 'Весёлые моменты с котиками', False)

    # Регистрация пользователей
    urtube.register("Sh4Lf", "987654321", 25)
    urtube.register("amorevelo", "miska1234", 15)

    # Добавление видео

    urtube.add_video("Как скачать PyCharm", "Ресурс для скачивания. Метод установки.", False)
    urtube.add_video("DeepMIX", "Музыкальный сет с лёгкой электронной музыкой.", False)
    urtube.add_video("Видео для взрослых", "Это видео для взрослых.", True)

    # Использование методов
    print(urtube.watch_video("Sh4Lf", "Котики"))
    try:
        print(urtube.watch_video("amorevelo", "Котики"))
        print(urtube.watch_video("amorevelo", "Видео для взрослых"))
    except ValueError as e:
        print(e)

    # Переключение режима для взрослых
    urtube.users["Sh4Lf"].toggle_adult_mode()
    print(urtube.watch_video("Sh4Lf", "Видео для взрослых"))

    # Получение списка видео
    print(urtube.get_videos())