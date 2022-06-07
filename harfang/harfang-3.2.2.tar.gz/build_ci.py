# Harfang continuous integration script
#
# This build script requires at least Python 3.6.
# Do not forget to set the following environment variables :
# MSVC/Windows build:
# 	PYTHON3_EXECUTABLE_x86 : path to x86 Python 3 binary (ex: C:\Python36\x86\python.exe)
# 	PYTHON3_LIBRARY_x86    : path to x86 Python 3 library (ex: C:\Python36\x86\libs\python3.lib)
# 	PYTHON3_EXECUTABLE_x64 : path to x64 Python 3 binary (ex: C:\Python36\x64\python.exe)
# 	PYTHON3_LIBRARY_x64    : path to x64 Python 3 library (ex: C:\Python36\x64\libs\python3.lib)
#   FBX_SDK                : path to the Autodesk(c)(tm) FBX SDK (ex: C:\sdk\FBX\2018.1.1)
#
# Linux:
#   FBX_SDK                : path to the Autodesk(c)(tm) FBX SDK (ex: /opt/fbx/2018.1.1)
#
import subprocess
import argparse
import pathlib
import shutil
import time
import sys
import stat
import os
import pygit2
import io
import zipfile
import fnmatch

cmake_exe = 'cmake'

source_dir = os.getcwd()
build_dir = None

hg_version = 'unknown'

# ----
def flush_print(msg):
	print(msg)
	sys.stdout.flush()


def print_header(msg):
	print('')
	print('[-- %s --]' % msg)
	print('')
	sys.stdout.flush()


def rmtree(path):
	if os.path.isdir(path):
		shutil.rmtree(path)
		time.sleep(2)  # HACK try to prevent Windows "folder is in use"


def get_build_id():
	return os.environ["CI_JOB_ID"] if "CI_JOB_ID" in os.environ else "test"


def get_build_branch_name():
	return os.environ["CI_COMMIT_REF_NAME"] if "CI_COMMIT_REF_NAME" in os.environ else "test"


def clone_from_github(url, name, branch='master'):
	out_path = os.path.join(build_dir, name)

	if not os.path.isdir(out_path):
		pygit2.clone_repository(url, out_path, checkout_branch=branch)

	return True, out_path

def artifact_name(*args):
	return  str.join('-', args)

# ----
action_time = []


def action(action_func):
	def action_wrapper(*args, **kwargs):
		start_time = time.time()
		os.chdir(source_dir)  # every action starts at source root

		print_header("STARTING action: %s" % action_func.__name__)
		if not action_func(*args, **kwargs):
			print_header("FAILED action: %s" % action_func.__name__)
			sys.exit(1)
		duration = time.time() - start_time
		print_header("COMPLETED action: %s (duration: %fs)" % (action_func.__name__, duration))

		action_time.append((action_func.__name__, duration))
	return action_wrapper


def run_cmake(params, cwd=None, env=None):
	#with subprocess.Popen(params, cwd=cwd, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as proc:
	with subprocess.Popen(params, cwd=cwd, env=env, stderr=subprocess.PIPE) as proc:
		outs, errs = proc.communicate()  # proc.wait() will HANG on Linux (tested up to Python 3.7), use communicate to fix
		if proc.returncode != 0:
			print('\nError(s):\n\n' + errs.decode('utf-8'))
			return False
		return True

def compile_tests_assets(assetc, api, src, dst):
	print('-- Preparing C++ tests assets', flush=True)
	with subprocess.Popen([assetc, src, dst, '-api', api, '-debug'], stderr=subprocess.PIPE) as proc:
		outs, errs = proc.communicate()  # proc.wait() will HANG on Linux (tested up to Python 3.7), use communicate to fix
		if proc.returncode != 0:
			print('\nError(s):\n\n' + errs.decode('utf-8'))
			return False
		return True

def run_tests(config, timeout=3600):
	print('-- Running C++ tests', flush=True)

	cwd = os.path.join(build_dir, 'install', 'cppsdk', 'bin', config)

	env = os.environ.copy()
	env['LD_LIBRARY_PATH'] = cwd

	with subprocess.Popen(os.path.join(cwd, 'tests'), cwd=cwd, env=env, stderr=subprocess.PIPE) as proc:
		outs, errs = proc.communicate()  # proc.wait() will HANG on Linux (tested up to Python 3.7), use communicate to fix
		if proc.returncode != 0:
			print('\nError(s):\n\n' + errs.decode('utf-8'))
			return False
		return True

