#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tkinter import Tk, Frame, Label, Entry, Button, StringVar
from tkinter import BOTH, LEFT, RIGHT, X, S
import tkinter.messagebox as msg_box
import tkinter.filedialog
from shutil import copyfile
import os, re

class App(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent

        if os.name == 'nt':
            self.hosts_filename = 'c:\\Windows\\System32\\drivers\\etc\\hosts'
            self.vhosts_filename = 'manifests\\make-vhosts.sh'
            self.vagrantfile_filename = 'Vagrantfile'
        else:
            self.hosts_filename = '/etc/hosts'
            self.vhosts_filename = './manifests/make-vhosts.sh'
            self.vagrantfile_filename = './Vagrantfile'

        self._initUI()

    def _initUI(self):
        '''The UI initialiser'''
        self.parent.title('Vhost Creator')

        # Hosts frame
        frm_hosts = Frame(self)
        frm_hosts.pack(fill=X)

        # Hosts filename label
        lbl_hosts = Label(frm_hosts, text='Hosts file:', width=12)
        lbl_hosts.pack(side=LEFT, padx=5, pady=(5,0))

        # Hosts browse for file button
        btn_hosts = Button(frm_hosts, text='Browse', command=self.onHostsClick, width=5)
        btn_hosts.pack(side=RIGHT, padx=5, pady=(5,0))

        # Hosts filename entry
        self.entr_hosts_var = StringVar()
        self.entr_hosts_var.set(self.hosts_filename)
        entr_hosts = Entry(frm_hosts, textvariable=self.entr_hosts_var, justify=RIGHT)
        entr_hosts.pack(fill=X, pady=(5,0), ipady=4)

        # VHosts frame
        frm_vhosts = Frame(self)
        frm_vhosts.pack(fill=X)

        # VHosts filename label
        lbl_vhosts = Label(frm_vhosts, text='VHosts file:', width=12)
        lbl_vhosts.pack(side=LEFT, padx=5, pady=(5,0))

        # VHosts browse for file button
        btn_vhosts = Button(frm_vhosts, text='Browse', command=self.onVHostsClick, width=5)
        btn_vhosts.pack(side=RIGHT, padx=5, pady=(5,0))

        # VHosts filename entry
        self.entr_vhosts_var = StringVar()
        self.entr_vhosts_var.set(self.vhosts_filename)
        entr_vhosts = Entry(frm_vhosts, textvariable=self.entr_vhosts_var, justify=RIGHT)
        entr_vhosts.pack(fill=X, pady=(5,0), ipady=4)

        # Vagrantfile frame
        frm_vagrantfile = Frame(self)
        frm_vagrantfile.pack(fill=X)

        # Vagrantfile filename label
        lbl_vagrantfile = Label(frm_vagrantfile, text='Vagrantfile file:', width=12)
        lbl_vagrantfile.pack(side=LEFT, padx=5, pady=(5,0))

        # Vagrantfile browse for file button
        btn_vagrantfile = Button(frm_vagrantfile, text='Browse', command=self.onVagrantfileClick, width=5)
        btn_vagrantfile.pack(side=RIGHT, padx=5, pady=(5,0))

        # Vagrantfile filename entry
        self.entr_vagrantfile_var = StringVar()
        self.entr_vagrantfile_var.set(self.vagrantfile_filename)
        entr_vagrantfile = Entry(frm_vagrantfile, textvariable=self.entr_vagrantfile_var, justify=RIGHT)
        entr_vagrantfile.pack(fill=X, pady=(5,0), ipady=4)

        # New host frame
        frm_new_host = Frame(self)
        frm_new_host.pack(fill=X)

        # New host label
        lbl_new_host = Label(frm_new_host, text='New host:', width=12)
        lbl_new_host.pack(side=LEFT, padx=5, pady=(5,0))

        # Quit button
        btn_quit = Button(frm_new_host, text='Quit', command=self.quit, width=5)
        btn_quit.pack(side=RIGHT, anchor=S, padx=5, pady=(0,5))

        # Create button
        btn_create = Button(frm_new_host, text='Create', command=self.onCreate, width=5)
        btn_create.pack(side=RIGHT, anchor=S, pady=(0,5))

        # New host entry
        self.entr_new_host_var = StringVar()
        entr_new_host = Entry(frm_new_host, textvariable=self.entr_new_host_var, justify=RIGHT)
        entr_new_host.pack(fill=X, padx=(0, 5), pady=5, ipady=4)

        self.pack(fill=BOTH, expand=True)

    def onHostsClick(self):
        '''The on btn_hosts click event'''
        self.file_types = [('All files', '*')]
        dlg = tkinter.filedialog.Open(self, filetypes = self.file_types)
        filename = dlg.show()

        if filename != '':
            self.entr_hosts_var.set(filename)

    def onVHostsClick(self):
        '''The on btn_vhosts click event'''
        self.file_types = [('Shell files', '*.sh'), ('All files', '*')]
        dlg = tkinter.filedialog.Open(self, filetypes = self.file_types)
        filename = dlg.show()

        if filename != '':
            self.entr_vhosts_var.set(filename)

    def onVagrantfileClick(self):
        '''The btn_vagrantfile click event'''
        self.file_types = [('All files', '*')]
        dlg = tkinter.filedialog.Open(self, filetypes = self.file_types)
        filename = dlg.show()

        if filename != '':
            self.entr_vagrantfile_var.set(filename)

    def onCreate(self):
        '''The btn_create on click event'''
        # Check if new host field empty
        new_host_name = self.entr_new_host_var.get()
        if new_host_name == '':
            error = 'Empty new host field'
            print('Error: ' + error)
            msg_box.showerror('Error', error)

            return error

        result = True

        # Check Vagrantfile for the IP address
        host_ip = self._check_host_ip()

        if '.' not in host_ip:
            error = 'Can not find VMs external IP address in the Vagrant file'
            print(error)
            msg_box.showerror('Error', error)

            return error

        # Edit VHosts file
        result = self._edit_vhosts_file(new_host_name);

        if result == True:
            # # Edit Hosts file
            result = self._edit_hosts_file(host_ip, new_host_name);

        if result == True:
            msg_box.showinfo('Host Created', 'The new host has been created. Now run "vagrant up --provision"')
        else:
            msg_box.showerror('Error', result)

    def _check_host_ip(self):
        '''Check if the VMs external IP exists in the Vagrantfile'''
        # Check what the virtual host's external IP is
        with open(self.vagrantfile_filename, 'r') as fin:
            for line in fin:
                if 'private_network' in line:
                    pattern = '\d[0-9]+\.\d[0-9]+\.\d[0-9]+\.\d[0-9]+'
                    match = re.findall(pattern, line)

                    return match[0]

        return error

    def _edit_hosts_file(self, host_ip, new_host_name):
        '''Edit the hosts file with the new host

        Args:
            host_ip (string): The IP address of the VM
            new_host_name (string): The new host string
        '''
        # Create backups of the hosts file
        hosts_filename = self.entr_hosts_var.get()
        self._backup_file(hosts_filename)

        # Check hosts file for existing host
        with open(hosts_filename, 'r') as fin:
            for line in fin:
                pattern = '\d[0-9]+\.\d[0-9]+\.\d[0-9]+\.\d[0-9]+\s+' + new_host_name
                if re.findall(pattern, line):
                    error = 'Host exists'
                    print('Error: ' + error)

                    return error

        # Add new host
        with open(hosts_filename, 'a') as fout:
            fout.write('\n%s\t\t%s' % (host_ip, new_host_name))
            print('New host added to hosts file')

        return True

    def _edit_vhosts_file(self, new_host_name):
        '''Edit the make-vhosts.sh file with the new host

        Args:
            new_host_name (string): The new host string
        '''
        # Create backups of the make-vhosts file
        vhosts_filename = self.entr_vhosts_var.get()
        self._backup_file(vhosts_filename)

        vhosts = []
        with open(vhosts_filename, 'r') as fin:
           for line in fin:
               vhosts.append(line)
               if 'DOMAINS=(' in line:
                   vhosts.append('    "%s"\n' % new_host_name)

        with open(vhosts_filename, 'w') as fout:
            fout.write(''.join(vhosts))

        return True

    def _backup_file(self, filename):
        '''Backup a file - make a copy and add .bak

        Args:
            filename (string): The filename full path
        '''
        copyfile(filename, filename + '.bak')

    def _restore_file(self, filename):
        '''Restore a file - swap the .bak version with the other

        Args:
            filename (string): The filename full path
        '''
        copyfile(filename + '.bak', filename)


def main():
    root = Tk()
    root.geometry('640x140+300+300')
    app = App(root)
    app.mainloop()

if __name__ == '__main__':
    main()
