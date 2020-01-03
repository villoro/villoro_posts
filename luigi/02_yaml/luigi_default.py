import time
import luigi
import oyaml as yaml

from datetime import date, datetime


PATH_LUIGI_YAML = "runs/{:%Y%m%d}/{}.yaml"


class StandardTask(luigi.Task):
    """
        Extends luigi task, instead of calling run, one must call run_std

        Params:
            mdate:          date of execution
            t_data:         is a dictionary with instance data
            worker_timeout: maximum time allowed for a task to run in seconds
    """

    mdate = luigi.DateParameter(default=date.today())
    worker_timeout = 1 * 3600  # Default timeout is 1h per task
    t_data = {}

    # This is meant to be overwritten
    module = "change_this_to_module_name"

    def __init__(self, *args, **kwargs):
        """ Extends init in order to store task name before task init """

        self.name = self.__class__.__name__
        super().__init__(*args, **kwargs)

    def output(self):

        # output will be a yaml file inside a folder with date
        return luigi.LocalTarget(PATH_LUIGI_YAML.format(self.mdate, self.name))

    def save_result(self, success=True, **kwa):
        """ Stores result as a yaml file """

        # Store basic execution info
        self.t_data["end_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.t_data["duration"] = time.time() - self.start_time
        self.t_data["success"] = success

        # Allow extra params like 'exception'
        self.t_data.update(**kwa)

        # Export them as an ordered yaml
        with self.output().open("w") as stream:
            yaml.dump(self.t_data, stream)

    def on_failure(self, exception):

        # If there is an error store it anyway
        self.save_result(success=False, exception=repr(exception))
        self.disabled = True

        # If needed, do extra stuff (like log.error)

        # End up raising the error to Luigi
        super().on_failure(exception)

    def run_std(self):
        """
            This is what the task will actually do.

            If it is not overwritten it will 'import module' and then run:

                module.main(mdate)
        """

        # Run the task and store the resutls
        module = __import__(self.module)
        module.main(self.mdate.strftime("%Y_%m_%d"))

    def run(self):
        # Store start time and task name
        self.t_data["name"] = self.name
        self.start_time = time.time()
        self.t_data["start_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self.run_std()

        return self.save_result()
