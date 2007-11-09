Cover Art Server 1.0
by Jacob Weber


You must have python 2.4.3 installed to run this script. You can get it from http://www.python.org/download/releases/2.4.3/

To search for covers on Amazon, you'll need a free Amazon Web Services account. Go to http://www.amazon.com/gp/browse.html?node=3435361 and sign up there. When you get your Access Key ID, put it in the text file "amazonLicense.txt" in the same directory as these scripts.

Turn off Personal Web Sharing in the Sharing preferences pane. Turn off any other web servers on port 80.

Edit /etc/hosts and add the following lines. You'll need an administrator password. If you're not sure how to edit this file, download http://macupdate.com/info.php/id/17880. This will temporarily prevent the iTunes Music Store from working.
  127.0.0.1		ax.phobos.apple.com.edgesuite.net
  127.0.0.1		a1.phobos.apple.com
  127.0.0.1		phobos.apple.com
In Terminal, type "lookupd -flushcache" to make sure these settings take effect.

In Terminal, "cd" into the directory with these scripts. Type "sudo ./coverArtServer.py" to start the cover art server. You'll need to enter your administrator password.

In iTunes, select any albums that have incorrect artwork, control-click them, and choose "Clear Downloaded Artwork." You will need to select all tracks from the albums for this to work. Then control-click again and choose "Get Album Artwork". Or, to get artwork for all albums that don't have it, chooes "Get Album Artwork" from the Advanced menu.

The first time you do this, it won't actually get any artwork; it will just tell our program which albums need it. Go to http://localhost/ to see a list of the albums needing artwork. When you click an album on the left side, we search Amazon for covers. If you don't find one, you can enter your own search terms and try again. Or if you know the URL of an image from another source, you can enter it. When you're done, go back to iTunes, and choose "Get Album Artwork" again. This time, the images will be loaded into the iTunes cover art database.

When you're done:
In Terminal, press control-C to stop the server.
Delete the lines from /etc/hosts.
In Terminal, type "lookupd -flushcache" again.
