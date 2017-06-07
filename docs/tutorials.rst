Distributed Resource Management Application API
===============================================

This guide is a tutorial for getting started programming with DRMAA. It is
basically a one to one translation of the original in C for Grid Engine. It
assumes that you already know what DRMAA is and that you have drmaa-python
installed. If not, have a look at Installing. The following code segments are
also included in the repository.

Starting and Stopping a Session
-------------------------------

The following two code segments show the most basic DRMAA python binding
program.

.. code-block:: python
   :linenos:
   :caption: example1.py
   :name: example-1

   #!/usr/bin/env python

   import drmaa

   def main():
      """Create a drmaa session and exit"""
      with drmaa.Session() as s:
         print('A session was started successfully')

   if __name__=='__main__':
      main()

The first thing to notice is that every call to a DRMAA function will return an
error code. In this tutorial, we ignore all error codes.

Now let's look at the functions being called. First, on line 7, we initialise a
``Session`` object by calling ``drmaa.Session()``. The ``Session`` is
automatically initialized via ``initialize()``, and it creates a session and starts
an event client listener thread. The session is used for organizing jobs
submitted through DRMAA, and the thread is used to receive updates from the
queue master about the state of jobs and the system in general. Once
``initialize()`` has been called successfully, it is the responsibility of the
calling application to also call ``exit()`` before terminating, but since we're
using it as a context manager via the ``with`` statement, that will happene
automatically. If an application does not call ``exit()`` before terminating,
session state may be left behind in the user's home directory, and the queue
master may be left with a dead event client handle, which can decrease queue
master performance.

At the end of our program, ``exit()`` is called automatically when we leave the
``with`` block. ``exit()`` cleans up the session and stops the event client
listener thread. Most other DRMAA functions must be called before ``exit()``.
Some functions, like ``getContact()``, can be called after ``exit()``, but these
functions only provide general information. Any function that does work, such as
``runJob()`` or ``wait()`` must be called before ``exit()`` is called. If such a
function is called after ``exit()`` is called, it will return an error.

.. code-block:: python
   :linenos:
   :caption: example1.1.py
   :name: example-1-1
   :emphasize-lines: 13,15,18,19

   #!/usr/bin/env python

   import drmaa

   def main():
       """
       Create a session, show that each session has an ID, use session ID to
       disconnect, then reconnect. Finally, exit.
       """
       s = drmaa.Session()
       s.initialize()
       print('A session was started successfully')
       response = s.contact
       print('session contact returns: %s' % response)
       s.exit()
       print('Exited from session')

       s.initialize(response)
       print('Session was restarted successfullly')
       s.exit()


   if __name__=='__main__':
       main()

This example is very similar to :ref:`Example 1 <example-1>`. The difference is
that it uses the Grid Engine feature of reconnectable sessions. The DRMAA
concept of a session is translated into a session tag in the Grid Engine job
structure. That means that every job knows to which session it belongs. With
reconnectable sessions, it's possible to initialize the DRMAA library to a
previous session, allowing the library access to that session's job list. The
only limitation, though, is that jobs which end between the calls to ``exit()``
and ``init()`` will be lost, as the reconnecting session will no longer see
these jobs, and so won't know about them.

On line 13, we use the contact attribute to get the contact information for this
session. On line 15 we then exit the session. On line 18, we use the stored
contact information to reconnect to the previous session. Had we submitted jobs
before calling ``exit()``, those jobs would now be available again for
operations such as ``wait()`` and ``synchronize()``. Finally, on line 19 we exit
the session a second time.

Running a Job
-------------

The following code segments show how to use the DRMAA python binding to
submit a job to Grid Engine. It submits a small shell script (``sleeper.sh``)
which takes two arguments:

.. code-block:: bash

   #!/bin/bash
   echo "Hello world, the answer is $1"
   sleep 3s
   echo "$2 Bye world!"

