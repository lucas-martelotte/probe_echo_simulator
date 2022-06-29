#==================================#
#======= EDITABLE VARIABLES =======#
#==================================#

BASE_PORT = 1000
ADJACENCY_LIST_PATH = './adjacency_list.txt'

#==================================#
#========= NO TOUCH AREA ==========#
#==================================#

def get_port_by_process_id(process_id):
    global BASE_PORT
    return BASE_PORT + process_id
