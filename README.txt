Cover Art Server 1.2
by Jacob Weber
with contributions by Simon Long

Works with iTunes 7.7, on Mac OS 10.5 or Windows XP. For Windows XP you'll need Cygwin installed. Also compatible with other operating systems, with some changes.

You must have Python installed to run this script. Version 2.5.1 is recommended, which comes with Mac OS 10.5. For other systems, you can download it from http://www.python.org/download/. If you do, you'll need to change the first line of the file coverArtServer.py to point to the python binary. For example:
#!/Library/Frameworks/Python.framework/Versions/Current/bin/python

To search for covers on Amazon, you'll need a free Amazon Web Services account. Go to http://www.amazon.com/gp/browse.html?node=3435361 and sign up there. When you get your Access Key ID, put it in the text file "amazonLicense.txt" in the same directory as these scripts.

On Mac OS, turn off "Personal Web Sharing" or "Web Sharing" in the Sharing preferences pane. Turn off any other web servers on port 80.

Open your hosts file in a text editor. On Mac OS, this is /etc/hosts. On Windows, it's c:\windows\system32\drivers\etc\hosts. Add the following lines. This will temporarily prevent the iTunes Music Store from working.
  127.0.0.1		ax.phobos.apple.com.edgesuite.net
  127.0.0.1		a1.phobos.apple.com
To make sure these changes take effect, you should flush the DNS cache, using a command-line utility. On Mac OS 10.5, type "dscacheutil -flushcache". On Mac OS 10.4, type "lookupd -flushcache". On Windows XP with Cygwin, type "ipconfig /flushdns".

At the command-line, "cd" into the directory with these scripts. Type "sudo ./coverArtServer.py" to start the cover art server. You'll need to enter your administrator password.

In iTunes, select any albums that have incorrect artwork, control-click them, and choose "Clear Downloaded Artwork." Then control-click again and choose "Get Album Artwork". Or, to get artwork for all albums that don't have it, choose "Get Album Artwork" from the Advanced menu.

The first time you do this, it won't actually get any artwork; it will just tell our program which albums need it. Go to http://localhost/ to see a list of the albums needing artwork. When you click an album on the left side, we search Amazon for covers. If you don't find one, you can enter your own search terms and try again. Or if you know the URL of an image from another source, you can enter it. When you're done, go back to iTunes, select the same tracks, and choose "Get Album Artwork" again. This time, the images will be loaded into the iTunes cover art database.

When you're done:
At the command-line, press control-C to stop the server.
Delete the lines you added to /etc/hosts.
Flush the DNS cache again, using the same command as before.