.. code-block:: python
   :linenos:
   :caption: example2.py
   :name: example-2
   :emphasize-lines: 12-22

   #!/usr/bin/env python

   import drmaa
   import os

   def main():
      """
      Submit a job.
      Note, need file called sleeper.sh in current directory.
      """
      with drmaa.Session() as s:
          print('Creating job template')
          jt = s.createJobTemplate()
          jt.remoteCommand = os.path.join(os.getcwd(), 'sleeper.sh')
          jt.args = ['42', 'Simon says:']
          jt.joinFiles=True

          jobid = s.runJob(jt)
          print('Your job has been submitted with ID %s' % jobid)

          print('Cleaning up')
          s.deleteJobTemplate(jt)

   if __name__=='__main__':
      main()

The beginning and end of this program are the same as the first example. What's
new is in lines 12--22. On line 12 we ask DRMAA to allocate a job template
for us. A job template is a structure used to store information about a job to
be submitted. The same template can be reused for multiple calls to ``runJob()``
or ``runBulkJob()``.

On line 13 we set the ``remoteCommand`` attribute. This attribute tells DRMAA
where to find the program we want to run. Its value is the path to the
executable. The path can be either relative or absolute. If relative, it is
relative to the ``workingDirectory`` attribute, which if not set defaults to the
user's home directory. For more information on DRMAA attributes, please see the
attributes man page. Note that for this program to work, the script
``sleeper.sh`` must be in the current directory.

On line 14 we set the ``args`` attribute. This attribute tells DRMAA what
arguments to pass to the executable.

On line 17 we submit the job with ``runJob()``. DRMAA will place the ID assigned
to the job into the character array we passed to ``runJob()``. The job is now
running as though submitted by ``qsub`` or ``bsub``. At this point calling
``exit()`` and/or terminating the program will have no effect on the job.

To clean things up, we delete the job template on line 21. This frees the memory
DRMAA set aside for the job template, but has no effect on submitted jobs.

If instead of a single job we had wanted to submit an array job, we could have
replaced the else on line 18 and 19 with the following:

.. code-block:: python
   :caption: example2.1.py
   :name: example-2-1

   jobid = s.runBulkJobs(jt, 1, 30, 2)
   print('Your jobs have been submitted with IDs %s' % jobid)

This code segment submits an array job with 15 tasks numbered 1, 3, 5, 7, etc.
An important difference to note is that ``runBulkJobs()`` returns the job ids in
a list. On the last line, we print all the job ids.

Waiting for a Job
-----------------

Now we're going to extend our example to include waiting for a job to finish.


.. code-block:: python
   :linenos:
   :caption: example3.py
   :name: example-3
   :emphasize-lines: 21-22

   #!/usr/bin/env python

   import drmaa
   import os

   def main():
       """
       Submit a job and wait for it to finish.
       Note, need file called sleeper.sh in home directory.
       """
       with drmaa.Session() as s:
           print('Creating job template')
           jt = s.createJobTemplate()
           jt.remoteCommand = os.path.join(os.getcwd(), 'sleeper.sh')
           jt.args = ['42', 'Simon says:']
           jt.joinFiles = True

           jobid = s.runJob(jt)
           print('Your job has been submitted with ID %s' % jobid)

           retval = s.wait(jobid, drmaa.Session.TIMEOUT_WAIT_FOREVER)
           print('Job: {0} finished with status {1}'.format(retval.jobId, retval.hasExited))

           print('Cleaning up')
           s.deleteJobTemplate(jt)

   if __name__=='__main__':
       main()


This example is very similar to :ref:`Example 2 <example-2>` except for line
21. On line 21 we call ``wait()`` to wait for the job to end. We have to give
``wait()`` both the ID of the job for which we want to wait, and also how long
we are willing to wait for the job to finish. This could be a number of
seconds, or it could be either ``TIMEOUT_WAIT_FOREVER`` or ``TIMEOUT_NO_WAIT``.
``wait()`` returns a ``JobInfo`` tuple, which has the following attributes:
``jobId``, ``hasExited``, ``hasSignal``, ``terminatedSignal``, ``hasCoreDump``,
``wasAborted``, ``exitStatus``, and ``resourceUsage``. ``jobId`` is
particularly useful if we passed in ``JOB_IDS_SESSION_ANY`` as the ID argument
for ``wait()``, because without it we would have no way of knowing which job it
actually waited for.  Lastly, we print out the job ID and the exit status on
line 22.

