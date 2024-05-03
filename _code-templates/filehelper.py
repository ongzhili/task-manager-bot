import os

class FileHelper:
    def __init__(self, file_path, uuid):
        if not isinstance(file_path, str):
            print("[!] Something is very wrong, file_path is not a string! Perhaps someone is trying to pwn?")
        self.file_path = file_path
        self.uuid = uuid

    def read(self):
        try:
            with open(self.file_path+self.uuid+".txt", "r") as f:
                file_contents = f.read()
                if file_contents == "":
                    f.close()
                    return []
                else:
                    f.close()
                    return file_contents.split("|")
        except FileNotFoundError:
            f.close()
            return []

    def append(self, string):
        with open(self.file_path+self.uuid+".txt", "a+") as f:
            f.seek(0, os.SEEK_SET)
            if f.read() == "":
                f.seek(0, os.SEEK_END)
                f.write(string)
                f.close()
            else:
                f.seek(0, os.SEEK_END)
                f.write("|"+string)
                f.close()
        return

    def delete(self, index):
        with open(self.file_path+self.uuid+".txt", "r+") as f:
            file_contents = f.read()
            if file_contents == "" or file_contents is None:
                raise LookupError("File is already empty!")
            else:
                task_arr = file_contents.split("|")
                print(task_arr)
                try:
                    task_arr.pop(index)
                    new_string = ""
                    if len(task_arr) > 0 and task_arr[0] != "":
                        for task in task_arr:
                            new_string += task + "|"
                        f.seek(0, os.SEEK_SET)
                        f.truncate(0)
                        f.write(new_string.rstrip("|"))
                        f.close()
                    else:
                        f.truncate(0)
                    return 0
                except IndexError:
                    return 1