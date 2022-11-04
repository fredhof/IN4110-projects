import re
#from tkinter.messagebox import RETRY
from typing import Tuple
from filter_urls import find_urls
from requesting_urls import get_html

## -- Task 3 (IN3110 optional, IN4110 required) -- ##

# create array with all names of months
month_names = [
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec",
]


def get_date_patterns() -> Tuple[str, str, str]:
    """Return strings containing regex pattern for year, month, day
    arguments:
        None
    return:
        year, month, day (tuple): Containing regular expression patterns for each field
    """

    # Regex to capture days, months and years with numbers
    # year should accept a 4-digit number between at least 1000-2029
    year = r"(?P<year>([0-9]{4}))"
    # month should accept month names or month numbers (ISO)
    month_nam = r"(?P<month>(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|(Nov|Dec)(?:ember)?))"
    month_ISO = r"(?P<month>(-1[0-2]-|-0[1-9]-))" # we capture ISO dates nicely with this
    # day should be a number, which may or may not be zero-padded
    day = r"(?P<day>((\d?\d|100)))"

    return year, month_nam, month_ISO, day


def convert_month(s: str) -> str:
    """Converts a string month to number (e.g. 'September' -> '09'.

    You don't need to use this function,
    but you may find it useful.

    arguments:
        month_name (str) : month name
    returns:
        month_number (str) : month number as zero-padded string
    """
    # If already digit do nothing
    if s.isdigit():
        return s

    # Convert to number as string
    for i, month in enumerate(month_names):
        if month in s:
            if i+1 < 10: return "0" + str(i+1)
            return str(i+1)


def zero_pad(n: str):
    """zero-pad a number string

    turns '2' into '02'

    You don't need to use this function,
    but you may find it useful.
    """
    if int(n) < 10: return "0" + str(n)


def find_dates(text: str, output: str = None) -> list:
    """Finds all dates in a text using reg ex

    arguments:
        text (string): A string containing html text from a website
    return:
        results (list): A list with all the dates found
    """
    year, month_nam, month_ISO, day = get_date_patterns()
    
    # Date on format YYYY/MM/DD - ISO
    ISO = re.compile(f'{year}{month_ISO}{day}')

    # Date on format DD/MM/YYYY
    DMY = re.compile(f'{day} {month_nam} {year}')

    # Date on format MM/DD/YYYY
    MDY = re.compile(f'{month_nam} {day}, {year}')

    # Date on format YYYY/MM/DD
    YMD = re.compile(f'{year} {month_nam} {day}')

    # list with all supported formats
    formats = [ISO, DMY, MDY, YMD]
    dates = []

    # find all dates in any format in text
    for i in formats:
        for date in i.findall(text):
            dates.append(date)
    # Write to file if wanted
    # convert nested tuple to nested list, [(1,2), (1.2)] -> [[1,2], [1.2]]
    dates = list(map(list, dates))
    
    # remove empty strings in nested list
    for i in range(len(dates)):
        while("" in dates[i]):
            dates[i].remove("")
  
    for i in range(len(dates)):
        for j in range(len(dates[i])):
            try:
                dates[i][j] = int(dates[i][j])
                if dates[i][j] < 10: d = zero_pad(dates[i][j])
                elif 10 <= dates[i][j] < 100: d = dates[i][j]
                else: yr = dates[i][j]
                
            # if dates[i][j] is str, int(dates[i][j]) gives ValueError
            except ValueError:
                dates[i][j] = dates[i][j].replace("-","") # ISO months formated as "-x-"
                mn = convert_month(dates[i][j])   
        
        dates[i] = f"{yr}/{mn}/{d}"
        
    if output:
        with open(output, 'w', encoding='utf8') as file:
            [file.write(match + '\n') for match in dates]
    
    return dates