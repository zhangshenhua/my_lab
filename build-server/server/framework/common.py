# common.py
import os
import subprocess


def ls(str_path):
    return os.popen('ls ' + str_path).read().split('\n')


def iif(expr, v1, v2):
    if expr:
        return v1
    else:
        return v2


def sys_call(str_command):
    return subprocess.check_call(str_command, shell=True)


def init_repo(str_git, str_path):
    if os.path.exists(str_path):
        sys_call("rm -rf " + str_path)
    sys_call("mkdir -p " + str_path)
    sys_call("git clone " + str_git + " " + str_path)


def git_update(str_git, str_dir):
    if not os.path.exists(str_dir):
        init_repo(str_git, str_dir)
    return sys_call(
        'cd ' + str_dir + '\n'
        'git checkout master' '\n'
        'if [ ! -z $(git remote) ]; then' '\n'
        'git reset origin/master' '\n'
        'git pull' '\n'
        'fi'
    )


def git_checkout(str_git, str_dir, str_commit, ):
    # git_update(str_git, str_dir )
    return sys_call(
        'cd ' + str_dir + '\n'
        'git reset --hard ' + str_commit
    )


def get_commit_of_tag(str_git, str_dir, str_tag):
    # git_update(str_git, str_dir )
    return subprocess.check_output(
        'cd ' + str_dir + '\n'
        'git log -1 ' + str_tag + ' --pretty=format:"%H"',
        shell=True)


def tar(str_tar_filepath,
        str_src_dirpath,
        str_zip_contains='.',
        str_zip_exclude='.git'):
    sys_call('mkdir -p ' + os.path.dirname(str_tar_filepath))
    sys_call('cd ' + str_src_dirpath + '\n'
             'tar cjvf ' + str_tar_filepath +
             ' --exclude=%s' % str_zip_exclude +
             ' %s ' % str_zip_contains)


def this_server_ip():
    ip = os.popen(
        "/sbin/ifconfig | grep 'inet addr' | awk '{print $2}'"
    ).read()
    ip = ip[ip.find(':')+1:ip.find('\n')]
    return ip


def try_get_xml_str(node, str_name, default=None):
    val = default
    try:
        val = str(node.nodes[str_name])
    except:
        pass
    finally:
        return val
