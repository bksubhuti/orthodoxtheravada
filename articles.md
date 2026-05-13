---
title: "Articles"
layout: single
permalink: /articles/
---

Welcome to the articles section of Orthodox Theravāda.

<div class="articles-list">
  <ul>
    {% for post in site.articles %}
    <li>
      {% if post.featured_image %}
        <img src="{{ post.featured_image | relative_url }}" alt="{{ post.title }}" class="article-thumb">
      {% else %}
        <img src="/images/logo.png" alt="Default Icon" class="article-thumb">
      {% endif %}
      <div class="article-content">
        <a href="{{ post.url | relative_url }}">{{ post.title }}</a>
        <div class="meta">
          Published: {{ post.date | date: "%B %d, %Y" }}
        </div>
      </div>
    </li>
    {% endfor %}
  </ul>
</div>

<style>
.articles-list ul {
  list-style-type: none;
  padding-left: 0;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
.articles-list li {
  display: flex;
  align-items: center;
  background-color: #ffffff;
  border: 1px solid #eaeaea;
  border-radius: 8px;
  padding: 1rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.articles-list li:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}
.article-thumb {
  width: 64px;
  height: 64px;
  border-radius: 8px;
  margin-right: 1.2rem;
  object-fit: cover;
  flex-shrink: 0;
  background-color: #f9f9f9;
  padding: 4px;
  border: 1px solid #eee;
}
.article-content {
  display: flex;
  flex-direction: column;
}
.articles-list a {
  font-weight: bold;
  font-size: 1.1rem;
  text-decoration: none;
  color: #2a7ae2;
  margin-bottom: 0.3rem;
  line-height: 1.3;
}
.articles-list a:hover {
  text-decoration: underline;
}
.articles-list .meta {
  color: #777;
  font-size: 0.9rem;
}
</style>