def run_fbx_converter_tests(timeout=3600):
	print('-- Running FBX Converter tests', flush=True)

	cwd =  os.path.join(build_dir, 'install', 'fbx_converter')

	env = os.environ.copy()
	env['LD_LIBRARY_PATH'] = cwd

	with subprocess.Popen(os.path.join(cwd, 'tests'), cwd=cwd, env=env, stderr=subprocess.PIPE) as proc:
		outs, errs = proc.communicate()  # proc.wait() will HANG on Linux (tested up to Python 3.7), use communicate to fix
		if proc.returncode != 0:
			print('\nError(s):\n\n' + errs.decode('utf-8'))
			return False
		return True

@action
def build_binaries_win(config, arch, paths, keep_build, enable_physics):
	os.chdir(os.path.join(build_dir, 'cmake'))

	arch_opt = {'x86': 'Win32', 'x64': 'x64'}

	cfg_params = [
		cmake_exe, source_dir,
		'-G', 'Visual Studio 16 2019',
		'-A', arch_opt[arch],
		'-DCMAKE_BUILD_TYPE=Release',
		'-DCMAKE_INSTALL_PREFIX=' + os.path.join(build_dir, 'install'),
		'-DPYTHON_EXECUTABLE:FILEPATH=' + os.environ["PYTHON3_EXECUTABLE_" + arch],
		'-DPYTHON_LIBRARY:FILEPATH=' + os.environ["PYTHON3_LIBRARY_" + arch],
		'-DHG_FBX_SDK:PATH=' + os.environ["FBX_SDK"],
		'-DHG_FABGEN_PATH:PATH=' + paths['fabgen'],
		'-DHG_BUILD_ASSETC:BOOL=ON',
		'-DHG_BUILD_CPP_SDK:BOOL=ON',
		'-DHG_BUILD_ASSIMP_CONVERTER:BOOL=ON',
		'-DHG_BUILD_FBX_CONVERTER:BOOL=ON',
		'-DHG_BUILD_GLTF_IMPORTER:BOOL=ON',
		'-DHG_BUILD_GLTF_EXPORTER:BOOL=ON',
		'-DHG_BUILD_HG_LUA:BOOL=ON',
		'-DHG_BUILD_HG_PYTHON:BOOL=ON',
		'-DHG_BUILD_HG_GO:BOOL=ON',
		'-DHG_BUILD_TESTS:BOOL=ON',
		'-DHG_ENABLE_OPENVR_API:BOOL=ON',
		'-DHG_BUILD_DOCS:BOOL=OFF']

	if arch == 'x86':
		cfg_params.append('-DHG_HOST_PREFIX:STRING=windows-x86')  # [EJ03182021] force host architecture as we may build Win32 on a Win64 host

	run_cmake(cfg_params)  # configure

	install_params = [
		cmake_exe,
		'--build', os.path.join(build_dir, 'cmake'),
		'--config', config,
		'--target', 'install',
		'-j']

	run_cmake(install_params)  # build and install

	os.makedirs(os.path.join(build_dir, 'dist'), exist_ok=True)
	for name in ['assetc', 'cppsdk', 'hg_lua', 'hg_python', 'hg_go', 'assimp_converter', 'fbx_converter', 'gltf_importer', 'gltf_exporter']:
		shutil.make_archive(os.path.join(build_dir, 'dist', artifact_name(name, 'win', arch, hg_version)), 'zip', os.path.join(build_dir, 'install', name), '.')

	if not compile_tests_assets(os.path.join(build_dir, 'install', 'assetc', 'assetc.exe'), "DX11", os.path.join(source_dir, 'harfang', 'tests', 'data'), os.path.join(build_dir, 'install', 'cppsdk', 'bin', config, 'data')):
		return False
	if not run_tests(config):
		return False

	return run_fbx_converter_tests()

