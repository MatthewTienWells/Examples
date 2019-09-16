def trim_xml(filename):
    """Reads an xml file and returns text containing only the reel list.

    Inputs:
        The name of the file to begin with.
    Outputs:
        Text containing a list of reels."""
    xml = open(filename, 'r')
    out_text = ''
    reading_list = False
    for line in xml:
        if '<ReelList>' in line:
            reading_list = True
        if reading_list:
            out_text = out_text + line
        if '</ReelList>' in line:
            reading_list = False
    xml.close()
    return out_text

class dataset():
    def __init__(self, text):
        lines = text.split('\n')
        self.properties = {}
        for line in lines:
            key = line[line.index('<')+1:line.index('>')]
            line = line[line.index('>')+1:]
            value = line[:line.index('<')]
            self.properties[key] = value
        self.id = self.properties['Id']


class reel():
    def __init__(self, text):
        lines = text.split('\n')
        title = lines[0]
        self.frames = int(
            title[title.index(','):].strip(', ').strip(' frames -->')
        )
        header = lines[1]
        header = header[header.index('>')+1:]
        self.id = header[:header.index('<')]
        lines = lines[2:-1]

        picturedata = ''
        sounddata = ''
        subtitledata = ''
        rpic = False
        rson = False
        rsub = False

        for line in lines:
            if '</MainPicture>' in line:
                rpic = False
            if '</MainSound>' in line:
                rson = False
            if '</MainSubtitle>' in line:
                rsub = False
            if rpic:
                picturedata = picturedata + line + '\n'
            if rson:
                sounddata = sounddata + line + '\n'
            if rsub:
                subtitledata = subtitledata + line + '\n'
            if '<MainPicture>' in line:
                rpic = True
            if '<MainSound>' in line:
                rson = True
            if '<MainSubtitle>' in line:
                rsub = True

        picturedata = picturedata.strip('\n')
        sounddata = sounddata.strip('\n')
        subtitledata = subtitledata.strip('\n')
        
        self.picture = dataset(picturedata)
        self.sound = dataset(sounddata)
        self.subtitle = dataset(sounddata)

class ReelList():
    def __init__(self, text):
        text = text[text.index('<Reel>'):]
        to_strip = ['\n', '</ReelList>', ' ', '\n']
        for seq in to_strip:
            text = text.strip(seq)
        reels = text.split('<Reel>')
        self.reel_dict = {}
        reel_num = 0
        self.reels_by_id = {}
        for item in reels:
            trimmed = item.strip('\n').strip('\n    </Reel>')
            self.reel_dict[reel_num] = reel(trimmed)
            self.reels_by_id[self.reel_dict[reel_num].id] = self.reel_dict[reel_num]
            reel_num += 1

def compare_reels(original_list, new_list):
    changes = 'The changes between the first and the second are:\n'
    reels_to_check = []
    for item in original_list.reels_by_id:
        if item not in new_list.reels_by_id:
            changes = changes + 'The reel with ID ' + item + ' was deleted.\n'
        else:
            reels_to_check.append(item)
    for item in new_list.reels_by_id:
        if item not in original_list.reels_by_id:
            changes = changes + 'The reel with ID ' + item + ' was added.\n'
    for item in reels_to_check:
        for prop in original_list.reels_by_id[item].picture.properties:
            if (
                original_list.reels_by_id[item].picture.properties[prop] !=
                new_list.reels_by_id[item].picture.properties[prop]):
                changes = changes + 'In the reel with ID ' + item
                changes = changes + ', the picture\'s ' + prop + 'changed from '
                changes = changes + original_list.reels_by_id[
                    item].picture.properties[prop] + ' to '
                changes = changes + new_list.reels_by_id[
                    item].picture.properties[prop] + '\n'
        for prop in original_list.reels_by_id[item].sound.properties:
            if (
                original_list.reels_by_id[item].sound.properties[prop] !=
                new_list.reels_by_id[item].sound.properties[prop]):
                changes = changes + 'In the reel with ID ' + item
                changes = changes + ', the sound\'s ' + prop + 'changed from '
                changes = changes + original_list.reels_by_id[
                    item].sound.properties[prop] + ' to '
                changes = changes + new_list.reels_by_id[
                    item].sound.properties[prop] + '\n'
        for prop in original_list.reels_by_id[item].subtitle.properties:
            if (
                original_list.reels_by_id[item].subtitle.properties[prop] !=
                new_list.reels_by_id[item].subtitle.properties[prop]):
                changes = changes + 'In the reel with ID ' + item
                changes = changes + ', the subtitles\' ' + prop + 'changed from '
                changes = changes + original_list.reels_by_id[
                    item].subtitle.properties[prop] + ' to '
                changes = changes + new_list.reels_by_id[
                    item].subtitle.properties[prop] + '\n'
    return changes

