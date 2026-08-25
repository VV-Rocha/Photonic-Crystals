from .ssh.config import SSHConfig
from .ssh.function import ShiqiXia_ssh_modulation, site_by_site_ssh


class ShiqiXiaSSH(SSHConfig):
    def landscape_function(self, mesh):
        return ShiqiXia_ssh_modulation(
                xx = mesh.xx,
                a = self.a,
                c = self.c,
                intra_cell = self.intra_cell,
                dimerization = self.dimerization,
        )
        
class SiteBySiteSSH(SSHConfig):
    def landscape_function(self, mesh):
        return site_by_site_ssh(
                xx = mesh.xx,
                a = self.a,
                c = self.c,
                intra_cell = self.intra_cell,
                dimerization = self.dimerization,
        )