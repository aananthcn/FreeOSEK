#ifndef ACN_OSEK_SG_ALARMS_H
#define ACN_OSEK_SG_ALARMS_H
#include <osek.h>


typedef enum {
    AAT_ACTIVATETASK,
    AAT_SETEVENT,
    AAT_ALARMCALLBACK,
    AAT_MAX_TYPE
} AlarmActionType;


typedef struct {
    char* name;                     /* short name of alarm */ 
    AlarmType cntr_id;              /* OS Counter ID (= index of OsCounters + 1) */ 
    TickType* pacntr;               /* pointer to AppAlarmCounters */ 
    TickType* pcycle;               /* pointer to AppAlarmCycle */ 
    bool* palrm_state;              /* pointer to the state of AppAlarmCounters */ 
    AlarmActionType aat;            /* Refer enum AlarmActionType */ 
    void* aat_arg1;                 /* arg1: task_name | callback_fun */
    void* aat_arg2;                 /* arg2: event | NULL */
    bool is_autostart;              /* does this alarm start at startup? */
    u32 alarmtime;                  /* when does it expire? */
    u32 cycletime;                  /* cyclic time - for repetition */
    const AppModeType* appmodes;    /* alarm active in which modes? */
    u32 n_appmodes;                 /* how may appmodes for this entry? */
} AppAlarmType;

extern const AppModeType Alarm_WakeTaskA_AppModes[];


typedef struct {
    const AppAlarmType* alarm;
    u32 len;
} AppAlarmCtrlBlockType;


#define MAX_APP_ALARMS  (2)
extern const AppAlarmCtrlBlockType AppAlarms[MAX_APP_ALARMS];
#define MAX_APP_ALARM_COUNTERS    (3)
extern TickType AppAlarmCounters[MAX_APP_ALARM_COUNTERS];
extern TickType AppAlarmCycles[MAX_APP_ALARM_COUNTERS];
extern bool AppAlarmStates[MAX_APP_ALARM_COUNTERS];


extern void Alarm_uSecAlarm_callback(void);

extern const AlarmType AlarmID2CounterID_map[];

#endif