An alternative to ``wait()`` when working with multiple jobs, such as jobs
submitted by ``runBulkJobs()`` or multiple calls to ``runJob()`` is
``synchronize()``. ``synchronize()`` waits for a set of jobs to finish. To use
``synchronize()``, we could replace lines 18--22 with the following:

.. code-block:: python
   :caption: example3.1.py
   :name: example-3-1

   joblist = s.runBulkJobs(jt, 1, 30, 2)
   print('Your jobs have been submitted with IDs %s' % joblist)

   s.synchronize(joblist, drmaa.Session.TIMEOUT_WAIT_FOREVER, True)


With the switch to ``runBulkJobs()`` we now have several jobs for which to wait.
On line 20, instead of calling ``wait()``, we call ``synchronize()``.
``synchronize()`` takes only three interesting parameters. The first is the list
of string IDs for which to wait. If the special ID, ``JOB_IDS_SESSION_ALL``,
appears in the array, ``synchronize()`` will wait for all jobs submitted via
DRMAA during this session (i.e., since ``initialize()`` was called). The second
is how long to wait for all the jobs in the list to finish. This is the same as
the timeout parameter for ``wait()``. The third is whether this call to
``synchronize()`` should clean up after the job. After a job completes, it
leaves behind accounting information, such as exit status and usage, until
either ``wait()`` or ``synchronize()`` with ``dispose`` set to ``True`` is
called. It is the responsibility of the application to make sure one of these
two functions is called for every job. Not doing so creates a memory leak. Note
that calling ``synchronize()`` with dispose set to true flushes all accounting
information for all jobs in the list. If you want to use ``synchronize()`` and
still recover the accounting information, set ``dispose`` to ``False`` and call
``wait()`` for each job. To do this in :ref:`Example 3 <example-3>`, we would
replace lines 18--22 with the following:

.. code-block:: python
   :caption: example3.2.py
   :name: example-3-2

   joblist = s.runBulkJobs(jt, 1, 30, 2)
   print('Your jobs have been submitted with IDs %s' % joblist)

   s.synchronize(joblist, drmaa.Session.TIMEOUT_WAIT_FOREVER, False)
   for curjob in joblist:
       print('Collecting job ' + curjob)
       retval = s.wait(curjob, drmaa.Session.TIMEOUT_WAIT_FOREVER)
       print('Job: {0} finished with status {1}'.format(retval.jobId,
                                                        retval.hasExited))


What's different is that on line 21 we set ``dispose`` to ``False``, and then on
lines 22--26 we wait once for each job, printing the exit status and usage
information as we did in :ref:`Example 3 <example-3>`.

We pass ``joblist`` to ``synchronize()`` to wait for each job specifically.
Otherwise, the ``wait()`` could end up waiting for a job submitted after the
call to ``synchronize()``.

Controlling a Job
-----------------

Now let's look at an example of how to control a job from DRMAA:

.. code-block:: python
   :linenos:
   :caption: example4.py
   :name: example-4
   :emphasize-lines: 20

   #!/usr/bin/env python

   import drmaa
   import os

   def main():
       """Submit a job, then kill it.
       Note, need file called sleeper.sh in home directory.
       """
       with drmaa.Session() as s:
           print('Creating job template')
           jt = s.createJobTemplate()
           jt.remoteCommand = os.path.join(os.getcwd(), 'sleeper.sh')
           jt.args = ['42', 'Simon says:']
           jt.joinFiles = True

           jobid = s.runJob(jt)
           print('Your job has been submitted with ID %s' % jobid)
           # options are: SUSPEND, RESUME, HOLD, RELEASE, TERMINATE
           s.control(jobid, drmaa.JobControlAction.TERMINATE)

           print('Cleaning up')
           s.deleteJobTemplate(jt)

   if __name__=='__main__':
       main()


