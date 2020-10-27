import os
import glob
import yaml
import shutil


POSTS_PATH = '_posts'

CATEGORIES_PATH = 'categories'
CATEGORY_LAYOUT = 'category'


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

def get_categories():
    all_categories = []

    Filelist = list_all_files(POSTS_PATH)
    for filePath in  Filelist :
        print(filePath)
        for file in glob.glob(filePath):
            meta = yaml.load(get_front_matter(file))
            try:
                category = meta['category']
            except KeyError:
                try:
                    categories = meta['categories']
                except KeyError:
                    err_msg = (
                        "[Error] File:{} at least "
                        "have one category.").format(file)
                    print(err_msg)
                else:
                    if type(categories) == str:
                        error_msg = (
                            "[Error] File {} 'categories' type"
                            " can not be STR!").format(file)
                        raise Exception(error_msg)

                    for ctg in meta['categories']:
                        if ctg not in all_categories:
                            all_categories.append(ctg)
            else:
                if type(category) == list:
                    err_msg = (
                        "[Error] File {} 'category' type"
                        " can not be LIST!").format(file)
                    raise Exception(err_msg)

                if category not in all_categories:
                    all_categories.append(category)

    return all_categories


def generate_category_pages():
    categories = get_categories()
    if os.path.exists(CATEGORIES_PATH):
        shutil.rmtree(CATEGORIES_PATH)

    os.makedirs(CATEGORIES_PATH)

    for category in categories:
        new_page = CATEGORIES_PATH + '/' + category.replace(" ", "-") + '.html'
        with open(new_page, 'w+') as html:
            html.write("---\n")
            html.write("layout: {}\n".format(CATEGORY_LAYOUT))
            html.write("title: {}\n".format(category.title()))
            html.write("category: {}\n".format(category))
            html.write("---")
            print("[INFO] Created page: " + new_page)
    print("[INFO] Succeed! {} category-pages created.\n"
          .format(len(categories)))


def main():
    generate_category_pages()

main()