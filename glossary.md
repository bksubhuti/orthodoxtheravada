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
        </div>
      {% endif %}
      <h2 id="{{ first_letter }}">{{ first_letter }}</h2>
      <div class="ot-index-grid">
      {% assign current_letter = first_letter %}
    {% endif %}
    
    <a href="{{ term.url | relative_url }}" class="ot-index-card">
      <strong class="ot-index-card__title">{{ term.title }}</strong>
      {% if term.pali_spelling %}
        <span class="ot-index-card__subtitle">({{ term.pali_spelling }})</span>
      {% endif %}
    </a>
  {% endfor %}
  
  {% if current_letter != "" %}
    </div>
  {% endif %}
</div>
