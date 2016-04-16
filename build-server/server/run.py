import sys
import os
import traceback
import os.path
from framework.common import *
from framework import simplexml

str_cur_dir = os.path.dirname(os.path.realpath(sys.argv[0]))
sys.path.append(str_cur_dir)
sys.path.append(os.path.dirname(os.path.realpath(os.path.curdir)))


global config
xml_config = simplexml.parse('config.xml')

class software(object):
    def __init__(self, str_software_id, str_tag_or_commit='HEAD' ):
        system = xml_config.system
        try:
            self.xml_software_node = xml_config.softwares.nodes[str_software_id]
        except:
            traceback.print_exc()
            raise Exception, 'Can not found node: {0}'.format(str_software_id)
        self.str_software_id = str_software_id

        self.git  = try_get_xml_str(self.xml_software_node, 'git')
        self.make_commands = try_get_xml_str(self.xml_software_node, 'make_commands')
        
        str_src_dir = try_get_xml_str(self.xml_software_node, 'repo_dir', self.str_software_id)
        self.src_dir = os.path.join(str(system.root_dir), 
                                    str(system.repos_dir), 
                                    str(str_src_dir))

        str_out_dir = try_get_xml_str(self.xml_software_node, 'out_dir', str_src_dir)
        self.out_dir = os.path.join(str(system.root_dir), 
                                    str(system.out_dir), 
                                    str(str_out_dir))
        
        self.install_commands = str(self.xml_software_node.install_commands)

        if self.make_commands:
            try:
                self.str_commit = get_commit_of_tag(self.git, self.src_dir, str_tag_or_commit )
            except:
                traceback.print_exc()
                raise Exception, 'Can not found version: {0} of software: {1}. ' \
                    .format( str_tag_or_commit, self.str_software_id )
        else:
            self.str_commit = None
            
    def make(self):
        sys_call(
            ('WORK_DIR={0}' '\n'
             'cd $WORK_DIR' '\n').format(self.src_dir) + self.make_commands)
    
    def get_tar_filepath(self, str_commit=None):
        return os.path.join(self.out_dir, iif(str_commit, str_commit , self.str_commit) + '.tar.bz2')

    def build(self, str_tag_or_commit='HEAD' ):
        if self.make_commands:
            print '>'*10 + ' ' + 'build [%s] begin ' % self.str_software_id + ' ' + '>' * 10
            try:
                git_update(self.git, self.src_dir)
                str_commit = get_commit_of_tag(self.git, self.src_dir, str_tag_or_commit)
                str_tar_filepath = self.get_tar_filepath(str_commit)

                if os.path.exists( str_tar_filepath ):
                    print "The file {} already Existed, not need to build.".format(str_tar_filepath)
                else:
                    git_checkout(self.git, self.src_dir, str_commit)
                    self.make()
                    tar( str_tar_filepath, self.src_dir,
                         try_get_xml_str(self.xml_software_node, 'zip_contains', '.'))    
            except:
                traceback.print_exc()
                print 'Error:Fail to build software {}.'.format(self.str_software_id)
            print '<' * 10 + ' ' + 'build [%s] end ' % self.str_software_id +' ' +  '<'*10 

    def get_shell_code_for_install(self):
        if self.make_commands:
            str_tar_filepath = self.get_tar_filepath()
            if not os.path.exists(str_tar_filepath):
                return 'echo Sorry, there is no this version in server.' 
            else:
                str_workdir = self.src_dir
                return \
                    ('WORK_DIR={0}\n'
                     'rm -rf $WORK_DIR; mkdir -p $WORK_DIR; cd $WORK_DIR\n'
                     'curl -u tester:123456 sftp://{1}/{2} -o {3}\n'
                     'tar -jxvf {3}\n'
                     '{4}') \
                     .format(str_workdir,
                             this_server_ip(),
                             os.path.join(self.out_dir, self.str_commit+'.tar.bz2'),
                             'dist.tar.bz2',
                             self.install_commands )
        else:
            return self.install_commands
    
    def get_python_code_for_install(self):
        return \
            ('import subprocess\n'
             'subprocess.check_call("""{}""",shell=True)\n'
             ).format(self.get_shell_code_for_install())

def main():
    if sys.argv[1] == 'build':
        #2 para form
        if len(sys.argv[2:]) == 2:  
            software(sys.argv[2:][0]).build(sys.argv[2:][1])
        #1 para form
        elif len(sys.argv[2:]) == 1:
            software(sys.argv[2:][0]).build()
        #0 para form, build all softwares.
        elif len(sys.argv[2:]) == 0:
            for node in xml_config.softwares.nodes:
                software(str(node)).build()
    elif sys.argv[1] == 'get-install-code':
        if len(sys.argv[2:]) == 2:
            print software(sys.argv[2:][0],sys.argv[2:][1]).get_python_code_for_install()
        elif len(sys.argv[2:]) == 1:
            print software(sys.argv[2:][0]).get_python_code_for_install()
        
if __name__ == '__main__':
    main()

    
