import re
from collections import Counter
from typing import Dict, Iterator

import calplot
import click
import enum
import matplotlib.pyplot
import pandas as pd
import pysbd
import sklearn.feature_extraction.text
import yaml
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer

from data_analytics.posts import load_posts
from data_analytics.title import DATE_FORMAT

STOP_WORDS = list(sklearn.feature_extraction.text.ENGLISH_STOP_WORDS)


@click.group()
@click.pass_context
def cli(ctx: click.Context):
    ctx.ensure_object(dict)

    posts = load_posts()
    ctx.obj["posts"] = posts


@cli.command
@click.pass_context
def calendar_plot(ctx: click.Context):
    """
    Sources:
      - https://matplotlib.org/stable/users/explain/colors/colormaps.html
      - https://python-charts.com/evolution/calendar-heatmap-matplotlib/
    """

    # Create an ordinal scale based on post type.
    posts = sorted(
        [post for post in ctx.obj["posts"] if not post.external], key=lambda p: p.date
    )
    PostType = enum.Enum("PostType", sorted(set(post.type for post in posts)))

    datestr_weights: Dict[str, int] = {}

    for post in posts:
        datestr = post.date.strftime(DATE_FORMAT)
        weight = PostType[post.type].value
        datestr_weights[datestr] = weight

    drange = pd.date_range(posts[0].date, posts[-1].date, freq="D")
    weights = drange.map(lambda d: datestr_weights.get(d.strftime(DATE_FORMAT), 0))

    series = pd.Series(weights, index=drange)

    calplot.calplot(
        series,
        cmap="tab10",
        colorbar=False,
        vmax=max(e.value for e in PostType),
        vmin=0.0,
    )
    matplotlib.pyplot.show()


@cli.command
@click.pass_context
def idf(ctx: click.Context):
    """
    Sources:
      - https://www.capitalone.com/tech/machine-learning/understanding-tf-idf/
      - https://stackoverflow.com/questions/48431173/
    """
    texts = [post.text for post in ctx.obj["posts"] if not post.encrypted]

    # Perform IDF (TF doesn't matter)
    vectorizer = TfidfVectorizer(stop_words=STOP_WORDS)
    vectorizer.fit_transform(texts)

    weighted = []

    for term, col in vectorizer.vocabulary_.items():
        idf_ = vectorizer.idf_[col]
        weighted.append([term, idf_])

    sorted_weighted = sorted(weighted, key=lambda d: (d[1], d[0]))

    for term, idf_ in sorted_weighted:
        print(term, idf_)


@cli.command()
@click.pass_context
def phrase_frequency(ctx: click.Context):
    """
    Sources:
      - https://stackoverflow.com/questions/11763613/
    """

    texts = [post.text for post in ctx.obj["posts"] if not post.encrypted]

    vectorizer = CountVectorizer(ngram_range=(3, 6), stop_words=STOP_WORDS)
    ngrams = vectorizer.fit_transform(texts)

    freqs = ngrams.toarray().sum(axis=0)

    term_freqs = []

    for term, col in vectorizer.vocabulary_.items():
        freq = freqs[col]
        term_freqs.append([term, freq])

    sorted_weighted = sorted(term_freqs, key=lambda d: (-d[1], -len(d[0]), d[0]))

    seens = set()

    for term, freq in sorted_weighted:
        if freq == 1:
            continue
        # Only print result if it is not a subset of a more frequent result.
        if any(term in seen for seen in seens):
            continue

        seens.add(term)
        print(term, freq)


@cli.command()
@click.pass_context
def sentence_frequency(ctx: click.Context):
    """
    Sources:
      - https://stackoverflow.com/questions/4576077/
    """
    texts = [post.text for post in ctx.obj["posts"] if not post.encrypted]

    segmenter = pysbd.Segmenter()

    counter: Counter[str] = Counter()

    for text in texts:
        for sentence in segmenter.segment(text):
            stripped = sentence.strip()
            counter[stripped] += 1

    for term, freq in counter.most_common():
        print(term, freq)


@cli.command()
@click.pass_context
def tag_frequency(ctx: click.Context):
    contents = [post.content for post in ctx.obj["posts"] if not post.encrypted]

    counter: Counter[str] = Counter()

    for content in contents:
        match = re.search(r"---\n(.*?)\n---", content, flags=re.DOTALL)
        if match:
            captured = match.group(1).strip()
            items: Iterator[Dict] = yaml.safe_load_all(captured)
            for item in items:
                for _, tags in item.items():
                    for tag in tags:
                        counter[tag] += 1
        else:
            raise ValueError(f"Could not find tags in {content}.")

    for term, freq in counter.most_common():
        print(term, freq)


@cli.command()
@click.pass_context
def word_frequency(ctx: click.Context):
    """
    Sources:
      - https://stackoverflow.com/questions/27488446/
      - https://stackoverflow.com/questions/67881662/
    """
    texts = [post.text for post in ctx.obj["posts"] if not post.encrypted]

    # Get term counts per document
    vectorizer = CountVectorizer(stop_words=STOP_WORDS)
    counts = vectorizer.fit_transform(texts)

    tokens = vectorizer.get_feature_names_out()
    freqs = counts.sum(axis=0).tolist()[0]

    counter: Counter[str] = Counter(dict(zip(tokens, freqs)))
    for term, freq in counter.most_common():
        print(term, freq)


if __name__ == "__main__":
    cli(obj={})
