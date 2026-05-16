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
  border-bottom: 2px solid #f2f2f2;
  margin-top: 2em;
  padding-bottom: 0.5em;
  color: #333;
}
.term-list {
  list-style: none;
  padding-left: 0;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 10px;
}
.term-list li {
  margin-bottom: 5px;
}
</style>
