==========================
Frequently Asked Questions
==========================

Why the name jug?
-----------------

The cluster I was using when I first started developing jug was called
"juggernaut". That is too long and there is a Unix tradition of 3-character
programme names, so I abbreviated it to jug.

It doesn't work with random input!
----------------------------------

Normally the problem boils down to the following::

    from jug import Task
    from random import random

    def f(x):
        return x*2

    result = Task(f, random())

Now, if you check ``jug status``, you will see that you have one task, an ``f``
task. If you run ``jug execute``, jug will execute your one task. But, now, if
you check ``jug status`` again, there is still one task that needs to be run!

While this may be surprising, it is actually correct. Everytime you run the
script, you build a task that consists of calling ``f`` with a different number
(because it's a randomly generated number). Given that tasks are defined as the
a Python function and its arguments, every time you run jug, you build a
different task (unless you, by chance, draw twice the same number).

My solution is typically **to set the random seed at the start of the
computation explicitly**::

    from jug import Task
    from random import random, seed

    def f(x):
        return x*2

    seed(123) # <- set the random seed
    result = Task(f, random())

Now, everything will work as expected.

(As an aside: given that jug was developed in a context where it is important
to be able to reproduce your results, it is a good idea, in general, if your
computation dependends of pseudo-random numbers, to be explicit about the
seeds. So, *this is a feature not a bug*.)

Will jug work on batch cluster systems (like SGE or PBS)?
---------------------------------------------------------

Yes, it was built for it.

There is no interaction with the batch system, but if you submit jobs that look
like::

    jug execute my_jug_script.py --jugdir=my_jug_dir

And it will work fine. Given that jobs can join the computation at any time and
all of the communication is through the backend (file system by default), jug
especially suited for these environments.

Can jug handle non-pickle() objects?
------------------------------------

Short answer: No.

Long answer: Yes, with a little bit of special code. If you have another way to
get them from one machine to another, you could write a special backend for
that. Right now, only ``numpy`` arrays are treated as a special case (they are
not pickled, but rather saved in their native format), but you could extend
this. Ask on the `mailing list <http://groups.google.com/group/jug-users>`_ if
you want to learn more.

