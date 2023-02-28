import os
import json
import xmltodict
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

def get_headers(token=os.getenv('token-value',"None")):

    headers = {
        'Authorization': 'Bearer {}'.format(token),
    }
    return headers

def get_projectinfo(url="https://teamcity.duckcreek.com",suburl="/app/rest/projects/id:_Root"):
    print("\n-----------API_Called------------\n")
    print(url+suburl)
    
    try:
        response = requests.get(url+suburl, headers=get_headers(),verify=False)
        response.raise_for_status()
        return json.dumps(xmltodict.parse(response.content), indent=2)
    except requests.exceptions.HTTPError as err :
        return err


if __name__== '__main__':

    teamcity_url = os.getenv('server-url',"https://teamcity.duckcreek.com")

    project_data = json.loads(get_projectinfo(url=teamcity_url,suburl = "/app/rest/projects"))

    projects_details = []

    project_count = 0

    for project in project_data["projects"]["project"]:

        projectfilter_data = {
                "project_id":"",
                "project_parentId":"",
                "project_webUrl":"",
                "latest_build_id":"",
                "latest_build_number":"",
                "latest_build_status":"",
                "latest_build_finish_date":"",
                "latest_build_finish_time":"",
                                
            }

        projectfilter_data["project_name"] = project["@name"]
        projectfilter_data["project_id"] = project["@id"]
        projectfilter_data["project_webUrl"] = project["@webUrl"]
        if project["@id"] == "_Root":
            continue
        projectfilter_data["project_parentId"] = project["@parentProjectId"]
        latest_build_url = "/app/rest/builds?locator=project:{},running:any,count:1".format(project["@id"])
        latest_build_data = get_projectinfo(url=teamcity_url,suburl=latest_build_url)
        if "404" in str(latest_build_data):
            projectfilter_data["latest_build_id"]="NA"
            projectfilter_data["latest_build_number"] = "NA"
            projectfilter_data["latest_build_status"] = "NA"
            projectfilter_data["latest_build_finish_time"] = "NA"
        else:
            latest_build_data = json.loads(latest_build_data)["builds"]
            count = latest_build_data["@count"]
            if count == "0":
                projectfilter_data["latest_build_id"]="NA"
                projectfilter_data["latest_build_number"] = "NA"
                projectfilter_data["latest_build_status"] = "NA"
                projectfilter_data["latest_build_finish_time"] = "NA"
                projectfilter_data["latest_build_finish_date"] = "NA"
            else:
                projectfilter_data["latest_build_id"]= latest_build_data["build"]["@id"]
                projectfilter_data["latest_build_number"] = latest_build_data["build"]["@number"]
                latest_build_state = latest_build_data["build"]["@state"]
                if latest_build_state == "running":
                    projectfilter_data["latest_build_finish_time"] = datetime.strptime('000000', '%H%M%S').time().isoformat()
                    projectfilter_data["latest_build_finish_date"] = datetime.strptime('99991231', '%Y%m%d').date().isoformat()
                    projectfilter_data["latest_build_status"] = "RUNNING"
                else:
                    projectfilter_data["latest_build_status"] = latest_build_data["build"]["@status"]
                    projectfilter_data["latest_build_finish_date"] = datetime.strptime(latest_build_data["build"]["finishOnAgentDate"].split("T")[0],"%Y%m%d").date().isoformat()
                    projectfilter_data["latest_build_finish_time"] = datetime.strptime(latest_build_data["build"]["finishOnAgentDate"].split("T")[1].split("+")[0],"%H%M%S").time().isoformat()
        projects_details.append(projectfilter_data)

        with open("project_details.json", "r+") as json_file:
            file_data = json.load(json_file)
            file_data.append(projectfilter_data)
            json_file.seek(0)
            json.dump(file_data,json_file,indent=2, default=str)
        
        project_count= project_count + 1
        print("\n--------------- DONE FOR {} projects -------------\n".format(project_count))
    