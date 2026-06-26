#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Anissia Caption Status Updater

역할:
1. _data/anissia_watchlist.json 에서 animeNo 목록을 읽는다.
2. Anissia API로 작품 정보와 최신 자막 정보를 조회한다.
3. _data/anissia_caption_status.json 을 자동 갱신한다.

사용 예:
python _scripts/update_anissia_caption_status.py
"""

import json
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "_data"

WATCHLIST_PATH = DATA_DIR / "anissia_watchlist.json"
STATUS_PATH = DATA_DIR / "anissia_caption_status.json"

DETAIL_API = "https://api.anissia.net/anime/animeNo/{animeNo}"
CAPTION_API = "https://api.anissia.net/anime/caption/animeNo/{animeNo}"

KST = timezone(timedelta(hours=9))

WEEK_MAP = {
    "0": "일요일",
    "1": "월요일",
    "2": "화요일",
    "3": "수요일",
    "4": "목요일",
    "5": "금요일",
    "6": "토요일",
    "7": "기타",
    "8": "신작",
}


def fetch_json(url: str) -> Any:
    """
    지정 URL에서 JSON 응답을 가져온다.
    """
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "xixsxix.github.io Anissia caption status updater"
        },
    )

    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            charset = response.headers.get_content_charset() or "utf-8"
            text = response.read().decode(charset)
            return json.loads(text)

    except urllib.error.HTTPError as exc:
        raise RuntimeError(f"HTTP error {exc.code} while fetching {url}") from exc

    except urllib.error.URLError as exc:
        raise RuntimeError(f"URL error while fetching {url}: {exc.reason}") from exc

    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Invalid JSON response from {url}") from exc


def load_watchlist() -> List[Dict[str, Any]]:
    """
    _data/anissia_watchlist.json 을 읽는다.

    지원 형식 1:
    {
      "items": [
        { "animeNo": 3341, "memo": "황천의 츠가이" }
      ]
    }

    지원 형식 2:
    {
      "animeNos": [3341, 3371, 3334, 3223]
    }
    """
    if not WATCHLIST_PATH.exists():
        raise FileNotFoundError(f"Watchlist file not found: {WATCHLIST_PATH}")

    with WATCHLIST_PATH.open("r", encoding="utf-8") as file:
        data = json.load(file)

    if "items" in data:
        items = []
        for item in data["items"]:
            if "animeNo" not in item:
                continue

            items.append(
                {
                    "animeNo": int(item["animeNo"]),
                    "memo": item.get("memo", ""),
                }
            )

        return items

    if "animeNos" in data:
        return [
            {
                "animeNo": int(anime_no),
                "memo": "",
            }
            for anime_no in data["animeNos"]
        ]

    raise ValueError("Watchlist must contain either 'items' or 'animeNos'.")


def normalize_detail_response(response: Any) -> Optional[Dict[str, Any]]:
    """
    Anissia 상세 API 응답을 정규화한다.

    기대 형태:
    {
      "code": "ok",
      "data": {
        "animeNo": 3341,
        "subject": "...",
        "captions": [...]
      }
    }
    """
    if not isinstance(response, dict):
        return None

    data = response.get("data")

    if isinstance(data, dict):
        return data

    return None


def normalize_caption_response(response: Any) -> List[Dict[str, Any]]:
    """
    caption API 응답을 captions 배열로 정규화한다.

    가능한 형태 1:
    [
      { "episode": "12", "updDt": "...", "website": "...", "name": "..." }
    ]

    가능한 형태 2:
    {
      "code": "ok",
      "data": [
        { "episode": "12", "updDt": "...", "website": "...", "name": "..." }
      ]
    }

    가능한 형태 3:
    {
      "code": "ok",
      "data": {
        "captions": [...]
      }
    }
    """
    if isinstance(response, list):
        return response

    if isinstance(response, dict):
        data = response.get("data")

        if isinstance(data, list):
            return data

        if isinstance(data, dict) and isinstance(data.get("captions"), list):
            return data["captions"]

    return []


def episode_sort_key(value: Any) -> float:
    """
    episode 값을 정렬 가능한 숫자로 변환한다.
    예: "1" -> 1.0, "12" -> 12.0, "0.5" -> 0.5
    """
    try:
        return float(str(value))
    except (TypeError, ValueError):
        return -1.0


def pick_latest_caption(captions: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    """
    captions 배열에서 최신 자막 하나를 선택한다.
    기본 기준:
    1. episode 숫자가 큰 것
    2. episode가 같으면 updDt가 최신인 것
    """
    if not captions:
        return None

    return sorted(
        captions,
        key=lambda caption: (
            episode_sort_key(caption.get("episode")),
            str(caption.get("updDt", "")),
        ),
        reverse=True,
    )[0]


def get_latest_caption_from_api_or_detail(
    anime_no: int,
    detail_data: Optional[Dict[str, Any]],
) -> Optional[Dict[str, Any]]:
    """
    1차: 상세 API의 captions 사용
    2차: 별도 caption API 호출
    """
    if detail_data and isinstance(detail_data.get("captions"), list):
        latest = pick_latest_caption(detail_data["captions"])
        if latest:
            return latest

    caption_url = CAPTION_API.format(animeNo=anime_no)
    caption_response = fetch_json(caption_url)
    captions = normalize_caption_response(caption_response)
    return pick_latest_caption(captions)


def build_status_item(
    watch_item: Dict[str, Any],
    detail_data: Optional[Dict[str, Any]],
    latest_caption: Optional[Dict[str, Any]],
) -> Dict[str, Any]:
    """
    Jekyll 페이지에서 사용할 item 구조를 만든다.
    """
    anime_no = int(watch_item["animeNo"])
    memo = watch_item.get("memo", "")

    if detail_data:
        week = str(detail_data.get("week", ""))

        display_name = detail_data.get("subject") or memo or f"#{anime_no}"
        original_title = detail_data.get("originalSubject", "")
        status = detail_data.get("status", "")
        broadcast_week = WEEK_MAP.get(week, week)
        broadcast_time = detail_data.get("time", "")
        genres = detail_data.get("genres", "")
        start_date = detail_data.get("startDate", "")
        end_date = detail_data.get("endDate", "")
        official_website = detail_data.get("website", "")
        official_x = detail_data.get("x", "")
        caption_count = detail_data.get("captionCount", 0)

    else:
        display_name = memo or f"#{anime_no}"
        original_title = ""
        status = "UNKNOWN"
        broadcast_week = ""
        broadcast_time = ""
        genres = ""
        start_date = ""
        end_date = ""
        official_website = ""
        official_x = ""
        caption_count = 0

    if latest_caption:
        latest_episode = str(latest_caption.get("episode", ""))
        latest_upd_dt = latest_caption.get("updDt", "")
        caption_author = latest_caption.get("name", "")
        caption_url = latest_caption.get("website", "")

        if caption_url:
            subtitle_status = "subtitle_ready"
        else:
            subtitle_status = "subtitle_wait"

    else:
        latest_episode = ""
        latest_upd_dt = ""
        caption_author = ""
        caption_url = ""
        subtitle_status = "subtitle_wait"

    return {
        "animeNo": anime_no,
        "display_name": display_name,
        "original_title": original_title,
        "status": status,
        "broadcast_week": broadcast_week,
        "broadcast_time": broadcast_time,
        "genres": genres,
        "startDate": start_date,
        "endDate": end_date,
        "official_website": official_website,
        "official_x": official_x,
        "captionCount": caption_count,
        "latest_episode": latest_episode,
        "latest_updDt": latest_upd_dt,
        "caption_author": caption_author,
        "caption_url": caption_url,
        "subtitle_status": subtitle_status,
    }


def main() -> int:
    try:
        watchlist = load_watchlist()

    except Exception as exc:
        print(f"[ERROR] Failed to load watchlist: {exc}", file=sys.stderr)
        return 1

    items: List[Dict[str, Any]] = []

    for watch_item in watchlist:
        anime_no = int(watch_item["animeNo"])

        print(f"[INFO] Fetching animeNo={anime_no}")

        try:
            detail_url = DETAIL_API.format(animeNo=anime_no)
            detail_response = fetch_json(detail_url)
            detail_data = normalize_detail_response(detail_response)

            latest_caption = get_latest_caption_from_api_or_detail(
                anime_no=anime_no,
                detail_data=detail_data,
            )

            status_item = build_status_item(
                watch_item=watch_item,
                detail_data=detail_data,
                latest_caption=latest_caption,
            )

            items.append(status_item)

            print(
                "[OK] "
                f"{status_item['animeNo']} "
                f"{status_item['display_name']} "
                f"{status_item['latest_episode']}화 "
                f"{status_item['caption_author']}"
            )

        except Exception as exc:
            print(f"[WARN] Failed to update animeNo={anime_no}: {exc}", file=sys.stderr)

            items.append(
                {
                    "animeNo": anime_no,
                    "display_name": watch_item.get("memo", "") or f"#{anime_no}",
                    "original_title": "",
                    "status": "ERROR",
                    "broadcast_week": "",
                    "broadcast_time": "",
                    "genres": "",
                    "startDate": "",
                    "endDate": "",
                    "official_website": "",
                    "official_x": "",
                    "captionCount": 0,
                    "latest_episode": "",
                    "latest_updDt": "",
                    "caption_author": "",
                    "caption_url": "",
                    "subtitle_status": "api_error",
                    "error": str(exc),
                }
            )

        # API 서버 부담 완화용 짧은 대기
        time.sleep(0.3)

    now = datetime.now(KST).strftime("%Y-%m-%d %H:%M:%S")

    output = {
        "last_updated_at": now,
        "source": "Anissia API",
        "items": items,
    }

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    with STATUS_PATH.open("w", encoding="utf-8") as file:
        json.dump(output, file, ensure_ascii=False, indent=2)

    print(f"[DONE] Updated {STATUS_PATH}")

    return 0


if __name__ == "__main__":
    sys.exit(main())