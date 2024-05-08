# DJPress docs

## Overview

DJPress is insprired by the old, "classic" WordPress sites.

DJPress can power all the CMS requirements of a website, or can be used to add a blog to an existing website.

Posts are what powers the blog.

Pages can be used for static content.

## URL Structure

Pages have a simple URL - they are at the root of the djpress app, and just have a slug. (although, I still need to think through whether I support multiple layers, e.g. `/about`, `/about/team`, `/about/me`

Posts are more complicated...

 - They can have a prefix - i.e. the entire blog part of djpress can be prefixed into its own section, eg. `/blog/...`.
 - Categories - returns a list of blog posts with a specific category and are prefixed with a configurable word which is `category` by default, e.g. `/category/dev`, `/category/general`, `/category/general`.
 - Authors - returns a list of blog posts for a specific author. This is prefixed with a configuraable word which is `author` by default, e.g. `/author/stuart`, `/author/chris`.
 - Archives - returns a list of blog posts for a particular date. This is prefixed with a configurable word which is `archives` by default, e.g. `/archives/2024`, `/archives/01`, `/archives/2024/01/14`.
 - Single posts - each post has a slug which is its unique identifier, but users can also include dates in the path, e.g. `/my-test-post`, `/2024/my-test-post`, `/2024/01/my-test-post`, `/2024/01/14/my-test-post`.

### URL Parser for single posts:

```
"(
  ^(
    \/(?P<prefix>blog)
  )?
  (
    (
      \/(?P<year>[0-9]{4})
    )
    (
      (
        \/(?P<month>[0][1-9]|[1][0-2])
      )
      (
        \/(?P<day>[012][0-9]|3[01])
      )?
    )?
  )?
  (
    \/(?P<slug>[a-zA-Z0-9_-]+)$
  )
)"mgx
```
