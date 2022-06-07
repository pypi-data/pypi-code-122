# System
import os
import ast

# External
import numpy
import yaml
import pickle5 as pickle

# Local
from .extract import get_samples

def sbatch(config,**kwargs):
    make_slurm_script(config['path'],**config['dist'],**config['prms'])
    
def make_slurm_script(path, sbatch={}, operation=None, nsteps=1, ntasks=1,
                      node_type='cpu', cpu_mem=20, module=None, conda='', cd=None, export=None, 
                      proc_per_node=None, no_submit=False, system='cori', nevals=None, **kwargs):
    procs = {'cori':{'cpu':{'haswell':32,'knl':68},'gpu':{'gpu':8}},'perl':{'gpu':{'gpu':4}}}
    if system in procs.keys() and node_type in ['cpu','gpu'] and 'constraint' in sbatch.keys():
        proc_per_node = procs[system][node_type][sbatch['constraint']]
    operations = ['evaluation','surrogate'] if operation==None else [operation]
    script = open('hpo.sh','w')
    script.write('#!/bin/bash\n')
    # ----------------------------------------------
    #   SBATCH directive
    # ----------------------------------------------
    for key,value in sbatch.items():
        script.write('#SBATCH --%s %s\n'%(key,value))
        if key=='ntasks-per-node':
            proc_per_node = value
    if proc_per_node!=None:
        script.write('#SBATCH --nodes %i\n' % numpy.ceil(nsteps * ntasks / proc_per_node) )
    script.write('#SBATCH --ntasks %i\n' % (nsteps * ntasks) )
    if node_type=='cpu':
        srun_spec = '--cpus-per-task 1 --mem=%iGB --gres=craynetwork:0' % cpu_mem
    if node_type=='gpu':
        srun_spec = '--gpus-per-task 1 --gpu-bind=none'
        script.write('#SBATCH --dependency singleton\n')
        script.write('#SBATCH --exclusive\n')
    script.write('#SBATCH --%ss-per-task 1\n' % node_type)
    script.write('#SBATCH --output %x-%j.out\n')
    script.write('#SBATCH --error %x-%j.err\n')
    # ----------------------------------------------
    #   Load modules
    # ----------------------------------------------
    script.write('module load parallel\n')
    if module!=None:
        for mod in module.split(';'):
            script.write('module load %s\n' % mod)
    if conda!='':
        script.write('conda activate %s\n' % conda)
        conda = 'conda activate %s &&' % conda
    if export!=None:
        script.write('export PYTHONPATH=$PYTHONPATH:%s\n' % export)
    # ----------------------------------------------
    #   Create sampling
    # ----------------------------------------------
    if 'evaluation' in operations:
        script.write('python $HOME/hyppo/bin/hyppo sampling config.yaml\n')
    # ----------------------------------------------
    #   Parallel SRUN command
    # ----------------------------------------------
    for operation in operations:
        slurm_steps = nevals if operation=='evaluation' and nevals<nsteps else nsteps
        parallel = 'parallel --delay .2 -j %i' % slurm_steps
        srun = 'srun --exclusive --nodes 1 --ntasks %i' % ntasks
        hpo = 'python $HOME/hyppo/bin/hyppo %s config.yaml' % operation
        script.write('%s "%s %s %s %s && {1}" ::: {0..%i}\n' % (parallel, conda, srun, srun_spec, hpo, slurm_steps-1))
    script.close()
    if not no_submit:
        os.system('sbatch hpo.sh')

# def slurm_split(config,**kwargs):
#     assert 'dist' in config.keys(), 'You did not add the dist section in configuration file. Abort.'
#     # Estimate total number of CPUs
#     nproc = int(config['dist']['sbatch']['nodes'])*32
#     # Write SLURM script
#     samples = get_samples('logs',surrogate=True,mult=False)
#     times   = numpy.hstack((samples['evals'][:,-1],samples['sgate'][:,-1]))
#     times   = numpy.array([numpy.ceil(time/60) for time in times])
#     samples = numpy.vstack((samples['evals'][:,:-2],samples['sgate'][:,:-2]))
#     script  = ''
#     for i in range(len(samples)):
#         trial_path = os.path.abspath('trials/sample_%03i/'%(i+1))
#         os.makedirs(trial_path,exist_ok=True)
#         samp_to_save = numpy.array([samples[i] for n in range(nproc)])
#         filehandler = open(trial_path+'/samples.pickle', 'wb')
#         pickle.dump(samp_to_save, filehandler)
#         copy_config(config,filename=trial_path+'/config.yaml')
#         write_slurm(config,nproc,path=trial_path+'/script.sh',conf=trial_path+'/config.yaml',time=times[i])
#         script += 'sbatch %s/script.sh\n'%trial_path
#     batch = open('trials/batch.sh','w')
#     batch.write(script)
#     batch.close()
        
# def copy_config(config,filename):
#     config = ast.literal_eval(config['original'])
#     config['prms']['record'] = 'samples.pickle'
#     with open(filename, 'w') as f:
#         yaml.dump(config, f, default_flow_style=False)
