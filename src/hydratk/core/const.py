# -*- coding: utf-8 -*-
"""HydraTK constants

.. module:: core.const
   :platform: Unix
   :synopsis: HydraTK constants
.. moduleauthor:: Petr Czaderna <pc@hydratk.org>

"""

''' Application metadata '''
APP_NAME               = "HydraTK"
APP_VERSION            = "0.3.0a.dev1"
APP_REVISION           = ""
APP_DEVEL_YEAR         = "2009 - 2016"
APP_AUTHORS            = "Petr Czaderna <pc@hydratk.org>, HydraTK Team"
CP_STRING              = "(c) "+ APP_DEVEL_YEAR +" "+ APP_AUTHORS

''' Default configuration '''  
CONFIG_FILE            = "/etc/hydratk/hydratk.conf"
EXT_CONFIG_DIR         = "/etc/hydratk/conf.d"
NUM_CORE_THREADS       = 4
DEFAULT_LANGUAGE       = "en"
DEBUG_LEVEL            = 1
DEBUG_CHANNEL          = [1,10]
DEFAULT_RUN_MODE       = 1

''' Core running mode '''
CORE_RUN_MODE_SINGLE_APP = 1
CORE_RUN_MODE_PP_APP     = 2
CORE_RUN_MODE_PP_DAEMON  = 3

core_run_mode_enum_desc = {
    CORE_RUN_MODE_SINGLE_APP : 'CORE_RUN_MODE_SINGLE_APP',
    CORE_RUN_MODE_PP_APP     : 'CORE_RUN_MODE_PP_APP',
    CORE_RUN_MODE_PP_DAEMON  : 'CORE_RUN_MODE_PP_DAEMON'
}
 
''' Core thread activity statuses '''
CORE_THREAD_EXIT       = 0
CORE_THREAD_ALIVE      = 1
CORE_THREAD_WAIT       = 2
CORE_THREAD_WORK       = 3

''' Core thread action statuses '''
CORE_THREAD_ACTION_NONE            = 0
CORE_THREAD_ACTION_PROCESS_PRIVMSG = 1
CORE_THREAD_ACTION_PROCESS_MSG     = 2

''' Core thread misc constants '''
CORE_THREAD_ACTIVITY_CHECK_TIME = 10
CORE_THREAD_PING_TIME           = 20
CORE_OBSERVER_SLEEP_TIME        = 1
CORE_THREAD_SLEEP_TIME          = 0.5
CORE_THREAD_NORESPONSE          = 3 

''' Messages '''
MSG_PRIORITY_URGENT    = 0
MSG_PRIORITY_HIGH      = 1
MSG_PRIORITY_MEDIUM    = 2
MSG_PRIORITY_LOW       = 3

APP_STATUS_STOP        = 0
APP_STATUS_START       = 1
APP_STATUS_RUNNING     = 2

''' Application services '''
SERVICE_STATUS_STOPPED = 0
SERVICE_STATUS_STARTED = 1  

''' Processes '''
PROCESS_JOIN_TIMEOUT = 10

'''Run Workflow levels '''
RUNLEVEL_SHUTDOWN   = 0
RUNLEVEL_BASEINIT   = 1
RUNLEVEL_CONFIG     = 2
RUNLEVEL_EXTENSIONS = 3 
RUNLEVEL_CLI        = 4
RUNLEVEL_CORE       = 5          
RUNLEVEL_APPL       = 6

''' Events '''
EVENT_HOOK_PRIORITY = 50
            

