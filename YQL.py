import mmap, json

class YQL:
    def __init__(self):
        # Load json into memory
        self.json_disk_file = open("geoDatabase.json", "r")
        self.json_mem_file = mmap.mmap(self.json_disk_file.fileno(), 0, prot=mmap.PROT_READ)
        self.json_disk_file.close()
        self.json_file = json.load(self.json_mem_file)

    def getWoeid(self, q, formatted=False):
        if formatted:
            return q
        try:
            woeid = (q[q.find("(")+1:q.find(")")]).split("=")[1]
        except:
            woeid = (q[q.find("(")+1:q.find(")")]).split("=")[0]
        if "or" in woeid:
            woeid = str(woeid).split(" ")[0]
        return woeid
    
    def getWoeidName(self, q, formatted=False):
        woeid = self.getWoeid(q, formatted)
        ret = self.json_file["woeid"][woeid]
        return(ret)
       
    def getSimilarName(self, q):
        resultsList = []
        for i in self.json_file["country"].items():
            if q.lower() in i[0].lower():
                resultsList.append({
                    "name": i[0],
                    "iso": self.json_file["country"][i[0]][1],
                    "woeid": self.json_file["country"][i[0]][0],
                    "type": "country"
                })
        for i in self.json_file["city"].items():
            if q.lower() in i[0].lower():
                resultsList.append({
                    "name": i[0],
                    "iso": self.json_file["city"][i[0]][1],
                    "woeid": self.json_file["city"][i[0]][0],
                    "type": "city"
                })
        for i in self.json_file["state"].items():
            if q.lower() in i[0].lower():
                resultsList.append({
                    "name": i[0],
                    "iso": self.json_file["state"][i[0]][1],
                    "woeid": self.json_file["state"][i[0]][0],
                    "type": "state"
                })
        for i in self.json_file["small"].items():
            if q.lower() in i[0].lower():
                resultsList.append({
                    "name": i[0],
                    "iso": self.json_file["small"][i[0]][1],
                    "woeid": self.json_file["small"][i[0]][0],
                    "type": "small"
                })
                
        # Deduplicate
        # for i in resultsList:
        #     print(i)    
        #     if any(o["name"] == i["name"] for o in resultsList):
        #         resultsList.remove(i)
                
        return resultsList
    
