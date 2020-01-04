import luigi

from luigi_default import StandardTask, date


class RegisterTask(StandardTask):
    module = "register"


class ReportTask(StandardTask):
    module = "report"


class DoAllTask(luigi.WrapperTask):

    mdate = luigi.DateParameter(default=date.today())

    def requires(self):
        return RegisterTask(self.mdate), ReportTask(self.mdate)


if __name__ == "__main__":
    luigi.build([DoAllTask()])
