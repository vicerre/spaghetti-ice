---
humorous:
  - tom scott
tags:
  - meme
---

# Meta 015 – Internet Archaeology

[In my previous post,](2023-12-21_rendition-045_hairstyle-meme.md) I shared a blank meme template passed around a friend group of mine. In citing the template, I had to perform substantial internet archaeology to reach that point. Considering the level of effort I had to go through to find the original template, I felt I should document my findings.

---

The first step I took was to find a reference to the empty meme template. The original empty meme template was unsourced, so I took to Google.

If you search for "hairstyle meme" on Google, you'll receive plenty of results. Hairstyles and memes aren't the most uncommon combination of ideas, after all. Finding the exact iteration of the meme was essential to citing it correctly.

Luckily, Google provided a lead immediately. [Hiba-tan's "Hairstyle meme" post on DeviantArt](https://www.deviantart.com/hiba-tan/art/Hairstyle-meme-559431302) uses the same template and provides a link to the empty template.

Naturally, [the link led to a dead page;](https://www.deviantart.com/lynniica/art/Hairstyle-Meme-181892402) since Hiba-tan shared her image, the original post had been deleted. I checked Bing, Google, and Yandex, as well as the Wayback Machine, but none of them saved a cached version of the page. If I wanted to find the original template, I would need to investigate further.

The broken link was essential here. Despite it leading to an empty page, there was still useful information to be gleaned. In particular, I could see the meme template was posted by a user named Lynniica, and the image had a Deviation ID of `181892402`.

---

This is a good time to talk about DeviantArt's URL structure.

As of this post, DeviantArt post URLs use the following template:

```
https://www.deviantart.com/<username>/art/<slug>-<deviation_id>
```

This was not always the case.

On 2018-01-27, [DeviantArt switched from using subdomains to HTML paths for usernames](https://www.deviantart.com/danlev/journal/New-Profile-URLs-751783111). This meant that all content once archived under `<username>.deviantart.com` would be redirected to `deviantart.com/<username>`. When searching for DeviantArt URLs prior to this date, you would need to account for this level of indirection.

In addition, there is a second major factor that compounds DeviantArt image source lookup: username changes.

Users on DeviantArt can switch usernames. Any links that pointed to the old username would automatically redirect to the new one. Redirects from old usernames to new usernames were plentiful, but tracing through a user's new username to one of old presented a headache.

I suspected the reason why Lynniica's meme template did not appear in any caches was due to username changes. As it turns out, this was the case. After a bit of searching, I found [a profile comment](https://www.deviantart.com/comments/4/10293809/2698828357) linking to a post for Lynniica. [In this post,](https://www.deviantart.com/shane-zero/art/gift-for-akizakura7000-death-the-kidd-321538430), Lynniica's username is provided as akizakura7000. Navigating to `deviantart.com/akizakura7000` brings me to Lynnniica's page, confirming the connection.

---

With this knowledge in mind, we know where to look. [If we search the Wayback Machine for URLs archived under `akizakura7000.deviantart.com`](https://web.archive.org/web/*/akizakura7000.deviantart.com*), we can see a reference to a page at `art/Hairstyle-Meme-181892402`. The Deviation ID matches, confirming this is the original post. From here, we can cite this meme template properly.

Aside: It is also here I discovered Lynniica had changed usernames more than once. The captured URL under the username `akizakura7000` actually redirects to the username `Jesslicious-Arts`. From here, we can see the creator of the meme template changed their username to [pastel-vamp on Tumblr](https://www.tumblr.com/jesslicious-arts), which, [after following the Wayback Machine,](https://web.archive.org/web/20201030053932/https://pastel-vamp.tumblr.com/) leads to a NSFW Twitter account of the same name.

<!--

---

My conclusion to this post is one on history.

The internet, as information-laden as it can be, often seems like a modern-day Library of Alexandria. Yet, like the Library of Alexandria, the contents within are under threat of being lost. Significant events can be shared and saved in perpetuity, but less-prolific content can be lost entirely—or, at best, preserved in brief snapshots, bereft of essential context.

When you post on the internet, it can be tempting to move or delete old content—it might be out of date, irrelevant, and no longer seen. Maybe your content no longer represents your online identity. In doing so, however, you confound future historians of your legacy.

When creating something, think about the history you're creating. Even if you don't find value in one of your creations now, it might have inspired someone, and, with time, that person might want to share it again. And then, one day, you might end up in a blog post about how a meme you made thirteen years ago made this person's evening.
-->
