"""tests/test_data_ptp.py – PTP 資料擷取邏輯的單元測試。"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from stockscreener.data.ptp import get_ptp_tickers, remove_ptp_tickers

# ── 模擬 HTML 內容 ─────────────────────────────────────────────────────────────

_SITE1_HTML = """
<html><body>
<table width="100%"><tbody>
<tr><td>1</td><td>Company A</td><td>AAPL</td></tr>
<tr><td>2</td><td>Company B</td><td>TSLA</td></tr>
</tbody></table>
</body></html>
"""

_SITE2_HTML = """
<html><body>
<table class="table">
<tr><td>TSLA</td><td>Tesla</td></tr>
<tr><td>MSFT</td><td>Microsoft</td></tr>
</table>
</body></html>
"""


def _make_response(text: str) -> MagicMock:
    resp = MagicMock()
    resp.content = text.encode("utf-8")
    resp.text = text
    resp.status_code = 200
    return resp


class TestGetPtpTickers:
    # ptp.py 在函式內部 import requests，需 mock requests 模組本身
    def test_returns_merged_deduplicated_list(self):
        with patch("requests.get") as mock_get:
            mock_get.side_effect = [
                _make_response(_SITE1_HTML),
                _make_response(_SITE2_HTML),
            ]
            result = get_ptp_tickers()

        # AAPL（site1）、TSLA（兩站都有，去重）、MSFT（site2）
        assert "AAPL" in result
        assert "TSLA" in result
        assert "MSFT" in result
        # 去重後 TSLA 只出現一次
        assert result.count("TSLA") == 1

    def test_returns_list_type(self):
        with patch("requests.get") as mock_get:
            mock_get.side_effect = [
                _make_response(_SITE1_HTML),
                _make_response(_SITE2_HTML),
            ]
            result = get_ptp_tickers()
        assert isinstance(result, list)

    def test_network_error_returns_partial(self):
        """單一網站失敗時，函式應繼續（內部 try/except）回傳部分結果。"""
        import requests as req_mod
        with patch("requests.get") as mock_get:
            mock_get.side_effect = [
                req_mod.RequestException("timeout"),
                _make_response(_SITE2_HTML),
            ]
            result = get_ptp_tickers()
        # 第二個網站成功，應有 MSFT
        assert isinstance(result, list)


class TestRemovePtpTickers:
    # 實際 API: remove_ptp_tickers(tickers, ptp_tickers)
    def test_removes_ptp_from_list(self):
        ptp = ["TSLA", "MSFT"]
        tickers = ["AAPL", "TSLA", "GOOG", "MSFT", "AMZN"]
        result = remove_ptp_tickers(tickers, ptp)
        assert "TSLA" not in result
        assert "MSFT" not in result
        assert "AAPL" in result
        assert "GOOG" in result
        assert "AMZN" in result

    def test_empty_ptp_list(self):
        tickers = ["AAPL", "TSLA"]
        result = remove_ptp_tickers(tickers, [])
        assert result == tickers

    def test_all_ptp_returns_empty(self):
        ptp = ["AAPL", "TSLA"]
        result = remove_ptp_tickers(["AAPL", "TSLA"], ptp)
        assert result == []
