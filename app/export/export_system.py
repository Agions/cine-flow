#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Voxplore Export System
导出一个中心化的任务调度系统，管理导出队列、预设和信号。
"""

import time
import uuid
import json
import threading
import logging
from pathlib import Path
from typing import Optional, List, Dict, Any
from dataclasses import dataclass, field
from enum import Enum
from concurrent.futures import ThreadPoolExecutor, Future

from app.core._signals import QObject, Signal

logger = logging.getLogger(__name__)


class ExportStatus(Enum):
    """导出状态"""
    PENDING = "pending"
    QUEUED = "queued"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    PAUSED = "paused"


class ExportFormat(Enum):
    """导出格式"""
    MP4 = "mp4"
    MOV = "mov"
    GIF = "gif"
    JIANYING = "jianying"


@dataclass
class ExportPreset:
    """导出预设"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = "默认预设"
    description: str = ""
    format: ExportFormat = ExportFormat.MP4
    resolution: tuple = (1920, 1080)
    fps: int = 30
    bitrate: int = 8000  # kbps
    audio_bitrate: int = 128  # kbps
    codec: str = "h264"
    audio_codec: str = "aac"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "format": self.format.value if isinstance(self.format, ExportFormat) else self.format,
            "resolution": list(self.resolution) if isinstance(self.resolution, tuple) else self.resolution,
            "fps": self.fps,
            "bitrate": self.bitrate,
            "audio_bitrate": self.audio_bitrate,
            "codec": self.codec,
            "audio_codec": self.audio_codec,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ExportPreset":
        fmt = data.get("format", "mp4")
        if isinstance(fmt, str):
            fmt = ExportFormat(fmt)
        res = data.get("resolution", [1920, 1080])
        if isinstance(res, list):
            res = tuple(res)
        return cls(
            id=data.get("id", str(uuid.uuid4())),
            name=data.get("name", "未命名预设"),
            description=data.get("description", ""),
            format=fmt,
            resolution=res,
            fps=data.get("fps", 30),
            bitrate=data.get("bitrate", 8000),
            audio_bitrate=data.get("audio_bitrate", 128),
            codec=data.get("codec", "h264"),
            audio_codec=data.get("audio_codec", "aac"),
        )


@dataclass
class ExportTask:
    """导出任务"""
    id: str = field(default_factory=lambda: f"export_{int(time.time() * 1000)}")
    project_id: str = ""
    name: str = ""
    output_path: str = ""
    preset_id: str = ""
    preset: Optional[ExportPreset] = None
    status: ExportStatus = ExportStatus.PENDING
    progress: float = 0.0
    error_message: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)
    started_at: Optional[float] = None
    completed_at: Optional[float] = None
    created_at: float = field(default_factory=time.time)
    error_detail: str = ""

    def to_dict(self) -> Dict[str, Any]:
        result = {
            "id": self.id,
            "project_id": self.project_id,
            "name": self.name,
            "output_path": self.output_path,
            "preset_id": self.preset_id,
            "status": self.status.value,
            "progress": self.progress,
            "error_message": self.error_message,
            "metadata": self.metadata,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "created_at": self.created_at,
            "error_detail": self.error_detail,
        }
        if self.preset:
            result["preset"] = self.preset.to_dict()
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ExportTask":
        status = ExportStatus(data.get("status", "pending"))
        preset_data = data.get("preset")
        preset = ExportPreset.from_dict(preset_data) if preset_data else None
        return cls(
            id=data.get("id", str(uuid.uuid4())),
            project_id=data.get("project_id", ""),
            name=data.get("name", ""),
            output_path=data.get("output_path", ""),
            preset_id=data.get("preset_id", ""),
            preset=preset,
            status=status,
            progress=data.get("progress", 0.0),
            error_message=data.get("error_message", ""),
            metadata=data.get("metadata", {}),
            started_at=data.get("started_at"),
            completed_at=data.get("completed_at"),
            created_at=data.get("created_at", time.time()),
            error_detail=data.get("error_detail", ""),
        )


