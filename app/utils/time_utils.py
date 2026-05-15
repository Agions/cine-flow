#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Time formatting utilities — unified time/duration formatting functions.

Replaces duplicated _format_time / _format_duration methods across the codebase.
"""

from datetime import datetime, timedelta


def format_time(seconds: float) -> str:
    """
    Format seconds to MM:SS or HH:MM:SS.

    >>> format_time(65)
    '01:05'
    >>> format_time(3661)
    '1:01:01'
    """
    if seconds < 0:
        return "00:00"

    total_seconds = int(seconds)
    m, s = divmod(total_seconds, 60)
    h, m = divmod(m, 60)

    if h > 0:
        return f"{h}:{m:02d}:{s:02d}"
    return f"{m:02d}:{s:02d}"


def format_time_hms(seconds: float) -> str:
    """
    Format seconds to HH:MM:SS (always shows hours).

    >>> format_time_hms(65)
    '00:01:05'
    """
    if seconds < 0:
        return "00:00:00"

    total_seconds = int(seconds)
    m, s = divmod(total_seconds, 60)
    h, m = divmod(m, 60)

    return f"{h:02d}:{m:02d}:{s:02d}"


def format_time_from_ms(ms: int) -> str:
    """
    Format milliseconds to MM:SS.

    >>> format_time_from_ms(65000)
    '01:05'
    """
    return format_time(ms / 1000.0)


def format_duration(seconds: float) -> str:
    """
    Format duration in human-readable form.

    >>> format_duration(45)
    '45秒'
    >>> format_duration(90)
    '1分30秒'
    >>> format_duration(3661)
    '1小时1分1秒'
    """
    if seconds < 0:
        return "0秒"

    total_seconds = int(seconds)
    h, remainder = divmod(total_seconds, 3600)
    m, s = divmod(remainder, 60)

    parts = []
    if h > 0:
        parts.append(f"{h}小时")
    if m > 0:
        parts.append(f"{m}分")
    if s > 0 or not parts:
        parts.append(f"{s}秒")

    return "".join(parts)


def format_timestamp(ts: float) -> str:
    """
    Format a Unix timestamp to a relative or absolute time string.

    - < 1 min ago: "刚刚"
    - < 1 hour: "X分钟前"
    - < 1 day: "X小时前"
    - >= 1 day: "YYYY-MM-DD HH:MM"
    """
    try:
        dt = datetime.fromtimestamp(ts)
    except (ValueError, OSError):
        return "--"

    now = datetime.now()
    delta = now - dt

    if delta < timedelta(minutes=1):
        return "刚刚"
    elif delta < timedelta(hours=1):
        return f"{delta.seconds // 60}分钟前"
    elif delta < timedelta(days=1):
        return f"{delta.seconds // 3600}小时前"
    else:
        return dt.strftime("%Y-%m-%d %H:%M")
