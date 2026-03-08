import sys
import json
import time

try:
    import psutil
except ImportError:
    print("psutil not installed. Run: pip install psutil")
    sys.exit(1)

WARN_CPU   = 70;  CRIT_CPU   = 90
WARN_RAM   = 80;  CRIT_RAM   = 95
WARN_DISK  = 85;  CRIT_DISK  = 95

def fmt_bytes(n):
    for unit in ['B','KB','MB','GB','TB']:
        if n < 1024: return f"{n:.1f} {unit}"
        n /= 1024
    return f"{n:.1f} PB"

def status_icon(val, warn, crit):
    if val >= crit: return "🚨"
    if val >= warn: return "⚠️ "
    return "✅"

def check():
    cpu_pct   = psutil.cpu_percent(interval=1)
    cpu_cores = psutil.cpu_count()
    ram       = psutil.virtual_memory()
    ram_pct   = ram.percent
    ram_used  = fmt_bytes(ram.used)
    ram_total = fmt_bytes(ram.total)

    disks = {}
    for part in psutil.disk_partitions():
        try:
            usage = psutil.disk_usage(part.mountpoint)
            disks[part.device] = usage
        except PermissionError:
            pass

    procs = []
    for p in psutil.process_iter(['name','memory_info']):
        try:
            mem = p.info['memory_info'].rss
            if mem > 50 * 1024 * 1024:
                procs.append((p.info['name'], mem))
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    procs.sort(key=lambda x: x[1], reverse=True)

    worst = 0
    if cpu_pct  >= CRIT_CPU  or ram_pct >= CRIT_RAM:  worst = 2
    elif cpu_pct >= WARN_CPU or ram_pct >= WARN_RAM:   worst = 1
    for usage in disks.values():
        if usage.percent >= CRIT_DISK:  worst = max(worst, 2)
        elif usage.percent >= WARN_DISK: worst = max(worst, 1)

    return {
        "cpu_pct": cpu_pct, "cpu_cores": cpu_cores,
        "ram_pct": ram_pct, "ram_used": ram_used, "ram_total": ram_total,
        "disks": {k: {"free": fmt_bytes(v.free), "total": fmt_bytes(v.total), "pct": v.percent}
                  for k, v in disks.items()},
        "top_procs": [(n, fmt_bytes(m)) for n, m in procs[:5]],
        "status": worst
    }

def render(d):
    icon_cpu  = status_icon(d["cpu_pct"],  WARN_CPU,  CRIT_CPU)
    icon_ram  = status_icon(d["ram_pct"],  WARN_RAM,  CRIT_RAM)

    lines = ["💻 SYSTEM HEALTH", ""]
    lines.append(f"CPU:    {icon_cpu} {d['cpu_pct']}% ({d['cpu_cores']} cores)")
    lines.append(f"RAM:    {icon_ram} {d['ram_used']} used / {d['ram_total']} total ({d['ram_pct']}%)")

    for dev, disk in d["disks"].items():
        icon_disk = status_icon(disk["pct"], WARN_DISK, CRIT_DISK)
        label = dev.rstrip(":\\/ ")
        lines.append(f"Disk {label}: {icon_disk} {disk['free']} free / {disk['total']} total ({disk['pct']}% used)")

    if d["top_procs"]:
        lines += ["", "TOP PROCESSES (by RAM)"]
        for name, mem in d["top_procs"]:
            lines.append(f"  {name:<22} {mem}")

    overall = ["✅ Healthy", "⚠️  Warning", "🚨 Critical"][d["status"]]
    lines += ["", f"Status: {overall}"]
    return "\n".join(lines)

if __name__ == "__main__":
    args = sys.argv[1:]

    if "--threshold-only" in args:
        d = check()
        sys.exit(d["status"])

    if "--watch" in args:
        interval = 30
        while True:
            print("\033[2J\033[H", end="")
            d = check()
            print(render(d))
            print(f"\n(refreshing every {interval}s — Ctrl+C to stop)")
            time.sleep(interval)

    d = check()

    if "--json" in args:
        print(json.dumps(d, indent=2))
    else:
        print(render(d))