class ExportSystem(QObject):
    """
    导出一个中心化的任务调度系统。
    
    管理导出队列、预设持久化、并发控制和信号发射。
    """

    # 信号定义
    export_started = Signal(str)  # task_id
    export_progress = Signal(str, float)  # task_id, progress (0.0-1.0)
    export_completed = Signal(str, str)  # task_id, output_path
    export_failed = Signal(str, str)  # task_id, error_message
    export_cancelled = Signal(str)  # task_id
    export_paused = Signal(str)  # task_id
    export_resumed = Signal(str)  # task_id
    queue_updated = Signal()  # 无参数

    def __init__(
        self,
        max_concurrent: int = 2,
        presets_file: Optional[str] = None,
        history_file: Optional[str] = None,
    ):
        """
        初始化导出系统。
        
        Args:
            max_concurrent: 最大并发导出数
            presets_file: 预设持久化文件路径
            history_file: 任务历史持久化文件路径
        """
        super().__init__()
        self._max_concurrent = max_concurrent
        self._presets_file = presets_file or self._default_presets_file()
        self._history_file = history_file or self._default_history_file()
        self._tasks: Dict[str, ExportTask] = {}
        self._presets: Dict[str, ExportPreset] = {}
        self._lock = threading.RLock()
        self._executor = ThreadPoolExecutor(max_workers=max_concurrent)
        self._futures: Dict[str, Future] = {}
        self._cancelled: set = set()
        self._cleanup_timer: Optional[threading.Timer] = None
        self._auto_cleanup_days = 7  # 默认保留7天

        self._load_presets()
        self._load_history()
        self._init_default_presets()

    # ── 公共 API ──────────────────────────────────────────────────────────────

    def export_project(
        self,
        project_id: str,
        output_path: str,
        preset_id: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        添加单个导出任务到队列。
        
        Returns:
            task_id
        """
        preset = self._presets.get(preset_id)
        if not preset:
            preset = self._get_default_preset()

        task = ExportTask(
            project_id=project_id,
            name=metadata.get("project_name", f"Project_{project_id}") if metadata else f"Project_{project_id}",
            output_path=output_path,
            preset_id=preset_id,
            preset=preset,
            status=ExportStatus.QUEUED,
            metadata=metadata or {},
        )

        with self._lock:
            self._tasks[task.id] = task

        self._submit_task(task)
        self.queue_updated.emit()
        return task.id

    def export_batch(
        self,
        batch_configs: List[Dict[str, Any]],
    ) -> List[str]:
        """
        添加批量导出任务。
        
        Args:
            batch_configs: [{"project_id", "output_path", "preset_id", "metadata"}, ...]
        
        Returns:
            [task_id, ...]
        """
        task_ids = []
        for config in batch_configs:
            task_id = self.export_project(
                project_id=config.get("project_id", ""),
                output_path=config.get("output_path", ""),
                preset_id=config.get("preset_id", ""),
                metadata=config.get("metadata"),
            )
            task_ids.append(task_id)
        return task_ids

    def get_task(self, task_id: str) -> Optional[ExportTask]:
        """获取任务"""
        with self._lock:
            return self._tasks.get(task_id)

    def get_task_history(self) -> List[ExportTask]:
        """获取所有任务（含历史的）"""
        with self._lock:
            return list(self._tasks.values())

    def get_active_tasks(self) -> List[ExportTask]:
        """获取活动任务"""
        with self._lock:
            return [
                t for t in self._tasks.values()
                if t.status in (ExportStatus.PENDING, ExportStatus.QUEUED, ExportStatus.PROCESSING)
            ]

    def get_presets(self) -> List[ExportPreset]:
        """获取所有预设"""
        with self._lock:
            return list(self._presets.values())

    def get_preset(self, preset_id: str) -> Optional[ExportPreset]:
        """获取预设"""
        return self._presets.get(preset_id)

    def add_preset(self, preset: ExportPreset) -> None:
        """添加预设"""
        with self._lock:
            self._presets[preset.id] = preset
        self._save_presets()
        self.queue_updated.emit()

    def update_preset(self, preset_id: str, data: Dict[str, Any]) -> bool:
        """更新预设"""
        with self._lock:
            if preset_id not in self._presets:
                return False
            preset = self._presets[preset_id]
            for key, value in data.items():
                if hasattr(preset, key):
                    setattr(preset, key, value)
        self._save_presets()
        self.queue_updated.emit()
        return True

    def delete_preset(self, preset_id: str) -> bool:
        """删除预设"""
        with self._lock:
            if preset_id in self._presets:
                del self._presets[preset_id]
                self._save_presets()
                return True
        return False

    def cancel_export(self, task_id: str) -> bool:
        """取消导出任务"""
        with self._lock:
            task = self._tasks.get(task_id)
            if not task:
                return False
            if task.status in (ExportStatus.COMPLETED, ExportStatus.FAILED, ExportStatus.CANCELLED):
                return False
            self._cancelled.add(task_id)
            task.status = ExportStatus.CANCELLED
            task.completed_at = time.time()
        if task_id in self._futures:
            self._futures[task_id].cancel()
        self.export_cancelled.emit(task_id)
        self.queue_updated.emit()
        return True

    def pause_export(self, task_id: str) -> bool:
        """暂停导出任务"""
        with self._lock:
            task = self._tasks.get(task_id)
            if not task or task.status != ExportStatus.PROCESSING:
                return False
            task.status = ExportStatus.PAUSED
        self.export_paused.emit(task_id)
        self.queue_updated.emit()
        return True

    def resume_export(self, task_id: str) -> bool:
        """恢复导出任务"""
        with self._lock:
            task = self._tasks.get(task_id)
            if not task or task.status != ExportStatus.PAUSED:
                return False
            task.status = ExportStatus.QUEUED
        self.export_resumed.emit(task_id)
        self._submit_task(task)
        self.queue_updated.emit()
        return True

    def remove_from_queue(self, task_id: str) -> bool:
        """从队列移除任务"""
        with self._lock:
            task = self._tasks.get(task_id)
            if not task:
                return False
            if task.status in (ExportStatus.PROCESSING, ExportStatus.QUEUED):
                self._cancelled.add(task_id)
                if task_id in self._futures:
                    self._futures[task_id].cancel()
            if task_id in self._tasks:
                del self._tasks[task_id]
        self.queue_updated.emit()
        return True

    def clear_completed(self) -> bool:
        """清除已完成的任务"""
        with self._lock:
            to_remove = [
                tid for tid, t in self._tasks.items()
                if t.status in (ExportStatus.COMPLETED, ExportStatus.FAILED, ExportStatus.CANCELLED)
            ]
            for tid in to_remove:
                del self._tasks[tid]
        self.queue_updated.emit()
        return True

    def set_concurrent_limit(self, limit: int) -> None:
        """设置最大并发数"""
        self._max_concurrent = limit
        self._executor._max_workers = limit  # ThreadPoolExecutor 支持动态调整

    def set_auto_cleanup(self, days: int) -> None:
        """设置自动清理（保留天数）"""
        self._auto_cleanup_days = days
        self._schedule_cleanup()

    def shutdown(self) -> None:
        """关闭导出系统"""
        if self._cleanup_timer:
            self._cleanup_timer.cancel()
        for future in self._futures.values():
            future.cancel()
        self._executor.shutdown(wait=True)

    # ── 内部方法 ──────────────────────────────────────────────────────────────

    def _submit_task(self, task: ExportTask) -> None:
        """提交任务到线程池"""
        with self._lock:
            if task.id in self._cancelled:
                return
            task.status = ExportStatus.QUEUED
        future = self._executor.submit(self._run_export, task)
        with self._lock:
            self._futures[task.id] = future

    def _run_export(self, task: ExportTask) -> None:
        """执行导出（在线程池中运行）"""
        if task.id in self._cancelled:
            return

        task.status = ExportStatus.PROCESSING
        task.started_at = time.time()
        self.export_started.emit(task.id)

        try:
            # 构建导出配置
            from app.services.export.export_manager import ExportManager, ExportFormat as EMFormat
            from app.services.export.export_manager import ExportConfig

            fmt_map = {
                "mp4": EMFormat.MP4,
                "mov": EMFormat.MOV,
                "gif": EMFormat.GIF,
                "jianying": EMFormat.JIANYING,
            }

            preset = task.preset
            if preset:
                export_fmt = fmt_map.get(preset.format.value, EMFormat.MP4)
                resolution_str = preset.resolution if isinstance(preset.resolution, str) else f"{preset.resolution[0]}x{preset.resolution[1]}"
            else:
                export_fmt = EMFormat.MP4
                resolution_str = "1920x1080"

            config = ExportConfig(
                format=export_fmt,
                quality="high",
                resolution=resolution_str,
                fps=preset.fps if preset else 30,
                codec=preset.codec if preset else "h264",
                audio_codec=preset.audio_codec if preset else "aac",
                bitrate=f"{preset.bitrate // 1000}M" if preset else "8M",
                output_path=task.output_path,
                progress_callback=lambda p: self._on_progress(task.id, p),
            )

            # 构建项目数据
            project_data = {
                "id": task.project_id,
                "name": task.name,
                "metadata": task.metadata,
            }

            manager = ExportManager()
            success = manager.export(project_data, config)

            if task.id in self._cancelled:
                task.status = ExportStatus.CANCELLED
                task.completed_at = time.time()
                self.export_cancelled.emit(task.id)
                return

            if success:
                task.status = ExportStatus.COMPLETED
                task.progress = 100.0
                task.completed_at = time.time()
                self.export_completed.emit(task.id, task.output_path)
                self._save_history()
            else:
                raise Exception("ExportManager returned False")

        except Exception as e:
            task.status = ExportStatus.FAILED
            task.error_message = str(e)
            task.error_detail = repr(e)
            task.completed_at = time.time()
            logger.error(f"Export task {task.id} failed: {e}")
            self.export_failed.emit(task.id, str(e))
        finally:
            with self._lock:
                if task.id in self._futures:
                    del self._futures[task.id]
            self.queue_updated.emit()

    def _on_progress(self, task_id: str, progress: float) -> None:
        """进度回调"""
        with self._lock:
            task = self._tasks.get(task_id)
            if task:
                task.progress = max(task.progress, progress)
        self.export_progress.emit(task_id, progress)

    def _get_default_preset(self) -> ExportPreset:
        """获取默认预设"""
        for preset in self._presets.values():
            if preset.name == "默认预设":
                return preset
        default = ExportPreset(
            name="默认预设",
            description="系统默认导出预设",
            format=ExportFormat.MP4,
            resolution=(1920, 1080),
            fps=30,
            bitrate=8000,
            audio_bitrate=128,
            codec="h264",
            audio_codec="aac",
        )
        self._presets[default.id] = default
        return default

    def _init_default_presets(self) -> None:
        """初始化默认预设（如果没有任何预设）"""
        if not self._presets:
            defaults = [
                ExportPreset(
                    name="高质量 1080p",
                    description="1920x1080 高质量导出",
                    format=ExportFormat.MP4,
                    resolution=(1920, 1080),
                    fps=30,
                    bitrate=12000,
                    audio_bitrate=192,
                    codec="h264",
                    audio_codec="aac",
                ),
                ExportPreset(
                    name="快速导出",
                    description="低比特率快速导出",
                    format=ExportFormat.MP4,
                    resolution=(1280, 720),
                    fps=30,
                    bitrate=4000,
                    audio_bitrate=96,
                    codec="h264",
                    audio_codec="aac",
                ),
                ExportPreset(
                    name="剪映草稿",
                    description="导出为剪映草稿格式",
                    format=ExportFormat.JIANYING,
                    resolution=(1920, 1080),
                    fps=30,
                    bitrate=8000,
                    audio_bitrate=128,
                    codec="h264",
                    audio_codec="aac",
                ),
            ]
            with self._lock:
                for p in defaults:
                    self._presets[p.id] = p
            self._save_presets()

    def _schedule_cleanup(self) -> None:
        """安排自动清理"""
        if self._cleanup_timer:
            self._cleanup_timer.cancel()
        interval = 24 * 3600  # 每天执行一次
        self._cleanup_timer = threading.Timer(interval, self._auto_cleanup)
        self._cleanup_timer.daemon = True
        self._cleanup_timer.start()

    def _auto_cleanup(self) -> None:
        """自动清理过期任务"""
        cutoff = time.time() - (self._auto_cleanup_days * 24 * 3600)
        with self._lock:
            to_remove = [
                tid for tid, t in self._tasks.items()
                if t.completed_at and t.completed_at < cutoff
                and t.status in (ExportStatus.COMPLETED, ExportStatus.FAILED, ExportStatus.CANCELLED)
            ]
            for tid in to_remove:
                del self._tasks[tid]
        if to_remove:
            self._save_history()
            self.queue_updated.emit()
        self._schedule_cleanup()

    # ── 持久化 ───────────────────────────────────────────────────────────────

    def _default_presets_file(self) -> str:
        return str(Path.home() / ".voxplore" / "presets.json")

    def _default_history_file(self) -> str:
        return str(Path.home() / ".voxplore" / "export_history.json")

    def _load_presets(self) -> None:
        """从文件加载预设"""
        try:
            path = Path(self._presets_file)
            if path.exists():
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for pdata in data if isinstance(data, list) else data.get("presets", []):
                        preset = ExportPreset.from_dict(pdata)
                        self._presets[preset.id] = preset
                logger.info(f"Loaded {len(self._presets)} presets")
        except Exception as e:
            logger.warning(f"Failed to load presets: {e}")

    def _save_presets(self) -> None:
        """保存预设到文件"""
        try:
            path = Path(self._presets_file)
            path.parent.mkdir(parents=True, exist_ok=True)
            with open(path, "w", encoding="utf-8") as f:
                json.dump([p.to_dict() for p in self._presets.values()], f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"Failed to save presets: {e}")

    def _load_history(self) -> None:
        """从文件加载任务历史"""
        try:
            path = Path(self._history_file)
            if path.exists():
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    tasks_data = data.get("tasks", []) if isinstance(data, dict) else data
                    for tdata in tasks_data:
                        task = ExportTask.from_dict(tdata)
                        self._tasks[task.id] = task
                logger.info(f"Loaded {len(self._tasks)} history tasks")
        except Exception as e:
            logger.warning(f"Failed to load history: {e}")

    def _save_history(self) -> None:
        """保存任务历史到文件"""
        try:
            path = Path(self._history_file)
            path.parent.mkdir(parents=True, exist_ok=True)
            with open(path, "w", encoding="utf-8") as f:
                json.dump(
                    {"tasks": [t.to_dict() for t in self._tasks.values()]},
                    f, ensure_ascii=False, indent=2
                )
        except Exception as e:
            logger.error(f"Failed to save history: {e}")
