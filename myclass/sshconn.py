"""SSH connection Class."""

from subprocess import check_output, CalledProcessError


class SSHConn():
    """SSH Connection Class"""
    def __init__(self):
        self.sshbase = ["/usr/bin/ssh", "-o", "ConnectTimeout=30", "-o", "StrictHostKeyChecking=no"]
        self.sshpbase = ["/usr/bin/sshpass", "-p"]

    def do_ssh(self, Hst, Cmd="uname -n", Usr="root", Pswd=None):
        """Function to perform SSH"""
        hst_str = str(Usr + '@' + Hst)
        sshcmd = self.sshbase + [hst_str, Cmd]
        if Pswd:
            fullsshcmd = self.sshpbase + [Pswd] + sshcmd
        else:
            fullsshcmd = sshcmd
        try:
            sshout = check_output(fullsshcmd, text=True)
            return sshout
        except CalledProcessError as e:
            return f"SSH failed for command - {sshcmd} with Error: {e}"
