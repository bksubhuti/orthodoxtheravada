---
title: "Articles"
layout: single
permalink: /articles/
---

Welcome to the articles section of Orthodox Theravāda.

<div class="ot-article-list">
  {% for post in site.articles %}
  <a href="{{ post.url | relative_url }}" class="ot-article-card">
    {% if post.featured_image %}
      <img src="{{ post.featured_image | relative_url }}" alt="{{ post.title }}" class="ot-article-card__thumb">
    {% else %}
      <img src="/images/Orthodox_theravada_logo_trans.png" alt="Default Icon" class="ot-article-card__thumb">
    {% endif %}
    <div class="ot-article-card__body">
      <h3 class="ot-article-card__title">{{ post.title }}</h3>
      <div class="ot-article-card__meta">
        Published: {{ post.date | date: "%B %d, %Y" }}
      </div>
    </div>
  </a>
  {% endfor %}
</div>
