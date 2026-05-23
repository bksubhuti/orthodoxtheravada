---
title: "Forum"
permalink: /forum/
layout: single
lang: en
description: "Discuss Orthodox Theravāda Buddhism at the Classical Theravāda forum."
excerpt: "Join the Classical Theravāda discussion forum to ask questions and connect with others on the path."
keywords: ["Orthodox Theravāda", "discussion", "forum", "Classical Theravāda", "questions", "Dhamma study"]
---

### The Classical Theravāda Forum

<div style="text-align: center; margin: 2rem 0;">
  <a href="https://classicaltheravada.org" target="_blank" rel="noopener">
    <img src="https://classicaltheravada.org/uploads/default/optimized/2X/9/9c7021f8b586822eec097369a13b4dbb4e0c1598_2_180x180.png" alt="Classical Theravāda Logo" style="max-width: 300px; height: auto;" />
  </a>
</div>

**[ClassicalTheravada.org](https://classicaltheravada.org)** is the dedicated community forum for discussing these teachings openly. Whether you are a beginner with basic questions or an experienced practitioner, this is the place to ask, discuss, and connect with others on the path.

Topics covered include:
- Dhamma study and understanding
- Abhidhamma and Paramattha Dhammas
- Vinaya questions
- Meditation in the context of the Pāḷi Canon
- Book discussions and recommended readings

<div style="text-align: center; margin: 2.5rem 0;">
  <a href="https://classicaltheravada.org" target="_blank" rel="noopener" class="btn btn--primary btn--large" id="join-forum-btn" style="font-size: 1.2rem; padding: 1rem 2.5rem;">
    Join the Discussion Forum →
  </a>
</div>

---

### Recent Discussions

Here are the latest discussions from the forum.

<div id="discourse-posts" class="ot-article-list">
  {% for post in site.data.forum_posts %}
  <a href="{{ post.url }}" target="_blank" class="ot-article-card">
    <img src="https://classicaltheravada.org/uploads/default/optimized/2X/9/9c7021f8b586822eec097369a13b4dbb4e0c1598_2_180x180.png" alt="Forum Icon" class="ot-article-card__thumb" style="background-color: #faf8f5; object-fit: contain;">
    <div class="ot-article-card__body">
      <div class="ot-article-card__title">{{ post.title }}</div>
      <div class="ot-article-card__meta">
        Last activity: {{ post.date }}
      </div>
    </div>
  </a>
  {% endfor %}
</div>

<script>
document.addEventListener("DOMContentLoaded", function() {
  const discourseUrl = "https://classicaltheravada.org";
  const container = document.getElementById("discourse-posts");
  const iconUrl = "https://classicaltheravada.org/uploads/default/optimized/2X/9/9c7021f8b586822eec097369a13b4dbb4e0c1598_2_180x180.png";

  fetch(discourseUrl + "/latest.json")
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.json();
    })
    .then(data => {
      const topics = data.topic_list.topics;
      if (!topics || topics.length === 0) {
        return;
      }

      let html = '';
      topics.slice(0, 10).forEach(topic => {
        const date = new Date(topic.last_posted_at).toLocaleDateString();
        html += `
          <a href="${discourseUrl}/t/${topic.slug}/${topic.id}" target="_blank" class="ot-article-card">
            <img src="${iconUrl}" alt="Forum Icon" class="ot-article-card__thumb" style="background-color: #faf8f5; object-fit: contain;">
            <div class="ot-article-card__body">
              <div class="ot-article-card__title">${topic.title}</div>
              <div class="ot-article-card__meta">
                Replies: ${topic.posts_count - 1} | Last activity: ${date}
              </div>
            </div>
          </a>
        `;
      });
      container.innerHTML = html;
    })
    .catch(error => {
      console.log('Live fetch failed, showing static fallback.', error);
    });
});
</script>