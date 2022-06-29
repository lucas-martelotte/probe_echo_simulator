from rpyc.utils.server import ThreadedServer
from config import get_port_by_process_id
from node import Node
import rpyc

#====================================#
#============== SETUP ===============#
#====================================#

print('Please type the process id.')
# Object that will store all the information
# that is relevant to the algorithm.
node = Node(int(input()))
print(f'My PORT is: {get_port_by_process_id(node.process_id)}.')
print(f'My adjacency list is: {node.adjacency}.')

#====================================#
#============== CLIENT ==============#
#====================================#

class ProbEcho(rpyc.Service):

    def on_connect(self, conn):
        print(f'Connected: {conn}.')

    def on_disconnect(self, conn):
        print(f'Disconnected: {conn}.')

    def exposed_reset(self):
        global node
        node.reset()


    def exposed_echo(self, sender_process_id, sender_output):
        print(f'Received echo from node {sender_process_id}.')
        global node

        node.partial_output.append(sender_output)

        try:
            print(f'Removing node {sender_process_id} from children.')
            node.children.remove(sender_process_id)
            print(f'Current children: {node.children}.')
        except:
            print(f'Failed to remove {sender_process_id} from children {node.children}.')

    def exposed_probe(self, sender_process_id):
        global node

        if node.probe:
            return 'ACK'
        else:
            node.probe = True
            node.father_process_id = sender_process_id
            print(f'Received probe from {sender_process_id}. Node set to father.')
            return 'OK'

    def exposed_election(self):
        global node

        # Checking if this was called by the simulator or by another node
        # If the father's id is different from zero, then this node can't be the root,
        # so the election must've been called from another that father, which will be
        # removed from the adjacency list.
        if node.father_process_id != 0:
            print('An election has been started.')
            try:
                print(f'Removing {node.father_process_id} from adjacency {node.adjacency}.')
                node.adjacency.remove(node.father_process_id)
                print(f'Current adjacency: {node.adjacency}.')
                print(node.adjacency)
            except:
                print(f'ERROR: Failed to remove {node.father_process_id} ' +\
                      f'from adjacency {node.adjacency}.')
        # In this case, the election was started from the simulator,
        # so we'll update the node flags to reflect that.
        else:
            print('Starting election.')
            node.initial_node = True
            node.probe = True

        print('Calling probe to all adjacent nodes.')
        for neighbor in node.adjacency:

            conn = rpyc.connect('localhost', get_port_by_process_id(neighbor))
            res  = conn.root.exposed_probe(node.process_id)
            conn.close()

            # If the returned value is not ACK, calling election for that neighbor
            if res != 'ACK':
                print(f'Node {neighbor} answered OK. Adding it to the children list.')
                node.children.append(neighbor)

                print(f'Current children: {node.children}.')

                print(f'Calling election to node {neighbor}.')
                conn = rpyc.connect('localhost', get_port_by_process_id(neighbor))
                conn.root.exposed_election()
                conn.close()

        while True:
            # Waiting for the child nodes to finish their processing
            # Each time a child echoes this node, it will be removed
            # from the children list. When it's empty, this node will
            # echo as well.

            if node.children == []:
                node.partial_output.append(node.process_id)
                node.final_output = max(node.partial_output)

                if node.initial_node:
                    print(f'Election is over. Result: {node.final_output}')
                    return node.final_output

                conn = rpyc.connect('localhost', get_port_by_process_id(node.father_process_id))
                conn.root.exposed_echo(node.process_id, node.final_output)
                conn.close()

                print(f'Final output: {node.final_output}.\nReseting...')
                self.exposed_reset()
                break

#====================================#
#=============== MAIN ===============#
#====================================#

if __name__ == "__main__":
    server = ThreadedServer(ProbEcho, port=get_port_by_process_id(node.process_id))
    server.start()
