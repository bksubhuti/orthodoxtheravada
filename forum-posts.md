---
title: "Recent Discussions"
permalink: /forum-posts/
layout: single
---

Here are the latest discussions from the [Classical Theravada Forum](https://classicaltheravada.org).

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
// We keep the script to try and fetch live updates.
// If it succeeds, it will replace the static list above.
// If it fails (due to CORS or network), the static list remains!
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
        return; // Keep static content if no topics
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
      console.log('Live fetch failed (likely CORS), showing static fallback.', error);
      // Do nothing, static list is already there.
    });
});
</script>

