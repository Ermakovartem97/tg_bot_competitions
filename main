from managment_bd import take_all_persons, take_all_competitions, check_person_in_competition, insert_person


def create_person(competition_name):
    print('Введите ФИО')
    full_name = input()
    print('Введите компнию')
    company_name = input()
    # Добавление телеграмм к записи в БД
    person_tg = '@ermakov'
    insert_person(competition_name, (full_name, company_name, person_tg))
    print('Если нет напишите администратору')
    print('Если да - то все хорошо вы зарегестрированы')


def check_competitions():
    print('Выбирите соревнование')
    all_competition = take_all_competitions()
    print('\n'.join(all_competition))
    number_competition = int(input('Введите номер: '))
    print(f'Вы выбрали {all_competition[number_competition]}')
    return all_competition[number_competition]


if __name__ == '__main__':
    competition_name = check_competitions()
    is_person_in_competition = check_person_in_competition(competition_name, '@ermakov')
    if is_person_in_competition:
        print('Вы уже зарегестрированы на соревновании')
    else:
        print('Вы еще не зарегестрированы. Хотите зарегестрироваться?')
