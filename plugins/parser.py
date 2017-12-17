from plugins.pyknp.knp.knp import KNP


def find_original_word(bunsetsu):
    """
    @param bunsetsu pyknp.knp.bunsetsu Class
    @return an original word
    """
    return bunsetsu.mrph_list()[0].genkei


def find_nodes(line):
    knp = KNP()
    # knp = pyknp.KNP()
    result = knp.parse(line)
    bnst_list = result.bnst_list()
    nodes = []
    for bnst in bnst_list:
        nodes.append(find_original_word(bnst))

    return nodes


def find_parent_child(line):
    knp = KNP()
    # knp = pyknp.KNP()
    result = knp.parse(line)
    bnst_list = result.bnst_list()
    bnst_dict = dict((x.bnst_id, x) for x in bnst_list)

    tuples = []
    for bnst in bnst_list:
        if bnst.parent_id != -1:
            tuples.append((find_original_word(bnst),
                           find_original_word(bnst_dict[bnst.parent_id])))

    return tuples


if __name__ == '__main__':
    line = '太郎は花子が読んでいる本を次郎に渡した'
    tuples = find_parent_child(line)
    for t in tuples:
        print(t[0] + ' => ' + t[1])
