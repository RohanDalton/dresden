[![RohanDalton](https://circleci.com/gh/RohanDalton/dresden.svg?style=shield)](https://circleci.com/gh/RohanDalton/dresden)

# Dresden

Dresden is a Python library for profiling your code.

## Why?
There are already a bunch of Python profilers out there, why write another one?
The short answer is that I'm lazy, and stupid. 

If I want to profile my code using say `cProfile` I have to run some command line function.
But because I don't profile code very often, I don't remember what that is. 
So I have to look it up. 

Then once I've looked that up, and profiled my code, I have an output that's hard to read. 
To make sense of it, I want to create some kind of visualization. 
Personally I like to `gprof2dot` for that, but `snakeviz` is also good.
Either way though, I need to run some other obscure command in my terminal.

And what if I don't want to profile my whole program, but just a small part of it?
Technically profiling the whole program will profile just the part that I want to profile, but sometimes that can make the output harder to interpret.
Especially if the code that I want to profile makes calls to functions that are also called extensively from parts of the program that I dont't want to profile.

Or what if running my program from the command line is hard for some reason?

Or I want to actually profile the code when it runs in production on some server, because it's slower in production than it is in local testing?

The things that *I* want from my profiler are:
* *Easy to use* I don't want to have to remember anything. 
I want my visualizations to appear like magic.
* *Precise* I want to be able to profile very specific pieces of code.


## Usage
Dresden can be used in two ways: as a decorator, or as a context manager.

```python
from dresden import Harry

@Harry
def some_func():
    ...
```

Or

```python
with Harry():
    some_func()
```

You can also view your profile results using [snakeviz](https://jiffyclub.github.io/snakeviz) if you have it installed in your environment.

```bash
python cli.py
```

