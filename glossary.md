---
layout: single
title: "Pāḷi Glossary"
permalink: /glossary/
author_profile: false
---

Welcome to the Orthodox Theravāda Glossary. Here you will find detailed definitions and textual references for key Pāḷi terms and doctrinal concepts.

<div class="glossary-index">
  {% assign sorted_terms = site.terms | sort: "title" %}
  {% assign current_letter = "" %}

  {% for term in sorted_terms %}
    {% capture first_letter %}{{ term.title | truncate: 1, "" | upcase }}{% endcapture %}
    
    {% if first_letter != current_letter %}
      {% if current_letter != "" %}
        </ul>
      {% endif %}
      <h2 id="{{ first_letter }}">{{ first_letter }}</h2>
      <ul class="term-list">
      {% assign current_letter = first_letter %}
    {% endif %}
    
    <li>
      <a href="{{ term.url | relative_url }}"><strong>{{ term.title }}</strong></a> 
      {% if term.pali_spelling %}
        <em>({{ term.pali_spelling }})</em>
      {% endif %}
    </li>
  {% endfor %}
  
  {% if current_letter != "" %}
    </ul>
  {% endif %}
</div>

<style>
.glossary-index h2 {
  font-family: "Plus Jakarta Sans", sans-serif;
  font-weight: 700;
  border-bottom: 2px solid #edeae4;
  margin-top: 2.5rem;
  padding-bottom: 0.5rem;
  color: #6c2e1f; /* Cohesive monastic theme color */
  letter-spacing: -0.01em;
}
.term-list {
  list-style: none;
  padding-left: 0;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 1.25rem;
  margin-top: 1rem;
}
.term-list li {
  margin-bottom: 0;
  padding: 0.75rem 1.1rem;
  background: #ffffff;
  border: 1px solid #edeae4;
  border-left: 4px solid #edeae4; /* Left border accent */
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.015);
  transition: all 0.25s cubic-bezier(0.2, 0.8, 0.2, 1);
}
.term-list li:hover {
  transform: translateY(-4px);
  border-color: rgba(108, 46, 31, 0.25);
  border-left-color: #6c2e1f; /* highlight border on hover */
  background: #ffffff;
  box-shadow: 0 10px 24px rgba(108, 46, 31, 0.05), 0 3px 8px rgba(0, 0, 0, 0.01);
}
.term-list a {
  text-decoration: none;
  font-family: "Plus Jakarta Sans", sans-serif;
  font-weight: 700;
  font-size: 1.05rem;
  color: #6c2e1f; /* Theme maroon link color */
  transition: color 0.2s ease;
}
.term-list a:hover {
  color: #4d2015;
  text-decoration: none;
}
.term-list em {
  display: block;
  font-family: "Lora", serif;
  font-style: italic;
  font-size: 0.88rem;
  color: #666666;
  margin-top: 0.25rem;
}
</style>
