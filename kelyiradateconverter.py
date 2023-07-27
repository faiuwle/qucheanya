import sys
import re
import math
# -*- coding: utf-8 -*-

def earth_date_to_hours(month, day, leap):
    hours = 0
    
    if month > 12:
        print(f"Invalid month: {month}")
        return (None, None)
    if month in [9, 4, 6, 11] and day > 30:
        print(f"Invalid day of month {month}: {day}")
        return (None, None)
    if month == 2 and ((leap and day > 29) or (not leap and day > 28)):
        print(f"Invalid day of month 2: {day}")
        return (None, None)
    if day > 31:
        print(f"Invalid day of month {month}: {day}")
        return (None, None)

    for m in range(1, month):
        if m in [9, 4, 6, 11]:
            hours += 30 * 24
        elif m == 2:
            hours += (29 if leap else 28) * 24
        else:
            hours += 31 * 24
            
    rest = (day - 1) * 24
    start = hours + rest
    end = start + 24
    return (start, end)
    
def kelyira_date_to_hours(month, week, day, leap):
    hours = 0
    
    if month > 9:
        print(f"Invalid month: {month}")
        return (None, None)
    if week > 5:
        print(f"Invalid week: {week}")
        return (None, None)
    if week != 3 and day > 6:
        print(f"Invalid day of week {week}: {day}")
        return (None, None)
    if month not in ([3, 6, 9] if leap else [3, 6]) and day > 8:
        print(f"Invalid day of week {week} in month {month}: {day}")
        return (None, None)
    if day > 9:
        print(f"Invalid day in week {week}: {day}")
        return (None, None)
        
    for m in range(1, month):
        if m in [3, 6]:
            hours += 33 * 30.5
        else:
            hours += 32 * 30.5
            
    for w in range(1, week):
        if w == 3:
            if month in ([3, 6, 9] if leap else [3, 6]):
                hours += 9 * 30.5
            else:
                hours += 8 * 30.5
        else:
            hours += 6 * 30.5
            
    rest = (day - 1) * 30.5
    start = hours + rest
    end = start + 30.5
    return (start, end)
    
