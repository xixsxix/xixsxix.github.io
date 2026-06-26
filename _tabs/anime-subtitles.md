---

layout: page
title: Anime Subs
icon: fas fa-closed-captioning
order: 4
permalink: /anime-subtitles/
----------------------------

# 애니 자막 상태

사용자가 직접 선정한 애니 작품의 Anissia 자막 등록 상태를 확인하는 페이지입니다.

마지막 업데이트: `{{ site.data.anissia_caption_status.last_updated_at | replace: "T", " " | replace: "+09:00", "" }}`

<div class="table-wrapper">
  <table>
    <thead>
      <tr>
        <th>작품</th>
        <th>방영</th>
        <th>최신 자막</th>
        <th>제작자</th>
        <th>등록 시간</th>
        <th>링크</th>
      </tr>
    </thead>
    <tbody>
      {% for item in site.data.anissia_caption_status.items %}
      <tr>
        <td>
          <strong>{{ item.display_name }}</strong><br>
          <small>{{ item.original_title }} · #{{ item.animeNo }}</small>
        </td>

```
    <td>
      {% assign broadcast_week = item.broadcast_week | default: "" %}
      {% assign broadcast_time = item.broadcast_time | default: "" %}
      {% if broadcast_week != "" or broadcast_time != "" %}
        {{ broadcast_week }} {{ broadcast_time }}
      {% else %}
        -
      {% endif %}
    </td>

    <td>
      {% assign latest_episode = item.latest_episode | default: "" %}
      {% if latest_episode != "" %}
        {{ latest_episode }}화
      {% else %}
        -
      {% endif %}
    </td>

    <td>
      {% assign caption_author = item.caption_author | default: "" %}
      {% if caption_author != "" %}
        {{ caption_author }}
      {% else %}
        대기중
      {% endif %}
    </td>

    <td>
      {% assign latest_updDt = item.latest_updDt | default: "" %}
      {% if latest_updDt != "" %}
        {{ latest_updDt | replace: "T", " " }}
      {% else %}
        -
      {% endif %}
    </td>

    <td>
      {% assign caption_url = item.caption_url | default: "" %}
      {% if caption_url != "" %}
        <a href="{{ caption_url }}" target="_blank" rel="noopener noreferrer">자막</a>
      {% else %}
        <span>대기중</span>
      {% endif %}
    </td>
  </tr>
  {% endfor %}
</tbody>
```

  </table>
</div>