def find_python_lib_linux():
	if 'PYTHON3_LIBRARY_x64' in os.environ:
		return os.environ["PYTHON3_LIBRARY_x64"]
	
	for file in os.listdir('/usr/lib/x86_64-linux-gnu/'):
		if fnmatch.fnmatch(file, 'libpython3.*m.so'):
			return file
	return ""

@action
def build_binaries_linux(config, arch, paths, keep_build, enable_physics):
	os.chdir(os.path.join(build_dir, 'cmake'))

	python_lib = find_python_lib_linux()
	
	cfg_params = [
		cmake_exe, source_dir,
		'-DCMAKE_BUILD_TYPE=Release',
		'-DCMAKE_INSTALL_PREFIX=' + os.path.join(build_dir, 'install'),
		'-DPYTHON_EXECUTABLE:FILEPATH=' + (os.environ["PYTHON3_EXECUTABLE_x64"] if 'PYTHON3_LIBRARY_x64' in os.environ else '/usr/bin/python3'),
		'-DPYTHON_LIBRARY:FILEPATH=' + python_lib,
		'-DHG_FBX_SDK:PATH=' + os.environ["FBX_SDK"],
		'-DHG_FABGEN_PATH:PATH=' + paths['fabgen'],
		'-DHG_BUILD_ASSETC:BOOL=ON',
		'-DHG_BUILD_CPP_SDK:BOOL=ON',
		'-DHG_BUILD_ASSIMP_CONVERTER:BOOL=ON',
		'-DHG_BUILD_FBX_CONVERTER:BOOL=ON',
		'-DHG_BUILD_GLTF_IMPORTER:BOOL=ON',
		'-DHG_BUILD_GLTF_EXPORTER:BOOL=ON',
		'-DHG_BUILD_HG_LUA:BOOL=ON',
		'-DHG_BUILD_HG_PYTHON:BOOL=ON',
		'-DHG_BUILD_HG_GO:BOOL=ON',
		'-DHG_BUILD_TESTS:BOOL=ON',
		'-DHG_BUILD_DOCS:BOOL=OFF']

	run_cmake(cfg_params)  # configure

	install_params = [
		cmake_exe,
		'--build', os.path.join(build_dir, 'cmake'),
		'--config', config,
		'--target', 'install',
		'-j', '6']  # [EJ] limit to 6 core to prevent build machine from going out of memory

	run_cmake(install_params)  # build and install

	os.makedirs(os.path.join(build_dir, 'dist'), exist_ok=True)
	for name in ['assetc', 'cppsdk', 'hg_lua', 'hg_python', 'hg_go', 'assimp_converter', 'fbx_converter', 'gltf_exporter', 'gltf_importer']:
		shutil.make_archive(os.path.join(build_dir, 'dist', artifact_name(name, 'ubuntu', arch, hg_version)), 'zip', os.path.join(build_dir, 'install', name), '.')

	if not compile_tests_assets(os.path.join(build_dir, 'install', 'assetc', 'assetc'), "GL", os.path.join(source_dir, 'harfang', 'tests', 'data'), os.path.join(build_dir, 'install', 'cppsdk', 'bin', config, 'data')):
		return False
	if not run_tests(config):
		return False

	return True