def hours_to_earth_date(hours, leap):
    month = 1
    day = 1
    
    while hours >= 28 * 24:
        min_days = 28
        if leap:
            min_days = 29
        if month in [9, 6, 4, 11]:
            min_days = 30
        elif month != 2:
            min_days = 31
    
        if hours >= min_days * 24:
            hours -= min_days * 24
            month += 1
        
        else:
            break
            
    day = int((hours // 24) + 1)
    remaining_hours = hours % 24
    hour = math.floor(remaining_hours)
    minute = math.floor((remaining_hours - math.floor(remaining_hours)) * 60)
    return (month, day, hour, minute)
        
    
def hours_to_kelyira_date(hours, leap):
    month = 1
    week = 1
    day = 1
    
    while hours >= 32 * 30.5:
        min_days = 32
        if month in ([3, 6, 9] if leap else [3, 6]):
            min_days = 33
    
        if hours >= min_days * 30.5:
            hours -= min_days * 30.5
            month += 1
        
        else:
            break
            
    while hours >= 6 * 30.5:
        min_days = 6
        if week == 3:
            if month in ([3, 6, 9] if leap else [3, 6]):
                min_days = 9
            else:
                min_days = 8
    
        if hours >= min_days * 30.5:
            hours -= min_days * 30.5
            week += 1
            
        else:
            break
            
    day = int((hours // 30.5) + 1)
    remaining_hours = hours % 30.5
    kelyira_hours = remaining_hours * (18 / 30.5)
    hour = math.floor(kelyira_hours)
    minute = math.floor((kelyira_hours - math.floor(kelyira_hours)) * 144)
    
    return (month, week, day, hour, minute)
    
def convert_hours(hours, leap, to_kelyira):
    march_1 = (31 + (29 if leap else 28)) * 24

    if leap:
        total_earth = 366 * 24
        total_kelyira = ((32 * 6) + (33 * 3)) * 30.5
    else:
        total_earth = 365 * 24
        total_kelyira = ((32 * 7) + (33 * 2)) * 30.5
        
    if to_kelyira:
        if hours >= march_1:
            hours -= march_1
        else:
            hours += total_earth - march_1
        
    if to_kelyira:
        total_to = total_kelyira
        total_from = total_earth
    else:
        total_to = total_earth
        total_from = total_kelyira
        
    percent = hours / total_from
    result = total_to * percent
    
    if not to_kelyira:
        result += march_1
        if result >= total_earth:
            result -= total_earth
    
    return result
    
def format_earth_date(month, day, hour, minute):
    months = ["", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
              "November", "December"]
    nth = ["th", "st", "nd", "rd"]
    nth += ["th"] * 6
    
    hour_number = f"{12 if hour == 0 else hour if hour < 13 else hour - 12}"
    time = f"{hour_number}:{minute:02} {'AM' if hour < 12 else 'PM'} on " if hour >= 0 else ""
        
    return f"{time}{months[month]} {day}{'th' if day > 10 and day < 20 else nth[day % 10]}"
    
def format_kelyira_date(month, week, day, hour, minute):
    hour_number = f"{hour + 1 if hour < 6 else hour - 5 if hour < 12 else hour - 11}"
    hour_set = f"{'Qä' if hour < 6 else 'Sua' if hour < 12 else 'Fo'}Qhai"
    time = f"{hour_number}:{minute:03} {hour_set} on " if hour >= 0 else ""

    return f"{time}{month} Yeari, {week} Soine {day}"

def main():
    leap = False
    date = None
    
    sys.stdout.reconfigure(encoding="utf-8")
    
    if len(sys.argv) < 2:
        print("Usage: \n" +
              "python kelyiradateconverter.py --date MM/DD [--leap] to convert from Earth date to Kelyira date\n" +
              "python kelyriadateconverter.py --date M.W.D [--leap] to convert from Kelyira date to Earth date\n" +
              "--leap option specifies to use a leap year")
        sys.exit()
        
    expect_date = False
    
    for arg in sys.argv[1:]:
        if arg == "--date":
            expect_date = True
            continue
            
        if date is not None:
            expect_date = False
            
        if arg == "--leap":
            leap = True
            
        if not expect_date:
            continue
           
        earth_match = re.match(r"(\d{2})/(\d{2})", arg)
        if earth_match is not None:
            date = (int(earth_match.group(1)), int(earth_match.group(2)))
            continue
            
        kelyira_match = re.match(r"(\d)\.(\d)\.(\d)", arg)
        if kelyira_match is not None:
            date = (int(kelyira_match.group(1)), int(kelyira_match.group(2)), int(kelyira_match.group(3)))
            continue
            
        print(f"Error: could not match date {arg}.  Earth dates should be MM/DD, Kelyira dates should be M.W.D")
        
    if date is None:
        sys.exit()
        
    if len(date) == 2:
        start, end = earth_date_to_hours(date[0], date[1], leap)
        if start is None:
            sys.exit()
        start = convert_hours(start, leap, True)
        end = convert_hours(end, leap, True)
        start = hours_to_kelyira_date(start, leap)
        end = hours_to_kelyira_date(end, leap)
        
        print(f"{format_earth_date(date[0], date[1], -1, -1)} begins on " +
              f"{format_kelyira_date(start[0], start[1], start[2], start[3], start[4])} and ends on " +
              format_kelyira_date(end[0], end[1], end[2], end[3], end[4]))
                  
    else:
        start, end = kelyira_date_to_hours(date[0], date[1], date[2], leap)
        if start is None:
            sys.exit()
        start = convert_hours(start, leap, False)
        end = convert_hours(end, leap, False)
        start = hours_to_earth_date(start, leap)
        end = hours_to_earth_date(end, leap)
        
        print(f"{format_kelyira_date(date[0], date[1], date[2], -1, -1)} begins on " +
              f"{format_earth_date(start[0], start[1], start[2], start[3])} and ends on " +
              format_earth_date(end[0], end[1], end[2], end[3]))
        
if __name__ == "__main__":
    main()