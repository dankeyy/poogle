# poogle
Jump to Python docs, 90% of the time works everytime.\
![poogle](https://user-images.githubusercontent.com/74069206/188282802-403eece1-96c5-4177-ae69-94e124dfcce2.gif)

For both CLI and Emacs users- I recommend putting the script in something like `~/.local/bin` (assuming it's on your path).\
For Emacs users- put the `.el` file somewhere in your load path and just load/ require it in your config. You could also just paste the function itself in it, it's short (just wraps around the snek script).

CLI usage:
```sh
./poogle -h
usage: poogle [-h] lookup

Jump to docs. 
Enter <function/module/whatever>.<method> (e.g `str.split`) 
or <function/module> (e.g. `getattr`). 
To look up a term, prefix term as the module- term.<some-python-jargon>, (e.g. `term.garbage-collection`)

positional arguments:
  lookup

options:
  -h, --help  show this help message and exit

```
