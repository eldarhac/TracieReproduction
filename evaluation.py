def evaluate_tracie_style(test_path: str, result_path: str, end:bool=True):
    glines = [x.strip() for x in open(test_path).readlines()]
    plines = [x.strip() for x in open(f"{result_path}/eval_results_lm.txt").readlines()]
    assert len(glines) == len(plines)
    total = 0
    correct = 0
    total_start = 0
    correct_start = 0
    total_end = 0
    correct_end = 0
    story_prediction_map = {}
    for i, l in enumerate(glines):
        if "story:" in l.split("\t")[0]:
            story = l.split("\t")[0].split("story:")[1]
        else:
            story = "no story"
        if story not in story_prediction_map:
            story_prediction_map[story] = []
        label = l.split("\t")[1].split()[1]
        p = plines[i].split()[1][:8]
        total += 1
        if label == p:
            correct += 1
            story_prediction_map[story].append(True)
        else:
            story_prediction_map[story].append(False)
        if "starts before" in l or "starts after" in l:
            total_start += 1
            if label == p:
                correct_start += 1
        else:
            total_end += 1
            if label == p:
                correct_end += 1
    s_total = 0
    s_correct = 0
    for key in story_prediction_map:
        s_total += 1
        cv = True
        for v in story_prediction_map[key]:
            cv = cv and v
        if cv:
            s_correct += 1
    print("Overall Acc: {}".format(str(float(correct) / float(total))))
    print("Start Acc: {}".format(str(float(correct_start) / float(total_start))))
    if end:
      print("End Acc: {}".format(str(float(correct_end) / float(total_end))))
    print("Story Acc: {}".format(str(float(s_correct) / float(s_total))))

def evaluate_symbolic(test_path: str, result_path: str, end:bool=True):
    glines = [x.strip() for x in open(test_path).readlines()]
    plines = [x.strip() for x in open(f"{result_path}/eval_results_lm.txt").readlines()]
    assert len(glines) == len(plines)
    total = 0
    correct = 0
    total_start = 0
    correct_start = 0
    total_end = 0
    correct_end = 0
    story_prediction_map = {}
    for i, l in enumerate(glines):
        story = l.split("\t")[0].split("story:")[1]
        if story not in story_prediction_map:
            story_prediction_map[story] = []
        label = l.split("\t")[-1].split()[1]
        p = plines[i].split("\t")
        if "starts before" in l.split("\t")[0] or "starts after" in l.split("\t")[0]:
            total_start += 1
            total += 1
            if label == p[0]:
                correct_start += 1
                correct += 1
                story_prediction_map[story].append(True)
            else:
                story_prediction_map[story].append(False)
        else:
            p = float(p[1][1:-1])
            pl = "before"
            if p < 0:
                pl = "after"
            if label != "positive":
                continue
            total_end += 1
            total += 1
            label = "before"
            if "ends after" in l.split("\t")[0]:
                label = "after"
            if label == pl:
                correct_end += 1
                correct += 1
                story_prediction_map[story].append(True)
            else:
                story_prediction_map[story].append(False)

    # print("Overall Acc: {}".format(str(float(correct) / float(total))))
    print("Start Acc: {}".format(str(float(correct_start) / float(total_start))))
    if end:
      print("End Acc: {}".format(str(float(correct_end) / float(total_end))))
    print("Overall Acc: {}".format(str(float(correct) / float(total))))

    s_total = 0
    s_correct = 0
    for key in story_prediction_map:
        s_total += 1
        cv = True
        for v in story_prediction_map[key]:
            cv = cv and v
        if cv:
            s_correct += 1
    print("Story Acc: {}".format(str(float(s_correct) / float(s_total))))
