# -*- coding : utf-8 -*-
# @Time   : 2021/10/2 1:00
# @Author : goodli
# @File   : distribute.py
# @Project: Valley 山谷

import torch
import torch.distributed as dist
import torch.multiprocessing as mp
from datetime import timedelta
from valley.utils import comm


def _find_free_port():
    import socket

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Binding to port 0 will cause the OS to find an available port for us
    sock.bind(("", 0))
    port = sock.getsockname()[1]
    sock.close()
    # NOTE: there is still a chance the port could be taken by other processes.
    return port


def dist_launch(entry_func, cfg):
    world_size = cfg.LAUNCH.HOST_NUM * cfg.LAUNCH.GPU_PER_HOST

    if cfg.LAUNCH.DEBUG is False or world_size > 1:
        if cfg.LAUNCH.DIST_URL == 'localhost':
            port = _find_free_port()
            dist_url = f"127.0.0.1:{port}"
            cfg.merge_from_list(['cfg.LAUNCH.DIST_URL', dist_url])

        mp.spawn(_dist_worker,
                 nprocs=cfg.LAUNCH.GPU_PER_HOST,
                 args=(entry_func, cfg),
                 daemon=False),
    else:
        _dist_worker(0, entry_func, cfg) # easy for debug

        '''
        mp.spawn(_dist_worker,
                 nprocs=cfg.LAUNCH.GPU_PER_HOST,
                 args=(entry_func, cfg),
                 join=True,
                 daemon=False),
        '''


def _dist_worker(local_rank, entry_func, cfg):

    assert torch.cuda.is_available(), "cuda is not available."

    global_rank = cfg.LAUNCH.HOST_RANK * cfg.LAUNCH.GPU_PER_HOST + local_rank
    world_size = cfg.LAUNCH.HOST_NUM * cfg.LAUNCH.GPU_PER_HOST

    cfg.merge_from_list(['LAUNCH.LOCAL_RANK', local_rank,
                         'LAUNCH.GLOBAL_RANK', global_rank,
                         'LAUNCH.WORLD_SIZE', world_size])

    if torch.distributed.is_nccl_available():
        backend = 'nccl'
    else:
        backend = 'gloo'

    dist.init_process_group(backend=backend,
                            init_method=cfg.LAUNCH.DIST_URL,
                            rank=global_rank,
                            world_size=world_size,
                            timeout=timedelta(minutes=30))

    comm.synchronize()

    torch.cuda.set_device(local_rank)

    # Setup the local process group (which contains ranks within the same machine)
    assert comm._LOCAL_PROCESS_GROUP is None
    #num_machines = world_size // num_gpus_per_machine
    for i in range( cfg.LAUNCH.HOST_NUM):
        ranks_on_i = list(range(i * cfg.LAUNCH.GPU_PER_HOST, (i + 1) * cfg.LAUNCH.GPU_PER_HOST))
        pg = dist.new_group(ranks_on_i)
        if i == cfg.LAUNCH.HOST_RANK:
            comm._LOCAL_PROCESS_GROUP = pg

    entry_func(cfg)
