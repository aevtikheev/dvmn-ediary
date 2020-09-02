"""
echo 'import script; script.main()' | python manage.py shell
"""

import sys
import random

from datacenter.models import Schoolkid, Mark, Chastisement, Lesson, Subject, Commendation

KID_NAME = 'Фролов Иван'
SUBJECT = 'Математика'

GRADES_TO_FIX = [2, 3]
DESIRABLE_GRADE = 5
COMMENDATION_TEXTS = ('Гораздо лучше, чем я ожидал!',
                      'Хорошо!',
                      'Ты на верном пути!',
                      'Ты растешь над собой!',
                      'Сказано здорово – просто и ясно!',
                      'Я вижу, как ты стараешься!',
                      'Талантливо!',
                      'Так держать!',
                      'Великолепно!',
                      'Уже существенно лучше!',
                      'Теперь у тебя точно все получится!',
                      'Ты меня приятно удивил!',
                      'Замечательно!',
                      'Я поражен!',
                      'Потрясающе!',
                      'Здорово!',
                      'Молодец!',
                      'С каждым разом у тебя получается всё лучше!',
                      'Мы с тобой не зря поработали!',
                      'Ты меня очень обрадовал!',
                      'Ты многое сделал, я это вижу!',
                      'Прекрасно!',
                      'Это как раз то, что нужно!',
                      'Я тобой горжусь!',
                      'Именно этого я давно ждал от тебя!',
                      'Прекрасное начало!',
                      'Очень хороший ответ!',
                      'Отлично!',
                      'Ты, как всегда, точен!',
                      'Ты сегодня прыгнул выше головы!')


def print_and_exit(message: str) -> None:
    print(message)
    sys.exit(0)


def get_kid(kid_name: str) -> Schoolkid:
    kids_by_name = Schoolkid.objects.filter(full_name__contains=kid_name)
    if kids_by_name.count() > 1:
        print_and_exit(f'Найдено больше одного ученика с именем {kid_name}. Попробуй добавить отчество.')
    elif kids_by_name.count() == 0:
        print_and_exit(f'Не найден ученик с именем {kid_name}. Проверь правильность написания имени')
    else:
        return kids_by_name[0]


def get_subject(kid: Schoolkid, subject_title: str) -> Subject:
    try:
        return Subject.objects.get(title=subject_title, year_of_study=kid.year_of_study)
    except Subject.DoesNotExist:
        print_and_exit(f'Предмет "{subject_title}" для {kid.year_of_study} класса не найден. '
                       f'Проверь, правильно ли написано название предмета (и есть ли такой вообще).')
    except Subject.MultipleObjectsReturned:
        print_and_exit(f'Найдено несколько предметов с "{subject_title}" в названии. '
                       f'Уточни название предмета.')


def fix_bad_grades(kid: Schoolkid) -> None:
    kid_bad_grades = Mark.objects.filter(schoolkid=kid, points__in=GRADES_TO_FIX)
    for grade in kid_bad_grades:
        grade.points = DESIRABLE_GRADE
        grade.save()
    print('Плохие оценки исправлены.')


def remove_chastisements(kid: Schoolkid) -> None:
    kid_chastisements = Chastisement.objects.filter(schoolkid=kid)
    kid_chastisements.delete()
    print('Замечания удалены.')


def add_commendation(kid: Schoolkid, subject: Subject) -> None:
    all_kid_lessons = Lesson.objects.filter(year_of_study=kid.year_of_study,
                                            group_letter=kid.group_letter,
                                            subject=subject)
    lesson_to_commend = random.choice(all_kid_lessons)
    Commendation.objects.create(text=random.choice(COMMENDATION_TEXTS),
                                created=lesson_to_commend.date,
                                schoolkid=kid,
                                subject=lesson_to_commend.subject,
                                teacher=lesson_to_commend.teacher)
    print('Похвала добавлена.')


def main() -> None:
    if not all((KID_NAME, SUBJECT)):
        print_and_exit("Заполни KID_NAME и SUBJECT")

    kid = get_kid(KID_NAME)
    subject = get_subject(kid, SUBJECT)

    fix_bad_grades(kid)
    remove_chastisements(kid)
    add_commendation(kid, subject)
