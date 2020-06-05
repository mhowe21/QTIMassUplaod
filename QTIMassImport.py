import requests
import zipfile
import os
import json


class userInput():
    def userRestToken(self):
        userToken = str(input("enter your token: ").replace(" ", ""))
        return userToken

    def canvasInstance(self):
        userToken = str(input("enter your Canvas Instance: ").replace(" ", ""))
        return userToken

    def canvasCourse(self):
        canvasCourseID = str(
            input("enter the Canvas course ID: ").replace(" ", ""))
        return canvasCourseID

    def pathToZip(self):
        with zipfile.ZipFile("QuizFiles.zip", "r") as z:
            print("extracting...")
            if os.path.exists("extractedFiles") == False:
                os.makedirs("extractedFiles")
            z.extractall("extractedFiles", members=None, pwd=None)


class directoryHandle():
    def readExtractedFolder(self):
        # filesList = os.listdir("extractedFiles")
        # return filesList
        fileList = []
        for fileName in os.listdir("extractedFiles"):
            if fileName.endswith(".zip"):

                fileList.append(os.path.join("extractedFiles", fileName))
            else:
                continue
        return fileList


class restCalls():
    def firstImportRequest(self, Instance, courseID, token, fileName):
        url = ("https://" + Instance + ".instructure.com/api/v1/courses/" +
               courseID + "/content_migrations")

        payload = {'migration_type': 'qti_converter',
        'pre_attachment[name]': fileName,
        'settings[overwrite_quizzes]': 'false'}

        headers = {
        'Authorization': 'Bearer ' + token, }

        response = requests.request("POST", url, headers=headers, data=payload)
        jsonData = response.json()
        # print(response.text.encode('utf8'))
        return jsonData

    def AWSFileUpload(self, firstResponse, fileName):
        uploadURL = firstResponse["pre_attachment"]["upload_url"]
        url= uploadURL
        payload = {}
        files = [('filename', open(fileName,'rb'))]
        headers = {}
        response = requests.request("POST", url, headers=headers, data = payload, files = files)
        print(response.text.encode('utf8'))


def main():
    userIn=userInput()
    userIn.pathToZip()
    token=userIn.userRestToken()
    instance=userIn.canvasInstance()
    course=userIn.canvasCourse()

    DH=directoryHandle()
    Flist=DH.readExtractedFolder()
    rest=restCalls()
    
    for fileName in Flist:
        firstCall=rest.firstImportRequest(instance, course, token, fileName)
        rest.AWSFileUpload(firstCall, fileName)





if __name__ == "__main__":
    main()
