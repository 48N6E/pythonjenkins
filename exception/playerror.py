from utils.logger import logger


class DeployError(RuntimeError):

    def __init__(self, msg=''):
        super().__init__(self)
        self.msg = "操作失败！" + msg
        logger.error(self.msg)

    def __str__(self):
        return self.msg




    # logger.flow('校验image是否存在', image)
    # with os.popen("docker image inspect %s " % image) as p:
    #     res = p.read()
    #     if res.startswith("[]"):
    #         logger.error("Error: No such image: %s" % image)
    #         raise DeployError()

