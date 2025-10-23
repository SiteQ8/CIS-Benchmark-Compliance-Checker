"""
System detection utilities.
"""

import platform
import distro


def detect_os():
    """Detect the operating system."""
    system = platform.system()

    if system == "Linux":
        dist = distro.id()
        version = distro.version()
        return f"{dist}_{version.replace('.', '_')}"
    elif system == "Windows":
        return f"windows_{platform.release()}"
    elif system == "Darwin":
        return f"macos_{platform.mac_ver()[0]}"

    return "unknown"


def get_os_info():
    """Get detailed OS information."""
    return {
        "system": platform.system(),
        "release": platform.release(),
        "version": platform.version(),
        "machine": platform.machine(),
        "processor": platform.processor()
    }
