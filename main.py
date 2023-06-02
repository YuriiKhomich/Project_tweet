"""Примитивный твитер"""

# Словарь для хранения пользователей
users = {}

# Словарь для хранения твитов
tweets = {}

# Словарь для хранения комментариев к твитам
comments = {}

# Словарь для хранения оценок твитов
ratings = {}


def registration():
    """ Регистрация нового пользователя"""
    username = input("Введите имя пользователя: ")
    password = input("Введите пароль: ")
    if username in users:
        print("Пользователь с таким именем уже существует")
    else:
        users[username] = password
        tweets[username] = []
        print(f"Пользователь {username} успешно зарегистрирован.")


def login():
    """ Вход в систему"""
    username = input("Введите имя пользователя: ")
    password = input("Введите пароль: ")
    if username not in users or users[username] != password:
        print("Неверный пароль или логин")
        return None
    print(f"Пользователь {username} успешно авторизован.")
    return username


def create_tweet():
    """ Создание нового твита"""
    tweet = input("Введите текст твита: ")
    print(f"Твит '{tweet}' успешно создан.")
    return tweet


def get_tweet_number(username):
    """Получение номера твита"""
    view_tweets(username)
    tweet_number = input("Выберите номер твита:")
    if tweet_number.isdigit() and 0 < int(tweet_number) <= len(tweets[username]):
        tweet_number = int(tweet_number) - 1
        return tweet_number


def view_tweets(username, other_user=None):
    """Просмотр твитов пользователя или другого пользователя"""
    if other_user is None:
        user_tweets = tweets.get(username, [])
    else:
        user_tweets = tweets.get(other_user, [])
    if user_tweets:
        print(f"Твиты пользователя {username}:")
        for num, tweet in enumerate(user_tweets, start=1):
            print(f"{num}. {tweet}")
            get_tweet_rating(username, num - 1)
            tweet_comments = comments.get((username, num - 1), [])
            if tweet_comments:
                print("Комментарии:")
                for comment_num, (comment_username, comment_text) in enumerate(tweet_comments, start=1):
                    print(f"  {comment_num}. {comment_username}: {comment_text}")
            else:
                print("К этому твиту нет комментариев.")
    else:
        print(f"Пользователь {username} не имеет твитов.")
        return None


def get_tweet_rating(other_user, tweet_number):
    """ Получение оценки за твит и среднеарифметическое значение"""
    tweet_ratings = ratings.get((other_user, tweet_number), [])
    if tweet_ratings:
        ratings_values = [rating for _, rating in tweet_ratings
                          if isinstance(rating, int) and 1 <= rating <= 5]
        if ratings_values:
            average_rating = sum(ratings_values) / len(ratings_values)
            print(f"\n--- Пользователь: {other_user}  ---")
            print(f"Средняя оценка за твит: {average_rating:.2f}")
        else:
            print("У этого твита пока нет оценок.")
    else:
        print("У этого твита пока нет оценок.")


def search_users(username):
    """Меню поиска других пользователей"""
    while True:
        print("\n--- Меню поиска других пользователей ---")
        print("1. Список всех зарегистрированных пользователей")
        print("2. Просмотр профиля пользователя")
        print("3. Назад")
        print("4. Основное меню")
        choice = input("Выберите опцию: ")
        if choice == "1":
            view_users()
        elif choice == "2":
            view_user_profile(username)
        elif choice == "3":
            break
        elif choice == "4":
            main_menu(username)
        else:
            print("Некорректный выбор. Попробуйте еще раз.")


def view_users():
    """Просмотр всех зарегестрированных пользователей"""
    if users:
        print("--- Доступные пользователи ---")
        for i, user in enumerate(users, start=1):
            print(f"{i}. {user}")


def view_user_profile(username):
    """Просмотр профиля пользователя"""
    view_users()
    user_choice = input("Выберите пользователя (введите номер): ")
    if user_choice.isdigit() and int(user_choice) <= len(users):
        other_user = list(users.keys())[int(user_choice) - 1]
        user_profile_menu(username, other_user)
    else:
        print("Пользователь не найден!")


def user_profile_menu(username, other_user):
    """Меню профиля пользователя"""
    while True:
        print(f"\n--- Меню Пользователя {other_user} ---")
        print("1. Посмотреть все твиты")
        print("2. Выбрать твит")
        print("3. Назад")
        print("4. Основное меню")
        choice = input("Выберите опцию: ")
        if choice == "1":
            view_tweets(other_user)
        elif choice == "2":
            read_tweet(username, other_user)
        elif choice == "3":
            break
        elif choice == "4":
            main_menu(username)
        else:
            print("Invalid option. Please try again.")