@action
def build_binaries_linux_aarch64(config, arch, paths, keep_build, enable_physics):
	os.chdir(os.path.join(build_dir, 'cmake'))

	target_sysroot_path = os.path.join(os.environ["YOCTO_SDK_PATH"], 'sysroots', 'aarch64-poky-linux')
	native_sysroot_path = os.path.join(os.environ["YOCTO_SDK_PATH"], 'sysroots', 'x86_64-pokysdk-linux')
	python_lib_path = os.path.join(target_sysroot_path, 'usr', 'lib', 'libpython3.5m.so')

	cfg_params = [
		cmake_exe, source_dir,
		'-DCMAKE_BUILD_TYPE=Release',
		'-DCMAKE_INSTALL_PREFIX=' + os.path.join(build_dir, 'install'),
		'-DCMAKE_TOOLCHAIN_FILE:FILEPATH=' + os.path.join(source_dir, 'harfang/cmake/aarch64-poky-linux.cmake'),
		'-DNATIVE_SYSROOT:PATH=' + native_sysroot_path,
		'-DTARGET_SYSROOT:PATH=' + target_sysroot_path,
		'-DCMAKE_MODULE_PATH=' + os.path.join(source_dir, 'harfang/cmake'),
		'-DPYTHON_EXECUTABLE:FILEPATH=/usr/bin/python3',
		'-DPYTHON_LIBRARY:FILEPATH=' + python_lib_path,
		'-DHG_FABGEN_PATH:PATH=' + paths['fabgen'],
		'-DHG_ASSETC_PATH:PATH=' + os.path.join(build_dir, 'assetc_x86_64', 'assetc'),
		'-DHG_BUILD_ASSETC:BOOL=OFF',
		'-DHG_BUILD_CPP_SDK:BOOL=ON',
		'-DHG_REBUILD_GLFW:BOOL=OFF',
		'-DHG_BUILD_TESTS:BOOL=ON',
		'-DHG_BUILD_FBX_CONVERTER:BOOL=OFF',
		'-DHG_BUILD_GLTF_IMPORTER:BOOL=OFF',
		'-DHG_BUILD_GLTF_EXPORTER:BOOL=OFF',
		'-DHG_BUILD_ASSIMP_CONVERTER:BOOL=OFF',
		'-DHG_BUILD_HG_LUA:BOOL=OFF',
		'-DHG_BUILD_HG_PYTHON:BOOL=OFF',
		'-DHG_BUILD_HG_GO:BOOL=OFF',
		'-DHG_ENABLE_RECAST_DETOUR_API:BOOL=OFF',
		'-DHG_BUILD_DOCS:BOOL=OFF']

	env = os.environ.copy()
	env['PKG_CONFIG_SYSROOT_DIR'] = env['SDKTARGETSYSROOT']
	env['PKG_CONFIG_PATH'] = ':'.join([os.path.join(env['SDKTARGETSYSROOT'], 'usr', 'lib', 'pkgconfig'), os.path.join(env['SDKTARGETSYSROOT'], 'usr', 'share', 'pkgconfig')])

	run_cmake(cfg_params, env=env)  # configure

	install_params = [
		cmake_exe,
		'--build', os.path.join(build_dir, 'cmake'),
		'--config', config,
		'--target', 'install',
		'-j', '6']  # [EJ] limit to 6 core to prevent build machine from going out of memory

	run_cmake(install_params, env=env)  # build and install

	os.makedirs(os.path.join(build_dir, 'dist'), exist_ok=True)
	for name in ['cppsdk']:
		shutil.make_archive(os.path.join(build_dir, 'dist', artifact_name(name, 'linux', arch, hg_version)), 'zip', os.path.join(build_dir, 'install', name), '.')

	return True


@action
def build_doc():
	os.chdir(os.path.join(build_dir, 'cmake'))

	cfg_params = [
		cmake_exe, source_dir,
		'-G', 'Visual Studio 16 2019',
		'-A', 'x64',
		'-DCMAKE_BUILD_TYPE=Release',
		'-DCMAKE_INSTALL_PREFIX=' + os.path.join(build_dir, 'install'),
		'-DPython3_ROOT_DIR:PATH=' + os.environ["PYTHON3_EXECUTABLE_x64"],
		'-DHG_FABGEN_PATH:PATH=' + paths['fabgen'],
		'-DHG_BUILD_ASSETC:BOOL=OFF',
		'-DHG_BUILD_CPP_SDK:BOOL=OFF',
		'-DHG_BUILD_TESTS:BOOL=OFF',
		'-DHG_USE_GLFW:BOOL=OFF',
		'-DHG_BUILD_FBX_CONVERTER:BOOL=OFF',
		'-DHG_BUILD_GLTF_IMPORTER:BOOL=OFF',
		'-DHG_BUILD_GLTF_EXPORTER:BOOL=OFF',
		'-DHG_BUILD_ASSIMP_CONVERTER:BOOL=OFF',
		'-DHG_BUILD_HG_LUA:BOOL=OFF',
		'-DHG_BUILD_HG_PYTHON:BOOL=OFF',
		'-DHG_BUILD_HG_GO:BOOL=OFF',
		'-DHG_ENABLE_RECAST_DETOUR_API:BOOL=OFF',
		'-DHG_BUILD_DOCS:BOOL=ON']

	run_cmake(cfg_params)  # configure

	install_params = [
		cmake_exe,
		'--build', os.path.join(build_dir, 'cmake'),
		'--config', 'Release',
		'--target', 'doc_cppsdk',  # [EJ] this target has no install step and outputs to the install folder directly (large file dir copy is VERY slow on Windows)
		'-j']

	run_cmake(install_params)  # build and install
	
	os.makedirs(os.path.join(build_dir, 'dist'), exist_ok=True)
	for name in ['cppsdk_docs']:
		shutil.make_archive(os.path.join(build_dir, 'dist', artifact_name(name, hg_version)), 'zip', os.path.join(build_dir, 'install', name), '.')

	return True

