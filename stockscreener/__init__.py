"""StockScreener – top-level package."""

from __future__ import annotations

import logging
import os
from pathlib import Path
from typing import Any, Dict

__all__ = ["load_config", "__version__"]

__version__ = "1.0.0"

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(name)s  %(message)s",
)

# ---------------------------------------------------------------------------
# Config loader
# ---------------------------------------------------------------------------
_CONFIG_PATH = Path(__file__).parent.parent / "config.yaml"
_config_cache: Dict[str, Any] = {}


def load_config(path: str | Path | None = None) -> Dict[str, Any]:
    """Load and return the YAML configuration.

    Results are cached after the first call.  Pass *path* to override the
    default ``config.yaml`` location next to ``pyproject.toml``.
    """
    global _config_cache

    if _config_cache:
        return _config_cache

    cfg_path = Path(path) if path else _CONFIG_PATH

    try:
        import yaml  # type: ignore
    except ImportError as exc:
        raise ImportError(
            "PyYAML is required to load config.yaml – install it with: pip install pyyaml"
        ) from exc

    with open(cfg_path, "r", encoding="utf-8") as fh:
        _config_cache = yaml.safe_load(fh) or {}

    return _config_cache
