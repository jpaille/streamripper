# Streamripper
A light version of streamripper software coded with Python. Streamripper records radio streams.

Installation
------------

```
git clone https://github.com/jpaille/streamripper
cd streamripper
pip install -r requirements.txt
```

Usage:
------

python streamripper.py URL

example :
  ``python streamripper.py http://hotmixradio-rock.ice.infomaniak.ch/hotmixradio-rock-128.mp3 ``

This command will record songs of the hotmixradio stream and place them in the current directory. 

So far I only recoded a few options:

* *-d* Select a different base directory for ripping.

* *--cut-begining N seconds*
* *--cut-end N seconds* 
Remove radio jingle songs by adding cutting limits.


* *-u* Use a different UserAgent than "Streamripper".

Todo:
-----

- Streamripper.py works well with hotmixradio streams http://www.mathdabomb.fr/?post/2011/01/08/Ecoutez-les-webradios-HotMixRadio-depuis-votre-player-pr%C3%A9f%C3%A9r%C3%A9.
  Because it handles the hotmix radio style metadata. Some streams use different forms of metadata.
  Add a new class that inherit from ```metadata_parser.MetadataParser``` to handle new style of metadata.
  
- Handle other streamripper options like *-A* (Don´t create individual tracks).