def read_tweet(username, other_user):
    """Просмотр твита пользователя"""
    if other_user in tweets and tweets[other_user]:
        print(f"--- Твиты {other_user} ---")
        for i, tweet in enumerate(tweets[other_user], start=1):
            print(f"{i}. {tweet}")
        tweet_number = input("Введите желаемый номер твита: ")
        if tweet_number.isdigit() and int(tweet_number) <= len(tweets[other_user]):
            tweet_number = int(tweet_number) - 1
            tweet = tweets[other_user][tweet_number]
            print(f"\n--- {other_user}'s Tweet ---")
            print(tweet)
            while True:
                print("\n--- Твит - меню ---")
                print("1. Оставить комментарий")
                print("2. Просмотреть комментарии")
                print("3. Оценить твит")
                print("4. Назад")
                print("5. Основное меню")
                choice = input("Выберите опцию: ")
                if choice == "1":
                    leave_comment(username, other_user, tweet_number)
                elif choice == "2":
                    view_comments(other_user, tweet_number)
                elif choice == "3":
                    rate_tweet(username, other_user, tweet_number)
                elif choice == "4":
                    break
                elif choice == "5":
                    main_menu(other_user)
                else:
                    print("Неверный выбор. Попробуйте еще раз!")
        else:
            print("Неверный номер твита!")
    else:
        print("Данный пользователь не имеет твитов!")


def leave_comment(username, other_user, tweet_number):
    """Оставление комментария"""
    comment = input("Введите ваш комментарий: ")
    comments.setdefault((other_user, tweet_number), []).append((username, comment))
    print("Комментарий успешно добавлен!")
    comments[(other_user, tweet_number)] = comments.get((other_user, tweet_number), [])


def view_comments(other_user, tweet_number):
    """Просмотр коментов пользователя"""
    tweet_comments = comments.get((other_user, tweet_number), [])
    if tweet_comments:
        print(f"\n--- Комментарии к твиту {other_user} ---")
        print(f"Твит: {tweets[other_user][tweet_number]}\nКомментарии:")
        for i, (username, comment) in enumerate(tweet_comments, start=1):
            print(f"{i}. {username}: {comment}")
    else:
        print("У этого твита еще нет комментариев.")


def rate_tweet(username, other_user, tweet_number):
    """Оценка твита"""
    rating = input("Введите оценку (от 1 до 5): ")
    if rating.isdigit() and 1 <= int(rating) and int(rating) <= 5:
        tweet_id = (other_user, tweet_number)
        ratings.setdefault(tweet_id, []).append((username, int(rating)))
        print("Твит успешно оценен.")
        ratings_list = ratings[tweet_id]
        average_rating = sum([rating for _, rating in ratings_list]) / len(ratings_list)
        print(f"Средняя оценка за твит: {average_rating:.2f}")
    else:
        print("Некорректная оценка. Оценка должна быть числом от 1 до 5.")


def main_menu(username):
    """ Основное меню твитера"""
    while True:
        print(f'\n--- Пользователь {username} ---')
        print("--- Основное меню ---")
        print("1. Создать твит")
        print("2. Просмотр своих твитов")
        print("3. Редактировать твит")
        print("4. Удалить твит")
        print("5. Средняя оценка за твит")
        print("6. Поиск другого пользователя")
        print("7. Выйти")
        choice = input("Выберите опцию: ")
        if choice == "1":
            tweet = create_tweet()
            tweets[username].append(tweet)
        elif choice == "2":
            view_tweets(username)
        elif choice == "3":
            number = get_tweet_number(username)
            if number is not None:
                tweets[username][number] = create_tweet()
        elif choice == "4":
            number = get_tweet_number(username)
            if number is not None:
                tweets[username].pop(number)
                print("Твит успешно удален!")
        elif choice == "5":
            number = view_tweets(username)
            if number is not None:
                tweet_number = input("Введите номер твита, чтобы узнать среднюю оценку: ")
                if tweet_number.isdigit() and int(tweet_number) <= len(tweets[username]):
                    tweet_number = int(tweet_number) - 1
                    get_tweet_rating(username, tweet_number)
                else:
                    print("Некорректный номер твита.")
        elif choice == "6":
            search_users(username)
        elif choice == "7":
            print("Выход из аккаунта.")
            break
        else:
            print("Некорректная опция. Попробуйте еще раз.")


def main():
    """ Вход и регистрация"""
    while True:
        print("--- Twitter Console App ---")
        print("1. Регистрация")
        print("2. Войти")
        print("3. Выйти")
        option = input("Выберите опцию: ")
        if option == "1":
            registration()
        elif option == "2":
            username = login()
            if username is not None:
                main_menu(username)
        elif option == "3":
            print("Завершение работы.")
            break
        else:
            print("Некорректная опция. Попробуйте еще раз.")


if __name__ == "__main__":
    main()
