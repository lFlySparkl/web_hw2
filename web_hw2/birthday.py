from datetime import date, timedelta, datetime

DAYS = { 0: "Monday",
         1:"Tuesday",
         2: "Wednesday",
         3: "Thursday",
         4: "Friday",
         5: "Saturday",
         6: "Sunday"}

def user_sort(result_dict, current_day):
    sorted_dict = {}
    if not result_dict:
        return {}
    else:
        step_day = current_day
        while step_day <= 6:
            search = result_dict.get(step_day)
            if search:
                if step_day >= 5:
                    get_user = sorted_dict.get(0)
                    if not get_user:
                        sorted_dict.update({0:search})
                    else:
                        sorted_dict[0].append(search[0])
                else:
                    sorted_dict.update({step_day:search})
            step_day += 1
        step_day = 0
        while step_day < current_day:
            search = result_dict.get(step_day)
            if search:
                if step_day == 0 and current_day > 0:
                    get_user = sorted_dict.get(0)
                    if not get_user:
                        sorted_dict.update({0:search})
                    else:
                        sorted_dict[0].append(search[0])
                else:
                    sorted_dict.update({step_day:search})
            step_day += 1
        converted_dict = {DAYS[key]: value for key, value in sorted_dict.items()}
        return(converted_dict)
        
def get_period(start_date: date, days: int):
    result = {}
    for _ in range(days):
        week_day = date(start_date.year, start_date.month, start_date.day)
        result[start_date.day, start_date.month] = start_date.year
        start_date += timedelta(1)
    return result

def get_birthdays_per_week(users: list, in_days = 7) -> list:
    result_dict = {}
    start_date = date.today()
    # start_date = date(2023, 12, 26)
    current_day = start_date.weekday()
    period = get_period(start_date, in_days)
    for user in users:
        bd: date = user["birthday"]
        date_bd = bd.day, bd.month
        if date_bd in list(period):
            this_year_bd = datetime(period[date_bd], bd.month, bd.day).date()
            bd_weak_day = this_year_bd.weekday()
            get_key = result_dict.get(bd_weak_day)
            set_user_name = []
            set_user_name.append(user["name"])
            if get_key == None:
                result_dict.update({bd_weak_day:(set_user_name)})
            else:
                result_dict[bd_weak_day].append(user["name"])
    # return result_dict
    users = user_sort(result_dict, current_day)
    return users

if __name__ == '__main__':
    users = [{"name": "Bill", "birthday": datetime(1990, 12, 26).date()},
             {"name": "John", "birthday": datetime(1995, 12, 29).date()},
             {"name": "Tilda", "birthday": datetime(2000, 12, 30).date()},
             {"name": "Marry", "birthday": datetime(2000, 1, 1).date()},
             {"name": "Denis", "birthday": datetime(2005, 1, 2).date()},
             {"name": "Alex", "birthday": datetime(1990, 1, 3).date()},
             {"name": "Jan Koum", "birthday": datetime(1976, 1, 4).date()},
             ]

    result = get_birthdays_per_week(users, 10)
    print(result)
    # Виводимо результат
    for day_name, names in result.items():
        print(f"{day_name}: {', '.join(names)}")