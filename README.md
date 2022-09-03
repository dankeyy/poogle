# poogle
Smol script to help you jump to python docs, 90% of the time works everytime. 
![poogle](https://user-images.githubusercontent.com/74069206/188282802-403eece1-96c5-4177-ae69-94e124dfcce2.gif)

I recommend putting the script in something like `~/.local/bin`, and the .el file somewhere in your load path. then just loading it in your config (or just putting the function in the config itself it's very short). 

Also useable from the command line.
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
