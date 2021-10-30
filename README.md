# hexo2hugo
migrate hexo's posts to hugo

Now only support toml metadata:

```toml
---
title: xxx

tags(catergories): xx
-> 
tags(catergories):
- xx

mathjax -> *any custom name*
---
```