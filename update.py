import os
import glob
import yaml
import shutil
import time
import sys

POSTS_PATH = '_posts'

UPDATE_PATH = '_data'
UPDATE_LAYOUT = 'update'

def get_front_matter(path):
    end = False
    front_matter = ""
    with open(path, 'r', encoding='utf-8') as f:
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

def get_updates():
    all_updates = []

    Filelist = list_all_files(POSTS_PATH)
    for filePath in  Filelist :
        for file in glob.glob(filePath):
            mtime = os.stat(file).st_mtime
            file_modify_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(mtime))
            file_name = os.path.splitext(os.path.basename(file))[0]
            
            # meta = yaml.load(get_front_matter(file))
            # try:
            #     update = meta['title']
            # except KeyError:
            #     err_msg = (
            #         "[Error] File:{} at least "
            #         "have one date.").format(file)
            #     print(err_msg)
            # if update not in all_updates:

            all_updates.append(str(file_name) + "!@!" + str(file_modify_time))

    return all_updates


def generate_update_pages():
    updates = get_updates()

    if os.path.exists(UPDATE_PATH + "\\updates.yml"):
        os.remove(UPDATE_PATH + "\\updates.yml")
        
    new_page = UPDATE_PATH + "\\updates.yml"
    with open(new_page, 'a') as html:
        html.write("#  The updates data.\n")
        html.write("#  v2.1\n")
        html.write("#  https://github.com/Lemon\n")
        html.write("#  2021 Lemon\n")
        html.write("#  MIT Licensed\n")
        html.write("\n")
        html.write("\n")

    for update in updates:
        with open(new_page, 'a') as html:
            html.write("-\n")
            # u = update.decode('utf-8')
            # g = u.encode('gbk')
            # print(g)
            filename = '  filename: "' + update.split("!@!")[0][11:] + '"\n'
            html.write(filename)
            html.write('  lastmod: "' + update.split("!@!")[1] + ' +0800"\n')
    print("[INFO] Succeed! {} update-pages created.\n"
          .format(len(updates)))

def main():
    generate_update_pages()

main()