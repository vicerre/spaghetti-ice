---
tags:
  - banner art
  - cherry blossoms
  - sakura
  - solana
  - vicerre
---

# Illustration 054 – Cherry Blossoms (2024-05-04 – 2024-05-05)

<img src="assets/2024-05-04_image-156.png">

## Overview

On 2024-02-12, I played with Google Gemini. By this stage of AI development, some models were multimodal. In other words, a model wouldn't necessarily be limited to text-to-text or text-to-image generation, but rather, they could operate on multiple types of content.

Google Gemini could read the contents of a URL and generate images. I was curious how well it functioned, so as a test, I asked the model to generate a hypothetical webcomic cover for the contents of my universe.

Three of the four images generated were rather schlocky epic fantasy-style book covers. The last one, however, caught my attention. The last image depicted two characters, one brunet and one red-haired, sitting underneath a cherry blossom tree.

[Originally, I penned this installment of my universe "Cherry Ice" using the cherry fruit as a theme.](../2022-h2/2022-10-17_meta-007_naming-conventions.md) While thematically relevant, I considered the trope of cherry blossoms a bonus theme. Having seen this generation, however, I felt inspired.

A few months later, Kiwi and Yu IOTJ on Discord told me how they were inspired by the romance writing of my universe. This feedback, in turn, inspired me to draw a romantic scene. Turning to the image that inspired me before, I drew the image depicted in this post.

## Overview – Image Description

- The scene takes place atop a grassy field.
- The grassy field is an island floating in the skies of New Quendon.
- Solana and Vic are sitting underneath a cherry blossom tree.
- Solana is looking up at windswept cherry blossom petals.
- Vic is looking at Solana.
- The image is captured from a bird's eye view.

## Design notes

- Several elements in my characters' designs were omitted for compositional purposes. These include Solana's armbands, shoes, and tail, as well as Vic's outerwear.
- Due to the wide composition of this piece, I applied several techniques to help it stand out:
  - The composition uses exaggerated perspective. To account for this, I incorporated depth of field into the elements in the image. For instance, the cherry blossoms closest to the camera are airbrushed to make them look out of focus.
  - Due to the image's wide field of view, image elements become decreasingly detailed the farther away from the image's focal point. Most visibly, the field of grass becomes more and more abstract the farther it spans from Solana and Vic.
  - To create a sense of movement, I used a soft airbrush to give the windswept cherry blossom petals the effect of motion blur.
- To enrich the image's color balance, I incorporated subsurface scattering on the cherry blossom petals to give them a glowing effect.

## Resources used

- Brushes used:
  - Oils & Acrylics > Round > Liner (outlines)
  - Oils & Acrylics > Round > Round Soft (colors)
  - Airbrushes > Spray (glow)
- [How can I fix the flower looking like plastic?](https://www.reddit.com/comments/1c9q2vh/)
- Image generations:
  - [Google Gemini](assets/2024-02-12_image-145.jpg)
  - [Counterfeit-V3.0](assets/2024-01-12_image-141.png)
  - [Pony Diffusion XL](assets/2024-05-04_image-157.png)
- [Yoshino cherry ソメイヨシノ 3](https://commons.wikimedia.org/wiki/File:Yoshino_cherry_%E3%82%BD%E3%83%A1%E3%82%A4%E3%83%A8%E3%82%B7%E3%83%8E_3.jpg)

## Workflow (Google Gemini)

Prompt:

> Generate some images of a potential webcomic cover for _Cherry Ice_, the third installment of _Spaghetti Ice_. Focus on the genre/description/theme/tone of the work. Don't reference anything from the _Spaghetti Ice_ installment.
>
> Information about Cherry Ice can be seen at the bottom of the following page.
>
> https://tvtropes.org/pmwiki/pmwiki.php/WebOriginal/SpaghettiIce

## Workflow (Counterfeit-V3.0, txt2img)

- Positive prompt: `masterpiece, armin_vicerre, panoramic shot, tilt shift, looking at viewer`
- Negative prompt: `nsfw, worst quality, low quality, text, signature, watermark, username, blurry, artist name, angry, head shot, profile shot`
- Steps: 20
- Sampler: DDIM
- CFG scale: 8.0
- Seed: 919776591462956
- Size: 912x512

## Workflow (Counterfeit-V3.0, latent upscale)

- Positive prompt: `masterpiece, armin_vicerre, panoramic shot, 5-point perspective, (skyscrapers: 1.2), looking at viewer`
- Negative prompt: `nsfw, worst quality, low quality, text, signature, watermark, username, blurry, artist name, angry, head shot, profile shot`
- Steps: 10
- Sampler: dpmpp_sde_gpu
- CFG scale: 8.0
- Seed: 104857099533157
- Upscale latent by: 2.00
- Denoising strength:

## Workflow (Pony Diffusion XL)

- Positive prompt: `score_9, score_8_up, score_7_up, score_6_up, score_5_up, score_4_up, source_anime, rating_safe, armin_vicerre sitting underneath a cherry tree, landscape, grass, floating landmass, golden hour, bird's eye view, banner art`
- Negative prompt: `(worst quality, low quality: 1.4), source_cartoon, source_furry, source_pony`
- Steps: 25
- Sampler: DDIM
- CFG Scale: 8.0
- Seed: 911866990028821
- Size: 1536x640

## WIPs

- [1](https://cdn.discordapp.com/attachments/1211633304856428544/1236437329376444456/image.png)
- [2](https://cdn.discordapp.com/attachments/1211633304856428544/1236835563072651345/tmp4.png)
