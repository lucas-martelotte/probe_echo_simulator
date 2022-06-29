from config import get_port_by_process_id
import rpyc

if __name__=='__main__':

    print('Ready to start election.')
    print('Please type the number of the node to start the election.')
    print('Type \"N\" to exit.')

    node = input()

    if node == 'N':
        exit()

    conn = rpyc.connect('localhost', get_port_by_process_id(int(node)))
    result = conn.root.exposed_election()
    conn.close()

    print(f'Election is done.\nLeader is node {result}.')