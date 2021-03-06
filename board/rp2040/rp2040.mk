COMPILER=arm-none-eabi-
CC=${COMPILER}gcc
LD=${COMPILER}ld
AS=${COMPILER}as
OBJCOPY=${COMPILER}objcopy
BOARD_NAME=rp2040

CC_VERS := $(shell ${CC} -dumpfullversion)
ifeq ($(OS),Windows_NT)
LIB_GCC_A_PATH=${MINGW_ROOT}/lib/gcc/arm-none-eabi/${CC_VERS}/thumb/v6-m/nofp/
else
LIB_GCC_A_PATH=/usr/lib/gcc/arm-none-eabi/${CC_VERS}/thumb/v6-m/nofp/
endif

INCDIRS  := -I ${CWD}/include \
            -I ${CWD}/include/arch/aarch32/ \
	    -I ${CWD}/board/${BOARD_NAME} \
	    -I ${CWD}/lib/include
	    

LDFLAGS  += -nostdlib -g -L${LIB_GCC_A_PATH} -lgcc
CFLAGS   += -Werror ${INCDIRS} -g
ASFLAGS  += ${INCDIRS} -g 

$(info compiling ${BOARD_NAME} board specific files)
CFLAGS  += -mthumb -mthumb-interwork -march=armv6-m -mcpu=cortex-m0plus
LDFILE	:= ${CWD}/board/${BOARD_NAME}/${BOARD_NAME}.lds
LDFLAGS += -mthumb -mthumb-interwork -marmelf  -T ${LDFILE}


STDLIBOBJS	:= \
	lib/libc-minimal/stdlib/abort.o \
	lib/libc-minimal/stdlib/atoi.o \
	lib/libc-minimal/stdlib/bsearch.o \
	lib/libc-minimal/stdlib/exit.o \
	lib/libc-minimal/stdlib/strtol.o \
	lib/libc-minimal/stdlib/strtoul.o \
	lib/libc-minimal/stdout/fprintf.o \

#	lib/libc-minimal/stdlib/malloc.o \


LIBOBJS	:= \
	lib/libc-minimal/string/string.o \
	lib/libc-minimal/stdout/printf.o
	

BRD_OBJS := \
	${CWD}/board/rp2040/boot_stage2.o \
	${CWD}/board/rp2040/board.o \
	${CWD}/board/rp2040/vector_handlers.o \
	${CWD}/board/rp2040/vectors.o \
	${CWD}/board/rp2040/interrupt.o \
	${CWD}/board/rp2040/startup.o \
	${CWD}/board/rp2040/bootrom.o 


