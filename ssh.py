import os
import paramiko


class SshPool:
    def __init__(self):
        self.pool = {}  # { (username, hostname, port, password): SSHClient }

    def clear(self):
        for sess in self.pool.values():
            sess.close()
        self.pool.clear()

    def get(self, username, hostname, port, password, logger=None):
        if (username, hostname, port, password) not in self.pool:
            sess = paramiko.SSHClient()
            sess.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            sess.connect(
                hostname, port,
                username=username,
                password=password,
                banner_timeout=10,
            )

            self.pool[(username, hostname, port)] = sess

            if logger is not None:
                logger.info('Connected to %s:%d' % (hostname, port))

        return self.pool.get((username, hostname, port))

    def mark_broken(self, sess):
        for k, v in self.pool.items():
            if sess == v:
                sess.close()
                self.pool.pop(k)
                break


ssh_pool_global = SshPool()
