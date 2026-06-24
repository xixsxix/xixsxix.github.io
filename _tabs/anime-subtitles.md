---
layout: page
title: Anime Subs
icon: fas fa-closed-captioning
order: 6
permalink: /anime-subtitles/
---

# 애니 자막 상태

사용자가 직접 선정한 애니 작품의 Anissia 자막 등록 상태를 확인하는 페이지입니다.

마지막 업데이트: `{{ site.data.anissia_caption_status.last_updated_at }}`

<div class="table-wrapper">
  <table>
    <thead>
      <tr>
        <th>작품</th>
        <th>원제</th>
        <th>방영</th>
        <th>장르</th>
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
          <small>#{{ item.animeNo }}</small>
        </td>
        <td>{{ item.original_title }}</td>
        <td>{{ item.broadcast_week }} {{ item.broadcast_time }}</td>
        <td>{{ item.genres }}</td>
        <td>{{ item.latest_episode }}화</td>
        <td>{{ item.caption_author }}</td>
        <td>{{ item.latest_updDt | replace: "T", " " }}</td>
        <td>
          {% if item.caption_url %}
            <a href="{{ item.caption_url }}" target="_blank" rel="noopener">자막</a>
          {% else %}
            -
          {% endif %}
        </td>
      </tr>
      {% endfor %}
    </tbody>
  </table>
</div>