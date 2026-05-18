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
        </ul>
      {% endif %}
      <h2 id="group-{{ list.list_count }}">{{ list.list_count }}-fold Dhamma</h2>
      <ul class="lists-list">
      {% assign current_count = list.list_count %}
    {% endif %}
    
    <li>
      <a href="{{ list.url | relative_url }}"><strong>{{ list.title }}</strong></a> 
      {% if list.pali_title %}
        <em>({{ list.pali_title }})</em>
      {% endif %}
    </li>
  {% endfor %}
  
  {% if current_count != 0 %}
    </ul>
  {% endif %}
</div>

<style>
.lists-index h2 {
  border-bottom: 2px solid #f2f2f2;
  margin-top: 2em;
  padding-bottom: 0.5em;
  color: #8b0000; /* Subtle dark red accent for canonical list sections */
}
.lists-list {
  list-style: none;
  padding-left: 0;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 15px;
}
.lists-list li {
  margin-bottom: 5px;
  padding: 10px;
  background: #fdfdfd;
  border: 1px solid #eaeaea;
  border-radius: 4px;
  transition: all 0.2s ease-in-out;
}
.lists-list li:hover {
  background: #f8f9fa;
  border-color: #d1d1d1;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
}
.lists-list a {
  text-decoration: none;
  color: #0056b3;
}
.lists-list a:hover {
  text-decoration: underline;
}
</style>
