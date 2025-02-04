import shutil

def get_disk_space_info(drive="C:\"):
    """Get detailed disk space information"""
    total, used, free = shutil.disk_usage(drive)
    return {
        'total_gb': total / (2**30),
        'used_gb': used / (2**30),
        'free_gb': free / (2**30),
        'free_percent': (free / total) * 100
    }