import time
from datetime import date, datetime, timedelta, timezone
from dateutil import parser

def get_week_dates(idx=0):
    today = date.today()
    start = today - timedelta(days=today.weekday())
    end = start + timedelta(days=6)
    
    start += timedelta(days=7 * idx)
    end += timedelta(days=7 * idx)
    return start, end

def local_to_iso(s):
    utc_offset_sec = time.altzone if time.localtime().tm_isdst else time.timezone
    utc_offset = timedelta(seconds=-utc_offset_sec)
    return s.replace(tzinfo=timezone(offset=utc_offset)).isoformat()

def iso_to_local(s):
    return parser.isoparse(s)
