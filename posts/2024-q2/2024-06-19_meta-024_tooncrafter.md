---
humorous:
  - Superwholock-era Tumblr GIFs
tags:
  - ai art
  - animation
  - vicerre
---

# Meta 024 – ToonCrafter (2024-06-18)

<img src="assets/2024-06-18_image-177.gif">

## Overview

We've seen a boom in generative AI technologies in the past few years. From text generation models like Character.AI and NovelAI to image generation models like DALL·E, Midjourney, and Stable Diffusion, to the nascent video generation models of Pika and Sora, diffusion-based models have become a boon for producing creative content.

Ever since these models became mainstream, I've looked forward to one use case in particular: frame interpolation.

When creating traditional animation, you need to interpolate animation keyframes. Compared to the process of storyboarding, drawing in-between frames is tedious and time-consuming. This is an area in which technology can supplement existing creativity.

When I found out on 2024-05-30 about [ToonCrafter](https://www.reddit.com/comments/1d470rv/) ([and its predecessor family of models](https://github.com/Doubiiu/DynamiCrafter#-crafter-family)), I became glad; diffusion-based image interpolation was the use case I was looking forward to, and technology has advanced to the point it was feasible to run on consumer hardware.

The animation you see in this post depicts my initial trial of ToonCrafter, where I drew two frames of Vic and asked the model to interpolate the rest. To give the model an ample chance of success, I kept the difference between frames minimal, with only his hair and scarf changing between frames. The end product is a one-second animation of Vic with his hair and scarf billowing in the wind.

## Workflow

ComfyUI custom node: [ComfyUI-DynamiCrafterWrapper](https://github.com/kijai/ComfyUI-DynamiCrafterWrapper)

- Positive prompt: `man with billowing hair and scarf`
- Negative prompt:
- Steps: 20
- ETA: 1.0 ([= DDPM](https://github.com/ermongroup/ddim))
- CFG scale: 7.0
- Seed: 307304882870607
- Size: 512x320
- Frames: 16
- FPS: 10 ([ = Frame Per Second Conditioning](https://www.reddit.com/comments/1dhvb05/comment/l90fauk/))
