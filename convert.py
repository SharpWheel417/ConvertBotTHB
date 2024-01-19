import commex, bitazza

## Получаем чисту цену
def clean(bat: int, course_THB: int, course_rub: int):
    return round(((float(bat)/float(course_THB)) * float(course_rub)), 2)


def set_course(new_course):
    global user_course_THB
    user_course_THB = new_course

def set_course_usdt(new_course):
    global user_course_rub
    user_course_rub = new_course

def set_marje(new_course):
    global marje
    marje = (new_course/100)+1


def parse_course():
    
    new_course_rub = commex.get_average()
    global course_rub
    if (new_course_rub>course_rub):
            course_rub = new_course_rub
    print("Average:", course_rub)

    new_course_THB = bitazza.get_currency()
    if new_course_THB == 'error':
        raise Exception('Failed to get THB course from Bitazza')
    global course_THB
    if(float(new_course_THB)<course_THB):
        course_THB = new_course_THB    
    print(course_THB)
    
    return float(course_THB)