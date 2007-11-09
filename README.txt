Cover Art Server 1.1
by Jacob Weber
with contributions by Simon Long

Works with iTunes 7.4 and Mac OS 10.5. Also compatible with Mac OS 10.4, with some changes.

You must have Python installed to run this script. Version 2.5.1 is recommended, which comes with Mac OS 10.5. For older systems, you can download it from http://www.python.org/download/. If you do, you'll need to change the first line of the file coverArtServer.py to:
#!/Library/Frameworks/Python.framework/Versions/Current/bin/python

To search for covers on Amazon, you'll need a free Amazon Web Services account. Go to http://www.amazon.com/gp/browse.html?node=3435361 and sign up there. When you get your Access Key ID, put it in the text file "amazonLicense.txt" in the same directory as these scripts.

Turn off "Personal Web Sharing" or "Web Sharing" in the Sharing preferences pane. Turn off any other web servers on port 80.

Edit /etc/hosts and add the following lines. You'll need an administrator password. If you're not sure how to edit this file, download http://macupdate.com/info.php/id/17880. This will temporarily prevent the iTunes Music Store from working.
  127.0.0.1		ax.phobos.apple.com.edgesuite.net
  127.0.0.1		a1.phobos.apple.com
In Terminal, type "dscacheutil -flushcache" to make sure these settings take effect. If you're running a version of Mac OS before 10.5, type "lookupd -flushcache" instead.

In Terminal, "cd" into the directory with these scripts. Type "sudo ./coverArtServer.py" to start the cover art server. You'll need to enter your administrator password.

In iTunes, select any albums that have incorrect artwork, control-click them, and choose "Clear Downloaded Artwork." You will need to select all tracks from the albums for this to work. Then control-click again and choose "Get Album Artwork". Or, to get artwork for all albums that don't have it, chooes "Get Album Artwork" from the Advanced menu.

The first time you do this, it won't actually get any artwork; it will just tell our program which albums need it. Go to http://localhost/ to see a list of the albums needing artwork. When you click an album on the left side, we search Amazon for covers. If you don't find one, you can enter your own search terms and try again. Or if you know the URL of an image from another source, you can enter it. When you're done, go back to iTunes, select the same tracks, and choose "Get Album Artwork" again. This time, the images will be loaded into the iTunes cover art database.

When you're done:
In Terminal, press control-C to stop the server.
Delete the lines you added to /etc/hosts.
In Terminal, type "dscacheutil -flushcache" again. If you're running a version of Mac OS before 10.5, type "lookupd -flushcache" instead.
