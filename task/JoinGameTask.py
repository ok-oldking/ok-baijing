from task.BJTask import BJTask


class JoinGameTask(BJTask):

    def __init__(self):
        super().__init__()
        self.route = None
        self.name = "启动游戏"
        self.description = "打开模拟器，启动游戏，签到，进入主页"

    def run(self):
        if self.ensure_main_page():
            self.log_info("进入游戏主页成功！", True)
        else:
            self.log_error("进入游戏主页失败！")
