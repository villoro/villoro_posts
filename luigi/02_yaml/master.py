import time
import luigi
import oyaml as yaml

from datetime import date, datetime


PATH_LUIGI_YAML = "runs/{:%Y%m%d}/{}.yaml"


class StandardTask(luigi.Task):
    """
        Extends luigi task, instead of calling run, one must call run_std

        Params:
            t_data:         is a dictionary with instance data
            worker_timeout: maximum time allowed for a task to run in seconds
    """

    worker_timeout = 1 * 3600  # Default timeout is 1h per task
    t_data = {}

    def __init__(self, *args, **kwargs):
        self.name = self.__class__.__name__
        super().__init__(*args, **kwargs)

    def run_std(self):  # pylint: disable=no-self-use
        """Default run, meant to be overrided and return results"""

        return True

    def output(self):
        uri = PATH_LUIGI_YAML.format(date.today(), self.name)
        return luigi.LocalTarget(uri)

    def save_result(self, success=True, **kwa):
        """Saves success to t_data"""

        self.t_data["end_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.t_data["duration"] = time.time() - self.start_time
        self.t_data["success"] = success

        self.t_data.update(**kwa)

        with self.output().open("w") as stream:
            yaml.dump(self.t_data, stream)

    def on_failure(self, exception):
        self.save_result(success=False, exception=repr(exception))
        self.disabled = True
        super().on_failure(exception)

    def run(self):
        self.t_data["name"] = self.name

        self.start_time = time.time()
        self.t_data["start_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.run_std()
        return self.save_result()


class RegisterTask(StandardTask):

    mdate = luigi.DateParameter(default=date.today())

    def run_std(self):
        from register import do

        do(self.mdate.strftime("%Y_%m_%d"))


class ReportTask(StandardTask):

    mdate = luigi.DateParameter(default=date.today())

    def run_std(self):
        from report import do

        do(self.mdate.strftime("%Y_%m_%d"))


class DoAllTask(StandardTask):

    mdate = luigi.DateParameter(default=date.today())

    def run_std(self):
        with open(self.mdate.strftime("output/%Y_%m_%d.info"), "w") as stream:
            stream.write("Done")

    def requires(self):
        return RegisterTask(self.mdate), ReportTask(self.mdate)


if __name__ == "__main__":
    luigi.build([DoAllTask()])
