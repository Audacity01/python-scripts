import sys
from datetime import datetime

MONTHS = ['', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
          'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
DAYS = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

PRESETS = {
    '@yearly': '0 0 1 1 *',
    '@monthly': '0 0 1 * *',
    '@weekly': '0 0 * * 0',
    '@daily': '0 0 * * *',
    '@hourly': '0 * * * *',
}

def parse_field(field, min_val, max_val):
    values = set()
    for part in field.split(','):
        step = 1
        if '/' in part:
            part, step = part.split('/')
            step = int(step)

        if part == '*':
            values.update(range(min_val, max_val + 1, step))
        elif '-' in part:
            start, end = part.split('-')
            values.update(range(int(start), int(end) + 1, step))
        else:
            values.add(int(part))
    return sorted(values)


def explain(expr):
    expr = PRESETS.get(expr, expr)
    parts = expr.split()

    if len(parts) != 5:
        return "Invalid cron expression (need 5 fields)"

    minute, hour, dom, month, dow = parts

    desc = []

    if minute == '*' and hour == '*':
        desc.append("Every minute")
    elif minute == '0' and hour == '*':
        desc.append("Every hour")
    elif minute == '*':
        desc.append(f"Every minute of hour {hour}")
    elif hour == '*':
        desc.append(f"At minute {minute} of every hour")
    else:
        desc.append(f"At {hour.zfill(2)}:{minute.zfill(2)}")

    if dom != '*':
        desc.append(f"on day {dom} of the month")
    if month != '*':
        months = parse_field(month, 1, 12)
        month_names = [MONTHS[m] for m in months if m < len(MONTHS)]
        desc.append(f"in {', '.join(month_names)}")
    if dow != '*':
        days = parse_field(dow, 0, 6)
        day_names = [DAYS[d] for d in days if d < len(DAYS)]
        desc.append(f"on {', '.join(day_names)}")

    return ' '.join(desc)


def will_run_at(expr, dt):
    expr = PRESETS.get(expr, expr)
    parts = expr.split()
    if len(parts) != 5:
        return False

    checks = [
        (parts[0], dt.minute, 0, 59),
        (parts[1], dt.hour, 0, 23),
        (parts[2], dt.day, 1, 31),
        (parts[3], dt.month, 1, 12),
        (parts[4], dt.weekday(), 0, 6),
    ]

    for field, current, mn, mx in checks:
        if field != '*' and current not in parse_field(field, mn, mx):
            return False
    return True


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python cron_parser.py '<cron_expression>'")
        print("Example: python cron_parser.py '*/5 * * * *'")
        print("Example: python cron_parser.py '@daily'")
        sys.exit(1)

    expr = sys.argv[1]
    print(f"Expression: {expr}")
    print(f"Meaning: {explain(expr)}")
    now = datetime.now()
    print(f"Would run now ({now.strftime('%H:%M %a')})? {'Yes' if will_run_at(expr, now) else 'No'}")
