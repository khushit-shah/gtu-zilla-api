import os
from pathlib import Path
import json

papers = list()
def getPapersByCode(basePath):
    global papers
    if(Path(basePath).is_file()):
        path = basePath
        filename = path.split(os.sep).pop().replace(".pdf", "")
        path = path.replace("./GTU-ZILLA-API/", "")
        curlist = [filename, path]
        papers.append(curlist)
    elif(Path(basePath).is_dir()):
        dirs = os.listdir(basePath)
        for dir in dirs:
            getPapersByCode(os.path.join(basePath, dir))
getPapersByCode("./GTU-ZILLA-API/EXAM-PAPERS")
papers_json = json.dumps(papers)
print(papers_json)
file = open("./GTU-ZILLA-API/papers.json", "w+")
file.write(papers_json)
file.close()
