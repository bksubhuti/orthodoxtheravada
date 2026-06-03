---
layout: single
title: "Pāḷi Glossary"
permalink: /glossary/
author_profile: false
---

Here you will find detailed definitions and textual references for key Pāḷi terms and doctrinal concepts.
Note: We are actively reviewing our 300 entries. Definitions marked with "Verified" inside the entry have been checked against the Pāli canon and often have quoted material to support the term given.

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
    
    {% assign stripped_content = term.content | strip_html | strip %}
    {% assign first_word = stripped_content | truncatewords: 1, "" %}
    <a href="{{ term.url | relative_url }}" class="ot-index-card">
      <strong class="ot-index-card__title">{{ term.title }}{% if first_word == "Verified" %} ✔️{% endif %}</strong>
      {% if term.pali_spelling %}
        <span class="ot-index-card__subtitle">({{ term.pali_spelling }})</span>
      {% endif %}
    </a>
  {% endfor %}
  
  {% if current_letter != "" %}
    </div>
  {% endif %}
</div>
