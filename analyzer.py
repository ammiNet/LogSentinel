from collections import Counter
from datetime import datetime, timedelta


def analyze_logs(search="", log_type="all"):
    with open("live.log", "r", encoding="utf-8") as log_file:
        lines = log_file.readlines()

    filtered_lines = []

    for line in lines:
        if search and search.lower() not in line.lower():
            continue

        if log_type == "login_attempt" and "Login attempt" not in line:
            continue

        if log_type == "login_success" and "Login successful" not in line:
            continue

        if log_type == "failed_login" and "Login failed" not in line:
            continue

        if log_type == "logout" and "Logout" not in line:
            continue

        if log_type == "registration" and "User registered" not in line:
            continue

        filtered_lines.append(line)

    successful_logins = []
    failed_logins = []
    logout_entries = []
    signin_entries = []

    for line in lines:
        if "Login successful" in line:
            successful_logins.append(line)

        if "Login failed" in line:
            failed_logins.append(line)

        if "Logout" in line:
            logout_entries.append(line)

        if "Signed In" in line:
            signin_entries.append(line)

    failed_ips = []

    for line in failed_logins:
        parts = line.split()

        if parts:
            ip = parts[-1].replace("ip=", "")
            failed_ips.append(ip)

    ip_counts = Counter(failed_ips)

    suspicious_ips = []

    for ip, count in ip_counts.items():
        if count >= 3:
            suspicious_ips.append(
                {
                    "ip": ip,
                    "attempts": count
                }
            )

    # Check for failed logins from the same IP
    # within a 5-minute window.

    for ip in set(failed_ips):
        ip_lines = []

        for line in failed_logins:
            if ip in line:
                ip_lines.append(line)

        for i in range(len(ip_lines)):
            first_time = datetime.strptime(
                " ".join(ip_lines[i].split()[:2]),
                "%Y-%m-%d %H:%M:%S"
            )

            attempts = 1

            for j in range(i + 1, len(ip_lines)):
                second_time = datetime.strptime(
                    " ".join(ip_lines[j].split()[:2]),
                    "%Y-%m-%d %H:%M:%S"
                )

                if second_time - first_time <= timedelta(minutes=5):
                    attempts += 1

            if attempts >= 3:
                already_added = False

                for suspicious in suspicious_ips:
                    if suspicious["ip"] == ip:
                        already_added = True

                if not already_added:
                    suspicious_ips.append(
                        {
                            "ip": ip,
                            "attempts": attempts
                        }
                    )

                break

    activity = {}

    for line in successful_logins:
        try:
            date = line.split()[0]

            if date not in activity:
                activity[date] = 0

            activity[date] += 1

        except (IndexError, ValueError):
            continue

    for line in failed_logins:
        try:
            date = line.split()[0]

            if date not in activity:
                activity[date] = 0

        except (IndexError, ValueError):
            continue

    activity_labels = sorted(activity.keys())
    activity_values = [activity[date] for date in activity_labels]

    return {
        "total_entries": len(lines),
        "successful_logins": len(successful_logins),
        "failed_logins": len(failed_logins),
        "logout_entries": len(logout_entries),
        "signin_entries": len(signin_entries),
        "suspicious_ips": suspicious_ips,
        "log_lines": filtered_lines,
        "activity_labels": activity_labels,
        "activity_values": activity_values
    }