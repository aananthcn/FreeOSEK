from common import print_info
from ob_globals import CntrParams

import colorama
from colorama import Fore, Back, Style


C_Counter_Type = "\n\ntypedef struct {\n\
    AlarmBaseType alarm; /* contains OSEK specified attributes */ \n\
    TickType countval; /* continuos incrementing counter */ \n\
    TickType tickduration; /* count in nano seconds */\n\
    char* name;\n\
} OsCounterType;\n\n"

def cntr_macro_name(txt):
    return str(txt).upper()+"_INDEX"

def generate_code(path, Counters):
    print_info("Generating code for counters")
    os_counter_index = -1
    os_counter_duration = -1

    # create header file
    filename = path + "/" + "sg_counter.h"
    hf = open(filename, "w")
    hf.write("#ifndef ACN_OSEK_SG_COUNTER_H\n")
    hf.write("#define ACN_OSEK_SG_COUNTER_H\n")
    hf.write("#include <osek.h>\n")
    hf.write(C_Counter_Type)
    hf.write("extern OsCounterType _OsCounters[];\n")

    # create source file
    filename = path + "/" + "sg_counter.c"
    cf = open(filename, "w")
    cf.write("#include \"sg_counter.h\"\n")
    cf.write("\n\nOsCounterType _OsCounters[] =  {\n")
    for i, cntr in enumerate(Counters):
        cf.write("\t{\n")
        cf.write("\t\t.alarm.mincycle = "+ str(cntr[CntrParams[1]]) + ",\n")
        cf.write("\t\t.alarm.maxallowedvalue = "+ str(cntr[CntrParams[2]]) + ",\n")
        cf.write("\t\t.alarm.ticksperbase = "+ str(cntr[CntrParams[3]]) + ",\n")
        cf.write("\t\t.tickduration = "+ str(cntr[CntrParams[4]]) + ",\n")
        cf.write("\t\t.name = \""+ cntr[CntrParams[0]] + "\"\n")
        cf.write("\t}")
        if i+1 == len(Counters):
            cf.write("\n")
        else:
            cf.write(",\n")
        
        # Find out if this Counter is optimal for OS Tick scheduling
        if int(cntr[CntrParams[4]]) >= 1000000: #nano sec
            if os_counter_duration == -1:
                os_counter_duration = cntr[CntrParams[4]]
                os_counter_index = i
            elif int(cntr[CntrParams[4]]) < os_counter_duration: 
                os_counter_duration = cntr[CntrParams[4]]
                os_counter_index = i

    cf.write("};\n")
    # close source file
    cf.close()

    # create counter index macros
    hf.write("\n")
    for i, cntr in enumerate(Counters):
        hf.write("\n#define "+cntr_macro_name(cntr[CntrParams[0]])+"   \t("+str(i)+")")
    hf.write("\n\n")


    # close header file
    if os_counter_duration == -1 or os_counter_index == -1:
        print(Fore.YELLOW+"\nWarning: None of the counter is (>= 1ms) is fit for OS tick timer!\n" +
            "Please check the OSEK-Builder.xlsx and configure COUNTER correctly!\n"+Style.RESET_ALL)
    else:
	    hf.write("\n#define OS_TICK_DURATION_ns \t("+str(os_counter_duration)+")")
	    hf.write("\n#define OS_TICK_COUNTER_IDX \t("+str(os_counter_index)+")")
    hf.write("\n#define OS_MAX_COUNTERS    \t("+str(len(Counters))+")\n")
    
    hf.write("\n\n#endif\n")
    hf.close()
