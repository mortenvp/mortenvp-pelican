Title: Creating slides using the iPython notebook
Date: 2015-03-03 12:43

This semester I'm teaching a free study activity called C++11/14 basic
introduction and as an experiment I decided to try to create my slides
using an iPython notebook.

Turns out this works pretty well, and

## Hosting the slides

Since the slides are basically a html website with some javascript we can
easily make the slides available for online viewing.

For the slides to work properly we also have to host the
[reveal.js](https://github.com/hakimel/reveal.js) javascript library. To
ensure that it will work as expected you should use the same version of
reveal.js as the iPython However, this did not work straight out of the box
so here is a small tip.

```
ipython nbconvert --to slides lecture1.ipynb --post serve --log-level=INFO
```

This will generate some output and show where the in-built webserver
forwards requests to the reveal.js library:

```
[NbConvertApp] Redirecting reveal.js requests to https://cdn.jsdelivr.net/reveal.js/2.5.0
```

So if we want to use the same version of reveal.js we should use version 2.5.0.
