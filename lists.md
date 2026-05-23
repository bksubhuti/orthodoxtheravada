---
layout: single
title: "Numerical Dhamma Lists"
permalink: /lists/
author_profile: false
---

Welcome to the Numerical Dhamma Lists. Here you will find structured, doctrinal lists from the Theravāda canonical texts and commentaries, organized by their numerical count.

<div class="lists-index">
  {% assign sorted_by_title = site.lists | sort: "title" %}
  {% assign sorted_lists = sorted_by_title | sort: "list_count" %}
  {% assign current_count = 0 %}

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
