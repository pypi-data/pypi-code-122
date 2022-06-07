from genericpath import exists
import os, argparse, sys, subprocess

def echo_file(args):
    text = args.text
    path = args.path
    dirname = os.path.dirname(path)
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    elif os.path.isfile(dirname):
        print(f'{dirname} is a file')
        sys.exit(1)
    elif os.path.isdir(path):
        print(f'{path} is a dir')
        sys.exit(1)
    else:
        with open(path, 'w') as f:
            f.write(text)

def exec(args):
    cmd = args.cmd
    bg = args.bg
    log_path = args.log_path
    output_path = args.output_path
    if bg:
        cmd = f'nohup {cmd} > {log_path} 2>&1 > {output_path} &'
        [os.makedirs(os.path.dirname(p)) for p 
            in [log_path, output_path] if not os.path.exists(os.path.dirname(p))]
    subprocess.call([cmd], shell=True)

def run():
    parser = argparse.ArgumentParser(description='Echo File, write text to file')
    subparser = parser.add_subparsers(help='subcommand help')

    echo_parser = subparser.add_parser('echo_file', help='write text to file')
    echo_parser.add_argument('--text', type=str, default='hello world',help='text written to file')
    echo_parser.add_argument('--path', type=str, default='/tmp/test.txt', help='file path')
    echo_parser.set_defaults(func=echo_file)

    run_parser = subparser.add_parser('run', help='run command')
    run_parser.add_argument('--cmd', type=str, default='echo hello world',help='run command')
    run_parser.add_argument('--bg', action='store_true', help='run command in background')
    run_parser.add_argument('--log_path', type=str, default='/tmp/pod_exec/log', help='log path')
    run_parser.add_argument('--output_path', type=str, default='/tmp/pod_exec/output', help='log path')
    run_parser.set_defaults(func=exec)

    args = parser.parse_args()
    args.func(args)
    

if __name__=='__main__':
    run()