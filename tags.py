import os
import glob
import yaml
import shutil


POSTS_PATH = '_posts'

TAGS_PATH = 'tags'
TAG_LAYOUT = 'tag'


def get_front_matter(path):
    end = False
    front_matter = ""
    with open(path, 'r') as f:
        for line in f.readlines():
            if line.strip() == '---':
                if end:
                    break
                else:
                    end = True
                    continue
            front_matter += line

    return front_matter

def list_all_files(rootdir):
    import os
    _files = []
    list = os.listdir(rootdir)
    for i in range(0, len(list)):
           path = os.path.join(rootdir, list[i])
           if os.path.isdir(path):
              _files.extend(list_all_files(path))
           if os.path.isfile(path):
              _files.append(path)
    return _files

def get_tags():
    all_tags = []

    Filelist = list_all_files(POSTS_PATH)
    for filePath in  Filelist :
        for file in glob.glob(filePath):
            meta = yaml.load(get_front_matter(file))
            try:
                tag = meta['tag']
            except KeyError:
                try:
                    tags = meta['tags']
                except KeyError:
                    err_msg = (
                        "[Error] File:{} at least "
                        "have one tag.").format(file)
                    print(err_msg)
                else:
                    if type(tags) == str:
                        error_msg = (
                            "[Error] File {} 'tags' type"
                            " can not be STR!").format(file)
                        raise Exception(error_msg)

                    for ctg in meta['tags']:
                        if ctg not in all_tags:
                            all_tags.append(ctg)
            else:
                if type(tag) == list:
                    err_msg = (
                        "[Error] File {} 'tag' type"
                        " can not be LIST!").format(file)
                    raise Exception(err_msg)

                if tag not in all_tags:
                    all_tags.append(tag)

    return all_tags

def generate_tag_pages():
    tags = get_tags()
    if os.path.exists(TAGS_PATH):
        shutil.rmtree(TAGS_PATH)

    os.makedirs(TAGS_PATH)

    for tag in tags:
        new_page = TAGS_PATH + '/' + tag.replace(" ", "-") + '.html'
        with open(new_page, 'w+') as html:
            html.write("---\n")
            html.write("layout: {}\n".format(TAG_LAYOUT))
            html.write("title: {}\n".format(tag.title()))
            html.write("tag: {}\n".format(tag))
            html.write("---")
            print("[INFO] Created page: " + new_page)
    print("[INFO] Succeed! {} tag-pages created.\n"
          .format(len(tags)))


def main():
    generate_tag_pages()

main()