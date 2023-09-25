# rc text export

## description

This is a python tool that can load a page in the RC and turn the text part into a word document

## Requirements

- BeautifulSoup
- requests

Optional, to speed things up:
<https://thehftguy.com/2020/07/28/making-beautifulsoup-parsing-10-times-faster/>
- lxml 
- cchardet

If you don't want to go through the trouble of installing lxml and cchardet,
you have to switch 
```python soup = BeautifulSoup(response.text, 'lxml')```

to

```python soup = BeautifulSoup(html_doc, 'html.parser')```



