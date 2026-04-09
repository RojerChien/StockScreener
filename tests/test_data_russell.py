"""tests/test_data_russell.py – Russell 1000 資料擷取邏輯的單元測試。"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from stockscreener.data.russell import _parse_iwb_csv, get_russell1000_tickers

# ── 模擬 iShares IWB CSV 內容 ──────────────────────────────────────────────────

_MOCK_CSV = """\
iShares Russell 1000 ETF
As of Date,04/09/2026
Inception Date,05/19/2000
Shares Outstanding,"180,500,000.00"
Stock,IWB
Net Assets,"$38,946,490,900.21"
Net Asset Value,$215.77

Name,Ticker,Asset Class,Market Value,Weight (%),Notional Value,Shares,Price,Location,Exchange,Currency
APPLE INC,AAPL,Equity,"2,123,456,789.00",5.45,"2,123,456,789.00","10,000,000",212.34,United States,NASDAQ,USD
MICROSOFT CORP,MSFT,Equity,"1,987,654,321.00",5.10,"1,987,654,321.00","5,000,000",397.53,United States,NASDAQ,USD
NVIDIA CORP,NVDA,Equity,"1,800,000,000.00",4.62,"1,800,000,000.00","15,000,000",120.00,United States,NASDAQ,USD
BLACKROCK CASH FUNDS,-,Cash Collateral and/or Derivatives,"500,000.00",0.00,,,,United States,,USD

"""

_MOCK_CSV_NO_ASSET_CLASS = """\
Name,Ticker,Market Value
APPLE INC,AAPL,"1,000"
MICROSOFT CORP,MSFT,"900"
"""

_MOCK_CSV_NO_HEADER = """\
iShares Russell 1000 ETF
As of Date,04/09/2026
"""


# ── _parse_iwb_csv 單元測試 ──────────────────────────────────────────────────────

class TestParseIwbCsv:
    def test_returns_equity_tickers_only(self):
        tickers = _parse_iwb_csv(_MOCK_CSV)
        assert "AAPL" in tickers
        assert "MSFT" in tickers
        assert "NVDA" in tickers

    def test_excludes_non_equity_rows(self):
        """現金、衍生品等非 Equity 列應被排除。"""
        tickers = _parse_iwb_csv(_MOCK_CSV)
        assert "-" not in tickers

    def test_returns_list_of_strings(self):
        tickers = _parse_iwb_csv(_MOCK_CSV)
        assert isinstance(tickers, list)
        assert all(isinstance(t, str) for t in tickers)

    def test_no_asset_class_column_returns_all(self):
        """無 Asset Class 欄時，回傳所有 Ticker（不做類型過濾）。"""
        tickers = _parse_iwb_csv(_MOCK_CSV_NO_ASSET_CLASS)
        assert "AAPL" in tickers
        assert "MSFT" in tickers

    def test_missing_name_header_raises(self):
        with pytest.raises(ValueError, match="無法識別"):
            _parse_iwb_csv(_MOCK_CSV_NO_HEADER)

    def test_strips_whitespace(self):
        csv_with_spaces = _MOCK_CSV.replace("AAPL", " AAPL ")
        tickers = _parse_iwb_csv(csv_with_spaces)
        assert "AAPL" in tickers
        assert " AAPL " not in tickers

    def test_handles_bom(self):
        """UTF-8 BOM 開頭的 CSV 應可正確解析（_parse_iwb_csv 接收已解碼字串）。"""
        csv_with_bom = "\ufeff" + _MOCK_CSV
        tickers = _parse_iwb_csv(csv_with_bom)
        assert "AAPL" in tickers


# ── get_russell1000_tickers 整合測試（mock requests）────────────────────────────

class TestGetRussell1000Tickers:
    def _make_response(self, text: str, status: int = 200):
        mock_resp = MagicMock()
        mock_resp.content = text.encode("utf-8")
        mock_resp.status_code = status
        mock_resp.raise_for_status = MagicMock()
        return mock_resp

    def test_returns_tickers(self):
        with patch("requests.get", return_value=self._make_response(_MOCK_CSV)):
            tickers = get_russell1000_tickers()
        assert isinstance(tickers, list)
        assert "AAPL" in tickers
        assert "MSFT" in tickers
        assert "NVDA" in tickers

    def test_excludes_non_equity(self):
        with patch("requests.get", return_value=self._make_response(_MOCK_CSV)):
            tickers = get_russell1000_tickers()
        assert "-" not in tickers

    def test_network_error_raises_connection_error(self):
        import requests as req_lib

        with patch("requests.get", side_effect=req_lib.RequestException("timeout")):
            with pytest.raises(ConnectionError, match="iShares IWB"):
                get_russell1000_tickers()

    def test_http_error_raises_connection_error(self):
        import requests as req_lib

        mock_resp = self._make_response("", status=403)
        mock_resp.raise_for_status.side_effect = req_lib.HTTPError("403")
        with patch("requests.get", return_value=mock_resp):
            with pytest.raises(ConnectionError):
                get_russell1000_tickers()
