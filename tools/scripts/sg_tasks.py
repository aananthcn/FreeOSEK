from common import print_info
from ob_globals import TaskParams, TNMI, EVTI, MSGI, ATSI, RESI, ACTI, SCHI, PRII

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
    u32 activations;\n\
    bool autostart;\n\
    const AppModeType** appmodes;\n\
    u32 n_appmodes;\n\
    MessageType** msglist;\n\
    u32 n_msglist;\n\
    ResourceType** reslist;\n\
    u32 n_reslist;\n\
    const EventMaskType** evtmsks;\n\
    u32 n_evtmsks;\n\
} OsTaskType;\n\
\n\
extern const OsTaskType OsTaskList[];\n\n"


def print_task_ids(hf, Tasks):
    hf.write("\n\nenum eTaskType {\n")
    for task in Tasks:
        hf.write("\tTASK_"+task[TaskParams[TNMI]].upper()+"_ID,\n")
    hf.write("\tTASK_ID_MAX\n")
    hf.write("};\n")


def print_task_len_macros(hf, Tasks):
    hf.write("\n\n")
    for task in Tasks:
        # app_modes
        if "AUTOSTART_APPMODE" in task:
            hf.write("#define "+task[TaskParams[TNMI]].upper()+"_APPMODE_MAX\t("+
                str(len(task["AUTOSTART_APPMODE"]))+")\n")
        else:
            hf.write("#define "+task[TaskParams[TNMI]].upper()+"_APPMODE_MAX\t(0)\n")

        # msg, res, evt
        for i in range(5, 8):
            if TaskParams[i] in task:
                hf.write("#define "+task[TaskParams[TNMI]].upper()+"_"+TaskParams[i]+"_MAX\t("+
                    str(len(task[TaskParams[i]]))+")\n")
            else:
                hf.write("#define "+task[TaskParams[TNMI]].upper()+"_"+TaskParams[i]+"_MAX\t(0)\n")

        # end of for loop
        hf.write("\n")


def generate_code(path, Tasks):
    print_info("Generating code for Tasks")

    # create header file
    filename = path + "/" + "sg_tasks.h"
    hf = open(filename, "w")
    hf.write("#ifndef ACN_OSEK_SG_TASKS_H\n")
    hf.write("#define ACN_OSEK_SG_TASKS_H\n")
    hf.write("\n#include <osek.h>\n")
    hf.write("#include <osek_com.h>\n")
    print_task_ids(hf, Tasks)
    print_task_len_macros(hf, Tasks)
    hf.write(OsTaskType_str)
    hf.write("\n#define OS_TASK(task)    (OSEK_Task_##task)\n")

    # create source file
    filename = path + "/" + "sg_tasks.c"
    cf = open(filename, "w")
    cf.write("#include <stddef.h>\n")
    cf.write("#include <stdbool.h>\n")
    cf.write("#include \"sg_tasks.h\"\n")
    cf.write("#include \"sg_appmodes.h\"\n")
    cf.write("#include \"sg_events.h\"\n")
    cf.write("#include \"sg_messages.h\"\n")
    cf.write("#include \"sg_resources.h\"\n")
    cf.write("\n\n/*   T A S K   D E F I N I T I O N S   */\n")
    cf.write("const OsTaskType OsTaskList[] = {\n")
    for i, task in enumerate(Tasks):
        cf.write("\t{\n")

        # TaskID, Declarations of tasks and Init tasks
        ##hf.write("\n#define "+task[TaskParams[TNMI]]+" OSEK_Task_"+task[TaskParams[TNMI]])
        hf.write("\nDeclareTask("+task[TaskParams[TNMI]]+");")
        cf.write("\t\t.handler = OS_TASK("+task[TaskParams[TNMI]]+"),\n")
        cf.write("\t\t.id = "+str(i)+",\n")

        # Init Schedule Type, priority
        cf.write("\t\t.sch_type = "+task[TaskParams[SCHI]]+"_PREEMPTIVE,\n")
        cf.write("\t\t.priority = "+task[TaskParams[PRII]]+",\n")

        # Init Activations
        cf.write("\t\t.activations = "+task[TaskParams[ACTI]]+",\n")

        # Init Autostart
        cf.write("\t\t.autostart = "+task[TaskParams[ATSI]].lower()+",\n")

        # Init AppModes
        if "AUTOSTART_APPMODE" in task:
            cf.write("\t\t.appmodes = (const AppModeType **) &"+task[TaskParams[TNMI]]+"_AppModes,\n")
        else:
             cf.write("\t\t.appmodes = NULL,\n")
        cf.write("\t\t.n_appmodes = "+task[TaskParams[TNMI]].upper()+"_APPMODE_MAX,\n")

        # Init EventMasks
        if TaskParams[EVTI] in task:
            cf.write("\t\t.evtmsks = (const EventMaskType**) &"+task[TaskParams[TNMI]]+"_EventMasks,\n")
        else:
             cf.write("\t\t.evtmsks = NULL,\n")
        cf.write("\t\t.n_evtmsks = "+task[TaskParams[TNMI]].upper()+"_EVENT_MAX,\n")

        # Init Messages
        if TaskParams[MSGI] in task:
            cf.write("\t\t.msglist = (MessageType**) &"+task[TaskParams[TNMI]]+"_Messages,\n")
        else:
            cf.write("\t\t.msglist = NULL,\n")
        cf.write("\t\t.n_msglist = "+task[TaskParams[TNMI]].upper()+"_MESSAGE_MAX,\n")

        # Init Resources
        if TaskParams[RESI] in task:
            cf.write("\t\t.reslist = (ResourceType**) &"+task[TaskParams[TNMI]]+"_Resources,\n")
        else:
            cf.write("\t\t.reslist = NULL,\n")
        cf.write("\t\t.n_reslist = "+task[TaskParams[TNMI]].upper()+"_RESOURCE_MAX\n")

        cf.write("\t}")
        if i+1 < len(Tasks):
            cf.write(",\n")
        else:
            cf.write("\n")
    cf.write("};\n")
    cf.close()
    hf.write("\n\n#endif\n")
    hf.close()
