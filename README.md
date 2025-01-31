# TestSergeant

**Disclaimer: This is a recreational project, use at your own discretion.**

## What is TestSergeant?

_TestSergeant_ started as a project to test various remote Linux Systems in a factory floor and evolved to be a generic modular task runing tool.

In short, it is a tool to run multiple user-defined Python scripts (_Commands_) in an user-defined hierarchy (_Pipeline_). Each _Command_ can receive inputs and have it's output be tested in an _Assertion_.

It's original intent went as follows:

- Run _TestSergeant_ in a central server connected to the different systems accross the factory;
- Clone itself on to those systems;
- _TestSergeant_ would then run each Clone of itself with different input files according to the situation;
- Each Clone would then run tests described in the input file and report back home with the results;
- These results were then saved by _TestSergeant_ in a database.

This was the initial use case and showcases the potential of this tool.

This version has been stripped of its' Linux-specific features (mainly checking for which Linux distribution and Python version is currently running in the Host) and I currently use it on my Windows machine to run a few tasks now and again.

**I have not used this version on Linux, so I'm not sure of it's viability.**

## What can I find in this project?

There's the main component _TestSergeant_ and there's three helper scripts.

    \ P2PConverter
    \ -- main.py
    \ TestBuilder
    \ -- main.py
    \ TestSergeant
    \ -- main.py
    \ -- genDicts.py

### TestSergeant/genDicts.py

Analyzes the contents within _./src/Models/Commands_ and _./src/Models/Assertions_ and generates two files within _../TestBuilder/info_.

These files are essentially a list of all _Commands_ (organized by _Category_) and _Assertions_ that you currently have, to be used in the _TestBuilder_

### TestBuilder

This is a console application that helps you build the input file for _TestSergeant_.

Here, you define:

- Which _Commands_ will be used;
- Which _Assertion_ goes with each _Command_;
- The Hierarchy (_Pipeline_) between _Commands_ and rules of execution.

It generates an _autosaved.json_ file as you go with the changes so you can see exactly what you're doing as you tinker with the _TestBuilder_.

The resulting final file must be then placed into _../TestSergeant/Inputs_ to be used in the main application.

### P2PConverter

**P2P** stands for _Pipeline to PUML_ / _PUML to Pipeline_.

This is a simple script that converts a **.puml** file into a _Pipeline_ (more on this later) or the other way around.

If you generate an input file with the TestBuilder, you'll notice there's a **pipeline** section to it.
While the _TestBuilder_ is capable of generating this section itself, for really large _Pipelines_ it's just easier to have a visual aid.
This is where **.puml** came to my aid. There's some online editors where you can visualise (and edit) your _Pipeline_ in. You then convert it back to the _TestSergeant_ format using the _P2PConverter_.

## Alright cool, how do I use it?

Start by setting up a Virtual Environment within the project's top folder.

    python -m venv venv
    venv\Scripts\activate
    pip install -r requirements.txt

After that you can run the provided example by runing:

    python main.py
