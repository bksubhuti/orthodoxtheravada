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

<div id="discourse-posts">
  <ul>
    {% for post in site.data.forum_posts %}
    <li>
      <a href="{{ post.url }}" target="_blank">{{ post.title }}</a>
      <div class="meta">
        Last activity: {{ post.date }}
      </div>
    </li>
    {% endfor %}
  </ul>
</div>

<style>
#discourse-posts ul {
  list-style-type: none;
  padding-left: 0;
}
#discourse-posts li {
  margin-bottom: 1.2rem;
  border-bottom: 1px solid #eee;
  padding-bottom: 0.8rem;
}
#discourse-posts a {
  font-weight: bold;
  font-size: 1.1rem;
  text-decoration: none;
  color: #2a7ae2;
}
#discourse-posts a:hover {
  text-decoration: underline;
}
#discourse-posts .meta {
  color: #777;
  font-size: 0.9rem;
  margin-top: 0.2rem;
}
</style>

<script>
document.addEventListener("DOMContentLoaded", function() {
  const discourseUrl = "https://classicaltheravada.org";
  const container = document.getElementById("discourse-posts");

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

      let html = '<ul>';
      topics.slice(0, 10).forEach(topic => {
        const date = new Date(topic.last_posted_at).toLocaleDateString();
        html += `
          <li>
            <a href="${discourseUrl}/t/${topic.slug}/${topic.id}" target="_blank">${topic.title}</a>
            <div class="meta">
              Replies: ${topic.posts_count - 1} | Last activity: ${date} (Live)
            </div>
          </li>
        `;
      });
      html += '</ul>';
      container.innerHTML = html;
    })
    .catch(error => {
      console.log('Live fetch failed, showing static fallback.', error);
    });
});
</script>
