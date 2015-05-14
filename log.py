from time import gmtime, strftime
import os

#You will find a fully updated version of this script at https://github.com/WilliamCipriano/log

#find local path, should still work if py2exe is used.
path = os.path.dirname(__file__).replace('\\library.zip','')

#default log location
log_default = 'log.html'
log_path = path + '\logs\\'

#Program details (these are just placed at the start of the log file, might help with version tracking etc)
app_name = 'OpenDental-Patient-Reminder'
app_version = '0.0.1 Alpha'
app_author = 'Will Cipriano'
app_email = 'logs@wfc.help'
email_subject = 'OpenDental-Patient-Reminder Error (Please Include All Logs)'

#attempt to grab system info, might be useful in debuging if user only sends you the log file. This is designed to fail softly to allow logging to continue.
#side note: ship your program without any logs inside of the log file dir so it will be populated by this information.
def system_info():
    try:
        import platform
        type = platform.machine()
        name = platform.node()
        processor = platform.processor()
        python_build_date = platform.python_build()[1]
        python_compiler = platform.python_compiler()
        python_release = platform.release()
        system_os = platform.system()
        timezone = strftime("%z", gmtime())
        html = "<I><center><h3>System Info</h3></I>"
        html += "Type: " + type + "<br>\n"
        html += "Hostname: " + name + "<br>\n"
        html += "Processor: " + processor + "<br>\n"
        html += "Python Build Date: " + python_build_date + "<br>\n"
        html += "Python Compiler: " + python_compiler + "<br>\n"
        html += "Python Release: " + python_release + "<br>\n"
        html += "System OS: " + system_os + "<br>\n"
        html += "Timezone: " + timezone + "<br></center>\n"
        html += "<HR>\n"
    except Exception as ex:
        html = '\n<br><font color="red">CRITICAL ERROR: Failed to load system information: "' + ex + '"</font><br>\n'
    return html


def check_path(path):
    if not os.path.exists(path):
        os.makedirs(path)

def check_file(path, file):
    time = strftime("%Y-%m-%d %H:%M:%S")
    if os.path.isfile(path + file) == False:
        f = open(path + file, 'a')
        html = "<HEAD><TITLE>" + app_name + " log</TITLE><HEAD>\n"
        html += "<center><H2>" + app_name + " Log file</H2><br>\n"
        html += "originally created: " + time + "<br>\n"
        html += "version: " + app_version + "<br>\n"
        html += "author: " + app_author + "<br>\n"
        html += "contact: <a href='mailto:" + app_email + "?Subject=" + email_subject + "'>" + app_email + "</a></center>\n\n"
        html += "<hr>"
        f.write(html)
        f.write(system_info())
        f.close()
        return False
    return True

def write(message, critcal = False,file = False):
    #Get current time/date.
    time = strftime("%Y-%m-%d %H:%M:%S")

    #Create log text, and set critical flag.
    if critcal:
        log = "<B><font color = 'red'>! " + str(time) + " !</B></font> [" + str(message) + "] <br>\n"
    else:
        log = '| ' + str(time) + ' | [' + str(message) + '] <br>\n'

    #Check path and create if needed.
    check_path(log_path)

    #Check file then open it, using location defined by function call if defined.
    if file == False:
        check_file(log_path, log_default)
        f = open(log_path + log_default, 'a')
    else:
        check_file(log_path, file)
        f = open(log_path + file, 'a')

    #Write a close file.
    f.write(log)
    f.close()
