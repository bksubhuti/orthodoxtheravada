---
layout: single
title: "Numerical Dhamma Lists"
permalink: /lists/
author_profile: false
---

<div class="lists-index">
  {% assign sorted_by_title = site.lists | sort: "title" %}
  {% assign sorted_lists = sorted_by_title | sort: "list_count" %}
  {% assign current_count = 0 %}

  {% comment %}--- Jump-bar of list numbers, frozen like the glossary letters ---{% endcomment %}
  {% assign counts = sorted_lists | map: "list_count" | uniq %}
  <nav class="glossary-letter-bar" aria-label="Jump to number">
    {% for n in counts %}
      <a href="#group-{{ n }}" class="glossary-letter-link">{{ n }}</a>
    {% endfor %}
  </nav>

  {% for list in sorted_lists %}
    {% if list.list_count != current_count %}
      {% if current_count != 0 %}
        </div>
      {% endif %}
      <h2 id="group-{{ list.list_count }}">{{ list.list_count }}-fold Dhamma</h2>
      <div class="ot-index-grid">
      {% assign current_count = list.list_count %}
    {% endif %}
    <a href="{{ list.url | relative_url }}" class="ot-index-card">
      <strong class="ot-index-card__title">{{ list.title }}</strong>
      {% if list.pali_title %}
        <span class="ot-index-card__subtitle">({{ list.pali_title }})</span>
      {% endif %}
    </a>
  {% endfor %}
  
  {% if current_count != 0 %}
    </div>
  {% endif %}
</div>