# ----
platforms = {
	'win32': ('WinPC', 'x86'),
	'win64': ('WinPC', 'x64'),
	'ubuntu64': ('Ubuntu', 'x64'),
	'aarch64': ('Poky', 'aarch64'),
	'doc': ('Doc', 'x64')
}


def run_build(platform, paths, keep_build, enable_physics):
	# setup platform
	config = "Release"

	if platform not in platforms:
		sys.exit(2)  # unsupported platform

	system, arch = platforms[platform]

	# start build
	ret = True
	flush_print("Build starting: %s|%s (%s)" % (config, arch, system))

	if system == "WinPC":
		ret = build_binaries_win(config, arch, paths, keep_build, enable_physics)
	elif system == "Ubuntu":
		ret = build_binaries_linux(config, arch, paths, keep_build, enable_physics)
	elif system == "Poky":
		ret = build_binaries_linux_aarch64(config, arch, paths, keep_build, enable_physics)
	elif system == "Doc":
		ret = build_doc()

	flush_print("Build complete: %s|%s" % (config, arch))
	return ret


# ----
if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('platform', help='Platform (%s)' % ', '.join(platforms.keys()))
	parser.add_argument('--cmake_exe', required=False, help='Path to CMake executable', default='cmake')
	parser.add_argument('--keep_build', action='store_true', required=False, help='Keep the existing build directory')
	parser.add_argument('--build_dir', required=False, help='Build directory', default='build')
	parser.add_argument('--fabgen_branch', required=False, help='Fabgen branch', default='master')
	parser.add_argument('--enable_physics', required=False, help='Enable physics engine', default=True, type=lambda x: (str(x).lower() in ['true','1', 'yes']))
	args = vars(parser.parse_args())

	if (not args['platform'] in ['aarch64', 'doc']) and (not 'FBX_SDK' in os.environ):
		print('Error: Please set FBX_SDK environment variable to the path of the Autodesk FBX SDK.')
		flush_print("EOB")
		sys.exit(0)

	build_dir = args['build_dir']
	build_dir = os.path.abspath(build_dir)
	print("Build dir: " + build_dir)
	
	if not args['enable_physics']:
		print("*** Physics engine is disabled ***")

	enable_physics = 'ON' if args['enable_physics'] else 'OFF'

	if not os.path.isdir(build_dir) or not args['keep_build']:
		rmtree(build_dir)
		out_build_dir = os.path.join(build_dir, 'cmake')
		print("Creating build dir: " + out_build_dir)
		os.makedirs(out_build_dir)
	os.chdir(build_dir)

	branch_name = get_build_branch_name()

	print_header("Continuous integration script starting (platform: '%s', source_dir: '%s', build_dir: '%s', branch: %s)" % (args['platform'], source_dir, build_dir, branch_name))

	paths = {}
	ok, paths['fabgen'] = clone_from_github('https://github.com/ejulien/FABGen.git', 'fabgen', args['fabgen_branch'])

	if args['cmake_exe'] is not None:
		cmake_exe = args['cmake_exe']

	with open(os.path.join(source_dir, 'harfang', 'version.txt'), encoding='utf8') as file:
		hg_version = file.read().strip()
		
	ret = run_build(args['platform'], paths, args['keep_build'], enable_physics)

	print_header("Build summary:")
	for profile in action_time:
		print("- %s: %fs" % (profile[0], profile[1]))

	flush_print("EOB")  # end of build
	sys.exit(0 if ok else 1)
