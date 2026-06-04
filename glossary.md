---
layout: single
title: "Pāḷi Glossary"
permalink: /glossary/
author_profile: false
---

{% assign verified_count = 0 %}
{% for term in site.terms %}
  {% assign stripped_content = term.content | strip_html | strip %}
  {% assign check_start = stripped_content | truncate: 10, "" %}
  {% if check_start contains "Verified" %}
    {% assign verified_count = verified_count | plus: 1 %}
  {% endif %}
{% endfor %}

 **{{ verified_count }} out of {{ site.terms.size }}** are verified. Verified entries are marked.

<div class="glossary-index">
  {% assign sorted_terms = site.terms | sort: "title" %}

  {% comment %}--- Build unique letter list for jump-bar ---{% endcomment %}
  {% assign all_letters = "" %}
  {% for term in sorted_terms %}
    {% capture fl %}{{ term.title | truncate: 1, "" | upcase }}{% endcapture %}
    {% unless all_letters contains fl %}
      {% if all_letters == "" %}
        {% assign all_letters = fl %}
      {% else %}
        {% assign all_letters = all_letters | append: "," | append: fl %}
      {% endif %}
    {% endunless %}
  {% endfor %}
  {% assign letter_array = all_letters | split: "," %}

  <nav class="glossary-letter-bar" aria-label="Jump to letter">
    {% for letter in letter_array %}
      <a href="#{{ letter }}" class="glossary-letter-link">{{ letter }}</a>
    {% endfor %}
  </nav>

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
    {% assign check_start = stripped_content | truncate: 10, "" %}
    <a href="{{ term.url | relative_url }}" class="ot-index-card">
      <strong class="ot-index-card__title">{{ term.title }}{% if check_start contains "Verified" %} ✔️{% endif %}</strong>
      {% if term.pali_spelling %}
        <span class="ot-index-card__subtitle">({{ term.pali_spelling }})</span>
      {% endif %}
    </a>
  {% endfor %}
  
  {% if current_letter != "" %}
    </div>
  {% endif %}
</div>
