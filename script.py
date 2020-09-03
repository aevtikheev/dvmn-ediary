import random

from datacenter.models import (Schoolkid, Mark, Chastisement,
                               Lesson, Subject, Commendation)

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


class BadInputException(Exception):
    """ Raised when input data is wrong or incomplete. """


def get_kid(kid_name: str) -> Schoolkid:
    kids_by_name = Schoolkid.objects.filter(full_name__contains=kid_name)
    if kids_by_name.count() > 1:
        BadInputException(f'Найдено больше одного ученика с именем {kid_name}.'
                          f' Попробуй добавить отчество.')
    elif kids_by_name.count() == 0:
        BadInputException(f'Не найден ученик с именем {kid_name}.'
                          f' Проверь правильность написания имени')
    else:
        return kids_by_name[0]


def get_subject(kid: Schoolkid, subject_title: str) -> Subject:
    try:
        return Subject.objects.get(title=subject_title,
                                   year_of_study=kid.year_of_study)
    except Subject.DoesNotExist:
        BadInputException(f'Предмет "{subject_title}" для {kid.year_of_study}'
                          f' класса не найден. Проверь, правильно ли написано'
                          f' название предмета (и есть ли такой вообще).')
    except Subject.MultipleObjectsReturned:
        BadInputException(f'Найдено несколько предметов с "{subject_title}"'
                          f' в названии. Уточни название предмета.')


def fix_bad_grades(kid: Schoolkid) -> None:
    kid_bad_grades = Mark.objects.filter(schoolkid=kid,
                                         points__in=GRADES_TO_FIX)
    for grade in kid_bad_grades:
        grade.points = DESIRABLE_GRADE
        grade.save()
    print('Плохие оценки исправлены.')


def remove_chastisements(kid: Schoolkid) -> None:
    kid_chastisements = Chastisement.objects.filter(schoolkid=kid)
    kid_chastisements.delete()
    print('Замечания удалены.')


def add_commendation(kid: Schoolkid, subject: Subject) -> None:
    lesson_to_commend = Lesson.objects.filter(
        year_of_study=kid.year_of_study,
        group_letter=kid.group_letter,
        subject=subject
    ).order_by('?')[0]
    Commendation.objects.create(text=random.choice(COMMENDATION_TEXTS),
                                created=lesson_to_commend.date,
                                schoolkid=kid,
                                subject=lesson_to_commend.subject,
                                teacher=lesson_to_commend.teacher)
    print('Похвала добавлена.')


def main() -> None:
    if not all((KID_NAME, SUBJECT)):
        BadInputException("Заполни KID_NAME и SUBJECT")

    kid = get_kid(KID_NAME)
    subject = get_subject(kid, SUBJECT)

    fix_bad_grades(kid)
    remove_chastisements(kid)
    add_commendation(kid, subject)
