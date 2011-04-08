MUSIC_PREFIX = "/music/somafm"
SOMAFM_BASE_URL = "http://somafm.com"

NAME = L('Title')

# make sure to replace artwork with what you want
# these filenames reference the example files in
# the Contents/Resources/ folder in the bundle
ART  = 'art-default.jpg'
ICON = 'icon-default.png'

####################################################################################################

def Start():

    ## make this plugin show up in the 'Music' section
    ## in Plex. The L() function pulls the string out of the strings
    ## file in the Contents/Strings/ folder in the bundle
    ## see also:
    ##  http://dev.plexapp.com/docs/mod_Plugin.html
    ##  http://dev.plexapp.com/docs/Bundle.html#the-strings-directory
    Plugin.AddPrefixHandler(MUSIC_PREFIX, MusicMainMenu, NAME, ICON, ART)

    Plugin.AddViewGroup("InfoList", viewMode="InfoList", mediaType="items")
    Plugin.AddViewGroup("List", viewMode="List", mediaType="items")

    ## set some defaults so that you don't have to
    ## pass these parameters to these object types
    ## every single time
    ## see also:
    ##  http://dev.plexapp.com/docs/Objects.html
    MediaContainer.title1 = NAME
    MediaContainer.viewGroup = "List"
    MediaContainer.art = R(ART)
    DirectoryItem.thumb = R(ICON)
    VideoItem.thumb = R(ICON)
    
    HTTP.CacheTime = CACHE_1HOUR 

  


#### the rest of these are user created functions and
#### are not reserved by the plugin framework.
#### see: http://dev.plexapp.com/docs/Functions.html for
#### a list of reserved functions above



#
# Example main menu referenced in the Start() method
# for the 'Music' prefix handler
#

def MusicMainMenu():

    # Container acting sort of like a folder on
    # a file system containing other things like
    # "sub-folders", videos, music, etc
    # see:
    #  http://dev.plexapp.com/docs/Objects.html#MediaContainer
    dir = MediaContainer(viewGroup="InfoList")


    root = XML.ElementFromURL(SOMAFM_BASE_URL, isHTML=True)
    Log(root)
    
    for liList in root.xpath("//div[@id='stations']/ul/li"):
        #Log(liList.xpath("h3")[0].text_content())
        name = liList.xpath("h3")[0].text_content()
        #Log(liList.xpath("p/a")[0].get('href'))
        url = SOMAFM_BASE_URL + liList.xpath("p/a")[0].get('href').replace('play/', '') + '.pls'
        #Log(url)
        #Log(liList.xpath("p/a/img")[0].get('src'))
        thumb = SOMAFM_BASE_URL + liList.xpath("p/a/img")[0].get('src').strip()
        Log('|' + thumb + '|');
        subtitle = liList.xpath("p[@class='descr']")[0].text_content();
        item = TrackItem(url, name, subtitle=subtitle, thumb=thumb)
        dir.Append(item)


    # ... and then return the container
    return dir

def CallbackExample(sender):

    ## you might want to try making me return a MediaContainer
    ## containing a list of DirectoryItems to see what happens =)

    return MessageContainer(
        "Not implemented",
        "In real life, you'll make more than one callback,\nand you'll do something useful.\nsender.itemTitle=%s" % sender.itemTitle
    )

  
