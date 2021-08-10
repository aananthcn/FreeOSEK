#include <stdio.h>
#include <board.h>
#include <osek.h>

#include <os_api.h>
#include <os_fifo.h>
#include <os_task.h>

#include <sg_appmodes.h>
#include <sg_tasks.h>
#include <sg_fifo.h>
#include <os_api.h>


int OsAppMode;

int SetActiveApplicationMode(AppModeType mode) {
	if (mode >= OS_MODES_MAX) {
		pr_log("Error: Invalid mode! New mode %d > MAX (%d)\n", mode, OS_MODES_MAX);
		return -1;
	}

	OsAppMode = mode;
	return 0;
}


AppModeType GetActiveApplicationMode(void) {
	return OsAppMode;
}


void StartOS(AppModeType mode) {
	pr_log("Entering %s.\n", __func__);
	SetActiveApplicationMode(mode);
	if (mode != OSDEFAULTAPPMODE) {
		pr_log("%s::%s(): Error: Invalid OS START mode!\n", __FILE__, __func__);
		pr_log("Info: Expected mode == %d mode, actual == %d!\n", 
			OSDEFAULTAPPMODE, mode);
		return;
	}
	
	SetupScheduler(mode);

	pr_log("Scheduler setup done! Scheduling Tasks Starts!\n");
	while (OsAppMode == OSDEFAULTAPPMODE) {
		ScheduleTasks();
	}
}


/*
 * This funtion runs in interrupt context, hence keep things as minimal as possible
 */
void SystemTickISR(void) {
	if (OsHandleTicks())
		pr_log("Error: OsHandleTicks return errors!\n");
}