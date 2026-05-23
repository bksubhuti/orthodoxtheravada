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
  font-family: "Plus Jakarta Sans", sans-serif;
  font-weight: 700;
  border-bottom: 2px solid #edeae4;
  margin-top: 2.5rem;
  padding-bottom: 0.5rem;
  color: #6c2e1f; /* Cohesive monastic theme color */
  letter-spacing: -0.01em;
}
.lists-list {
  list-style: none;
  padding-left: 0;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1.25rem;
  margin-top: 1rem;
}
.lists-list li {
  margin-bottom: 0;
  padding: 0.75rem 1.1rem;
  background: #ffffff;
  border: 1px solid #edeae4;
  border-left: 4px solid #edeae4; /* Left border accent */
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.015);
  transition: all 0.25s cubic-bezier(0.2, 0.8, 0.2, 1);
}
.lists-list li:hover {
  transform: translateY(-4px);
  border-color: rgba(108, 46, 31, 0.25);
  border-left-color: #6c2e1f; /* highlight border on hover */
  background: #ffffff;
  box-shadow: 0 10px 24px rgba(108, 46, 31, 0.05), 0 3px 8px rgba(0, 0, 0, 0.01);
}
.lists-list a {
  text-decoration: none;
  font-family: "Plus Jakarta Sans", sans-serif;
  font-weight: 700;
  font-size: 1.05rem;
  color: #6c2e1f; /* Theme maroon link color */
  transition: color 0.2s ease;
}
.lists-list a:hover {
  color: #4d2015;
  text-decoration: none;
}
.lists-list em {
  display: block;
  font-family: "Lora", serif;
  font-style: italic;
  font-size: 0.88rem;
  color: #666666;
  margin-top: 0.25rem;
}
</style>