This example is very similar to :ref:`Example 2 <example-2>` except for line
20. On line 20 we use ``control()`` to delete the job we just submitted. Aside
from deleting the job, we could have also used ``control()`` to suspend,
resume, hold, or release it.

Note that ``control()`` can be used to control jobs not submitted through DRMAA.
Any valid SGE job ID could be passed to ``control()`` as the ID of the job to
delete.

Getting Job Status
------------------

Here's an example of using DRMAA to query the status of a job:

.. code-block:: python
   :linenos:
   :caption: example5.py
   :name: example-5
   :emphasize-lines: 22-40

   #!/usr/bin/env python

   import drmaa
   import time
   import os

   def main():
       """
       Submit a job, and check its progress.
       Note, need file called sleeper.sh in home directory.
       """
       with drmaa.Session() as s:
           print('Creating job template')
           jt = s.createJobTemplate()
           jt.remoteCommand = os.path.join(os.getcwd(), 'sleeper.sh')
           jt.args = ['42', 'Simon says:']
           jt.joinFiles=True

           jobid = s.runJob(jt)
           print('Your job has been submitted with ID %s' % jobid)

           # Who needs a case statement when you have dictionaries?
           decodestatus = {drmaa.JobState.UNDETERMINED: 'process status cannot be determined',
                           drmaa.JobState.QUEUED_ACTIVE: 'job is queued and active',
                           drmaa.JobState.SYSTEM_ON_HOLD: 'job is queued and in system hold',
                           drmaa.JobState.USER_ON_HOLD: 'job is queued and in user hold',
                           drmaa.JobState.USER_SYSTEM_ON_HOLD: 'job is queued and in user and system hold',
                           drmaa.JobState.RUNNING: 'job is running',
                           drmaa.JobState.SYSTEM_SUSPENDED: 'job is system suspended',
                           drmaa.JobState.USER_SUSPENDED: 'job is user suspended',
                           drmaa.JobState.DONE: 'job finished normally',
                           drmaa.JobState.FAILED: 'job finished, but failed'}

           for ix in range(10):
               print('Checking %s of 10 times' % ix)
               print decodestatus(s.jobStatus(jobid))
               time.sleep(5)

           print('Cleaning up')
           s.deleteJobTemplate(jt)

   if __name__=='__main__':
       main()

Again, this example is very similar to :ref:`Example 2 <example-2>`, this time
with the exception of lines 22--40. On line 36, we use ``jobStatus()`` to get
the status of the job.  Line 43 determine what the job status is and report it.

Getting DRM information
-----------------------

Lastly, let's look at how to query the DRMAA library for information about the
DRMS and the DRMAA implementation itself:

.. code-block:: python
   :linenos:
   :caption: example6.py
   :name: example-6
   :emphasize-lines: 9-12

   #!/usr/bin/env python

   import drmaa

   def main():
       """ Query the system. """
       with drmaa.Session() as s:
           print('A DRMAA object was created')
           print('Supported contact strings: %s' % s.contact)
           print('Supported DRM systems: %s' % s.drmsInfo)
           print('Supported DRMAA implementations: %s' % s.drmaaImplementation)
           print('Version %s' % s.version)

           print('Exiting')

   if __name__=='__main__':
       main()

On line 9, we get the contact string list. This is the list of contact strings
that will be understood by this DRMAA instance. Normally on of these strings is
used to select to which DRM this DRMAA instance should be bound. On line 10, we
get the list of supported DRM systems. On line 11, we get the list of supported
DRMAA implementations. On line 12, we get the version number of the DRMAA C
binding specification supported by this DRMAA implementation.
