from common import print_info
from ob_globals import TaskParams
from sg_appmodes import print_appmodes
from sg_events import print_task_events

import colorama
from colorama import Fore, Back, Style


SchTypes = {
    "NON" : "NON_PREMPTIVE",
    "FULL" : "PREMPTIVE_TSK"
}

OsTaskType_str = "\n\ntypedef void (*TaskFuncType)(void);\n\
\n\
typedef struct {\n\
    TaskType id;\n\
    TaskFuncType handler;\n\
    u32 priority;\n\
    u8 sch_type;\n\
    u32 activation;\n\
    bool autostart;\n\
    const AppModeType** app_modes;\n\
    u32 n_app_modes;\n\
    MessageType** msg;\n\
    u32 n_msg;\n\
    ResourceType** res;\n\
    u32 n_res;\n\
    const EventMaskType** evt_msk;\n\
    u32 n_evt;\n\
} OsTaskType;\n\
\n\
extern const OsTaskType OsTaskList[];\n\n"


def print_task_ids(hf, Tasks):
    hf.write("\n\nenum eTaskType {\n")
    for task in Tasks:
        hf.write("\tTASK_"+task[TaskParams[0]].upper()+"_ID,\n")
    hf.write("\tTASK_ID_MAX\n")
    hf.write("};\n")


def print_task_len_macros(hf, Tasks):
    hf.write("\n\n")
    for task in Tasks:
        # app_modes
        if "AUTOSTART_APPMODE" in task:
            hf.write("#define "+task[TaskParams[0]].upper()+"_APPMODE_MAX\t("+
                str(len(task["AUTOSTART_APPMODE"]))+")\n")
        else:
            hf.write("#define "+task[TaskParams[0]].upper()+"_APPMODE_MAX\t(0)\n")

        # msg, res, evt
        for i in range(5, 8):
            if TaskParams[i] in task:
                hf.write("#define "+task[TaskParams[0]].upper()+"_"+TaskParams[i]+"_MAX\t("+
                    str(len(task[TaskParams[i]]))+")\n")
            else:
                hf.write("#define "+task[TaskParams[0]].upper()+"_"+TaskParams[i]+"_MAX\t(0)\n")

        # end of for loop
        hf.write("\n")


def generate_code(path, Tasks, AppModes):
    print_info("Generating code for Tasks")

    # create header file
    filename = path + "/" + "sg_tasks.h"
    hf = open(filename, "w")
    hf.write("#ifndef ACN_OSEK_SG_TASKS_H\n")
    hf.write("#define ACN_OSEK_SG_TASKS_H\n")
    hf.write("\n#include <osek.h>\n")
    hf.write("#include <osek_com.h>\n")
    #print_appmode_enum(hf, AppModes)
    print_task_ids(hf, Tasks)
    print_task_len_macros(hf, Tasks)
    hf.write(OsTaskType_str)

    # create source file
    filename = path + "/" + "sg_tasks.c"
    cf = open(filename, "w")
    cf.write("#include <stddef.h>\n")
    cf.write("#include \"sg_tasks.h\"\n")
    cf.write("#include \"sg_appmodes.h\"\n")
    cf.write("#include \"sg_events.h\"\n")
    cf.write("\n\n/*   T A S K   D E F I N I T I O N   */\n")
    print_appmodes(path, Tasks, AppModes)
    print_task_events(path, Tasks)
    #print_task_messages(hf, cf, Tasks)
    cf.write("\nconst OsTaskType OsTaskList["+str(len(Tasks))+"] = {\n")
    for i, task in enumerate(Tasks):
        cf.write("\t{\n")
        # Init AppModes
        if "AUTOSTART_APPMODE" in task:
            cf.write("\t\t.app_modes = (const AppModeType **) &"+task[TaskParams[0]]+"_AppModes,\n")
        else:
             cf.write("\t\t.app_modes = NULL,\n")
        cf.write("\t\t.n_app_modes = "+task[TaskParams[0]].upper()+"_APPMODE_MAX,\n")
        # Init EventMasks
        if TaskParams[6] in task:
            cf.write("\t\t.evt_msk = (const EventMaskType**) &"+task[TaskParams[0]]+"_EventMasks,\n")
        else:
             cf.write("\t\t.evt_msk = NULL,\n")
        cf.write("\t\t.n_evt = "+task[TaskParams[0]].upper()+"_EVENT_MAX\n")
        cf.write("\t}")
        if i+1 < len(Tasks):
            cf.write(",\n")
        else:
            cf.write("\n")
    cf.write("};\n")

    # Tasks is still in construction hence print it
    print(Tasks)
    print("\nTASKs in construction\n\n")

    cf.close()
    hf.write("\n\n#endif\n")
    hf.close()