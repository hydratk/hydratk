from multiprocessing import Process, Pipe, Value, current_process
from time import sleep, time
from zmq import Context, PUSH, PULL, POLLIN, NOBLOCK, Poller
from base64 import b64encode
from pickle import dumps


class CB():

    def __init__(self, fn_id=None, args=None, kwargs=None):

        self.fn_id = fn_id
        self.args = args
        self.kwargs = kwargs

    def loop(self):

        while (True):
            sleep(1)


def dummy_method(self, *args, **kwargs):

    return True


def init_process(method='loop', cmd='PING', th=None):

    parent_conn, child_conn = Pipe()
    if (method == 'loop'):
        method, args = loop, ()
    elif (method == 'send_pipe'):
        method, args = send_pipe, (child_conn, cmd)
    elif (method == 'recv_pipe'):
        method, args = recv_pipe, (child_conn, th)
    elif (method == 'send_mq'):
        method, args = send_mq, (th,)
    elif (method == 'receive_mq'):
        method, args = receive_mq, ()

    p = Process(target=method, args=args)
    p.pipe_conn = parent_conn
    p.last_ping = time()
    p.last_ping_response = 0
    p.next_check_time = time() + 20
    p.next_ping_time = time() + 20
    p.response_alert_level = 0
    p.status = Value('i', 3)
    p.action_status = Value('i', 0)
    p.is_alive_check = Value('d', time())
    p.num = 1

    p.start()
    return p


def kill_process(p):

    p.terminate()
    p.join()


def loop(*args):

    while (True):
        sleep(1)


def send_pipe(conn, cmd='PING'):

    msg = {}
    if (cmd == 'PING'):
        msg = {'zone': 'Core', 'type': 1, 'command': 10}
    elif (cmd == 'PONG'):
        msg = {'zone': 'Core', 'type': 2, 'command': 11, 'time': time()}
    conn.send(msg)


def recv_pipe(conn, th):

    current_process().pipe_conn = conn
    while (True):
        th._check_cw_privmsg()
        sleep(0.5)


def send_mq(th):

    init_sender(th)
    sleep(1)
    curr = current_process()
    print('sending message')
    msg = create_message()
    curr.msgq.send(msg)

    while (True):
        sleep(1)


def receive_mq():

    init_receiver()
    curr = current_process()

    while (True):
        msg = curr.msgq.recv()
        print('received message {0}'.format(msg))
        sleep(1)


def init_sender(th):

    curr = current_process()
    th._msg_router = None
    th._init_message_router()
    th._core_msg_service_id = 'c01'
    th._msg_router.register_service(
        'c01', 1, {'address': '/tmp/hydratk/core.socket'})
    context = Context()
    sender = context.socket(PUSH)
    sender.bind('ipc:///tmp/hydratk/core.socket')
    curr.msgq = sender


def init_receiver():

    curr = current_process()
    curr.action_status = Value('i', 0)
    context = Context()
    receiver = context.socket(PULL)
    receiver.connect('ipc:///tmp/hydratk/core.socket')
    curr.msgq = receiver
    #poller = Poller()
    #poller.register(receiver, POLLIN)
    #curr.poller = poller


def create_message(msg={'test': 'test'}):

    return b64encode(dumps(msg))
