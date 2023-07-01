---
tags:
  - vicerre
---

# Illustration 067 – Clip Studio Paint

<img src="assets/2023-07-28_image-079.png">

## Overview

I recently wanted to draw gift art for a friend of mine. In doing so, I desired perspective lines. Unfortunately, Adobe Photoshop lacks built-in means of drawing perspective guidelines. If I wanted to use Adobe Photoshop, I would need a makeshift solution.

When searching for alternate solutions, I saw a recommendation for Clip Studio Paint. Now, I am aware of the popularity of Clip Studio Paint; it is used commonly by talented artists on Pixiv, Tumblr, and Webtoon.

As I was frustrated with Adobe Photoshop's limitations, I decided to try out the program.

To practice drawing in Clip Studio Paint, I drew Vic, my standard subject. The image presented here represents one of these practice drawings.

## Design notes

While drawing in Clip Studio Paint, I noted how this program differed from Adobe Photoshop. These differences are listed below:

Pros:

- The UI and keyboard shortcuts translate well from Adobe Photoshop. A person familiar with Adobe Photoshop's workflow will adapt easily to Clip Studio Paint, given minor adjustments.
- Tools such as brush size and stroke width use floating-point precision instead of integer precision. This allows for finer control over images.
- The Auto Select tool is more intelligent than that of Photoshop. Whereas the Magic Wand tool in Photoshop relies on exact tolerances, the Auto Select Tool in Clip Studio Paint can select regions that are not perfectly connected.
- Layer Masks are more intuitive compared to Photoshop. In Photoshop, I always found it odd how applying a layer mask meant drawing in the parts to be erased. In contrast, using the Clip Studio Model, you erase the part of the image that should be erased.
- The Mesh Transform tool can be used on multiple layers. In contrast, Photoshop only allows the Warp tool to be used over a single image.

Cons:

- Layer Property > Border Effect: This tool lacks fine-grain control over falloff shape. If I want to apply an inner glow layer effect (which uses a quadratic falloff), I need alternate means. This is suboptimal, as I would prefer a layer effect that automatically updates as I make changes.
- Clip Studio Paint lacks a History Snapshot tool. If I need to restore an image to a "last good" state, I need to use workarounds, such as reverting to my previous save file or creating another layer. Anyone familiar with version control tooling can sympathize with the lack of ability to revert to a last good save.
- Clip Studio Paint lacks a robust library of image interpolation methods. My favorite image interpolation method when transforming selections is Bicubic Sharper, which preserves clarity when scaling up. Clip Studio Paint lacks an algorithm that suits my needs.
- Clip Studio Paint lacks robust support for non-destructive filters. In Photoshop, I can convert raster layers to Smart Layers, then apply any number of filters to them non-destructively. I cannot perform the same sequence of events in Clip Studio Paint.
- The mesh transform tool lacks the sophistication of Photoshop's.
- Clip Studio Paint lacks a convenient method of drawing horizontal and vertical lines with dynamic pressure. In Photoshop, I can simply hold the Shift key when drawing a stroke to lock it to a horizontal or vertical path. There is no equivalent in Clip Studio Paint, and [the closest workaround](https://www.reddit.com/xpdm9w) is clunky at best.

## Bonus – Solana Drawing

<img src="assets/2023-07-30_image-080.png">
